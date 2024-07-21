import boto3
from airflow.hooks.base import BaseHook
import logging
from botocore.exceptions import NoCredentialsError, ClientError
import os

class S3Hook(BaseHook):

    def __init__(self):
        self.bucket_name    = os.getenv('AWS_S3_BUCKET_NAME')
        self.access_key     = os.getenv('AWS_ACCESS_KEY')
        self.secret         = os.getenv('AWS_SECRET_KEY')

        if not self.access_key or not self.secret:
            print('Missing Creds')
            logging.error('Missing AWS Credentials')
            raise NoCredentialsError

    def upload(self, local_file, s3_file_key):
        client = boto3.client(
            's3',
            region_name             = 'us-west-1',
            aws_access_key_id       = self.access_key,
            aws_secret_access_key   = self.secret
        )

        try:
            client.upload_file(
                Filename = ''
                , Bucket    = self.bucket_name
                , Key       = s3_file_key
            )
        except ClientError as e:
            logging.error(e)    
    
    def check_bucket_exist(self, bucket=None):
        if not bucket:
            bucket = self.bucket_name
        
        client = boto3.client(
            's3',
            region_name             = 'us-west-1',
            aws_access_key_id       = self.access_key,
            aws_secret_access_key   = self.secret
        )

        res     = client.list_buckets()['Buckets']
        buckets = [b['Name'] for b in res]
        if bucket in buckets:
            return True
        return False
