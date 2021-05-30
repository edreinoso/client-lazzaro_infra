import os
import json
import boto3
import botocore
from boto3.dynamodb.conditions import Key
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Global vars: boto3 init
elb_client = boto3.client('elbv2')


def handling_service_deletion(client, port):
    # def handling_service_deletion(client, buildid):
    logger.info('Handling service deletion')

    logger.info("1. Creating Target Groups")
    # target groups
    targetg = elb_client.create_target_group(
        Name=client,  # dynamic name based on ngo
        Port=int(port),
        VpcId=os.environ['vpc_id'],  # this could probably be hardcoded
        Protocol='HTTP',  # this could possibly be dynamic
        HealthCheckPath='/healthcheck',
        HealthCheckPort=port,
        TargetType='ip',
    )
    target_arn = targetg['TargetGroups'][0]['TargetGroupArn']

    rules = elb_client.describe_rules(
        # this is gonna have to be dynamic
        ListenerArn=os.environ['listener_arn'],
    )

    # n_rules = len(rules['Rules'])  # the number of rules

    # print('rule: ', rules['Rules'])
    # print('number of rules: ', n_rules)

    # foo = len(rules['Rules'])-2
    # print('foo: num', foo)

    # print(rules['Rules'][foo])
    # # final_n = rules['Rules'][foo]['Priority']
    # final_n = int(rules['Rules'][len(rules['Rules'])-2]['Priority'])
    # print(type(final_n))

    # hello = final_n+1

    # print('hello: ', int(rules['Rules'][len(rules['Rules'])-2]['Priority'])+1)
    # print('hello: ',type(hello))

    logger.info("2. Creating Listener Rule")
    # create listener rule
    listener_rule = elb_client.create_rule(
        ListenerArn=os.environ['listener_arn'],
        Conditions=[
            {
                'Field': 'host-header',
                'Values': [
                    client+'.web.lazzaro.io'
                ]
            },
        ],
        Priority=int(rules['Rules'][len(rules['Rules'])-2]['Priority'])+1,
        Actions=[
            {
                'Type': 'forward',
                'TargetGroupArn': target_arn,
                'ForwardConfig': {
                    'TargetGroups': [
                        {
                            'TargetGroupArn': target_arn,
                        },
                    ]
                }
            },
        ],
    )
    rule_arn = listener_rule['Rules'][0]['RuleArn']


def handler(event, context):
    # boto3 init
    if(event['Records'][0]['eventName'] == "INSERT"):
        logger.info(event['Records'][0])  # need to judge whether there is
        # declaration of variables
        client = event['Records'][0]['dynamodb']['NewImage']['Client']['S']
        port = event['Records'][0]['dynamodb']['NewImage']['Port']['S']
        print("Client: ", client)
        # calling service deletion function
        # handling_service_deletion(client, port) # this is an empty build
    else:
        logger.info("Stream was not INSERT")

    return {
        'statusCode': 200,
        'body': json.dumps('Function triggred by DynamoDB Stream!')
    }
