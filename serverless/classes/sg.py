import os
import boto3
import botocore
import logging

logger = logging.getLogger()

# Global vars: boto3 init
sg_client = boto3.client('ec2')
sqs_client = boto3.client('sqs')


class security_group():
    def create_security_group(self, client, port, alb_sg, vpc_id, sg_name, tags):
        self.client = client
        self.port = port
        self.alb_sg = alb_sg
        self.vpc_id = vpc_id
        self.sg_name = sg_name
        self.tags = tags
        sg_id = ''

        try:
            create_sg = sg_client.create_security_group(
                GroupName=sg_name,
                Description='security group for client: '+client,
                VpcId=vpc_id,
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group',
                        'Tags': tags
                    },
                ]
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
                print(response)  # might have to delete soon
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
                logger.warn(
                    'Skipping this portion, security group already exist!')
            else:
                raise error

        return sg_id

    def delete_security_group(self, security_group_id):
        self.security_group_id = security_group_id
        response = ''
        try:
            response = sg_client.delete_security_group(
                GroupId=security_group_id,
            )
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'InvalidGroup.NotFound':
                logger.warn(
                    'Security group not found!')
            elif error.response['Error']['Code'] == 'UnauthorizedOperation':
                logger.warn('Unauthorized to perform DeleteSecurityGroup')
            else:
                raise error

        return response

    def call_sqs_queue(self, client, sg_id, sqs_url):
        self.client = client
        self.sg_id = sg_id  # there needs to be an exception here to handle empty strings
        self.sqs_url = sqs_url

        if (sg_id == ""):
            logger.warn("Nothing to do since the security group was empty")
        else:
            sqs_client.send_message(
                QueueUrl=sqs_url,
                MessageBody="Calling the sqs queue to delete security group for client: " + client,
                MessageAttributes={
                    'sgId': {
                        'StringValue': sg_id,
                        'DataType': 'String'
                    },
                }
            )
