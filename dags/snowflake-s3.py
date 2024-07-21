from airflow import DAG
from airflow.operators.python import PythonOperator
from aws_s3.s3_operator import S3Operator
from datetime import datetime



with DAG(dag_id = 'snowf_s3', start_date = datetime(2024,1,1), catchup=False, schedule = '@daily') as dag:
    
    t0 = S3Operator(
        task_id = 't0'
    )

    t0