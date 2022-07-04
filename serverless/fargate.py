import boto3
import json
import logging
from datetime import datetime

ecs = boto3.client('ecs')

currentTime = datetime.utcnow()

def handler(event, context):
    cluster = 'lazzaro-front-cluster-pre'

    # have to check couple of variables.
    # 1. whether eventbridge has events scheduled on gmt ✅
    # 2. 24h should be accounted ✅
    # 3. invocation would work exactly with the specified logic ✅

    print(currentTime.strftime('%H:%M'))

    if currentTime.strftime('%H:%M') == "06:00":
        # turn on services
        desireCount = 1
    else:
        # turn off services
        desireCount = 0

    response = ecs.list_services(
        cluster=cluster,
    )

    print(desireCount)

    for n in response['serviceArns']:
        ecs.update_service(
            cluster=cluster,
            service=n,
            desiredCount=desireCount,
        )

    return {
        'statusCode': 200,
        'body': json.dumps('ECS savings has been applied')
    }