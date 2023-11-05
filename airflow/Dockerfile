FROM apache/airflow:latest

COPY . /app

# Installs any necessary utilities
RUN \
    apt-get update
    && apt-get install -y curl make

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 -

# Ensures the project can successfully build
RUN make build

RUN poetry run airflow scheduler
