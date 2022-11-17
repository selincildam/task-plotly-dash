from dash import Dash, html, dcc, dash_table,callback
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
#import pandas as pd
import yfinance as yf
from dash.dependencies import Input, Output
from datetime import datetime,timedelta


dash.register_page(__name__)

#Download the data 
#For line plot


temp=yf.download(tickers=['BTC-USD','ETH-USD','DOGE-USD'], 
                period="1d",
                interval='15m',
                actions="inline")

btc_df=temp.reset_index()
btc_df.columns = [col[0]+"-"+col[1] for col in btc_df.columns.values]

#for bar plot
df = px.data.tips()


#figures 
fig_line = px.line(btc_df, x='Datetime-',y='Volume-BTC-USD',markers=True)
fig_pie = px.pie(df, values='tip', names='day',color_discrete_sequence=px.colors.qualitative.Safe)


#Page Layout
body=dbc.Container(html.Div(children=[
    html.H1(children="Crypto Dashboard Example", style={'color': '#7FDBFF','fontFamily': 'Verdana','backgroundColor':'#000000','textAlign':'center','padding':'5px 0px'}),
    
    dbc.Row(html.Div(children=[
    
        #Left Graph - Line Plot
        dbc.Col(html.Div(children=[
            html.Div(children=[
                dcc.Dropdown(id='crypto_dropdown', 
                            options=[{'label':'Bitcoin','value':'BTC'},
                                    {'label':'Ethereum','value':'ETH'},
                                    {'label':'DogeCoin','value':'DOGE'}]
                            ),
                html.Br(),
                html.H3("BTC",id="crypto_header",style={'color': '#191970','fontFamily': 'Verdana'})
            ]),
        
            html.Div(
                dcc.Graph(   
                    id='btc_line_graph',
                    figure=fig_line 
                    )
                )
            ]
        )), 
    
        
        #Right Graph - Pie Plot
        dbc.Col(html.Div(children=[
            html.Div(children=[
                html.H2("This is an example pie graph",style={'color': '#191970','fontFamily': 'Verdana'}),
                html.Br(),html.Br(),
                dcc.RadioItems(id='theme_radio', 
                            options=[{'label':'Light','value':'white'},
                                    {'label':'Dark','value':'gray'},]
                            )
            ]),
            html.Div(children=[dcc.Graph(   
                                id='pie_graph',
                                figure=fig_pie 
                                ),
                                html.P(id="pie_info", style={'color': '#191970','fontFamily': 'Verdana'})
                            ]
                    ),
        ]
        )
        ),
    ]
    )
    )
        
]))

layout=html.Div([body])

# Line plot callback
@callback(
    
    Output(component_id='btc_line_graph', component_property='figure'),
    Output(component_id='crypto_header', component_property='children'),
    Input(component_id='crypto_dropdown', component_property='value')
)

def update_figure(value):
    
    name="Volume-"+str(value)+"-USD"
    fig = px.line(btc_df, x='Datetime-',y=name,markers=True)

    return fig,value



#Pie plot callback
@callback(
    
    Output(component_id='pie_graph', component_property='figure'),
    Input(component_id='theme_radio', component_property='value')
)

def update_figure_theme(value):
    
    figure=fig_pie
    
    if value=="gray":
        
        figure.update_layout(
        paper_bgcolor=	'#2F4F4F',
        font_color='#FFFFFF')
        
    else:
        figure.update_layout(
        paper_bgcolor=	'#FFFFFF',
        font_color='#2F4F4F')
        
    return figure

@callback(
    
    Output(component_id='pie_info', component_property='children'),
    Input(component_id='pie_graph', component_property='hoverData')
)

def update_figure_theme(hoverData):
    
    lbl=hoverData['points'][0]['label']
    val=hoverData['points'][0]['value']   
    info=f"Label:{lbl}, Value:{val}"
    return (info)
    
    
    
    
    

