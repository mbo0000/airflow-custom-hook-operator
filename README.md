# WIP - airflow-custom-hook-operator
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.x-green)
![Snowflake](https://img.shields.io/badge/Snowflake-%23f3f1ff)
![Docker](https://img.shields.io/badge/Docker-%2B-blue)
![AWS](https://img.shields.io/badge/AWS-Yellow?style=flat&logo=Amazon&color=yellow)

## Introduction

## Table of Contents
- [Objective](#objective)
- [Architecture](#architecture)
- [Workflow](#workflow)
- [Installation and Setup](#installation-and-setup)
- [Code Walkthrough](#code-walkthrough)
- [Future Work and Improvement](#future-work-and-improvement)

## Objective 
Using the dataset from the [NBA](https://github.com/mbo0000/nba-sport-airflow) project, this project aims to export selected Snowflake tables to a S3 bucket as CSV files. Completion and failure notifications are sent via email. This process can be replicated, adjusted, and used for any data project.

## Architecture
- Snowflake: A cloud-based data warehouse that stores the data tables to be exported.
- Airflow: Manages the task scheduling and handles notifications for task completion and failures.
- Docker: Provides containerized environments the project.

## Workflow

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
6. 

## Code Walkthrough

## Future Work and Improvement
