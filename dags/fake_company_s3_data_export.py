from airflow import DAG
from fake_company.fake_comp_operator import FakeCompOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

DATABASE    = 'SNOWFLAKE_SAMPLE_DATA'
SCHEMA      = 'TPCH_SF1'
FILE_FORMAT = 'csv'
TO_EMAILS   = ['fake.client@company.com']


table_query = {
    'orders'        : '''
                        select 
                            * 
                        from orders 
                        limit 100
                    '''
    , 'customer'    : '''
                        select 
                            * 
                        from customer 
                        limit 100
                    '''
}

default_args = {
    'retries'           : 1
    ,'retry_delay'      : timedelta(seconds=5)
    , 'email_on_failure': True
    , 'email_on_retry'  : True
    , 'email'           : ['admin.account@company.com']
}

with DAG(
    dag_id          = 'snowf_s3_fake_company_data_export'
    , start_date    = datetime(2024,1,1)
    , catchup       = False
    , schedule      = '@daily'
    , default_args  = default_args
) as dag:
    
    data_export     = FakeCompOperator(
        task_id     = 'data_export'
        , params    = {
            'database'      : DATABASE
            , 'schema'      : SCHEMA
            , 'file_format' : FILE_FORMAT
            , 'table_query' : table_query
            , 'to_emails'   : TO_EMAILS
        }
    )

    data_export