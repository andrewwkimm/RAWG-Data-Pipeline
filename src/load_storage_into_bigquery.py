"""Load bucket into BigQuery via external connection."""

from google.cloud import bigquery
from utilities.google_cloud_utils import (
    create_external_connection_from_storage_to_bigquery_table,
)
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("SERVICE_KEY")


location = "us-east1"
query = "SELECT * FROM {table_id}"
schema = [
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("release_date", "DATE"),
    bigquery.SchemaField("genre", "STRING"),
    bigquery.SchemaField("rating", "FLOAT"),
    bigquery.SchemaField("game_id", "INT64"),
    bigquery.SchemaField("playtime", "INTEGER"),
    bigquery.SchemaField("year", "INTEGER"),
    bigquery.SchemaField("month", "STRING"),
    bigquery.SchemaField("week", "DATE"),
]
project_id = "rawg-data-pipeline"
dataset_id = "video_game_dataset"
table_id = "video_game_data"


if __name__ == "__main__":
    create_external_connection_from_storage_to_bigquery_table(
        query,
        schema,
        project_id,
        dataset_id,
        table_id,
        location,
    )
