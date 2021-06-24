import os
import boto3
import os
import botocore
import logging

logger = logging.getLogger()

# Global vars: boto3 init
log_client = boto3.client('logs')
ecs_client = boto3.client('ecs')

class ecs_service():
    def create_logs(self, client, date, log_group_name):
        self.client = client
        self.date = date
        self.log_group_name = log_group_name

        try:
            logger.info("1. Creating CloudWatch Logs")
            log_client.create_log_group(
                logGroupName=log_group_name,
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
    
    def register_task(self, client, port, log_group_name, task_definition_fam, container_name, image, role_arn):
        self.client = client
        self.port = port
        self.log_group_name = log_group_name
        self.task_definition_fam = task_definition_fam
        self.container_name = container_name
        self.image = image
        self.role_arn = role_arn

        print(client, port, log_group_name, container_name, image, role_arn)

        task_definition = ecs_client.register_task_definition(
            family=task_definition_fam,
            executionRoleArn=role_arn,
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
        return taskd_arn

    def create_service(self, client, port, date, service_name, target_arn, task_definition_fam, container_name, cluster_arn, sg_id, subnets):
        self.client = client
        self.port = port
        self.service_name = service_name
        self.target_arn = target_arn
        self.task_definition_fam = task_definition_fam
        self.container_name = container_name
        self.cluster_arn = cluster_arn
        self.sg_id = sg_id
        self.subnets = subnets
         
        try:
            ecs_client.create_service(
                # cluster=os.environ['cluster'],
                cluster=cluster_arn,
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
                            subnets['subnet_2_a'],
                            subnets['subnet_2_b'],
                            subnets['subnet_3_a'],
                            subnets['subnet_3_b'],
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
