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


def load_storage_data_to_bigquery_table(
    schema: list[bigquery.SchemaField],
    project_id: str,
    dataset_id: str,
    table_id: str,
    gcs_uri: str,
    location: str,
) -> None:
    """Loads the uploaded data in Google Cloud Storage to a BigQuery table."""
    client = bigquery.Client(location=location)

    table_ref = client.dataset(dataset_id, project=project_id).table(table_id)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        schema=schema,
        skip_leading_rows=1,
    )
    load_job = client.load_table_from_uri(gcs_uri, table_ref, job_config=job_config)
    load_job.result()

    print(f"Table {table_ref.table_id} created with {load_job.output_rows} rows.")
