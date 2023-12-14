import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from datetime import datetime
from dash.dependencies import Input, Output, State
from dash import dash_table
from sql_converter import SqlConverter, DirectSqlConverter, SqlConverterEventType

from lookml_palm import LookMaker

def Header(name, app):
  title = html.H1(name, style={"margin-top": 5})
  logo = html.Img(
    src=app.get_asset_url("looker.png"), style={"float": "right", "height": 60}
  )
  return dbc.Row([dbc.Col(title, md=8), dbc.Col(logo, md=4)])

# Initialize Dash app
app = dash.Dash(__name__)

conversation = html.Div(
  html.Div(id="display-conversation",
    children=[],
    style={
      "overflow-y": "auto",
      "display": "flex",
      "height": "calc(90vh - 132px)",
      "flex-direction": "column-reverse",
    },
  )
)

controls = dbc.InputGroup(
  style={"width": "80%", "max-width": "800px", "margin": "auto"},
  children=[
    dbc.Input(id="user-input", placeholder="Write to the chatbot...", type="text", style={"width": "80%", "max-width": "800px", "margin": "auto"}),
    dbc.Button("Submit", id="submit"),
  ]
)

app.layout = dbc.Container(
    fluid=False,
    children=[
        Header("Chatbot Example", app),
        html.Hr(),
        dcc.Store(id="store-conversation", data=[]),
        conversation,
        controls,
        dcc.Loading(
            id="loading-1",
            type="default",
            children=html.Div(id="loading-output-1")
        ),
        dcc.Interval(id='update-interval', interval=1000, n_intervals=0, disabled=True),
    ],
)

def textbox(message_type, text, box="user"):
  style = {
    "max-width": "80%",
    "width": "max-content",
    "padding": "10px 15px",
    "border-radius": "25px",
  }

  if box == "user":
    style["marginLeft"] = "auto"
    style["marginRight"] = 0
    style["background-color"] = "rgb(230, 230, 230)"
    color = "blue"
    inverse = True

  elif box == "ai":
    style["marginLeft"] = 0
    style["marginRight"] = "auto"
    color = "light"
    inverse = False

  else:
    raise ValueError("Incorrect option for `box`.")

  if message_type == "text":
    return dbc.Card(text, style=style, body=True, color=color, inverse=inverse)
  style['width'] = '80%'
  style['height'] = '50%'
  return html.Iframe( src=f"{text}", style=style)

@app.callback(
    Output("display-conversation", "children"),
    Input("store-conversation", "data"), Input("update-interval", "n_intervals"),
    State("display-conversation", "children"), State("update-interval", "disabled"),
)
def update_conversation(chat_history, n_interval, rows, time_trigger_disabled):
  print("update coversation triggered. :" + str(time_trigger_disabled))
  if chat_history is None or len(chat_history) == 0:
    return rows
  last_shown_element = len(rows)
  print(str(last_shown_element) + "/" + str(len(chat_history)))
  for element in chat_history:
    if element['last_message_id'] >= last_shown_element:
      rows.append(textbox(element['chat_type'], element['message'], element['chat_role']))
  return rows

# https://dash.plotly.com/datatable/editable
@app.callback(
    Output("store-conversation", "data"),
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
    [State("user-input", "value"), State("store-conversation", "data")],
)
def add_message(n_clicks, n_submit, user_input, chat_history):
  if n_clicks == 0 and n_submit is None:
    return chat_history
  if user_input is None or user_input == "":
    return chat_history
  print("user input: " + user_input)
  last_message_id = len(chat_history)
  chat_history.append({'last_message_id': last_message_id, 'timestamp' : datetime.now().timestamp(), 'message': user_input, 'chat_role': 'user', 'chat_type': 'text'})
  return chat_history

def sql_converter_callback(event_type : SqlConverterEventType, return_message : str):
  for child in app.layout.children:
    if hasattr(child, 'id'):
      if child.id == 'store-conversation':
        chat_history = child.data
        chat_history.append(return_message)
        print(chat_history)
        break
  return

## TODO : It's very difficult to update the store-conversation data from the callback of the sql_converter_callback.
@app.callback(
  Output("store-conversation", "data", allow_duplicate=True),
  [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
  [State("user-input", "value"), State("store-conversation", "data")],
  prevent_initial_call=True
)
def run_chatbot(n_clicks, n_submit, user_input, chat_history):
  if n_clicks == 0 and n_submit is None:
    return chat_history
  if user_input is None or user_input == "":
    return chat_history
  print("bot request input: " + user_input)
  
#   sql_converter = DirectSqlConverter(user_input)
#   sql_converter.register_callback(sql_converter_callback)
#   sql_converter.convert()
#   if sql_converter.get_result() is None:
#     last_message_id = len(chat_history)
#     chat_history.append({'last_message_id': last_message_id + 1, 'timestamp' : datetime.now().timestamp(), 'message': "Not applicable", 'chat_role': 'ai', 'chat_type': 'text'})
#   else:
#     result_tempate = """
# generated sql : {sql} 
# execution result : {result}
#     """.format(sql=sql_converter.get_result().get_converted_sql(), result=sql_converter.get_result().get_result_set().to_string())
#     last_message_id = len(chat_history)
#     chat_history.append({'last_message_id': last_message_id + 1, 'timestamp' : datetime.now().timestamp(), 'message': result_tempate, 'chat_role': 'ai', 'chat_type': 'text'})
  #rows.append(html.P(user_input, style={"margin": 0}))

  last_message_id = len(chat_history)
  maker = LookMaker(user_input)
  look = maker.make_look()
  chart_url = look.public_url.replace('looks','embed/public').replace('.txt?apply_formatting=true&apply_vis=true','')
  print(str(look.id) + ":" + look.public_url + ":" + chart_url)
  #chart_url = "http://localhost:8080/embed/public/QzgFjZKwJ7bKMGtCD9sq8KCQZsmVBt46"
  chat_history.append({'last_message_id': last_message_id + 1, 'timestamp' : datetime.now().timestamp(), 'message': chart_url, 'chat_role': 'ai', 'chat_type': 'iframe'})
  return chat_history



# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)