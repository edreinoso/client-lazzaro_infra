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


def handling_service_deletion(client, listener_arn, target_arn, taskd_arn):
    logger.info('Handling service deletion')
    # # hardcoded vars
    # # these could be passed as environment variables
    cluster='arn:aws:ecs:eu-central-1:648410456371:cluster/lazzaro-front-cluster'

    ## leftover services: build process | s3 object in bucket

    # delete
    logger.info('Deleting Log Group')
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

    logger.info('Deleting Listener')
    ## listener
    elb_client.delete_listener(
        ListenerArn=listener_arn
    )

    logger.info('Deleting Target Group')
    ## target groups
    elb_client.delete_target_group(
        TargetGroupArn=target_arn
    )

    logger.info('Deleting Service')
    ## service
    ecs_client.delete_service(
        cluster=cluster,
        service='service_'+client,
        force=True
    )

    logger.info('Deleting Task Definition')
    ## task definition
    ## might have to get the revision of the service (?)
    ecs_client.deregister_task_definition(
        taskDefinition=taskd_arn
    )


def handler(event, context):
    # boto3 init
    if(event['Records'][0]['eventName'] == "REMOVE"):
        logger.info(event['Records'][0])
        # declaration of variables
        listener_arn = event['Records'][0]['dynamodb']['OldImage']['ListenerArn']['S']
        taskd_arn = event['Records'][0]['dynamodb']['OldImage']['TaskDefinitionArn']['S']
        target_arn = event['Records'][0]['dynamodb']['OldImage']['TargetArn']['S']
        client = event['Records'][0]['dynamodb']['OldImage']['Client']['S']
        print(listener_arn,target_arn,client)

        # calling service deletion function
        handling_service_deletion(client, listener_arn, target_arn, taskd_arn)
    else:
        logger.info("Stream was not REMOVE")
        # logger.info("Stream was,: %s instead of REMOVED", event['Records'][0]['eventName'])

    return {
        'statusCode': 200,
        'body': json.dumps('Function triggred by DynamoDB Stream!')
    }
