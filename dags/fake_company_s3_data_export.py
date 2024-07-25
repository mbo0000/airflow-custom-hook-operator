from airflow import DAG
from airflow.operators.python import PythonOperator
from aws_s3.s3_operator import SnowfToS3Operator
from datetime import datetime

DATABASE    = 'SNOWFLAKE_SAMPLE_DATA'
SCHEMA      = 'TPCH_SF1'
FILE_FORMAT = 'csv'


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

def tables():
    print([key for key,_ in table_query.items()])

with DAG(dag_id = 'fake_company_s3_data_export', start_date = datetime(2024,1,1), catchup=False, schedule = '@daily') as dag:
    
    data_export = SnowfToS3Operator(
        task_id = 'data_export'
        , params = {
            'database'      : DATABASE
            , 'schema'      : SCHEMA
            , 'file_format' : FILE_FORMAT
            , 'table_query' : table_query
        }
        # implement email notifications per status
    )

    data_export
