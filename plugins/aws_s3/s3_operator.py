from s3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook

class S3Operator(BaseOperator):

    def __init__(self, *args, **kwargs):
        super(S3Operator, self).__init__(*args, **kwargs) 


    def execute(self, context):
        print('Custom Operator')