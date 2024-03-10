import os

from logging import INFO
from typing import Dict

from dialogflow_fulfillment import WebhookClient, QuickReplies, Context, Card, Image, Text

from flask import Flask, request
from flask.logging import create_logger
from retreiver import Retriever

app = Flask(__name__)
logger = create_logger(app)
logger.setLevel(INFO)

def sql_execution_handler(agent:WebhookClient) -> None:
  logger.info(f'Agent Query: {agent.query}')
  retriever = Retriever(agent.query)
  (success, response_text, dataframe) = retriever.get_values_from_the_question()
  if not success:
    agent.add(response_text)
    return
  agent.add(response_text)

def sql_question_handler(agent:WebhookClient) -> None:
  logger.info(f'Agent Query: {agent.query}')
  retriever = Retriever(agent.query)
  (success, response_text, dataframe) = retriever.get_query_from_the_question()
  if not success:
    agent.add(response_text)
    return
  agent.add(response_text)

## This is the entry point for the DialogFlow WebHook
@app.route("/dialogflow_webhook", methods=['POST'])
def intent_handler() -> Dict:
  request_ = request.get_json(force=True)
  logger.info(f'Request headers: {dict(request.headers)}')
  logger.info(f'Request body: {request_}')
  agent = WebhookClient(request_)
  agent.handle_request()
  logger.info(f'Response body: {agent.response}')
  return agent.response

@app.route("/sql_execution", methods=['POST'])
def question_and_execute() -> Dict:
  request_ = request.get_json(force=True)
  logger.info(f'Request headers: {request_}')
  question = request_['question']
  retriever = Retriever(question)
  (success, response_text, dataframe) = retriever.get_values_from_the_question()
  if not success:
    return {"success": False, "response_text": "오류가 발생하였습니다. 다시 시도해 주세요.", "dataframe": None}
  return {"success": True, "response_text": response_text, "dataframe": None} # Dataframe is too big to return it as a response.

## This is the entry point for the DialogFlow WebHook

@app.route("/sql_question", methods=['POST'])
def question_and_answer() -> Dict:
  request_ = request.get_json(force=True)
  logger.info(f'Request headers: {request_}')
  question = request_['question']
  retriever = Retriever(question)
  (success, response_text, dataframe) = retriever.get_query_from_the_question()
  if not success:
    return {"success": False, "response_text": "오류가 발생하였습니다. 다시 시도해 주세요.", "dataframe": None}
  return {"success": True, "response_text": response_text, "dataframe": None}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))