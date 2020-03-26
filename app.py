
import random
import os
import dash
import flask
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Output,Input
import plotly.graph_objs as go
color=['Red','Blue','Green']
# while indulen > 0:
#     r=random.randint(0,indulen)
#     g=random.randint(0,indulen)
#     b=random.randint(0,indulen)
#     rgb=[r,g,b]
#     color.append(rgb)
#     indulen=indulen-1

# data1=go.Scatter(
#     x=df_eda['Date_New_quarterly'],
#     y=df_eda.groupby(['Industry','Date_New_quarterly'])['marketcap'].sum(),
#     name="Total Market Cap",
#     marker=dict(
#         color='rgb(107, 107, 107)',
#         line=dict(
#             color='rgb(107, 107, 107)',
#             width=1.5),)
# )
# layout=go.Layout(
# title="Total Marketcap vs Marketcamp",
# xaxis=dict(title='date vise Industry'),
# yaxis=dict(title='Market Cap')
# )
#
# fig=go.Figure(data=data1,layout=layout)
global df_eda
df_eda=pd.read_csv('mydata.csv')
df_indu=df_eda.groupby(['Industry','Date_New_quarterly'])['marketcap'].sum()
df_indu=df_indu.reset_index()
indu=df_indu['Industry'].unique()
year=df_eda['Year'].unique()
month=[1,2,3,4,5,6,7,8,9,10,11,12]
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
app.layout = html.Div([
    html.Div(html.H1(children="Market Cap")),
    html.Label("Dash Graph"),
    html.Label("Select Industry"),
    html.Div(
        dcc.Dropdown(
                id="menu1",
                options=[
                    {'label':ik,'value':ik }for ik in indu
                ],
                value='Housing Finance'
        ),
    ),
    html.Label("Market cap Color"),
    html.Div(
            dcc.Dropdown(
                    id="cl",
                    options=[
                        {'label':c,'value':c }for c in color
                    ],
                value='Red'

        ),
    ),
    html.Label("Total Market cap Color "),
    html.Div(
        dcc.Dropdown(
            id="cll",
            options=[
                {'label': cc, 'value': cc} for cc in color
            ],
            value='Blue'

        ),
    ),
    html.Label("Perticuler Year"),
    dcc.RadioItems(
                id='year',
                options=[{'label': i, 'value': i} for i in year],
                value=2017


            ),
    html.Label("Perticuler Month"),
    dcc.RadioItems(
        id='month',
        options=[{'label': i, 'value': i} for i in month],
        value=3

    ),
    html.Div(
        dcc.Graph(id='Market_Chart')
    )
])
@app.callback(
     dash.dependencies.Output('Market_Chart','figure'),
    [Input('menu1','value'),
     Input('cl','value'),
    Input('cll','value'),
     Input('year','value'),
     Input('month', 'value')
     ]
)
def update_graph(input_value,c1,c2,yr,mon):
    data=[]
    df_industry=df_eda[df_eda['Industry']==input_value]
    df_industry=df_industry[df_industry['Year']==yr]
    df_industry = df_industry[df_industry['Month_y.1'] == mon]
    trace=go.Line(x=df_industry['Date_New_quarterly'].values,
                     y=df_industry['marketcap'].values,
                     text=df_industry['Industry'],
                     mode='line',
                     name="Market Cap",
                     line_color='rgb(231,107,243)',
                     marker=dict(
                         color=c1
                     )
                     )
    data1 = go.Line(
        x=df_industry['Date_New_quarterly'],
        y=df_industry.groupby(['Industry', 'Date_New_quarterly'])['marketcap'].sum(),
        mode="line",
        text=df_industry['Industry'],
        name="Total Market Cap",
        line_color='rgb(0,176,246)',
        marker=dict(
            color=c2
        )
    )
    data.append(trace)
    data.append(data1)
    layout=dict(
        xaxis={
            'title': "Date"

        },
        yaxis={
            'title': "Market cap & Total Market cap"

        },
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
        hovermode='closest'
    )
    return {
        "data":data,
        "layout":layout

    }

if __name__ =="__main__":
    app.run_server(debug=True)


