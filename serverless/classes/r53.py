import os
import boto3
import botocore
import logging

logger = logging.getLogger()

# Global vars: boto3 init
r53_client = boto3.client('route53')

class update_record():
    def change_record(self, action, dns, alb_zone, alb_dns):
        self.action = action
        self.dns = dns
        self.alb_zone = alb_zone
        self.alb_dns = alb_dns

        try:
            r53_client.change_resource_record_sets(
                HostedZoneId=os.environ['r53HostedZoneId'],
                ChangeBatch={
                    'Comment': 'DNS record creation for ' + os.environ['environment'] + ' environment',
                    'Changes': [
                        {
                            'Action': action,
                            'ResourceRecordSet': {
                                'Name': dns,
                                'Type': 'A',
                                'AliasTarget': {
                                    # zone of the load balancer
                                    'HostedZoneId': alb_zone,
                                    # need dns of balancer
                                    'DNSName': alb_dns,
                                    'EvaluateTargetHealth': True
                                },
                            }
                        },
                    ]
                }
            )
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'InvalidChangeBatch':
                logger.warn('Record set already exists')
            else:
                raise error
