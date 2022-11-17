from dash import Dash, html, dcc
import dash

app=Dash(__name__, use_pages=True)

app.layout=html.Div(children=[html.H3("Click the link below",
                            style={'color': '#191970','fontFamily':'Verdana'}),
                    html.Div([
                        html.Div(
                            dcc.Link(f"{page['name']}", href=page["relative_path"],
                                    style={'color': '#7FDBFF','fontFamily':'Verdana','textDecoration':'none'})
                        )
                        for page in dash.page_registry.values()
                    ]),
                        dash.page_container
                    
                    ])

if __name__=='__main__':
    app.run_server(debug=True)