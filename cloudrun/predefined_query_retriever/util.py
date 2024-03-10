import json
import ast


def parse_json_response(llm_json_response) -> any:
  #print('llm response:'+ response)
  start_char = '['
  end_char = ']'
  if llm_json_response.find('[') == -1 or max(0,llm_json_response.find('{')) < llm_json_response.find('[') :
    start_char = '{'
    end_char = '}'
  start_index = llm_json_response.find(start_char)
  end_index = llm_json_response.rfind(end_char)
  json_data = llm_json_response[start_index:end_index+1]
  parsed_json = json.loads(json_data)
  return parsed_json

def parse_python_object(llm_python_object) -> any:
  print('llm response:'+ llm_python_object)
  if llm_python_object.find('{') == -1:
    start_char = '['
    end_char = ']'
  elif llm_python_object.find('[') == -1 or llm_python_object.find('{') < llm_python_object.find('[') :
    start_char = '{'
    end_char = '}'
  start_index = llm_python_object.find(start_char)
  end_index = llm_python_object.rfind(end_char)
  object_data = llm_python_object[start_index:end_index+1]
  print(object_data)
  parsed_object = ast.literal_eval(object_data)
  return parsed_object

def parse_llm_result_to_object(llm_result_json_or_python) -> any:
  result = None
  try:
    result = parse_json_response(llm_result_json_or_python)
  except:
    try:
      result = parse_python_object(llm_result_json_or_python)
    except:
      raise Exception('Unable to parse llm result')
  return result