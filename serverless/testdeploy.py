import os
import json
import boto3
import botocore
from boto3.dynamodb.conditions import Key
import logging
import sys
sys.path.append("./classes")
from sg import security_group

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info('Testing security group deletion')
    
    # sg_id = event['Record'][0]['messageAttribute']['sgId']

    client = 'helloworld'
    security_group_id = 'sg-08ed227fd1347d68f'
    queue_url = 'https://sqs.eu-central-1.amazonaws.com/648410456371/lazzaro-sqs-service-pre'

    print(security_group_id, queue_url)

    sqs = security_group()

    sqs.call_sqs_queue(client, security_group_id, queue_url)

    return {
        'statusCode': 200,
        # 'body': json.dumps(res_del)
        'body': json.dumps('Hello world')
    }
