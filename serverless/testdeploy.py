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

# Global vars: boto3 init
elb_client = boto3.client('elbv2')

def handler(event, context):
    new_params = get_params()
    port="2345"
    client="testservice2"

    ## getting the parameters
    params = new_params.handler(os.environ['environment'])
    print(params)

    logger.info("2. Creating Target Groups")
    targetg = elb_client.create_target_group(
        Name=client,  # dynamic name based on ngo
        Port=int(port),
        # VpcId=os.environ['vpc_id'],
        VpcId=params['vpc_id'],
        Protocol='HTTP',  # this could possibly be dynamic
        HealthCheckPath='/healthcheck',
        HealthCheckPort=port,
        TargetType='ip',
    )
    target_arn = targetg['TargetGroups'][0]['TargetGroupArn']

    logger.info("3. Checking to see if there's a Listener")
    # checking for listener
    describe_listener_response = elb_client.describe_listeners(
        LoadBalancerArn=params['alb_arn'],
    )

    listener_arn = ''
    if(len(describe_listener_response['Listeners']) < 1):
        logger.info("3a. Creating Listener")
        # not going to create the listener itself
    else:
        # assigning arn of the listener
        listener_arn = describe_listener_response['Listeners'][0]['ListenerArn']

    rules = elb_client.describe_rules(
        # this is gonna have to be dynamic
        ListenerArn=listener_arn,
    )

    print(rules['Rules'])
    print(len(rules['Rules']))
    if(len(rules['Rules']) < 2):
        #priority should be 1
        print('priority should be 1')
        listener_rule = elb_client.create_rule(
            ListenerArn=listener_arn,
            Conditions=[
                {
                    'Field': 'host-header',
                    'Values': [
                        client+'.web.lazzaro.io'
                    ]
                },
            ],
            Priority=1,
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
        print(rule_arn)
    else:
        #priority should be len+1
        print('rule number: ', int(rules['Rules'][len(rules['Rules'])-2]['Priority'])+1)
        listener_rule = elb_client.create_rule(
            ListenerArn=listener_arn,
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
        print(rule_arn)

    return {
        'statusCode': 200,
        'body': json.dumps('Function triggered by S3!')
    }
