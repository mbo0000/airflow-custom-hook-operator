from airflow import DAG
from s3_exporter.s3_exporter_operator import S3ExporterOperator
from datetime import datetime, timedelta

DATABASE    = 'CLEAN'
SCHEMA      = 'NBA'
FILE_FORMAT = 'csv'
TO_EMAILS   = ['my.email@company.com']


tables = {
        'games' : 'games/'
        ,'games_statistics': 'games/statistics/'
        }

default_args = {
    'retries'           : 1
    ,'retry_delay'      : timedelta(seconds=5)
    , 'email_on_failure': True
    , 'email_on_retry'  : True
    , 'email'           : ['admin.account@fakecompany.com']
}

with DAG(
    dag_id          = 's3_data_exporter'
    , start_date    = datetime(2024,1,1)
    , catchup       = False
    , schedule      = '@daily'
    , default_args  = default_args
) as dag:
    
    data_export     = S3ExporterOperator(
        task_id     = 's3_data_export'
        , params    = {
            'database'      : DATABASE
            , 'schema'      : SCHEMA
            , 'file_format' : FILE_FORMAT
            , 'table_query' : tables
            , 'to_emails'   : TO_EMAILS
        }
    )

    data_export