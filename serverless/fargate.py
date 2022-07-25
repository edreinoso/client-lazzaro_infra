import boto3
import json
import logging
from datetime import datetime

ecs = boto3.client('ecs')
rds = boto3.client('rds', region_name="eu-west-1")

currentTime = datetime.utcnow()

def handler(event, context):
    cluster = 'lazzaro-front-cluster-pre'
    instance_id = 'treasure-map'
    print(currentTime.strftime('%H:%M'))

    if currentTime.strftime('%H:%M') == "06:00":
        # turn on services
        desire_count = 1
        turn_on_rds(instance_id)
    else:
        # turn off services
        desire_count = 0
        turn_off_rds(instance_id)

    response = ecs.list_services(
        cluster=cluster,
    )

    print(desire_count)

    for n in response['serviceArns']:
        ecs.update_service(
            cluster=cluster,
            service=n,
            desiredCount=desire_count,
        )

    return {
        'statusCode': 200,
        'body': json.dumps('ECS savings has been applied')
    }

def turn_on_rds(rds_id):
    rds_start = rds.start_db_instance(
        DBInstanceIdentifier=rds_id,
    )
    print("turning on rds instance", rds_id, rds_start)

def turn_off_rds(rds_id):
    rds_stop = rds.stop_db_instance(
        DBInstanceIdentifier=rds_id,
    )
    print("turning on rds instance", rds_id, rds_stop)