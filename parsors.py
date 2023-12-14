import json
import ast


def parse_json_response(llm_json_response) -> any:
  #print('llm response:'+ response)
  parsed_json = None
  try :
    start_char = '['
    end_char = ']'
    if llm_json_response.find('[') == -1 or llm_json_response.find('{') < llm_json_response.find('[') :
      start_char = '{'
      end_char = '}'
    start_index = llm_json_response.find(start_char)
    end_index = llm_json_response.rfind(end_char)
    json_data = llm_json_response[start_index:end_index+1]
    json_data = json_data.replace('\\n', '')
    parsed_json = json.loads(json_data)
  except Exception as ex:
    print(ex)
    print("json parse error: " + json_data)
  return parsed_json

def parse_python_object(llm_python_object) -> any: 
  #print('llm response:'+ llm_python_object)
  if llm_python_object.find('{') == -1:
    start_char = '['
    end_char = ']'
  elif llm_python_object.find('[') == -1:
    start_char = '{'
    end_char = '}'
  elif llm_python_object.find('{') < llm_python_object.find('[') :
    start_char = '{'
    end_char = '}'
  else:
    start_char = '['
    end_char = ']'
  start_index = llm_python_object.find(start_char)
  end_index = llm_python_object.rfind(end_char)
  object_data = llm_python_object[start_index:end_index+1]
  parsed_object = ast.literal_eval(object_data)
  return parsed_object  

if __name__ == "__main__":
  llm_json_test = '[{"national_pension_category_summary.create_yearmonth":"2022-10"},\n{"national_pension_category_summary.create_yearmonth":"2022-11"},\n{"national_pension_category_summary.create_yearmonth":"2022-12"}]'
  print(parse_json_response(llm_json_test))
