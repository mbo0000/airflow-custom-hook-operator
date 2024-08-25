airflow-custom-hook-operator
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.x-green)
![Snowflake](https://img.shields.io/badge/Snowflake-%23f3f1ff)
![Docker](https://img.shields.io/badge/Docker-%2B-blue)
![AWS](https://img.shields.io/badge/AWS-Yellow?style=flat&logo=Amazon&color=yellow)

## Introduction

## Table of Contents
- [Objective](#objective)
- [Architecture](#architecture)
- [Installation and Setup](#installation-and-setup)
- [Code Walkthrough](#code-walkthrough)
- [Future Work and Improvement](#future-work-and-improvement)

## Objective 
Using the dataset from the [NBA](https://github.com/mbo0000/nba-sport-airflow) project, this project aims to export selected Snowflake tables to a S3 bucket as CSV files. Completion and failure notifications are sent via email. This process can be replicated, adjusted, and used for any data project.

## Architecture
- Snowflake: A cloud-based data warehouse that stores the data tables to be exported.
- Airflow: Manages the task scheduling and handles notifications for task completion and failures.
- Docker: Provides containerized environments the project.

## Installation and Setup
### Prerequisites
- Python 3.9+
- Snowflake Account
- Apache Airflow (2.x recommended)
- Docker
- AWS Account

Below are the steps to locally setup the project:
1. Create a main project folder >> navigate to the project folder.
2. Clone the airflow repository in the main project directory:
   ```sh
     git clone https://github.com/mbo0000/airflow-custom-hook-operator.git
     cd airflow-custom-hook-operator
3. Create .env file:
    ```sh
    touch .env
4. Add AWS AIM creds and target S3 bucket name. For example:
    ```
    AWS_ACCESS_KEY=foo
    AWS_SECRET_KEY=foo
    AWS_S3_BUCKET_NAME=foo
    ```
    Alternative, AWS connection can be added in the Airflow web UI.
5. Ensure config/airflow.config file has correct configurations for the email and smtp sections:
    ```
    [email]
    email_backend = airflow.utils.email.send_email_smtp
    email_conn_id = smtp_default
    default_email_on_retry = True
    default_email_on_failure = True
    ssl_context = default

    [smtp]
    smtp_host = smtp.gmail.com
    smtp_starttls = True
    smtp_ssl = False
    ```
    The rest of the variables can be leave with default values.
6. Create [Google Account App Password](https://myaccount.google.com/apppasswords) and save the generated password.
7. Run docker compose to launch Airflow instance. Use [localhost:8080](http://localhost:8080/) access Airflow's web UI.
8. Navigate to Admin >> Connections and create 2 connections:
   - Snowflake:
      - Connection Id: `snowflake_conn`
      - Connection Type: Snowflake
      - Login: [your Snowflake username]
      - Password: [your Snowflake password]
      - Account: [your Snowflake account locator Id]   
   - SMPT:
     - Connection Id: `smtp_default` (Ensure this is spelled correctly)
     - Connection Type: Email
     - Port: 587
     - Login: [your_email@gmail.com]
     - Password: [password generated in step 6]
9. Update [TO_EMAILS](https://github.com/mbo0000/airflow-custom-hook-operator/blob/890c10d2d1e5809e866bcf6d88ce445ac62dc075/dags/s3_data_exporter.py#L8) and [email](https://github.com/mbo0000/airflow-custom-hook-operator/blob/890c10d2d1e5809e866bcf6d88ce445ac62dc075/dags/s3_data_exporter.py#L20) vars in the s3_data_expoert.py file with your target email addresses:
   - TO_EMAIL: a list of emails to send notification to when task is completed
   - email: DAG owner or admin email when task fails and retries. 

## Code Walkthrough
The DAG comprises a single task using the `S3ExporterOperator` found in the [s3_exporter](https://github.com/mbo0000/airflow-custom-hook-operator/tree/main/plugins/s3_exporter) directory of the plugins folder. This custom operator uses provided arguments to extract data from Snowflake and export it to a specified S3 bucket and directory. The DAG is set to notify DAG owner or airflow admin of failures and retries. 

Currently, the DAG exports data from two Snowflake tables to S3 on a daily schedule. These tables are specified in `tables_key`, which determines the directories where the exported files will be stored.
```
from airflow import DAG
from s3_exporter.s3_exporter_operator import S3ExporterOperator
from datetime import datetime, timedelta

DATABASE    = 'CLEAN'
SCHEMA      = 'NBA'
FILE_FORMAT = 'csv'
TO_EMAILS   = ['my.email@company.com']

tables_key  = {
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
            , 'table_query' : tables_key
            , 'to_emails'   : TO_EMAILS
        }
    )

    data_export
```

## Future Work and Improvement
- Integrate Slack notifications 
