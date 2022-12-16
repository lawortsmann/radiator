from __future__ import annotations

import pandas as pd
from google.cloud import bigquery
from google.oauth2.service_account import Credentials

PROJECT = "lawortsmann"


class GCPClient:
    """
    Client to interact with GCP resources, primarily bigquery
    """

    def __init__(self, key_path: str = ".gcp-secrets.json") -> None:
        self.credentials = Credentials.from_service_account_file(key_path)
        assert self.credentials.project_id == PROJECT
        self.bq_client = bigquery.Client(
            credentials=self.credentials,
            project=self.credentials.project_id,
        )

    def query_bq(self, query: str) -> pd.DataFrame:
        return self.bq_client.query(query).to_dataframe()

    def upload_bq(self, data: pd.DataFrame, destination: str) -> bigquery.LoadJob:
        job = self.bq_client.load_table_from_dataframe(
            dataframe=data,
            destination=destination,
        )
        return job
