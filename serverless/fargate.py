import boto3
import json
import logging
from datetime import datetime

ecs = boto3.client('ecs')
rds = boto3.client('rds', region_name="eu-west-1")

currentTime = datetime.utcnow()

def handler(event, context):
    cluster = 'lazzaro-front-cluster-pre'

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

    # stopping RDS instance
    instance_id = 'treasure-map'
    rds.stop_db_instance(
        DBInstanceIdentifier=instance_id,
    )

    return {
        'statusCode': 200,
        'body': json.dumps('ECS savings has been applied')
    }