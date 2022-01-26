"""
# @File    :    navbar_example.py
# @Time    :    22/01/2022 23:03
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description:
"""
# Copied from the Dash tutorial documentation at https://dash.plotly.com/layout on 24/05/2021
# Import section modified 10/10/2021 to comply with changes in the Dash library.

# Run this app with `python SeoulBike_dash.py` and visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.dependencies import Output, Input, State

PLOTLY_LOGO = "https://s2.loli.net/2022/01/21/bl8ZS5vzwjA3YaM.png"
external_stylesheets = [dbc.themes.BOOTSTRAP, ]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                # make it responsive to mobile
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
# Search bar
search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)
# Navbar
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Seoul Bike Company",
                                                className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavLink("Internal link1", href="/l/components/nav",
                        active=True),
            dbc.NavLink("Internal link2", href="/l/components/nav",
                        active=True),
            dbc.NavLink("Internal link3", href="/l/components/nav",
                        active=True),
            dbc.NavLink("Internal link4", href="/l/components/nav",
                        active=True),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),

            dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),

        ]
    ),
    color="dark",
    dark=True,
)

# assume you have a "long-form" data frame see https://plotly.com/python/px-arguments/ for more options

# ------Import data for visualization------
df = pd.read_csv('data/Prepared_data.csv')
print(df[:5])  # df.head()

line_fig1 = px.line(df, x='Temperature',y='Rented Bike Count')

seasons = df.groupby('Seasons')['Rented Bike Count'].sum().reset_index(name ='Total Amount')
season_total_bar=px.bar(seasons,x='Seasons',y='Total Amount',title='Seasonal Rent amount')
hour = df.groupby('Hour').sum()['Rented Bike Count'].reset_index(name ='Total Amount')

hour_toal_line=px.line(hour,x='Hour',y='Total Amount',title='fig2')
hour_toal_bar =px.bar(hour,x='Hour',y='Total Amount',title='fig3')
Hour_line=html.Div(
    children=dcc.Graph(
        id='hour amount1',
        figure=hour_toal_line,

    )
)

hour_bar=html.Div(
    children=dcc.Graph(
        id='hour amount2',
        figure=hour_toal_bar,
    )
)

season_bar= html.Div(children=dcc.Graph(
    id='seasonal amount',
    figure=season_total_bar,

)

)
title=html.H1(children='DATA DASHBOARD', style={'text-align':'center'})
# row of graphs

row1 = dbc.Row([  # row1
    dbc.Col(season_bar, width=6),
    dbc.Col(Hour_line, width=3),
    dbc.Col(hour_bar, width=3),

])
row2 = dbc.Row([  # row2
    dbc.Col('Column 1', width=5),
    dbc.Col('Column 2', width=4),
    dbc.Col('Column 3', width=3),
])
app.layout = html.Div(children=[
    navbar,
    title,
    row1,
    row2,
])

if __name__ == '__main__':
    app.run_server(debug=True)
