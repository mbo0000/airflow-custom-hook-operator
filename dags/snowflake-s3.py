from airflow import DAG
# from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
# from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from datetime import datetime

with DAG(dag_id = 'snowf_s3', start_date = datetime(2024,1,1), catchup=False, schedule = '@daily') as dag:
    
    
    my_task = BashOperator(
        task_id = 'my_task'
        , bash_command = 'echo my task'
    )

    my_task
