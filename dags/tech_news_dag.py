
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import include.extract_tech_news as extract
import include.transform_tech_news as transform


with DAG(
    dag_id='global_tech_news_pipeline',
    start_date=datetime(2026, 3, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    extract = PythonOperator(task_id='extract_data', python_callable=extract.extract_tech_news)
    transform = PythonOperator(task_id='transform_data', python_callable=transform.transform_tech_news)
   

    extract >> transform