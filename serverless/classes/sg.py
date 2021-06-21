import os
import boto3
import botocore
import logging

logger = logging.getLogger()

# Global vars: boto3 init
sg_client = boto3.client('ec2')

class security_group():
    def create_security_group(self, client, port, alb_sg, vpc_id, sg_name):
        self.client = client
        self.port = port
        self.alb_sg = alb_sg
        self.vpc_id = vpc_id
        self.sg_name = sg_name
        sg_id=''

        try:
            create_sg = sg_client.create_security_group(
                GroupName=sg_name,
                Description='security group for client: '+client,
                VpcId=vpc_id,
                # this would be great if it worked
                # TagSpecifications=[
                #     {
                #         'ResourceType': 'security-group',
                #         'Tags': tags
                #     },
                # ]
            )
            sg_id = create_sg['GroupId']
            sg_client.authorize_security_group_ingress(
                GroupId=sg_id,
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': int(port),
                        'ToPort': int(port),
                        'UserIdGroupPairs': [
                            {
                                'Description': 'allowing traffic from elb',
                                'GroupId': alb_sg,
                            },
                        ]
                    },
                ]
            )
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'InvalidGroup.Duplicate':
                response = sg_client.describe_security_groups(
                    Filters=[
                        {
                            'Name': 'group-name',
                            'Values': [
                                sg_name,
                            ]
                        },
                    ],
                )
                print(response) # might have to delete soon
                sg_id = response['SecurityGroups'][0]['GroupId']
                try:
                    sg_client.authorize_security_group_ingress(
                        GroupId=sg_id,
                        IpPermissions=[
                            {
                                'IpProtocol': 'tcp',
                                'FromPort': int(port),
                                'ToPort': int(port),
                                'UserIdGroupPairs': [
                                    {
                                        'Description': 'allowing traffic from elb',
                                        'GroupId': alb_sg,
                                    },
                                ]
                            },
                        ]
                    )
                except botocore.exceptions.ClientError as error:
                    if error.response['Error']['Code'] == 'InvalidPermission.Duplicate':
                        logger.warn('Security group rule already exist!')
                    else:
                        raise error
                logger.warn('Skipping this portion, security group already exist!')
            else:
                raise error
        
        return sg_id
