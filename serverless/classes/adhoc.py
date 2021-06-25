import os
import boto3
import botocore
import logging

logger = logging.getLogger()

# Global vars: boto3 init
s3_client = boto3.client('s3')
ecr_client = boto3.client('ecr')
codebuild_client = boto3.client('codebuild')

class adhoc_delete():
    def delete_s3_object(self, bucket, key):
        self.bucket = bucket
        self.key = key

        try:
            s3_client.delete_object(
                Bucket=os.environ['bucket'],
                Key=key
            )
        except botocore.exceptions.ClientError as error:
            raise error
    
    def delete_image(self, account, repo_name, client):
        self.account = account
        self.repo_name = repo_name
        self.client = client

        try:
            ecr_client.batch_delete_image(
                registryId=account,
                repositoryName=repo_name,
                imageIds=[
                    {
                        'imageTag': client
                    },
                ]
            )
        except botocore.exceptions.ClientError as error:
            raise error
    
    def delete_build(self, buildid):
        self.buildid = buildid

        try:
            codebuild_client.batch_delete_builds(
                ids=[
                    buildid,
                ]
            )
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'InvalidInputException':
                logger.warn('Invalid input operation')
            else:
                raise error
