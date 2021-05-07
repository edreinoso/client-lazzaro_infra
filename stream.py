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
s3_client = boto3.client('s3')
ecr_client = boto3.client('ecr')
codebuild_client = boto3.client('codebuild')


def handling_service_deletion(client, listener_arn, target_arn, buildid, taskd_arn):
    logger.info('Handling service deletion')

    # delete
    logger.info('1. Deleting Log Group')
    ## logs
    try: 
        log_client.delete_log_group(
            logGroupName='/ecs/front/'+client,
        )
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'ResourceNotFoundException':
            logger.warn('Resource has been already deleted') # might have to check whether this is possible
        else:
            raise error

    logger.info('2. Deleting Listener')
    ## listener
    # elb_client.delete_listener(
    #     ListenerArn=listener_arn
    # )

    # logger.info('3. Deleting Target Group')
    # ## target groups
    # elb_client.delete_target_group(
    #     TargetGroupArn=target_arn
    # )

    # logger.info('4. Deleting Service')
    # ## service
    # ecs_client.delete_service(
    #     cluster=os.environ['cluster'],
    #     service='service_'+client,
    #     force=True
    # )

    # logger.info('5. Deleting Task Definition')
    # ## task definition
    # ## might have to get the revision of the service (?)
    # ecs_client.deregister_task_definition(
    #     taskDefinition=taskd_arn
    # )

    # logger.info('6. Object Deletion from Bucket')
    # ## s3 object
    # s3_client.delete_object(
    #     Bucket=os.environ['bucket'],
    #     Key=client,
    # )

    # logger.info('7. Deleting image from ECR')
    # ## ecr image
    # ecr_client.batch_delete_image(
    #     registryId='648410456371.dkr.ecr.eu-central-1.amazonaws.com',
    #     repositoryName='lazzaro-front-repo',
    #     imageIds=[
    #         {
    #             'imageTag': client
    #         },
    #     ]
    # )

    # logger.info('8. Deleting build')
    # ## code build
    # codebuild_client.batch_delete_builds(
    #     ids=[
    #         buildid,
    #     ]
    # )


def handler(event, context):
    # boto3 init
    if(event['Records'][0]['eventName'] == "REMOVE"):
        logger.info(event['Records'][0])
        # declaration of variables
        listener_arn = event['Records'][0]['dynamodb']['OldImage']['ListenerArn']['S']
        taskd_arn = event['Records'][0]['dynamodb']['OldImage']['TaskDefinitionArn']['S']
        target_arn = event['Records'][0]['dynamodb']['OldImage']['TargetArn']['S']
        buildid = event['Records'][0]['dynamodb']['OldImage']['BuildId']['S']
        client = event['Records'][0]['dynamodb']['OldImage']['Client']['S']
        print(listener_arn,target_arn,client)

        # calling service deletion function
        handling_service_deletion(client, listener_arn, target_arn, buildid, taskd_arn)
    else:
        logger.info("Stream was not REMOVE")
        # logger.info("Stream was,: %s instead of REMOVED", event['Records'][0]['eventName'])

    return {
        'statusCode': 200,
        'body': json.dumps('Function triggred by DynamoDB Stream!')
    }
