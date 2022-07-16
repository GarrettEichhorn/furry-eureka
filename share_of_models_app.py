from turtle import color
from click import style
from colorama import Style
from dash import Dash, dash_table, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Share of Voice
total_category_spend = 52364682
client_category_spend = 5985376

# Share of Market
total_market_size =   7731000000
client_sales =   1347410000

budget_seed = 1000000

industry_constant = 0.62

market_growth_rate = .05
market_growth_cap =  8149829400 

# Function to aggregate data for dataframe
def agg_dataframe(increment, b, cs_t, cs_cl, ms_t, ms_cl, c, mgc):
    
    b_list = []
    cs_list = []
    sov_list = []
    esov_list = []
    sim_som_list = []
    som_list = []
    next_year_sales_sim_list = []
    incremental_sales_list = []
    romi_list = []

    category_spend_seed = cs_t - cs_cl
    market_share = (ms_cl / ms_t) * 100 

    for i in range(increment):

        i+=1

        b_seed = i*b
        b_list.append(b_seed)

        cs_seed = category_spend_seed + b_seed
        cs_list.append(cs_seed)

        sov_seed = (b_seed / cs_seed) * 100
        sov_list.append(sov_seed)

        esov_seed = sov_seed - market_share
        esov_list.append(esov_seed)

        sim_som_seed = esov_seed / 10 * c
        sim_som_list.append(sim_som_seed)

        som_seed = sim_som_seed + market_share
        som_list.append(som_seed)

        nys_seed = (som_seed / 100) * mgc
        next_year_sales_sim_list.append(nys_seed)

        inc_sales_seed = nys_seed - ms_cl
        incremental_sales_list.append(inc_sales_seed)

        romi_seed = inc_sales_seed / b_seed
        romi_list.append(romi_seed)

    df = pd.DataFrame(list(zip(b_list, 
                                cs_list, 
                                sov_list, 
                                esov_list, 
                                sim_som_list, 
                                som_list, 
                                next_year_sales_sim_list, 
                                incremental_sales_list, 
                                romi_list
                            )))
    
    return df

cols = ['Budget',
        'Category Spend',
        'SOV',
        'ESOV',
        'SOM Gain / Loss (simulated)',
        'SOM',
        'Next Year Sales (simulated)',
        'Next Year Incremental Sales',
        'ROMI'
        ]

df = agg_dataframe(25, budget_seed, total_category_spend, client_category_spend, total_market_size, client_sales, industry_constant, market_growth_cap)
df.columns = cols

# Dash App

app = Dash(__name__)

# The app layout
app.layout = html.Div(className='app-body', children=[

    # About the app + logos
    html.Div(className="row", children=[
        html.Div(className='twelve columns', children=[
            html.Div(style={'float': 'left'}, children=[
                    html.H1('Share of Voice & Share of Market'),
                    html.H4('Exploring relationships between variables!')
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

            html.Label('Total Category Spend'),
            dcc.Input(id='total_category_spend_inp',
                        type='number',
                        value=total_category_spend, 
                        debounce=True,
            )
        ]),

        html.Div(className="four columns pretty_container", children=[

            html.Label('Client Category Spend'),
            dcc.Input(id='client_category_spend_inp',
                        type='number',
                        value=client_category_spend, 
                        debounce=True,
            )
        ]),

        html.Div(className="four columns pretty_container", children=[

            html.Label('Total Market Size'),
            dcc.Input(id='market_share_inp',
                        type='number',
                        value=total_market_size, 
                        debounce=True,
            )
        ]),

        html.Div(className="four columns pretty_container", children=[

            html.Label('Client Sales'),
            dcc.Input(id='client_sales_inp',
                        type='number',
                        value=client_sales, 
                        debounce=True,
            )
        ]),

        html.Div(className="four columns pretty_container", children=[

            html.Label('Industry Constant'),
            dcc.Input(   id='industry_constant_inp',
                        type='number',
                        value=industry_constant, 
                        debounce=True,
            )
        ]),

        html.Div(className="four columns pretty_container", children=[

            html.Label('Market Growth Rate'),
            dcc.Input(id='market_growth_rate_inp',
                        type='number',
                        value=market_growth_rate, 
                        debounce=True,
            )
        ]),

         html.Div(className="four columns pretty_container", children=[

            html.Label('Market Growth Rate'),
            dcc.Input(id='market_growth_cap_inp',
                        type='number',
                        value=market_growth_cap, 
                        debounce=True,
            )
        ]),


    ]),
    
    html.Hr(),
    html.Div(id = "chart-title", children=[html.H2(id="dash-chart-title-output")], style={'textAlign': 'center'}),
    html.H2(children=''),
    dcc.Dropdown(['ESOV', 'ROMI'], 'ESOV', id='axis_dropdown'),
    dcc.Graph(id='linechart'),
    html.H2(children=''),
    html.Hr(),

    html.Div(id = 'div2', children=[dash_table.DataTable(id='table-editing-simple-output')])

])

@app.callback(
    Output("div2", "children"),
    Output("linechart", "figure"),
    Output("chart-title", "children"),
    Input("total_category_spend_inp", "value"),
    Input("client_category_spend_inp", "value"),
    Input("market_share_inp", "value"),
    Input("client_sales_inp", "value"),
    Input("industry_constant_inp", "value"),
    Input("market_growth_rate_inp", "value"),
    Input("market_growth_cap_inp", "value"),
    Input("axis_dropdown", "value")
)

def updated_dashtable(total_category_spend_inp, client_category_spend_inp, market_share_inp, client_sales_inp, industry_constant_inp, market_growth_rate_inp, market_growth_cap_inp, axis_dropdown):
    
    df = agg_dataframe(25, budget_seed, total_category_spend_inp, client_category_spend_inp, market_share_inp, client_sales_inp, industry_constant_inp, market_growth_cap_inp)

    df.columns = cols

    fig = px.line(df, x='Budget', y=axis_dropdown, markers=True)
    title = f"Budget vs. {axis_dropdown}"

    return dash_table.DataTable(
        columns= ([{'id': p, 'name': p} for p in df.columns]),
        data = df.to_dict('records'),
        export_format="csv"
        ), fig, title
        
if __name__ == '__main__':
    app.run_server(debug=True)