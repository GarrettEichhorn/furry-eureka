from ctypes import alignment
from turtle import color
from click import style
from colorama import Style
from dash import Dash, dash_table, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


# Dash App

external_stylesheets = []
app = Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

clients = [
            {'label': 'bludot', 
            'value': 'https://bludot_url.com'},
            {'label': 'cub cadet', 
            'value': 'https://cubcadet_url.com'},
            {'label': 'agco', 
            'value': 'https://agco_url.com'},
            {'label': 'chs / cenex', 
            'value': 'https://chscenex_url.com'},
        ]
source = ['google', 'facebook', 'bing', 'nytimes']
medium = ['cpc', 'organic', 'email']
campaign_name = ["option"]
content = ["option"]
term = ["option"]

utm_params = ['source', 'medium', 'campaign_name', 'content', 'term']

# The app layout
app.layout = html.Div(className='app-body', children=[

    # About the app + logos
    html.Div(className="row", children=[
        html.Div(className='twelve columns', children=[
            html.Div(style={'float': 'left'}, children=[
                    html.H1('UTM Builder'),
                    html.H4('Exploring data discrepancies one UTM at a time!')
                ]
            ),

            html.Div(style={'float': 'right'}, children=[
                html.A(
                    html.Img(
                        src=app.get_asset_url("cm.png"),
                        style={'float': 'right', 'height': '60px', 'margin-top': '20px'}
                    ),
                    href="https://www.collemcvoy.com/"),
            ]),
        ]),
    ]),

    # Control panel
    html.Div(className="row", id='control-panel', children=[
          
        html.Div(className="four columns pretty_container", children=[

            html.Label('Select client'),
            dcc.Dropdown(options=clients, value = 'hello', id='client'),

        ]),
        
        html.Div(className="four columns pretty_container", children=[
            
            html.Label('Select source'),
            dcc.Dropdown(options=source, value = 'hello', id='source'),

        ]),

        html.Div(className="four columns pretty_container", children=[
            
            html.Label('Select medium'),
            dcc.Dropdown(options=medium, value = 'hello', id='medium'),

        ]),

        html.Div(className="four columns pretty_container", children=[
            
            html.Label('Select campaign name'),
            dcc.Dropdown(options=campaign_name, value = 'hello', id='campaign_name'),

        ]),

        html.Div(className="four columns pretty_container", children=[
            
            html.Label('Select content'),
            dcc.Dropdown(options=content, value = 'hello', id='content'),

        ]),

        html.Div(className="four columns pretty_container", children=[
            
            html.Label('Select term'),
            dcc.Dropdown(options=term, value = 'hello', id='term'),

        ]),
    ]),
    
    html.Hr(),

    html.Div(className="row", children=[
        html.Div(className='twelve columns', children=[
            html.Div(style={'float': 'left'}, children=[
                html.Div(id='output'),

                ]
            ),
        ]),
    ]),

])

@app.callback(
    Output("output", "children"),
    Input("client", "value"),
    Input("source", "value"),
    Input("medium", "value"),
    Input("campaign_name", "value"),
    Input("content", "value"),
    Input("term", "value"),
)

def concat_utm_params(client, source, medium, campaign_name, content, term):

    return u'{}.{}.{}.{}.{}.{}'.format(client, source, medium, campaign_name, content, term)

if __name__ == '__main__':
    app.run_server(debug=True)