import os
import json
import boto3
import botocore
from boto3.dynamodb.conditions import Key
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Global vars: boto3 init
log_client = boto3.client('logs')
elb_client = boto3.client('elbv2')
ecs_client = boto3.client('ecs')
sg_client = boto3.client('ec2')
s3_client = boto3.client('s3')
ecr_client = boto3.client('ecr')
codebuild_client = boto3.client('codebuild')
r53_client = boto3.client('route53')

# def handling_service_deletion(client, target_arn, buildid, taskd_arn, security_group_id):
# def handling_service_deletion(client, rule_arn, target_arn, buildid, taskd_arn, security_group_id):
def handling_service_deletion(client, buildid):
    logger.info('Handling service deletion')

    # delete
    # logger.info('1. Deleting Log Group')
    # # logs
    # try:
    #     log_client.delete_log_group(
    #         logGroupName='/ecs/front/'+client,
    #     )
    # except botocore.exceptions.ClientError as error:
    #     if error.response['Error']['Code'] == 'ResourceNotFoundException':
    #         logger.warn('Resource has been already deleted')
    #     else:
    #         raise error

    # logger.info('2. Deleting Listener Rule')
    # # listener rule
    # # elb_client.delete_listener(
    # #     ListenerArn=listener_arn
    # # )
    # try:
    #     elb_client.delete_rule(
    #         RuleArn=rule_arn
    #     )
    # except botocore.exceptions.ClientError as error:
    #     raise error

    # logger.info('3. Deleting Target Group')
    # # target groups
    # try:
    #     #
    #     elb_client.delete_target_group(
    #         TargetGroupArn=target_arn
    #     )
    # except botocore.exceptions.ClientError as error:
    #     if error.response['Error']['Code'] == 'ValidationError':
    #         logger.warn('A target group ARN must be specified')
    #     else:
    #         raise error

    # logger.info('4. Deleting Service')
    # # service
    # try:
    #     ecs_client.delete_service(
    #         cluster=os.environ['cluster'],
    #         service='service_'+client,
    #         force=True
    #     )
    # except botocore.exceptions.ClientError as error:
    #     if error.response['Error']['Code'] == 'ServiceNotFoundException':
    #         logger.warn('Service not found')
    #     elif error.response['Error']['Code'] == 'InvalidParameterException':
    #         logger.warn('Service must match ^[a-zA-Z0-9\-_]{1,255}$')
    #     else:
    #         raise error

    # logger.info('5. Deleting Task Definition')
    # # task definition
    # # might have to get the revision of the service (?)
    # try:
    #     ecs_client.deregister_task_definition(
    #         taskDefinition=taskd_arn
    #     )
    #     #
    # except botocore.exceptions.ClientError as error:
    #     if error.response['Error']['Code'] == 'InvalidParameterException':
    #         logger.warn('Task Definition can not be blank')
    #     else:
    #         raise error

    logger.info('6. Object Deletion from Bucket')
    # s3 object
    try:
        s3_client.delete_object(
            Bucket=os.environ['bucket'],
            Key='frontend-code-build-service/'+client+'.json'
        )
        # logger.info(s3res)
    except botocore.exceptions.ClientError as error:
        raise error

    logger.info('7. Deleting image from ECR')
    # ecr image
    try:
        ecr_client.batch_delete_image(
            registryId=os.environ['account_id'],
            repositoryName=os.environ['repositoryName'],
            imageIds=[
                {
                    'imageTag': client
                },
            ]
        )
        # logger.info(ecr_res)
    except botocore.exceptions.ClientError as error:
        raise error

    logger.info('8. Deleting build')
    # code build
    try:
        codebuild_client.batch_delete_builds(
            ids=[
                buildid,
            ]
        )
        # logger.info(cb_res)
    except botocore.exceptions.ClientError as error:
        raise error

    # logger.info('9. Deleting Route 53 record')
    # ## record set
    # try:
    #     r53_client.change_resource_record_sets(
    #         HostedZoneId=os.environ['r53HostedZoneId'],
    #         ChangeBatch={
    #             'Comment': 'testing dns auto creation record',
    #             'Changes': [
    #                 {
    #                     'Action': 'DELETE',
    #                     'ResourceRecordSet': {
    #                         'Name': client+'.backend.lazzaro.io',
    #                         'Type': 'A',
    #                         'AliasTarget': {
    #                             # zone of the load balancer
    #                             'HostedZoneId': os.environ['elbHostedZoneId'],
    #                             # need dns of balancer
    #                             'DNSName': os.environ['dnsName'],
    #                             'EvaluateTargetHealth': True
    #                         },
    #                     }
    #                 },
    #             ]
    #         }
    #     )
    # except botocore.exceptions.ClientError as error:
    #     if error.response['Error']['Code'] == 'InvalidChangeBatch':
    #         logger.warn('Record was not found')
    #     else:
    #         raise error

    # logger.info('10. Deleting Security Group')
    # security group
    # try:
    #     sg_client.delete_security_group(
    #         GroupId=security_group_id
    #     )
    #     # MissingParameter
    # except botocore.exceptions.ClientError as error:
    #     if error.response['Error']['Code'] == 'MissingParameter':
    #         logger.warn(
    #             'The request must contain the parameter groupName or groupId')
    #     elif error.response['Error']['Code'] == 'InvalidGroup.NotFound':
    #         logger.warn(
    #             'The security group does not exist')
    #     elif error.response['Error']['Code'] == 'DependencyViolation':
    #         logger.warn(
    #             'The security group has a dependent object')
    #     else:
    #         raise error


def handler(event, context):
    # boto3 init
    if(event['Records'][0]['eventName'] == "REMOVE"):
        logger.info(event['Records'][0])  # need to judge whether there is
        # declaration of variables
        # rule_arn = event['Records'][0]['dynamodb']['OldImage']['RuleArn']['S']
        # taskd_arn = event['Records'][0]['dynamodb']['OldImage']['TaskDefinitionArn']['S']
        # target_arn = event['Records'][0]['dynamodb']['OldImage']['TargetArn']['S']
        # security_group_id = event['Records'][0]['dynamodb']['OldImage']['SecurityGroupId']['S']
        buildid = event['Records'][0]['dynamodb']['OldImage']['BuildId']['S']
        client = event['Records'][0]['dynamodb']['OldImage']['Client']['S']
        # print(listener_arn,target_arn,client)
        print("Client: ", client)
        # calling service deletion function
        # handling_service_deletion(client, target_arn, buildid, taskd_arn, security_group_id)
        # handling_service_deletion(
        #     client, rule_arn, target_arn, buildid, taskd_arn, security_group_id)
        handling_service_deletion(client, buildid) # this is an empty build
    else:
        logger.info("Stream was not REMOVE")
        # logger.info("Stream was,: %s instead of REMOVED", event['Records'][0]['eventName'])

    return {
        'statusCode': 200,
        'body': json.dumps('Function triggred by DynamoDB Stream!')
    }
