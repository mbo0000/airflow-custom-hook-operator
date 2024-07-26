from s3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.utils.email import send_email
import pandas as pd
import os
import logging

class FakeCompOperator(BaseOperator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        # extract and set params from kwargs
        self.database       = kwargs['params']['database']
        self.schema         = kwargs['params']['schema']
        self.file_format    = kwargs['params']['file_format']
        self.table_query    = kwargs['params']['table_query']
        self.to_emails      = kwargs['params']['to_emails']

    def send_email_notification(self, emails):
        if len(emails) < 1 or not emails:
            logging.error('Empty email list')
            return 
        
        logging.info('Sending Email')
        send_email(
            to = emails
            , subject = 'Data Upload Notification'
            , html_content = '''
                Hello Fake Client,

                Your scheduled data dump into S3 bucket is completed. 
                '''
        )

    def execute(self, context):
        tables = [key for key,_ in self.table_query.items()]

        snowf_engine = SnowflakeHook(
            'snowf_conn'
            , database  = self.database
            , schema    = self.schema
        ).get_sqlalchemy_engine()

        logging.info('Extracting data from Snowf')
        files = []
        with snowf_engine.begin() as conn:
            for table in tables:
                query   = self.table_query[table]
                
                # write data to file
                df      = pd.read_sql_query(query, conn)
                file    = f'{table}.{self.file_format}'
                df.to_csv(f'/tmp/{file}')
                files.append(file)
        
        logging.info('Uploading data to S3')
        s3_hook = S3Hook()
        for file in files:
            s3_hook.upload(f'/tmp/{file}', file)

            # remove file
            os.remove(f'/tmp/{file}')
        

        self.send_email_notification(self.to_emails)
        logging.info('Task completed')
