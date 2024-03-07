from typing import List
from google.cloud import bigquery
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

PROJECT_ID=os.getenv("PROJECT_ID")
LOCATION=os.getenv("LOCATION")
DATASET=os.getenv("DATASET")
TABLE_NAME=os.getenv("TABLE_NAME")

class SqlSearchSchema:

  def __init__(self, sql, parameters, description, explore_view, model_name, table_name, column_schema, desc_vector):
    self.sql = sql
    self.parameters = parameters
    self.description = description
    self.explore_view = explore_view
    self.model_name = model_name
    self.table_name = table_name
    self.column_schema = column_schema
    self.desc_vector = desc_vector


class BigQueryVectorDatabase():

  def __init__(self, project_id, location, dataset, table_name):
    self.dataset = dataset
    self.table_name = table_name
    self.project_id = project_id
    self.location = location
    self.bigquery_client = bigquery.Client(project=self.project_id, location=self.location)
    self.table_ref = self.bigquery_client.table(self.dataset, self.table_name)

  def get_connection(self):
    return self.bigquery_client.open()

  # Create a table in BigQuery)

  def create_table(self):
    query = self.bigquery_client.query(
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
        .format(project_id=self.project_id, dataset=self.dataset, table_name=self.table_name)
      )
    print(query.to_dataframe())
    query = self.bigquery_client.query(
      """
      """
    )

  def insert_record(self, insertRecords: List[SqlSearchSchema]) -> None:
    self.bigquery_client.insert_rows_json(json.dumps(insertRecords))
  
  # Select a similar row from the table
  def select_similar_query(self, desc_vector):

    with self.get_connection() as conn:
      try:
        with conn.cursor() as cur:
          select_record = ((desc_vector,))
          cur.execute(f"SELECT sql, description, parameters, explore_view, model_name, table_name, column_schema FROM rag_test ORDER BY desc_vector <-> %s LIMIT 1", select_record)
          return cur.fetchone()
      except Exception as e:
        print(e)
        conn.rollback()
        raise e
      conn.commit()

  def find_related_tables(self, desc_vector, consine_similarity_threshold):
    results = []
    with self.get_connection() as conn:
      try:
        with conn.cursor() as cur:
          select_record = ((desc_vector, consine_similarity_threshold))
          cur.execute(f"SELECT sql, description, parameters, explore_view, model_name, table_name, column_schema FROM rag_test WHERE (1 - (desc_vector <=> %s)) < %s", select_record)
          for row in cur.fetchall():
            results.append(row)
      except Exception as e:
        print(e)
        conn.rollback()
        raise e
      conn.commit()
    return results
  
vdb = BigQueryVectorDatabase(PROJECT_ID, LOCATION, DATASET, TABLE_NAME)
vdb.create_table()

