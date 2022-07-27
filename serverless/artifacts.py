import os
import json
import logging
import sys
sys.path.append("./classes")
# params imported from SSM
# external classes
from params import get_params
from ecs import ecs_service
from elb import elb_service
from sg import security_group
from ddb import update_table, query_table
from r53 import update_record
from cw import cwd_service

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle_service_creation(client, params):
    # Local vars
    image = params['ecs']['image']+client
    container_name = params['ecs']['container']+client

    # separation of variable names
    # prod and pre environments
    if os.environ['environment'] == 'pre':
        dns = os.environ['environment']+client+'.web.lazzaro.io'
        log_group_name = '/ecs/front/'+os.environ['environment']+'/'+client
        target_group_name = os.environ['environment']+'-'+client
        sg_name = os.environ['environment']+'_'+client+'_sg'
        task_definition_fam = 'task_definition_' + \
            os.environ['environment']+'_'+client
        service_name = 'service_'+os.environ['environment']+'_'+client
    else:
        dns = client+'.web.lazzaro.io'
        log_group_name = '/ecs/front/'+client
        target_group_name = client
        sg_name = client+'_sg'
        task_definition_fam = 'task_definition_' + \
            '_'+client
        service_name = 'service_'+client

    # Init classes
    ecs = ecs_service()
    cwd = cwd_service()
    elb = elb_service()
    security = security_group()
    r53 = update_record()
    ddb_update = update_table()
    ddb_query = query_table()

    # get stuff from dynamodb
    query = ddb_query.get_item(client)

    # assigning port and date vars
    port = query['Items'][0]['Port']
    date = query['Items'][0]['Date']

    # tags
    # is this allowed?
    tags = [
        {
            'Key': 'Name',
            'Value': client
        },
        {
            'Key': 'Port',
            'Value': port
        },
        {
            'Key': 'Date',
            'Value': date
        },
        {
            'Key': 'Environment',
            'Value': os.environ['environment']
        }
    ]

    # create
    # cw logs
    logger.info("1. Creating Logs")
    ecs.create_logs(client, date, log_group_name)

    logger.info("2. Creating Target Groups")
    # elb target groups
    target_arn = elb.create_target_groups(
        client, port, target_group_name, params['network']['vpc_id'], params['elb']['alb_arn'], tags)

    logger.info("3. Creating Listerner/Rules")
    # elb listener and rule
    alb_listener = elb.create_listener_rule(client, params['elb']['alb_arn'], params['elb']['certificate_arn'], target_arn, tags, dns, params['bucket'], params['kms'])

    logger.info("5. Creating Security Group")
    # security group
    sg_id = security.create_security_group(
        client, port, params['elb']['alb_sg'], params['network']['vpc_id'], sg_name, tags)
    print(sg_id)

    logger.info("6. Creating Task Definition")
    # task definition
    taskd_arn = ecs.register_task(
        client, port, log_group_name, task_definition_fam, container_name, image, params['ecs']['role_arn'])

    logger.info("7. Creating Service")
    # service
    ecs.create_service(client, port, date, service_name, target_arn, task_definition_fam,
                       container_name, params['ecs']['cluster_arn'], sg_id, params['network'])

    logger.info("8. Route53 Record Set")
    # record set
    r53.change_record(
        'CREATE', dns, params['elb']['alb_zone'], params['elb']['alb_dns'])

    logger.info("9. Updating Item in DDB table")
    # update item to include more attributes
    ddb_update.update_item(client, alb_listener['listener_arn'], alb_listener['rule_arn'],
                           target_arn, taskd_arn, sg_id)

    # create dashboards
    cwd.create_client_dashboard()
    cwd.append_client_compute(client, params['ecs']['cluster_arn'].split('/')[1], params['cwd'])

def handler(event, context):
    # params init
    new_params = get_params()

    # getting the parameters
    params = new_params.handler(os.environ['environment'])
    print(params)

    # getting client from s3 event
    key = event['Records'][0]['s3']['object']['key']
    obj = key.split('/')[1]
    client = obj.split('.')[0]

    print("Client: ", client)
    handle_service_creation(client, params)

    return {
        'statusCode': 200,
        'body': json.dumps('Function triggered by S3!')
    }
