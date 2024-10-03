from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scripts.extractf import load_api_data
from scripts.transforming import clean_transform_data
from scripts.loading import load_data_to_postgres

# DAG definition
default_args = {
    'owner': 'rose',
    'start_date': datetime(2024, 10, 10),
    'retries': 3,
}

dag = DAG(
    'car_data_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline to load web scrapped car data into PostgreSQL',
    schedule_interval='@daily',  # or adjust as per your schedule
)

# Task 1: Extract Data
extract_task = PythonOperator(
    task_id='extract_task',
    python_callable=load_api_data,
    provide_context=True,
    dag=dag,
)

# Task 2: Transform Data
transform_task = PythonOperator(
    task_id='transform_task',
    python_callable=clean_transform_data,
    provide_context=True,
    dag=dag,
)

# Task 3: Load Data into PostgreSQL
load_task = PythonOperator(
    task_id='load_task',
    python_callable=load_data_to_postgres,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
extract_task >> transform_task >> load_task
