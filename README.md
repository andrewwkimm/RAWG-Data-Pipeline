# RAWG-Data-Pipeline
A data pipeline I am working on made using RAWG's Database API to explore trends on video games through Streamlit.

# Architecture Diagram

![pipeline](images/architecture.png)

The pipeline is orchestrated by Prefect in the following steps:
1. The data is extracted and parsed from RAWG's API
2. A connection to Google Storage is programmatically made to load the data into it
3. Data modeling is done through dbt for use in Big Query
4. Streamlit connects to BigQuery to and visualizes the data

Terraform will be used to manage the Google Cloud Platform infrastructure while Docker will containerize the above steps.

CircleCI will be used for this project's CI/CD pipeline, ensuring that new code will not break the build and reflect the changes to Streamlit.

A preview of how the dashboard will look:

![dashboard](images/dashboard.JPG)

# Getting started

Poetry is used for dependency management; install the dependencies with poetry.
```
$ poetry install
```
Set the environment variable for the API key in the terminal. You'll have to register in RAWG's site [here](https://rawg.io/apidocs).
```
$ export API_KEY="enter-your-key-here"
```
The next steps will be building out the infrastructure with Terraform and running Prefect which are still in development but coming soon!

For now, though, a prototype web app is available using the sample data.
```
$ poetry run streamlit run streamlit/app.py
```
