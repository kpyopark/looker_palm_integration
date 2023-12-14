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
    children=dash_table.DataTable(
      id="converation_table",
      columns=[{"name": "Conversation", "id": "conversation"}],
      data=[],
      style_cell={
        "whiteSpace": "normal",
        "height": "auto",
        "textAlign": "left",
      },
      style_table={
        "height": "100%",
        "width": "100%",
        "overflowY": "scroll",
        "padding": "0px 5px",
      },
      style_header={
        "backgroundColor": "rgb(230, 230, 230)",
        "fontWeight": "bold",
      },
      style_data_conditional=[
        {
          "if": {"row_index": "odd"},
          "backgroundColor": "rgb(248, 248, 248)",
        }
      ],
    ),
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
    [Output("converation_table", "data"), Output("loading-component", "children")],
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
    [State("converation_table", "data"), State("user-input", "value")],
)
def run_chatbot(n_clicks, n_submit, rows, user_input):
    if n_clicks == 0 and n_submit is None:
      return rows, None
    if user_input is None or user_input == "":
      return rows, None
    print("User Input: {}".format(user_input))
    rows.append({'conversation': user_input})
    #maker = LookMaker(user_input)
    #look = maker.make_look()
    graph = html.Iframe(
      src='<iframe src="http://localhost:8080/explore/lookml_hol_sample/national_pension_mom?fields=bizcategory.cat_l1,national_pension_mom.average_monthly_fixed_amount&f[national_pension_mom.data_create_yearmonth_year]=2022&query_timezone=Asia%2FSeoul&vis=%7B%22type%22%3A%22looker_pie%22%2C%22hidden_fields%22%3A%5B%5D%7D&title=2022%EB%85%84%2C+%EC%82%B0%EC%97%85+%EB%8C%80%EB%B6%84%EB%A5%98%EB%B3%84+%ED%8F%89%EA%B7%A0+%EC%97%B0%EA%B8%88%EC%95%A1%EC%88%98%EB%A5%BC+%ED%8C%8C%EC%9D%B4%EC%B0%A8%ED%8A%B8%EB%A1%9C+%EB%B3%B4%EC%97%AC%EC%A4%98.4&look_id=25"></iframe>'
    )
    rows.append({'conversation': graph})
    return rows, None
    
    

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)