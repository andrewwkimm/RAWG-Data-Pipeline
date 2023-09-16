"""Load bucket into BigQuery via external connection."""

from google.cloud import bigquery
from utilities.google_cloud_utils import load_storage_data_to_bigquery_table
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("SERVICE_KEY")


location = "us-east1"
schema = [
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("release_date", "STRING"),
    bigquery.SchemaField("genre", "STRING"),
    bigquery.SchemaField("rating", "FLOAT"),
    bigquery.SchemaField("game_id", "INT64"),
    bigquery.SchemaField("playtime", "INTEGER"),
    bigquery.SchemaField("year", "INTEGER"),
    bigquery.SchemaField("month", "STRING"),
    bigquery.SchemaField("week", "STRING"),
]
project_id = "rawg-data-pipeline"
dataset_id = "video_game_dataset"
table_id = "video_game_data"
gcs_uri = f"gs://{project_id}/{table_id}.csv"


if __name__ == "__main__":
    load_storage_data_to_bigquery_table(
        schema,
        project_id,
        dataset_id,
        table_id,
        gcs_uri,
        location,
    )
