# import os
# import boto3

# # Global vars: boto3 init
# ecs_client = boto3.client('ecs')

# class ecs_service():
#     def task_definition():
#         print('hello world')
#         task_definition = ecs_client.register_task_definition(
#             family='task_definition_'+client,
#             # executionRoleArn=os.environ['role'],
#             executionRoleArn=params['role_arn'],
#             networkMode='awsvpc',
#             containerDefinitions=[
#                 {
#                     'name': containerName,
#                     'image': image,
#                     'portMappings': [
#                         {
#                             # dynamic from dynamodb
#                             'containerPort': int(port),
#                         },
#                     ],
#                     'logConfiguration': {
#                         'logDriver': 'awslogs',
#                         'options': {
#                             "awslogs-region": "eu-central-1",
#                             "awslogs-group": "/ecs/front/"+client,
#                             "awslogs-stream-prefix": "ecs"
#                         },
#                     },
#                 },
#             ],
#             requiresCompatibilities=[
#                 'FARGATE'
#             ],
#             cpu='512',
#             memory='1024',
#         )
#         taskd_arn = task_definition['taskDefinition']['taskDefinitionArn']

#     def create_service():
#         try:
#             ecs_client.create_service(
#                 # cluster=os.environ['cluster'],
#                 cluster=params['cluster_arn'],
#                 serviceName='service_'+client,
#                 taskDefinition='task_definition_'+client,
#                 loadBalancers=[
#                     {
#                         'targetGroupArn': target_arn,  # arn of target group
#                         'containerName': containerName,
#                         'containerPort': int(port)
#                     },
#                 ],
#                 desiredCount=1,
#                 capacityProviderStrategy=[
#                     {
#                         'capacityProvider': 'FARGATE',
#                         'weight': 100
#                     }
#                 ],
#                 networkConfiguration={
#                     'awsvpcConfiguration': {
#                         'subnets': [
#                             # os.environ['pub_subnet_a'],
#                             params['client_subnet_2_a'],
#                             # os.environ['pub_subnet_b']
#                             params['client_subnet_2_b'],
#                             params['client_subnet_3_a'],
#                             params['client_subnet_3_b']
#                         ],
#                         'securityGroups': [
#                             sg_id,
#                         ],
#                         'assignPublicIp': 'ENABLED'
#                     }
#                 },
#                 tags=[
#                     {
#                         'key': 'Name',
#                         'value': client
#                     },
#                     {
#                         'key': 'Port',
#                         'value': port
#                     },
#                     {
#                         'key': 'Date',
#                         'value': date
#                     },
#                 ],
#                 propagateTags='SERVICE',
#             )
#         except botocore.exceptions.ClientError as error:
#             if error.response['Error']['Code'] == 'InvalidParameterException':
#                 # might have to check whether this is possible
#                 logger.warn('Service already existing')
#             else:
#                 raise error
