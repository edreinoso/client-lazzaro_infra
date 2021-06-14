import os
import json
import boto3
import botocore
from boto3.dynamodb.conditions import Key
import logging
import sys
sys.path.append("./classes")
from params import get_params

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    new_params = get_params()

    params = new_params.handler(os.environ['environment'])

    print(params)

    return {
        'statusCode': 200,
        'body': json.dumps('Function triggred by S3!')
    }
