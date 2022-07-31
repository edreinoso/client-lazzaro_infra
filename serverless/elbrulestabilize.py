import boto3
import os
import json

"""
This function would be invoked by an event from eventbridge
Only after a client has been removed from the system
The purpose is to stabilize the priority rules
- Describe the rules from the load balancer - describe_rules()
- Loop through the rules
- Exclude the default one
- Append the priority rule number to a list
- Range number from (1,100)
- If n not in the list from above
"""

elb = boto3.client('elbv2')
s3 = boto3.client('s3')
lambda_function = boto3.client('lambda')
events = boto3.client('events')

def handle_stabilize_rules(listener_arn, bucket, kms_key):
    object_name = f"/{os.environ['environment']}/s3rules.json"
    file_name = '/tmp/rules.json'


    dict_rules = elb.describe_rules(
        ListenerArn = listener_arn
    )

    rule_priority = []

    for rule in dict_rules['Rules']:
        if rule['Priority'] != 'default':
            rule_priority.append(int(rule['Priority']))

    queue = []
    for number in range(1,100):
        if number not in rule_priority:
            queue.append(number)

    body = {
        "rules": queue
    }

    json_obj = json.dumps(body)

    # put the json_obj into a file
    with open(file_name, 'w') as file:
        file.write(json_obj)

    with open(file_name, "rb") as data:
        s3.put_object(
            Bucket=bucket,
            Body=data,
            Key=object_name,
            ServerSideEncryption='aws:kms',
            SSEKMSKeyId=kms_key,
        )

def handle_event_deletion(client):
    """
        Event in the bus should be deleted
        need to pass in the statement id (name of event)
    """
    lambda_function.remove_permission(
        FunctionName=os.environ['elb_lambda'].split('/')[6],
        StatementId=client,
    )

    events.remove_targets(
        Rule=client,
        Ids=[
            client,
        ],
    )
    events.delete_rule(
        Name=client,
    )

def handler(event, context):
    listener_arn = event['listener_arn']
    bucket = event['bucket']
    kms_key = event['kms_key']
    client = event['client']

    handle_stabilize_rules(listener_arn, bucket, kms_key)
    handle_event_deletion(client)