import os
import boto3
import json
from datetime import datetime, timedelta

events = boto3.client('events')
lambda_function = boto3.client('lambda')

class event_bridge():
    def put_rule(self, schedule):
        events.put_rule(
            Name=self.client,
            ScheduleExpression=schedule,
            State='ENABLED',
            Description=f"Self stabilizing ELB rules in S3 file after {self.client} has been deleted",
        )

    def put_target(self):
        body = {
            "client": self.client,
            "listener_arn": self.params['listener_arn'],
            "bucket": self.params['bucket'],
            "kms_key": self.params['kms_key'],
        }

        input_obj = json.dumps(body)

        events.put_targets(
            Rule=self.client,
            Targets=[
                {
                    'Id': self.client,
                    'Arn': self.target_arn,
                    'Input': input_obj
                },
            ]
        )

    def add_lambda_permissions(self):
        lambda_function.add_permission(
            FunctionName=self.function_name,
            StatementId=self.client,
            Action=self.action,
            Principal='events.amazonaws.com',
            SourceArn=f"arn:aws:events:eu-central-1:{os.environ['account_id']}:rule/{self.client}",
        )

    def datetime_to_cron(self, dt):
        self.dt = dt
        return f"cron({dt.minute} {dt.hour} {dt.day} {dt.month} ? {dt.year})"

    def stabilize_rules(self):
        five_minutes_from_now = datetime.now() + timedelta(minutes=5)

        schedule = self.datetime_to_cron(datetime.strptime(str(five_minutes_from_now.replace(microsecond=0)), "%Y-%m-%d %H:%M:%S"))

        self.put_rule(schedule)
        self.put_target()
        self.add_lambda_permissions()

    def __init__(self, client, function_name, action, target_arn, params):
        self.client = client
        self.function_name = function_name
        self.action = action
        self.target_arn = target_arn
        self.params = params