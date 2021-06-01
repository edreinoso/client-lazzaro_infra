import boto3
import os
import botocore
import re
from datetime import datetime
from flask import Flask, request, jsonify, Response
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
app = Flask(__name__)

# Global vars
codebuild_client = boto3.client('codebuild')
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
ddb_client = boto3.client('dynamodb')
table = dynamodb.Table(os.environ['ddbTable'])
# validating string
regex_string = '^[a-zA-Z]{3,}$'  # would probably have to change


def isValidString(string):
    return re.match(regex_string, string)


def build_process(port_n, name, parsedTime):
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
    return build


def readingFromDDBTable(name):
    # query dynamodb table for the item
    logger.info("Checking if client already exists")
    res = ddb_client.query(
        TableName=os.environ['ddbTable'],
        KeyConditionExpression='#Client = :Client',
        ExpressionAttributeNames={
            '#Client': 'Client'
        },
        ExpressionAttributeValues={
            ':Client': {
                'S': name,
            }
        }
    )
    return res


@app.route("/createclient", methods=['POST'])
def createclient():
    # time
    currentTime = ""
    currentTime = datetime.utcnow()
    parsedTime = str(currentTime.strftime("%Y-%m-%dT%H:%M:%SZ"))
    ddbQuery = {}
    name = request.json.get('name')
    port_n = request.json.get('port')

    # should probably return an error if a certain string is not within
    # certain parameters
    if isValidString(name):
        print('Client: ',name)
        ddbQuery = readingFromDDBTable(name)
        if (ddbQuery['Count'] == 0):
            logger.info("Starting Build process")
            build = build_process(port_n, name, parsedTime)

            # Putting item in dynamodb table
            logger.info("Putting dynamodb item")
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
            )
            res = Response("Client added successfully",
                            status=200, mimetype='application/json')
            return res
        else:
            res = Response("Client already exists",
                            status=400, mimetype='application/json')
            return res
    else:
        res = Response("Please enter a valid string",
                       status=400, mimetype='application/json')
        return res

    # codebuild module


@app.route("/removeclient", methods=['DELETE'])
def removeclient():
    name = request.json.get('name')  # client name

    # there should be a handler here to check whether the item
    # is in the db
    if isValidString(name):
        try:
            ddb_client.delete_item(
                TableName='frontend-ddb-client',
                Key={
                    'Client': {
                        'S': name,
                    }
                },
            )
            res = Response("Client removed successfully",
                           status=200, mimetype='application/json')
            return res
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'ConditionalCheckFailedException':
                # might have to check whether this is possible
                res = Response("Client was not found",
                               status=400, mimetype='application/json')
                return res
            else:
                raise error
    else:
        res = Response("Please enter a valid string",
                       status=400, mimetype='application/json')
        return res
