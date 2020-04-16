import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

import flask
from flask import send_file
import io

import boto3
client = boto3.client('s3')
resource = boto3.resource('s3')
my_bucket = resource.Bucket('eb-pandas-data')

obj = client.get_object(Bucket='eb-pandas-data',Key='customer_profile/Reddit_Historical_Data.csv')
df = pd.read_csv(obj['Body'])
date = df['date'].to_list()
depression_list = df['depression'].to_list()
anxiety_list = df['anxiety'].to_list()
OCD_list = df['OCD'].to_list()
social_list = df['socialanxiety'].to_list()
panic_list = df['panicdisorder'].to_list()
total_list = df['total'].to_list()

# Average of daily difference
depression_avg = int(round(df['depression'].diff().mean(),0))
anxiety_avg = int(round(df['anxiety'].diff().mean(),0))
OCD_avg = int(round(df['OCD'].diff().mean(),0))
social_avg = int(round(df['socialanxiety'].diff().mean(),0))
panic_avg = int(round(df['panicdisorder'].diff().mean(),0))
total_avg = int(round(df['total'].diff().mean(),0))

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
external_stylesheets=[dbc.themes.LUX]
app =dash.Dash(external_stylesheets=external_stylesheets)
application = app.server
app.title = 'Mental Health Depression'


colors = {
    'background':'#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Reddit Market Size',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='The number of users in mental health subreddit group', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Subreddit_Anxiety', 'value':'anxiety'},
            {'label': 'Subreddit_Depression', 'value':'depression'},
            {'label': 'Subreddit_Social_Anxiety', 'value':'social_anxiety'},
            {'label': 'Subreddit_OCD', 'value':'ocd'},
            {'label': 'Subreddit_Panic_Disorder', 'value':'panic'},
            {'label': 'Reddit_Market_Size', 'value':'reddit'}
        ],
        value='anxiety',
    ),

    html.Br(),

    html.Div(id='avg-num', style={'color':colors['text'],
                                'fontSize':20}),

    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                # {'x': ['3/26/20', '3/27/20', '3/28/20', '3/30/20', '3/31/20'],
                #  'y': [340890, 341175, 341495, 341949, 342210], 'type': 'line',
                #  'name': 'Subreddit_Anxiety'},
                # {'x': ['3/26/20', '3/27/20', '3/28/20', '3/30/20', '3/31/20']
                # , 'y': [617704, 617970, 618224, 618847, 619098], 'type': 'line',
                # 'name': u'Subreddit_Depression'},
                {'x': date
                , 'y': total_list, 'type': 'line',
                'name': u'Reddit_Market_Size'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])

@app.callback(
    dash.dependencies.Output('avg-num', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')]
)
def update_output(value):
    if value == 'anxiety':
        return f"The average of daily new users is {anxiety_avg} in this group."

    elif value == 'depression':
        return  f"The average of daily new users is {depression_avg} in this group."

    elif value == 'social_anxiety':
        return  f"The average of daily new users is {social_avg} in this group."

    elif value == 'ocd':
        return  f"The average of daily new users is {OCD_avg} in this group."

    elif value == 'panic':
        return  f"The average of daily new users is {panic_avg} in this group."

    else:
        return f"The average of daily new users is {total_avg} in total."


@app.callback(
    dash.dependencies.Output('example-graph-2', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')]
)
def update_output(value):
    if value == 'anxiety':
        num = anxiety_list
    elif value == 'depression':
        num = depression_list
    elif value == 'social_anxiety':
        num = social_list
    elif value == 'ocd':
        num = OCD_list
    elif value == 'panic':
        num = panic_list
    else:
        num = total_list


    return {
            "data":[
                dict(
                    x = date,
                    y = num,
                    type = 'line',
                    name =  value)],

            'layout': [
                dict(
                    plot_bgcolor=colors['background'],
                    paper_bgcolor= colors['background'],
                    font = {
                        'color': colors['text']
                        }
                )
            ]}

if __name__ == '__main__':
    application.run(debug=True, port=8080)
