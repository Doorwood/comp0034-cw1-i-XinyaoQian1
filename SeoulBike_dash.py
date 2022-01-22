# Copied from the Dash tutorial documentation at https://dash.plotly.com/layout on 24/05/2021
# Import section modified 10/10/2021 to comply with changes in the Dash library.

# Run this app with `python SeoulBike_dash.py` and visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px


external_stylesheets = [dbc.themes.ZEPHYR]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame see https://plotly.com/python/px-arguments/ for more options

# ------Import data for visualization------
df = pd.read_csv('Prepared_data.csv')
print(df[:5])  # df.head()
Date=px.bar(df,x="Date", y="Rented Bike Count")
app.layout = html.Div(children=[

        html.H1(children='DATA DASHBOARD', style={'text-align':'center'}),

        html.Div(children='''
        This is a <div>.
    '''),

            # dcc.Graph(
            #     id='example-graph',
            #     figure=fig
            # )
    html.Div(children=
    dcc.Graph(

        id='example-graph',
        figure=Date

    )


             )

    ]
    )

if __name__ == '__main__':
    app.run_server(debug=True)
