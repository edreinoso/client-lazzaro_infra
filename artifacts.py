import json
import os
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
log_client = boto3.client('logs')
r53_client = boto3.client('route53')
table = dynamodb.Table('frontend-ddb-client')

def handle_service_creation(client):
    image=os.environ['image']+client
    containerName=os.environ['containerName']+client

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
    ## logs
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
            logger.warn('Skipping this portion, cloudwatch logs already exist!')
        else:
            raise error


    logger.info("2. Creating Target Groups")
    ## target groups --- ## stops here
    targetg = elb_client.create_target_group(
        Name=client, #dynamic name based on ngo
        Port=int(port),
        VpcId=os.environ['vpc_id'],#this could probably be hardcoded
        Protocol='HTTP',#this could possibly be dynamic
        HealthCheckPath='/healthcheck',
        HealthCheckPort=port,
        TargetType='ip',
        Tags=tags
    )
    target_arn = targetg['TargetGroups'][0]['TargetGroupArn']

    logger.info("3. Creating Listener")
    ## listener
    listener = elb_client.create_listener(
        LoadBalancerArn=os.environ['lb_arn'],
        Protocol='HTTPS',
        Port=int(port),
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

    logger.info("4. Creating Task Definition")
    ## task definition
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
                        'containerPort': int(port), # dynamic from dynamodb
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

    logger.info("5. Creating Service")
    ## service
    try:
        ecs_client.create_service(
            cluster=os.environ['cluster'],
            serviceName='service_'+client,
            taskDefinition='task_definition_'+client,
            loadBalancers=[
                {
                    'targetGroupArn': target_arn, # arn of target group
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
                    'subnets': [ # might be hardcoded as well
                        os.environ['pub_subnet_a'],
                        os.environ['pub_subnet_b']
                    ],
                    # for now this can be hardcoded, but it should probably be
                    # segragated based on clients need
                    'securityGroups': [
                        os.environ['service_sg'],
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
            logger.warn('Service already existing') # might have to check whether this is possible
        else:
            raise error
    
    logger.info("6. Route53 Record Set")
    ## record set
    r53_client.change_resource_record_sets(
        HostedZoneId=os.environ['r53HostedZoneId'],
        ChangeBatch={
            'Comment': 'testing dns auto creation record',
            'Changes': [
                {
                    'Action': 'CREATE',
                    'ResourceRecordSet': {
                        'Name': client+'.backend.lazzaro.io',
                        'Type': 'A',
                        'AliasTarget': {
                            'HostedZoneId': os.environ['elbHostedZoneId'], # zone of the load balancer
                            'DNSName': os.environ['dnsName'], # need dns of balancer
                            'EvaluateTargetHealth': True
                        },
                    }
                },
            ]
        }
    )

    logger.info("7. Updating Item in DDB table")
    ## update item to include more attributes
    ddb_client.update_item(
        TableName='frontend-ddb-client',
        Key={
            'Client': {
                'S': client,
            }
        },
        UpdateExpression="SET ListenerArn = :LArn, TargetArn = :TArn, TaskDefinitionArn = :TDArn",
        ExpressionAttributeValues={
            ':LArn': {
                'S': listener_arn,
            },
            ':TArn': {
                'S': target_arn,
            },
            ':TDArn': {
                'S': taskd_arn,
            },
        }
    )

def handler(event, context):
    # getting client from s3 event
    key = event['Records'][0]['s3']['object']['key']
    obj = key.split('/')[1]
    client = obj.split('.')[0]

    handle_service_creation(client)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Function triggred by S3!')
    }
