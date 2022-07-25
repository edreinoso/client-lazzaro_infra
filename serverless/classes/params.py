import os
import boto3

# Global vars: boto3 init
ssm_params = boto3.client('ssm')

# Getting the infra parameters from SSM Parameter Store


class get_params():
    def handler(self, env):
        self.env = env

        params = {}

        # network
        network_request_values = ssm_params.get_parameters_by_path(
            Path='/'+env+'/share/network/')['Parameters']

        network_res = {}
        for param in network_request_values:
            key = param['Name'].replace('/'+env+'/share/network/', '')
            network_res[key] = param['Value']

        # ecs
        ecs_request_values = ssm_params.get_parameters_by_path(
            Path='/'+env+'/front/services/ecs/')['Parameters']

        ecs_res = {}
        for param in ecs_request_values:
            key = param['Name'].replace(
                '/'+env+'/front/services/ecs/', '')
            ecs_res[key] = param['Value']

        # elb
        elb_request_values = ssm_params.get_parameters_by_path(
            Path='/'+env+'/front/services/elb/')['Parameters']

        elb_res = {}
        for param in elb_request_values:
            key = param['Name'].replace(
                '/'+env+'/front/services/elb/', '')
            elb_res[key] = param['Value']

        # cw_dashboard
        dashboard_res = ssm_params.get_parameter(
            Name=f'/{env}/share/monitor/dashboard',
        )
        
        # s3 bucket
        bucket_res = ssm_params.get_parameter(
            Name=f'/{env}/share/storage/s3',
        )
        
        # kms id
        kms_res = ssm_params.get_parameter(
            Name=f'/{env}/share/security/kms',
        )

        # params.append({"network": network_res, "ecs": ecs_res, "elb": elb_res})
        params['network'] = network_res
        params['ecs'] = ecs_res
        params['elb'] = elb_res
        params['cwd'] = dashboard_res['Parameter']['Value']
        params['bucket'] = bucket_res['Parameter']['Value']
        params['kms'] = kms_res['Parameter']['Value']

        return params
