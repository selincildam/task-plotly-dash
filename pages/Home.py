from dash import Dash, html, dcc, callback,dash_table
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import yfinance as yf
import re


dash.register_page(__name__, path='/')


#Download data and filter 
temp=yf.download(tickers=['BTC-USD','ETH-USD','DOGE-USD'], 
                period="1d",
                interval='15m',
                actions="inline")

btc_df=temp.reset_index()
btc_df.columns = [col[0]+"-"+col[1] for col in btc_df.columns.values]


col_list=[i for i in btc_df.columns if re.search("BTC", str(i)) ]
col_list.insert(0, 'Datetime-')
filtered_df=btc_df[col_list].iloc[0:15,:]


#Layout
body=dbc.Container(dbc.Row(dbc.Col(html.Div(children=[
    html.H1("Welcome to Homepage",style={'color': '#7FDBFF','fontFamily':'Verdana','backgroundColor':'#000000','textAlign':'center','padding':'5px 0px'}),
    html.Div(dash_table.DataTable(id="crypto_table",
                                columns=[{"name": i, "id": i} for i in filtered_df.columns],
                                data=filtered_df.to_dict('records'),
                                style_header={'backgroundColor': 'rgb(30, 30, 30)',
                                            'color': 'white'
                                            },
                                
                                style_data_conditional=[{'if': {'row_index': 'odd'},
                                                        'backgroundColor': 'rgb(220, 220, 220)',}
                                                        ],
                                )
            )
    
    ]))))

layout=html.Div([body])






