import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
from dash import dash_table

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
    children=[
        dbc.Input(id="user-input", placeholder="Write to the chatbot...", type="text"),
        dbc.Button("Submit", id="submit"),
    ]
)

app.layout = dbc.Container(
    fluid=False,
    children=[
        Header("Chatbot Example", app),
        html.Hr(),
        dcc.Store(id="store-conversation", data=""),
        conversation,
        controls,
        dbc.Spinner(html.Div(id="loading-component")),
    ],
)

# https://dash.plotly.com/datatable/editable
@app.callback(
    [Output("display-conversation", "children"), Output("loading-component", "children")],
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
    [State("display-conversation", "children"), State("user-input", "value")],
)
def run_chatbot(n_clicks, n_submit, rows, user_input):
    if n_clicks == 0 and n_submit is None:
      return rows, None
    if user_input is None or user_input == "":
      return rows, None
    rows.append(html.P(user_input, style={"margin": 0}))
    #maker = LookMaker(user_input)
    #look = maker.make_look()
    graph = html.Iframe(
      src="<<>>",
      style={"height": "600", "width": "60%"}
    )
    rows.append(graph)
    print("added")
    return rows, None
    

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)