import os
import boto3
import botocore
from boto3.dynamodb.conditions import Key
import logging

logger = logging.getLogger()

# Global vars: boto3 init
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
table = dynamodb.Table(os.environ['ddbTable'])
ddb_client = boto3.client('dynamodb')

class query_table():
    def get_item(self, client):
        self.client = client

        query = table.query(
            KeyConditionExpression=Key('Client').eq(client)
        )
        return query


class update_table():
    def update_item(self, client, listener_arn, rule_arn, target_arn, taskd_arn, sg_id):
        self.client = client
        self.listener_arn = listener_arn
        self.rule_arn = rule_arn
        self.target_arn = target_arn
        self.taskd_arn = taskd_arn
        self.sg_id = sg_id

        ddb_client.update_item(
            TableName=os.environ['ddbTable'],
            Key={
                'Client': {
                    'S': client,
                }
            },
            # UpdateExpression="SET ListenerArn = :LArn, TargetArn = :TArn, SecurityGroupId = :SGId",
            UpdateExpression="SET ListenerArn = :LArn, RuleArn = :RArn, TargetArn = :TArn, TaskDefinitionArn = :TDArn, SecurityGroupId = :SGId",
            ExpressionAttributeValues={
                ':LArn': {
                    'S': listener_arn
                },
                ':RArn': {
                    'S': rule_arn
                },
                ':TArn': {
                    'S': target_arn
                },
                ':TDArn': {
                    'S': taskd_arn
                },
                ':SGId': {
                    'S': sg_id
                }
            }
        )
