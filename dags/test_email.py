from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.email import send_email
from airflow.hooks.base_hook import BaseHook

default_args = {
    'retries': 1
    ,'retry_delay' : timedelta(seconds=5)
    , 'email' : ['mbo0000da@gmail.com']
    , 'email_on_failure' : True
    , 'email_on_retry' : True
}

# def send_my_email():
#     conns = BaseHook.get_connection('smtp_default') 
#     print(conns.host)
#     print(conns.login)
#     print(conns.port)
#     print(conns)
#     send_email(to = 'mbo0000da@gmail.com', subject = 'test', html_content = 'test')

with DAG(
    dag_id = 'test_email'
    ,start_date = datetime(2024,1,1), catchup=False, schedule = '@daily', default_args = default_args
) as dag:
    task1 = BashOperator(
        task_id = 'task1'
        , bash_command = 'cd not_real_dir'
    )
    task1

    # task1 = PythonOperator(
    #     task_id = 'task1'
    #     , python_callable = send_my_email
    # )
    # task1