import json
import ast
import vertexai
from langchain_google_vertexai import VertexAI
import os
from dotenv import load_dotenv
from google.cloud import bigquery
from langchain_google_vertexai import VertexAIEmbeddings
from bigquery_vector_util import BigQueryVectorDatabase, SqlSearchSchema
from util import parse_json_response, parse_python_object
import pandas as pd
import traceback

load_dotenv()

PROJECT_ID=os.getenv("PROJECT_ID")  # @param {type:"string"}
LOCATION=os.getenv("LOCATION")
TARGET_LOCATION=os.getenv("TARGET_LOCATION")
DATASET=os.getenv("DATASET")
TABLE_NAME=os.getenv("TABLE_NAME")

vertexai.init(project=PROJECT_ID, location="us-central1")

llm_vertex = VertexAI(
    #model_name="text-bison@latest",
    model_name="text-bison-32k@002",
    max_output_tokens=8000,
    temperature=0,
    top_p=0.8,
    top_k=40,
)

llm = llm_vertex

embedding_model = VertexAIEmbeddings("textembedding-gecko-multilingual@latest")

vdb = BigQueryVectorDatabase(project_id=PROJECT_ID, location=LOCATION, dataset=DATASET, table_name=TABLE_NAME)
bigquery_client = bigquery.Client(project=PROJECT_ID, location=TARGET_LOCATION)

class Retriever:

  def __init__(self, question):
    self.question = question
    self.related_query = None
    self.filter_values = None

  def get_values_from_the_question(self) -> (bool, str, pd.DataFrame):
    try :
      print("get_related_query")
      self.get_related_query()
      print("extract_filter_values")
      self.extract_filter_values()
      print("listup_unfilled_filters")
      unfilled_filters = self.listup_unfilled_filters()
      print("before check")
      if len(unfilled_filters) > 0:
        return (False, "필요한 항목을 추가해서 다시한번 요청해 주세요. 필요항목: {unfilled_filters}".format(unfilled_filters), None)
      print("before adjust_filter_value")
      self.adjust_filter_value()
      result_df = self.prepared_statement_with_filter_values_in_bigquery()
      return (True, result_df[0:10].to_string(), result_df)
    except:
      traceback.print_exc()
      return (False, "오류가 발생했습니다. 다시한번 요청해 주세요.", None)
  
  def get_query_from_the_question(self) -> (bool, str, None):
    try :
      self.get_related_query()
      return (True, self.related_query['sql'], None)
    except:
      traceback.print_exc()
      return (False, "오류가 발생했습니다. 다시한번 요청해 주세요.", None)

  def get_related_query(self):
    question = self.question
    test_embedding =  embedding_model.embed_query(question)
    print("111")
    related_queries = vdb.select_similar_query(test_embedding)
    print("222")
    result = None
    if related_queries is not None:
      result = { 
        "uuid" : related_queries['uuid'][0],
        "sql" : related_queries['sql'][0],
        "description" : related_queries['description'][0],
        "parameters" : related_queries['parameters'][0],
        "explore_view" : related_queries['explore_view'][0],
        "model_name" : related_queries['model_name'][0],
        "table_name" : related_queries['table_name'][0],
        "column_schema" : related_queries['column_schema'][0],
        "distance" : related_queries['distance'][0]
      }
    else:
      result = { 
        "uuid" : "",
        "sql" : "",
        "description" : "",
        "parameters" : "",
        "explore_view" : "",
        "model_name" : "",
        "table_name" : "",
        "column_schema" : "",
        "distance" : 1
      }
    self.related_query = result

  def extract_filter_values(self):
    related_query = self.related_query
    question = self.question
    example_json = """
    {
      "filter_columns": [
        {
          "table_name": "sample_table",
          "column_name": "col_1",
          "operator" : "in", 
          "column_type" : "STRING",
          "filter_names": ["col_1_filter"],
          "filter_values": [null],
          "filter_order": 1
        },
        {
          "table_name": "sample_table",
          "column_name": "col_2",
          "operator" : "=", 
          "column_type" : "STRING",
          "filter_names": ["col_2_filter"],
          "filter_values": ["2022-01"],
          "filter_order": 2
        }
      ]
    }
    """

    prompt_template = """You are a serverside developer. Extract filter values from the question and fill the values into the 'filter_values' item for the given filter columns. Do not suggest codes. Output should be the following JSON format.

    given question:
    {question}
    
    given sql:
    {sql}

    given filters:
    {filters}

    ----------------------------

    output format(example) : json
    {example_json}

    """
    sql = related_query['sql']
    filters = related_query['parameters']
    prompt = prompt_template.format(sql=sql, filters=filters, example_json=example_json, question=question)
    response = llm.invoke(prompt)
    self.filter_values = parse_json_response(response)

  def listup_unfilled_filters(self):
    filter_values = self.filter_values
    unfilled_filters = []
    print(filter_values)
    for parameter in filter_values['filter_columns']:
      if None in parameter['filter_values'] or len(parameter['filter_values']) == 0:
        unfilled_filters.append(parameter)
    return unfilled_filters

  def get_field_unique_values(self, matched_table, matched_field) -> (list, int):
    if matched_table[0] != '`' :
      matched_table = '`' + matched_table + '`'
    sql_query = f"with distinct_values as ( select distinct {matched_field} as {matched_field} from {matched_table} ) select {matched_field}, (select count(1) from distinct_values) as total_count from distinct_values limit 500"
    df = bigquery_client.query(sql_query).to_dataframe()
    return df[matched_field].tolist(), df['total_count'][0]

  def choose_right_filter_value(self, filter_values, wanted_value):
    prompt_template = """As a looker developer, choose right filter value for the wanted value below without changing filter value itself.

    availabe filter values : {filter_values}

    values that the customer wants to filter on: {wanted_value}

    answer format: python list
  [filter_value1, filter_value2, ...]
    """
    response = llm.predict(prompt_template.format(filter_values=filter_values, wanted_value=wanted_value))
    return response 

  def adjust_filter_value(self):
    filter_columns = self.filter_values['filter_columns']
    for filter in filter_columns:
      matched_table = filter['table_name']
      matched_field = filter['column_name']
      filter['unique_values'], filter['unique_count'] = self.get_field_unique_values(matched_table, matched_field)
      # TODO: if unique_count < 500, then choose right filter value in the unique value list.
      if filter['unique_count'] < 500:
        response = self.choose_right_filter_value(filter['unique_values'], filter['filter_values'])
        if response.strip().find("```json") == 0 :
          filter['adjust_filter_values'] = parse_json_response(response)
        else:
          filter['adjust_filter_values'] = parse_python_object(response)
      else:
        filter['adjust_filter_values'] = filter['filter_values']
      filter['unique_values'] = None

  def prepared_statement_with_filter_values_in_bigquery(self):
    sql_and_filters = {
      'prepared_statement': self.related_query['sql'],
      'filter_columns': self.filter_values['filter_columns']
    }
    prepared_statement = sql_and_filters['prepared_statement']
    query_parameters = []
    for filter_column in sql_and_filters['filter_columns']:
      if len(filter_column['adjust_filter_values']) > 1:
        if len(filter_column['filter_names']) > 1:
          for filter_value in filter_column['adjust_filter_values']:
            if(filter_column['column_type'] == 'FLOAT64'):
              query_parameters.append(bigquery.ScalarQueryParameter(None, "FLOAT64", filter_value))
            elif(filter_column['column_type'] == 'INT64'):
              query_parameters.append(bigquery.ScalarQueryParameter(None, "INT64", filter_value))
            else:
              query_parameters.append(bigquery.ScalarQueryParameter(None, "STRING", filter_value))  
        else:
          if(filter_column['column_type'] == 'FLOAT64'):
            query_parameters.append(bigquery.ArrayQueryParameter(None, "FLOAT64", filter_column['adjust_filter_values']))
          elif(filter_column['column_type'] == 'INT64'):
            query_parameters.append(bigquery.ArrayQueryParameter(None, "INT64", filter_column['adjust_filter_values']))
          else:
            query_parameters.append(bigquery.ArrayQueryParameter(None, "STRING", filter_column['adjust_filter_values']))
      else:
        if(filter_column['column_type'] == 'FLOAT64'):
          query_parameters.append(bigquery.ScalarQueryParameter(None, "FLOAT64", filter_column['adjust_filter_values'][0]))
        elif(filter_column['column_type'] == 'INT64'):
          query_parameters.append(bigquery.ScalarQueryParameter(None, "INT64", filter_column['adjust_filter_values'][0]))
        else:
          query_parameters.append(bigquery.ScalarQueryParameter(None, "STRING", filter_column['adjust_filter_values'][0]))  
    job_config = bigquery.QueryJobConfig(
      query_parameters=query_parameters
    )
    query_job = bigquery_client.query(prepared_statement, job_config=job_config)
    return query_job.to_dataframe()

