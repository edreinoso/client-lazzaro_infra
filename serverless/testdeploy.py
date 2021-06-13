import os
import json
import boto3
import botocore
from boto3.dynamodb.conditions import Key
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Global vars: boto3 init
ssm_params = boto3.client('ssm')

# Getting the infra parameters from SSM Parameter Store
def get_all_params(env):
    dict_of_params = {}
    
    ### network
    ## getting vpc id
    vpc_id = ssm_params.get_parameter(
        Name='/prod/share/network/vpc/vpc_id',
    )
    dict_of_params['vpc_id'] = vpc_id

    ## getting subnet id - 2 a
    client_subnet_2_a = ssm_params.get_parameter(
        Name='/prod/share/network/subnet/client_subnet_2_a',
    )
    dict_of_params['client_subnet_2_a'] = client_subnet_2_a
    ## getting subnet id - 2 b
    client_subnet_2_b = ssm_params.get_parameter(
        Name='/prod/share/network/subnet/client_subnet_2_b',
    )
    dict_of_params['client_subnet_2_b'] = client_subnet_2_b
    ## getting subnet id - 3 a
    client_subnet_3_a = ssm_params.get_parameter(
        Name='/prod/share/network/subnet/client_subnet_3_a',
    )
    dict_of_params['client_subnet_3_a'] = client_subnet_3_a
    ## getting subnet id - 3 b
    client_subnet_3_b = ssm_params.get_parameter(
        Name='/prod/share/network/subnet/client_subnet_3_b',
    )
    dict_of_params['client_subnet_3_b'] = client_subnet_3_b
    
    ### ecs
    ## role
    role_arn = ssm_params.get_parameter(
        Name='/'+env+'/front/services/ecs/role_arn',
    )
    dict_of_params['role_arn'] = role_arn
    ## repo name
    repo_name = ssm_params.get_parameter(
        Name='/'+env+'/front/services/ecs/repo_name',
    )
    dict_of_params['repo_name'] = repo_name
    ## cluster arn
    cluster_arn = ssm_params.get_parameter(
        Name='/'+env+'/front/services/ecs/cluster_arn',
    )
    dict_of_params['cluster_arn'] = cluster_arn
    ## image
    image = ssm_params.get_parameter(
        Name='/'+env+'/front/services/ecs/image',
    )
    dict_of_params['image'] = image
    ## container name
    container = ssm_params.get_parameter(
        Name='/'+env+'/front/services/ecs/container',
    )
    dict_of_params['container'] = container

    ### elb
    ## arn
    alb_arn = ssm_params.get_parameter(
        Name='/'+env+'/front/services/elb/alb_arn',
    )
    dict_of_params['alb_arn'] = alb_arn
    ## dns
    alb_dns = ssm_params.get_parameter(
        Name='/'+env+'/front/services/elb/alb_dns',
    )
    dict_of_params['alb_dns'] = alb_dns
    ## zone
    alb_zone = ssm_params.get_parameter(
        Name='/'+env+'/front/services/elb/alb_zone',
    )
    dict_of_params['alb_zone'] = alb_zone
    ## sg
    alb_sg = ssm_params.get_parameter(
        Name='/'+env+'/front/services/elb/alb_sg',
    )
    dict_of_params['alb_sg'] = alb_sg
    ## certificate
    certificate_arn = ssm_params.get_parameter(
        Name='/'+env+'/front/services/elb/certificate_arn',
    )
    dict_of_params['certificate_arn'] = certificate_arn

    print(dict_of_params)

    return dict_of_params

def handler(event, context):
    params = get_all_params(os.environ['environment'])

    print(params)

    return {
        'statusCode': 200,
        'body': json.dumps('Function triggred by S3!')
    }
