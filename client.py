import boto3
import os
import botocore
from datetime import datetime
from flask import Flask, request, jsonify
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
app = Flask(__name__)

# Global vars
codebuild_client = boto3.client('codebuild')
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
ddb_client = boto3.client('dynamodb')
table = dynamodb.Table('frontend-ddb-client')

@app.route("/createclient", methods=['POST'])
def createclient():
    # time
    currentTime = ""
    currentTime = datetime.utcnow()
    parsedTime = str(currentTime.strftime("%Y-%m-%dT%H:%M:%SZ"))

    name=request.json.get('name')
    port_n=request.json.get('port')
    
    # codebuild module
    logger.info("Starting Build process")
    build = codebuild_client.start_build(
        projectName='frontend-code-build-service',
        environmentVariablesOverride=[
            {
                'name': 'port',
                'value': port_n,
            },
            {
                'name': 'ong_name',
                'value': name,
            },
            {
                'name': 'date',
                'value': parsedTime
            },
            {
                "name": "aws_account_id",
                "value": "648410456371"
            },
            {
                "name": "aws_default_region",
                "value": "eu-central-1"
            },
            {
                "name": "username",
                "value": "edreinoso23"
            }
        ],
    )

    # dynamodb module
    logger.info("Putting dynamodb item")
    try:
        table.put_item(
                Item={
                    'Client': name,
                    'Date': parsedTime,
                    'Port': port_n,
                    'BuildId': build['build']['id'],
                    'ListenerArn': '',
                    'RuleArn': '',
                    'TargetArn': '',
                    'TaskDefinitionArn': '',
                    'SecurityGroupId': ''
                },
                ConditionExpression='attribute_not_exists(Client)',
            )
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'ConditionalCheckFailedException':
            logger.warn('Item is already in table') # might have to check whether this is possible
        else:
            raise error
    
    return "Client added successfully"


@app.route("/removeclient", methods=['DELETE'])
def removeclient():
    name=request.json.get('name') # client name

    ddb_client.delete_item(
        TableName='frontend-ddb-client',
        Key={
            'Client': {
                'S': name,
            }
        },
    )
    return "Client removed successfully"