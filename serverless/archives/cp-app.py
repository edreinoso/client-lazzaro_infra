import boto3
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/createclient", methods=['POST'])
def createclient():
    elb_client = boto3.client('elbv2')
    ecs_client = boto3.client('ecs')
    log_client = boto3.client('logs')
    
    #hardcoded vars
    vpc_id='vpc-041e9a7015a49e342' # hardcoded value
    role='arn:aws:iam::648410456371:role/frontend-services-role'
    image='648410456371.dkr.ecr.eu-central-1.amazonaws.com/lazzaro-front-repo:v4'
    cluster='arn:aws:ecs:eu-central-1:648410456371:cluster/lazzaro-front-cluster'
    listener='arn:aws:elasticloadbalancing:eu-central-1:648410456371:listener/app/lb-test-frontend-tf/719baf42afe40dff/745a97766abfd211'
    pub_subnet_a='subnet-0a0eb52403e062c21'
    pub_subnet_b='subnet-05c1fa54f8b6e620d'
    service_sg='sg-0d88106cb83bfb963'

    containerName='ecs-cluster'
    currentTime = ""
    currentTime = datetime.utcnow()

    ## payload
    name=request.json.get('name')
    port_n=request.json.get('port')

    # try:
    # creating logs
    log_client.create_log_group(
        logGroupName='/ecs/front/'+name,
        tags={
            'Name': name,
            'Date': str(currentTime.strftime("%Y-%m-%dT%H:%M:%SZ"))
        }
    )

    # creating target groups
    targetg = elb_client.create_target_group(
        Name=name, #dynamic name based on ngo
        Port=port_n,
        VpcId=vpc_id,#this could probably be hardcoded
        Protocol='HTTP',#this could possibly be dynamic
        HealthCheckPath='/healthcheck', # may or may not have to configure this
        TargetType='ip',
        Tags=[
            {
                'Key': 'Name',
                'Value': name
            },
            {
                'Key': 'Date',
                'Value': str(currentTime.strftime("%Y-%m-%dT%H:%M:%SZ"))
            },
        ]
    )
    target_arn = targetg['TargetGroups'][0]['TargetGroupArn']
    print(target_arn)

    number_of_rules = elb_client.describe_rules(
        ListenerArn=listener,
    )

    # creating listener rules
    elb_client.create_rule(
        ListenerArn=listener,
        Conditions=[
            {
                'Field': 'path-pattern',
                'PathPatternConfig': {
                    'Values': [
                        '/'+name,
                    ]
                }
            }
        ],
        Priority=len(number_of_rules['Rules']),
        Actions=[
            {
                'Type': 'forward',
                'TargetGroupArn': target_arn,
                'ForwardConfig': {
                    'TargetGroups': [
                        {
                            'TargetGroupArn': target_arn,
                            'Weight': 1
                        },
                    ],
                }
            },
        ],
        Tags=[
            {
                'Key': 'Name',
                'Value': name
            },
            {
                'Key': 'Date',
                'Value': str(currentTime.strftime("%Y-%m-%dT%H:%M:%SZ"))
            },
        ]
    )

    # creating task definition
    ecs_client.register_task_definition(
        family='task_definition_'+name,
        executionRoleArn=role,
        networkMode='awsvpc',
        containerDefinitions=[
            {
                'name': containerName,
                'image': image, # this is required from ECR
                'portMappings': [
                    {
                        'containerPort': 3000,
                        # 'hostPort': #dynamic
                    },
                ],
                'logConfiguration': {
                    'logDriver': 'awslogs',
                    'options': {
                        "awslogs-region": "eu-central-1",
                        "awslogs-group": "/ecs/front/"+name,
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

    # creating service
    ecs_client.create_service(
        cluster=cluster,
        serviceName='service_'+name,
        taskDefinition='task_definition_'+name,
        loadBalancers=[
            {
                'targetGroupArn': target_arn, # arn of target group
                'containerName': containerName,
                'containerPort': port_n
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
        tags=[
            {
                'key': 'Name',
                'value': name
            },
            {
                'key': 'Date',
                'value': str(currentTime.strftime("%Y-%m-%dT%H:%M:%SZ"))
            },
        ],
        propagateTags='SERVICE',
    )

    return "Hello World!"
    # except:
    #     return jsonify({'message' : 'An error occurred'}), 400
    