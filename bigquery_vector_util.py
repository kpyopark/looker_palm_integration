from google.cloud import bigquery
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

PROJECT_ID=os.getenv("PROJECT_ID")
LOCATION=os.getenv("LOCATION")
DATASET=os.getenv("DATASET")
TABLE_NAME=os.getenv("TABLE_NAME")

class BigQueryVectorDatabase():

  def __init__(self, project_id, location, dataset, table_name):
    self.dataset = dataset
    self.table_name = table_name

  def create_table(self):
    client = bigquery.Client(project=PROJECT_ID, location=LOCATION)
    query = client.query(
      """CREATE TABLE IF NOT EXISTS `{project_id}.{dataset}.{table_name}` (
        uuid STRING DEFAULT GENERATE_UUID(), 
        sql STRING, 
        description STRING, 
        parameters STRING, 
        explore_view STRING, 
        model_name STRING, 
        table_name STRING, 
        column_schema STRING, 
        desc_vector ARRAY<FLOAT64>)"""
        .format(project_id=PROJECT_ID, dataset=DATASET, table_name=TABLE_NAME)
      )
    print(query.to_dataframe())

vdb = BigQueryVectorDatabase(PROJECT_ID, LOCATION, DATASET, TABLE_NAME)
vdb.create_table()

