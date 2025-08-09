# src/etl_to_bigquery.py
import os
import pandas as pd
from google.cloud import bigquery

# Config - edit to match your project/dataset/table
PROJECT_ID = "your-gcp-project-id"
DATASET = "performance_dashboard"      # create this dataset in BigQuery
TABLE = "orders"                       # destination table

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sample_orders.csv")

def load_csv_to_bq(csv_path=CSV_PATH, project_id=PROJECT_ID, dataset=DATASET, table=TABLE, if_exists="replace"):
    client = bigquery.Client(project=project_id)

    dataset_ref = client.dataset(dataset)
    # Create dataset if not exists
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset {dataset} exists.")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        client.create_dataset(dataset)
        print(f"Created dataset {dataset_ref}.")

    df = pd.read_csv(csv_path, parse_dates=["order_ts"])
    # cast types for safe upload
    df["order_ts"] = pd.to_datetime(df["order_ts"])
    # bigquery schema can be inferred, or provide explicit schema
    table_id = f"{project_id}.{dataset}.{table}"

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE if if_exists=="replace" else bigquery.WriteDisposition.WRITE_APPEND,
        autodetect=True,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
    )

    with open(csv_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)

    job.result()
    print(f"Loaded {job.output_rows} rows into {table_id}.")

if __name__ == "__main__":
    # set GOOGLE_APPLICATION_CREDENTIALS env var before running:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
    load_csv_to_bq()
