import os
import boto3

events = boto3.client('events')
lambda_function = boto3.client('lambda')

class event_bridge():
    def put_rule(self, client, schedule):
        self.client = client
        self.schedule = schedule
        
        events.put_rule(
            Name=client,
            ScheduleExpression=schedule,
            State='ENABLED',
            Description=f"Self stabilizing ELB rules in S3 file after {client} has been deleted",
        )

    def put_target(self, client, target_arn):
        self.client = client
        self.target_arn = target_arn

        events.put_targets(
            Rule=client,
            Targets=[
                {
                    'Id': client,
                    'Arn': target_arn,
                },
            ]
        )

    def add_lambda_permissions(self, client, function_name, action):
        self.function_name = function_name
        self.client = client
        self.action = action
        
        lambda_function.add_permission(
            FunctionName=function_name,
            StatementId=client,
            Action=action,
            Principal='events.amazonaws.com',
            SourceArn=f"arn:aws:events:eu-central-1:{os.environ['Account_Number']}:rule/{client}",
        )

    def stabilize_rules(self, client, function_name, action, schedule, target_arn):
        self.client = client
        self.schedule = schedule
        self.function_name = function_name # this could be from serverless
        self.action = action
        self.target_arn = target_arn # this should be obtained from serverless output

        self.put_rule(client, schedule)
        self.put_target(client, target_arn)
        self.add_lambda_permissions(client, function_name, action)
        