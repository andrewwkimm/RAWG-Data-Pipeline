"""Orchestrate the steps in the data pipeline."""

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago


default_args = {
    "owner": "airflow",
    "depends_on_past": True,
    "retries": 1,
    "schedule_interval": "@weekly",
    "start_date": days_ago(14),
}

with DAG(
    dag_id="RAWG_Data_Pipeline",
    description="Strava data EtLT pipeline",
    default_args=default_args,
    catchup=True,
    max_active_runs=1,
    tags=["RAWG_Data_Pipeline"],
) as dag:

    extract = BashOperator(
        task_id="extract_rawg_data",
        bash_command="poetry run python src/extract_data_from_api.py",
        dag=dag,
    )
    extract.doc_md = (
        "Extract data from RAWG and store it in a Google Cloud Storage bucket."
    )

    load = BashOperator(
        task_id="load_storage_into_bigquery",
        bash_command="poetry run python src/load_storage_into_bigquery.py",
        dag=dag,
    )
    load.doc_md = "Load data from GCS and into BigQuery."

    transform = BashOperator(
        task_id="deploy_dbt_to_big_query",
        bash_command="cd dbt && dbt run && cd ..",
        dag=dag,
    )


extract >> transform >> load
