import json
import boto3
from boto3.dynamodb.conditions import Key
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handling_service_deletion():
    print('hello world')


def handler(event, context):
    # boto3 init
    if(event['Records'][0]['eventName'] == "REMOVE"):
        # logging test service
        logger.info(event['Records'][0]['dynamodb']['OldImage']['ListenerArn']['S'])
        logger.info(event['Records'][0]['dynamodb']['OldImage']['TargetArn']['S'])

        # declaration of variables
        listener_arn = event['Records'][0]['dynamodb']['OldImage']['ListenerArn']['S']
        target_arn = event['Records'][0]['dynamodb']['OldImage']['TargetArn']['S']
        print(listener_arn, target_arn)
        handling_service_deletion()
    else:
        logger.info("Stream was,: %s instead of REMOVED", event['Records'][0]['eventName'])

    # # hardcoded vars
    # # these could be passed as environment variables
    # cluster='arn:aws:ecs:eu-central-1:648410456371:cluster/lazzaro-front-cluster'

    # # create
    # ## logs
    # log_client.delete_log_group(
    #     logGroupName='/ecs/front/'+client,
    # )

    # ## listener
    # elb_client.delete_listener(
    #     ListenerArn=listener_arn
    # )

    # ## target groups
    # elb_client.delete_target_group(
    #     TargetGroupArn=target_arn
    # )

    # ## task definition
    # ecs_client.deregister_task_definition(
    #     taskDefinition='task_definition_'+client
    # )

    # ## service
    # ecs_client.delete_service(
    #     cluster=cluster,
    #     serviceName='service_'+client,
    # )

    return {
        'statusCode': 200,
        'body': json.dumps('Function triggred by S3!')
    }
