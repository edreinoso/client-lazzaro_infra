import os
import boto3

# Global vars: boto3 init
ssm_params = boto3.client('ssm')

# Getting the infra parameters from SSM Parameter Store
class get_params():
    def handler(self, env):
        self.env = env
        
        print('line 12, get parmas: ', env)

        dict_of_params = {}

        ### network
        ## getting vpc id
        vpc_id = ssm_params.get_parameter(
            Name='/prod/share/network/vpc/vpc_id',
        )
        dict_of_params['vpc_id'] = vpc_id['Parameter']['Value']

        ## getting subnet id - 2 a
        client_subnet_2_a = ssm_params.get_parameter(
            Name='/prod/share/network/subnet/client_subnet_2_a',
        )
        dict_of_params['client_subnet_2_a'] = client_subnet_2_a['Parameter']['Value']
        ## getting subnet id - 2 b
        client_subnet_2_b = ssm_params.get_parameter(
            Name='/prod/share/network/subnet/client_subnet_2_b',
        )
        dict_of_params['client_subnet_2_b'] = client_subnet_2_b['Parameter']['Value']
        ## getting subnet id - 3 a
        client_subnet_3_a = ssm_params.get_parameter(
            Name='/prod/share/network/subnet/client_subnet_3_a',
        )
        dict_of_params['client_subnet_3_a'] = client_subnet_3_a['Parameter']['Value']
        ## getting subnet id - 3 b
        client_subnet_3_b = ssm_params.get_parameter(
            Name='/prod/share/network/subnet/client_subnet_3_b',
        )
        dict_of_params['client_subnet_3_b'] = client_subnet_3_b['Parameter']['Value']

        ### ecs
        ## role
        role_arn = ssm_params.get_parameter(
            Name='/'+env+'/front/services/ecs/role_arn',
        )
        dict_of_params['role_arn'] = role_arn['Parameter']['Value']
        ## repo name
        repo_name = ssm_params.get_parameter(
            Name='/'+env+'/front/services/ecs/repo_name',
        )
        dict_of_params['repo_name'] = repo_name['Parameter']['Value']
        ## cluster arn
        cluster_arn = ssm_params.get_parameter(
            Name='/'+env+'/front/services/ecs/cluster_arn',
        )
        dict_of_params['cluster_arn'] = cluster_arn['Parameter']['Value']
        ## image
        image = ssm_params.get_parameter(
            Name='/'+env+'/front/services/ecs/image',
        )
        dict_of_params['image'] = image['Parameter']['Value']
        ## container name
        container = ssm_params.get_parameter(
            Name='/'+env+'/front/services/ecs/container',
        )
        dict_of_params['container'] = container['Parameter']['Value']

        ### elb
        ## arn
        alb_arn = ssm_params.get_parameter(
            Name='/'+env+'/front/services/elb/alb_arn',
        )
        dict_of_params['alb_arn'] = alb_arn['Parameter']['Value']
        ## dns
        alb_dns = ssm_params.get_parameter(
            Name='/'+env+'/front/services/elb/alb_dns',
        )
        dict_of_params['alb_dns'] = alb_dns['Parameter']['Value']
        ## zone
        alb_zone = ssm_params.get_parameter(
            Name='/'+env+'/front/services/elb/alb_zone',
        )
        dict_of_params['alb_zone'] = alb_zone['Parameter']['Value']
        ## sg
        alb_sg = ssm_params.get_parameter(
            Name='/'+env+'/front/services/elb/alb_sg',
        )
        dict_of_params['alb_sg'] = alb_sg['Parameter']['Value']
        ## certificate
        certificate_arn = ssm_params.get_parameter(
            Name='/'+env+'/front/services/elb/certificate_arn',
        )
        dict_of_params['certificate_arn'] = certificate_arn['Parameter']['Value']
        
        return dict_of_params
