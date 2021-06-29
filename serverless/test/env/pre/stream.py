import os
import json
import boto3
import botocore
from boto3.dynamodb.conditions import Key
import logging
import sys
sys.path.append("./classes")
from ecs import ecs_service
from elb import elb_service
from sg import security_group
from ddb import update_table, query_table
from r53 import update_record
from adhoc import adhoc_delete
from params import get_params


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handling_service_deletion(client, rule_arn, target_arn, buildid, taskd_arn, security_group_id, params):
    # Init classes
    ecs = ecs_service()
    elb = elb_service()
    r53 = update_record()
    adhoc = adhoc_delete()
    sqs = security_group()

    # Local vars
    log_group_name = '/ecs/front/'+os.environ['environment']+'/'+client
    service_name = 'service_'+os.environ['environment']+'_'+client
    s3_key = 'frontend-code-build-service/'+client+'.json'
    dns = os.environ['environment']+client+'.web.lazzaro.io'

    logger.info('Handling service deletion')

    # delete
    logger.info('1. Deleting Log Group')
    # logs
    ecs.delete_logs(log_group_name)

    logger.info('2. Deleting Listener Rule')
    # listener rule
    elb.delete_listener_rule(rule_arn)

    logger.info('3. Deleting Target Group')
    # target groups
    elb.delete_target_group(target_arn)

    logger.info('4. Deleting Service')
    # service
    ecs.delete_service(service_name, params['ecs']['cluster_arn'])

    logger.info('5. Deleting Task Definition')
    # task definition
    ecs.deregister_task(taskd_arn)

    logger.info('6. Object Deletion from Bucket')
    # s3 object
    adhoc.delete_s3_object(os.environ['bucket'], s3_key)

    logger.info('7. Deleting image from ECR')
    # ecr image
    adhoc.delete_image(os.environ['account_id'],
                       params['ecs']['repo_name'], client)

    logger.info('8. Deleting build')
    # code build
    adhoc.delete_build(buildid)

    logger.info('9. Deleting Route 53 record')
    # record set
    r53.change_record(
        'DELETE', dns, params['elb']['alb_zone'], params['elb']['alb_dns'])

    logger.info('10. Calling SQS queue')
    # sqs queue !
    sqs.call_sqs_queue(client, security_group_id, params['ecs']['queue_url'])


def handler(event, context):
    # params init
    new_params = get_params()

    ## getting the parameters
    params = new_params.handler(os.environ['environment'])

    print(params)

    if(event['Records'][0]['eventName'] == "REMOVE"):
        logger.info(event['Records'][0])  # need to judge whether there is
        # declaration of variables
        rule_arn = event['Records'][0]['dynamodb']['OldImage']['RuleArn']['S']
        taskd_arn = event['Records'][0]['dynamodb']['OldImage']['TaskDefinitionArn']['S']
        target_arn = event['Records'][0]['dynamodb']['OldImage']['TargetArn']['S']
        security_group_id = event['Records'][0]['dynamodb']['OldImage']['SecurityGroupId']['S']
        buildid = event['Records'][0]['dynamodb']['OldImage']['BuildId']['S']
        client = event['Records'][0]['dynamodb']['OldImage']['Client']['S']
        # print(listener_arn,target_arn,client)
        print("Client: ", client)
        # calling service deletion function
        # handling_service_deletion(client, target_arn, buildid, taskd_arn, security_group_id)
        handling_service_deletion(
            client, rule_arn, target_arn, buildid, taskd_arn, security_group_id, params)
        # handling_service_deletion(client, buildid) # this is an empty build
    else:
        logger.info("Stream was not REMOVE")
        logger.info("Stream was,: %s instead of REMOVED",
                    event['Records'][0]['eventName'])

    return {
        'statusCode': 200,
        'body': json.dumps('Function triggred by DynamoDB Stream!')
    }
