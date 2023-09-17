"""Orchestrate the steps of the data pipeline."""

from prefect import flow, task
from prefect_shell import ShellOperation


@task(retries=3)
def extract() -> None:
    """Extract and parses API response into GCS."""
    ShellOperation(commands=["poetry run python src/extract_data_from_api.py"])


@task(retries=3)
def load() -> None:
    """Connects data uploaded to GCS into a BigQuery table."""
    ShellOperation(commands=["poetry run python src/load_storage_into_bigquery.py"])


@task(retries=3)
def transform() -> None:
    """Deploys dbt data models to BigQuery."""
    ShellOperation(commands=["cd dbt && dbt run && cd .."])


@flow
def elt() -> None:
    """Defines tasks within the flow for Prefect deployment."""
    extract()
    load()
    transform()


if __name__ == "__main__":
    elt.serve(name="RAWG-Data-Pipeline")
