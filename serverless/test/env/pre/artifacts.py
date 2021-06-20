import os
import json
import boto3
import botocore
from boto3.dynamodb.conditions import Key
import logging
import sys
sys.path.append("./classes")
from params import get_params

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
table = dynamodb.Table(os.environ['ddbTable'])

def handle_service_creation(client, params):
    image = params['image']+client
    container_name = params['container']+client
    dns = os.environ['environment']+client+'.web.lazzaro.io'
    log_group_name = '/ecs/front/'+os.environ['environment']+'/'+client
    target_group_name = os.environ['environment']+'-'+client
    sg_name = os.environ['environment']+'_'+client+'_sg'
    task_definition_fam = 'task_definition_'+os.environ['environment']+'_'+client
    service_name = 'service_'+os.environ['environment']+'_'+client

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
        {
            'Key': 'Environment',
            'Value': os.environ['environment']
        }
    ]

    # create
    # logs
    try:
        logger.info("1. Creating CloudWatch Logs")
        log_client.create_log_group(
            logGroupName=log_group_name,
            tags= {
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
    try:
        targetg = elb_client.create_target_group(
            Name=target_group_name,
            Port=int(port),
            VpcId=params['vpc_id'],
            Protocol='HTTP',
            HealthCheckPath='/healthcheck',
            HealthCheckPort=port,
            TargetType='ip',
            Tags=tags
        )
        target_arn = targetg['TargetGroups'][0]['TargetGroupArn']
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'DuplicateTargetGroupName':
            logger.warn(
                'A target group with the same name '+ client +' exists, but with different settings')
            targetg = elb_client.describe_target_groups(
                LoadBalancerArn=params['alb_arn'],
                Names=[ client ]
            )
            target_arn = targetg['TargetGroups'][0]['TargetGroupArn']
        else:
            raise error
    

    # if no listener has been found in the load balancer
    # then create a listener
    # this might require a lot of computation?
    logger.info("3. Checking to see if there's a Listener")
    # checking for listener
    describe_listener_response = elb_client.describe_listeners(
        LoadBalancerArn=params['alb_arn'],
    )

    listener_arn = ''
    if(len(describe_listener_response['Listeners']) < 1):
        logger.info("3a. Creating Listener")
        # listener
        listener = elb_client.create_listener(
            # LoadBalancerArn=os.environ['lb_arn'],
            LoadBalancerArn=params['alb_arn'],
            Protocol='HTTPS',
            Port=443,
            SslPolicy='ELBSecurityPolicy-2016-08',
            Certificates=[
                {
                    'CertificateArn': params['certificate_arn'],
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
    rule_arn=''
    if(len(rules['Rules']) < 2):
        #priority should be 1
        print('priority should be 1')
        listener_rule = elb_client.create_rule(
            ListenerArn=listener_arn,
            Conditions=[
                {
                    'Field': 'host-header',
                    'Values': [
                        dns
                    ]
                },
            ],
            Priority=1,
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
        )
        rule_arn = listener_rule['Rules'][0]['RuleArn']
    else:
        #priority should be len+1
        print('rule number: ', int(
            rules['Rules'][len(rules['Rules'])-2]['Priority'])+1)
        listener_rule = elb_client.create_rule(
            ListenerArn=listener_arn,
            Conditions=[
                {
                    'Field': 'host-header',
                    'Values': [
                        dns
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
        )
        rule_arn = listener_rule['Rules'][0]['RuleArn']

    logger.info("5. Creating Security Group")
    sg_id = ''
    # security group
    try:
        create_sg = sg_client.create_security_group(
            GroupName=sg_name,
            Description='security group for client: '+client,
            VpcId=params['vpc_id'],
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
                    'FromPort': int(port),
                    'ToPort': int(port),
                    'UserIdGroupPairs': [
                        {
                            'Description': 'allowing traffic from elb',
                            'GroupId': params['alb_sg'],
                        },
                    ]
                },
            ]
        )
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidGroup.Duplicate':
            response = sg_client.describe_security_groups(
                Filters=[
                    {
                        'Name': 'group-name',
                        'Values': [
                            sg_name,
                        ]
                    },
                ],
            )
            print(response)
            sg_id = response['SecurityGroups'][0]['GroupId']
            try:
                sg_client.authorize_security_group_ingress(
                    GroupId=sg_id,
                    IpPermissions=[
                        {
                            'IpProtocol': 'tcp',
                            'FromPort': int(port),
                            'ToPort': int(port),
                            'UserIdGroupPairs': [
                                {
                                    'Description': 'allowing traffic from elb',
                                    # 'GroupId': os.environ['elb_sg'],
                                    'GroupId': params['alb_sg'],
                                },
                            ]
                        },
                    ]
                )
            except botocore.exceptions.ClientError as error:
                if error.response['Error']['Code'] == 'InvalidPermission.Duplicate':
                    logger.warn('Security group rule already exist!')
                else:
                    raise error
            logger.warn('Skipping this portion, security group already exist!')
        else:
            raise error

    print(sg_id)

    logger.info("6. Creating Task Definition")
    # task definition
    task_definition = ecs_client.register_task_definition(
        family='task_definition_'+os.environ['environment']+'_'+client,
        # executionRoleArn=os.environ['role'],
        executionRoleArn=params['role_arn'],
        networkMode='awsvpc',
        containerDefinitions=[
            {
                'name': container_name,
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
                        "awslogs-group": log_group_name,
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
            # cluster=os.environ['cluster'],
            cluster=params['cluster_arn'],
            serviceName=service_name,
            taskDefinition=task_definition_fam,
            loadBalancers=[
                {
                    'targetGroupArn': target_arn,  # arn of target group
                    'containerName': container_name,
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
                        params['client_subnet_2_a'],
                        params['client_subnet_2_b'],
                        params['client_subnet_3_a'],
                        params['client_subnet_3_b']
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
                {
                    'key': 'Environment',
                    'value': os.environ['environment']
                },
            ],
            propagateTags='SERVICE',
        )
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidParameterException':
            logger.warn('Service already existing')
        else:
            raise error

    logger.info("8. Route53 Record Set")
    # record set
    try:
        r53_client.change_resource_record_sets(
            HostedZoneId=os.environ['r53HostedZoneId'],
            ChangeBatch={
                'Comment': 'DNS record creation for ' + os.environ['environment'] + ' environment',
                'Changes': [
                    {
                        'Action': 'CREATE',
                        'ResourceRecordSet': {
                            'Name': dns,
                            'Type': 'A',
                            'AliasTarget': {
                                # zone of the load balancer
                                'HostedZoneId': params['alb_zone'],
                                # need dns of balancer
                                'DNSName': params['alb_dns'],
                                'EvaluateTargetHealth': True
                            },
                        }
                    },
                ]
            }
        )
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidChangeBatch':
            logger.warn('Record set already exists')
        else:
            raise error

    logger.info("9. Updating Item in DDB table")
    # update item to include more attributes
    ddb_client.update_item(
        TableName=os.environ['ddbTable'],
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
    new_params = get_params()

    ## getting the parameters
    params = new_params.handler(os.environ['environment'])
    print(params)
    
    # getting client from s3 event
    key = event['Records'][0]['s3']['object']['key']
    obj = key.split('/')[1]
    client = obj.split('.')[0]

    print("Client: ", client)
    handle_service_creation(client, params)

    return {
        'statusCode': 200,
        'body': json.dumps('Function triggered by S3!')
    }
