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

def handler(event, context):
    logger.info('11. Deleting Security Group')
    print(event)

    sg_id = event['Records'][0]['messageAttributes']['sgId']['stringValue']
    
    print(sg_id)

    sg = security_group()

    res_del = sg.delete_security_group(sg_id)

    print(res_del)

    return {
        'statusCode': 200,
        'body': json.dumps(res_del)
        # 'body': json.dumps('Hello world')
    }
