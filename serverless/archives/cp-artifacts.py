import json
import boto3
from boto3.dynamodb.conditions import Key

def handler(event, context):
    # boto3 init
    dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
    elb_client = boto3.client('elbv2')
    ecs_client = boto3.client('ecs')
    log_client = boto3.client('logs')
    table = dynamodb.Table('frontend-dynamodb-service')
    
    # getting client from s3 event
    key = event['Records'][0]['s3']['object']['key']
    obj = key.split('/')[1]
    client = obj.split('.')[0]

    #hardcoded vars
    vpc_id='vpc-041e9a7015a49e342' # hardcoded value
    role='arn:aws:iam::648410456371:role/frontend-services-role'
    image='648410456371.dkr.ecr.eu-central-1.amazonaws.com/lazzaro-front-repo:'+client
    containerName='ecs-cluster-'+client
    cluster='arn:aws:ecs:eu-central-1:648410456371:cluster/lazzaro-front-cluster'
    lb_arn='arn:aws:elasticloadbalancing:eu-central-1:648410456371:loadbalancer/app/lb-test-frontend-tf/719baf42afe40dff'
    # listener='arn:aws:elasticloadbalancing:eu-central-1:648410456371:listener/app/lb-test-frontend-tf/719baf42afe40dff/745a97766abfd211'
    pub_subnet_a='subnet-0a0eb52403e062c21'
    pub_subnet_b='subnet-05c1fa54f8b6e620d'
    service_sg='sg-0d88106cb83bfb963'


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
    ]

    # create
    ## logs
    log_client.create_log_group(
        logGroupName='/ecs/front/'+client,
        tags={
            'Name': client,
            'Date': date
        }
    )

    ## target groups
    targetg = elb_client.create_target_group(
        Name=client, #dynamic name based on ngo
        Port=port,
        VpcId=vpc_id,#this could probably be hardcoded
        Protocol='HTTP',#this could possibly be dynamic
        HealthCheckPath='/healthcheck',
        TargetType='ip',
        Tags=tags
    )
    target_arn = targetg['TargetGroups'][0]['TargetGroupArn']

    ## listener
    elb_client.create_listener(
        LoadBalancerArn=lb_arn,
        Protocol='HTTP',
        Port=port,
        # this might be useful later
        # SslPolicy='string',
        # Certificates=[
        #     {
        #         'CertificateArn': 'string',
        #     },
        # ],
        DefaultActions=[
            {
                'Type': 'forward',
                'TargetGroupArn': target_arn,
            },
        ],
        Tags=tags
    )


    ## task definition
    ecs_client.register_task_definition(
        family='task_definition_'+client,
        executionRoleArn=role,
        networkMode='awsvpc',
        containerDefinitions=[
            {
                'name': containerName,
                'image': image,
                'portMappings': [
                    {
                        'containerPort': port, # dynamic from dynamodb
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

    ## service
    ecs_client.create_service(
        cluster=cluster,
        serviceName='service_'+client,
        taskDefinition='task_definition_'+client,
        loadBalancers=[
            {
                'targetGroupArn': target_arn, # arn of target group
                'containerName': containerName,
                'containerPort': port
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
                    pub_subnet_a,
                    pub_subnet_b
                ],
                # for now this can be hardcoded, but it should probably be
                # segragated based on clients need
                'securityGroups': [
                    service_sg,
                ],
                'assignPublicIp': 'ENABLED'
            }
        },
        tags=tags,
        propagateTags='SERVICE',
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Function triggred by S3!')
    }
