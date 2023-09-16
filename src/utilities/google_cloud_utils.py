"""Utilities for programmatically interacting with Google Cloud Platform."""

import os

import pandas as pd
from google.cloud import storage, bigquery

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("SERVICE_KEY")


def upload_data_to_google_storage(
    data: pd.DataFrame, bucket_name: str, blob_name: str
) -> None:
    """Uploads data to Google Storage as a .csv file."""
    csv_data = data.to_csv(index=False)
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(csv_data, content_type="text/csv")

    print(f"Uploaded data to gs://{bucket_name}/{blob_name}")


def create_external_connection_from_storage_to_bigquery_table(
    query: str,
    schema: list,
    project_id: str,
    dataset_id: str,
    table_id: str,
    location: str,
) -> None:
    """Creates external connection to load data from storage into a BigQuery table."""
    client = bigquery.Client(location=location)
    dataset_ref = bigquery.DatasetReference(client.project, dataset_id)
    external_config = bigquery.ExternalConfig("CSV")
    external_config.source_uris = [f"gs://{project_id}/{table_id}.csv"]
    external_config.schema = schema
    external_config.csv_options.skip_leading_rows = 1

    table_ref = bigquery.Table(dataset_ref.table(table_id))
    table_ref.external_data_configuration = external_config

    client.create_table(table_ref)
    client.query(query)

    print("Uploaded data from storage into BigQuery")
