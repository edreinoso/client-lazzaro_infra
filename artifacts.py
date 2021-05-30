import os
import json
import boto3
import botocore
from boto3.dynamodb.conditions import Key
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Global vars: boto3 init
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
ddb_client = boto3.client('dynamodb')
elb_client = boto3.client('elbv2')
ecs_client = boto3.client('ecs')
sg_client = boto3.client('ec2')
log_client = boto3.client('logs')
r53_client = boto3.client('route53')
table = dynamodb.Table('frontend-ddb-client')


def handle_service_creation(client):
    image = os.environ['image']+client
    containerName = os.environ['containerName']+client

    # get stuff from dynamodb
    query = table.query(
        KeyConditionExpression=Key('Client').eq(client)
    )

    # assigning port and date vars
    port = query['Items'][0]['Port']
    date = query['Items'][0]['Date']

    # tags
    # is this allowed?
    tags = [
        {
            'Key': 'Name',
            'Value': client
        },
        {
            'Key': 'Port',
            'Value': port
        },
        {
            'Key': 'Date',
            'Value': date
        },
    ]

    # create
    # logs
    try:
        logger.info("1. Creating CloudWatch Logs")
        log_client.create_log_group(
            logGroupName='/ecs/front/'+client,
            tags={
                'Name': client,
                'Date': date
            }
        )
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'ResourceAlreadyExistsException':
            logger.warn(
                'Skipping this portion, cloudwatch logs already exist!')
        else:
            raise error

    logger.info("2. Creating Target Groups")
    # target groups
    targetg = elb_client.create_target_group(
        Name=client,  # dynamic name based on ngo
        Port=int(port),
        VpcId=os.environ['vpc_id'],  # this could probably be hardcoded
        Protocol='HTTP',  # this could possibly be dynamic
        HealthCheckPath='/healthcheck',
        HealthCheckPort=port,
        TargetType='ip',
        Tags=tags
    )
    target_arn = targetg['TargetGroups'][0]['TargetGroupArn']

    # if no listener has been found in the load balancer
    # then create a listener
    # this might require a lot of computation?
    logger.info("3. Checking to see if there's a Listener")
    # checking for listener
    describe_listener_response = elb_client.describe_listeners(
        LoadBalancerArn=os.environ['lb_arn'],
    )

    listener_arn = ''
    if(len(describe_listener_response['Listeners']) < 1):
        logger.info("3a. Creating Listener")
        # listener
        listener = elb_client.create_listener(
            LoadBalancerArn=os.environ['lb_arn'],
            Protocol='HTTPS',
            Port=443,
            SslPolicy='ELBSecurityPolicy-2016-08',
            Certificates=[
                {
                    'CertificateArn': os.environ['certificateArn'],
                },
            ],
            DefaultActions=[
                {
                    'Type': 'forward',
                    'TargetGroupArn': target_arn,
                },
            ],
            Tags=tags
        )
        listener_arn = listener['Listeners'][0]['ListenerArn']
    else:
        # assigning arn of the listener
        listener_arn = describe_listener_response['Listeners'][0]['ListenerArn']

    # need to get the number of listeners
    # just add one more on top of the latest that
    # the highest priority
    rules = elb_client.describe_rules(
        # this is gonna have to be dynamic
        ListenerArn=listener_arn,
    )

    logger.info("4. Creating Listener Rule")
    print('rule number: ', int(rules['Rules']
          [len(rules['Rules'])-2]['Priority'])+1)
    # create listener rule
    listener_rule = elb_client.create_rule(
        ListenerArn=listener_arn,
        Conditions=[
            {
                'Field': 'host-header',
                'Values': [
                    client+'.web.lazzaro.io'
                ]
            },
        ],
        Priority=int(rules['Rules'][len(rules['Rules'])-2]['Priority'])+1,
        Actions=[
            {
                'Type': 'forward',
                'TargetGroupArn': target_arn,
                'ForwardConfig': {
                    'TargetGroups': [
                        {
                            'TargetGroupArn': target_arn,
                        },
                    ]
                }
            },
        ],
        Tags=tags
    )
    rule_arn = listener_rule['Rules'][0]['RuleArn']

    logger.info("5. Creating Security Group")
    sg_id = ''
    # security group
    try:
        create_sg = sg_client.create_security_group(
            GroupName=client+'_sg',
            Description='security group for client: '+client,
            VpcId=os.environ['vpc_id'],
            # TagSpecifications=[
            #     {
            #         'ResourceType': 'security-group',
            #         'Tags': tags
            #     },
            # ]
        )
        sg_id = create_sg['GroupId']
        sg_client.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'UserIdGroupPairs': [
                        {
                            'Description': 'allowing ingress from nat',
                            'GroupId': os.environ['nat_sg'],
                        },
                    ]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 443,
                    'ToPort': 443,
                    'UserIdGroupPairs': [
                        {
                            'Description': 'allowing ingress from nat',
                            'GroupId': os.environ['nat_sg'],
                        },
                    ]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': int(port),
                    'ToPort': int(port),
                    'UserIdGroupPairs': [
                        {
                            'Description': 'allowing traffic from elb',
                            'GroupId': os.environ['elb_sg'],
                        },
                    ]
                },
            ]
        )
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidGroup.Duplicate':
            logger.warn(
                'Skipping this portion, security group already exist!')
        else:
            raise error

    logger.info("6. Creating Task Definition")
    # task definition
    task_definition = ecs_client.register_task_definition(
        family='task_definition_'+client,
        executionRoleArn=os.environ['role'],
        networkMode='awsvpc',
        containerDefinitions=[
            {
                'name': containerName,
                'image': image,
                'portMappings': [
                    {
                        # dynamic from dynamodb
                        'containerPort': int(port),
                    },
                ],
                'logConfiguration': {
                    'logDriver': 'awslogs',
                    'options': {
                        "awslogs-region": "eu-central-1",
                        "awslogs-group": "/ecs/front/"+client,
                        "awslogs-stream-prefix": "ecs"
                    },
                },
            },
        ],
        requiresCompatibilities=[
            'FARGATE'
        ],
        cpu='512',
        memory='1024',
    )
    taskd_arn = task_definition['taskDefinition']['taskDefinitionArn']

    logger.info("7. Creating Service")
    # service
    try:
        ecs_client.create_service(
            cluster=os.environ['cluster'],
            serviceName='service_'+client,
            taskDefinition='task_definition_'+client,
            loadBalancers=[
                {
                    'targetGroupArn': target_arn,  # arn of target group
                    'containerName': containerName,
                    'containerPort': int(port)
                },
            ],
            desiredCount=1,
            capacityProviderStrategy=[
                {
                    'capacityProvider': 'FARGATE',
                    'weight': 100
                }
            ],
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': [
                        os.environ['pub_subnet_a'],
                        os.environ['pub_subnet_b']
                    ],
                    'securityGroups': [
                        sg_id,
                    ],
                    'assignPublicIp': 'ENABLED'
                }
            },
            tags=[
                {
                    'key': 'Name',
                    'value': client
                },
                {
                    'key': 'Port',
                    'value': port
                },
                {
                    'key': 'Date',
                    'value': date
                },
            ],
            propagateTags='SERVICE',
        )
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidParameterException':
            # might have to check whether this is possible
            logger.warn('Service already existing')
        else:
            raise error

    logger.info("8. Route53 Record Set")
    # record set
    try:
        r53_client.change_resource_record_sets(
            HostedZoneId=os.environ['r53HostedZoneId'],
            ChangeBatch={
                'Comment': 'testing dns auto creation record',
                'Changes': [
                    {
                        'Action': 'CREATE',
                        'ResourceRecordSet': {
                            'Name': client+'.web.lazzaro.io',
                            'Type': 'A',
                            'AliasTarget': {
                                # zone of the load balancer
                                'HostedZoneId': os.environ['elbHostedZoneId'],
                                # need dns of balancer
                                'DNSName': os.environ['dnsName'],
                                'EvaluateTargetHealth': True
                            },
                        }
                    },
                ]
            }
        )
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidChangeBatch':
            # might have to check whether this is possible
            logger.warn('Record set already exists')
        else:
            raise error
    # 

    logger.info("9. Updating Item in DDB table")
    # update item to include more attributes
    ddb_client.update_item(
        TableName='frontend-ddb-client',
        Key={
            'Client': {
                'S': client,
            }
        },
        # UpdateExpression="SET ListenerArn = :LArn, TargetArn = :TArn, SecurityGroupId = :SGId",
        UpdateExpression="SET ListenerArn = :LArn, RuleArn = :RArn, TargetArn = :TArn, TaskDefinitionArn = :TDArn, SecurityGroupId = :SGId",
        ExpressionAttributeValues={
            ':LArn': {
                'S': listener_arn
            },
            ':RArn': {
                'S': rule_arn
            },
            ':TArn': {
                'S': target_arn
            },
            ':TDArn': {
                'S': taskd_arn
            },
            ':SGId': {
                'S': sg_id
            }
        }
    )


def handler(event, context):
    # getting client from s3 event
    key = event['Records'][0]['s3']['object']['key']
    obj = key.split('/')[1]
    client = obj.split('.')[0]

    print("Client: ", client)
    handle_service_creation(client)

    return {
        'statusCode': 200,
        'body': json.dumps('Function triggred by S3!')
    }
