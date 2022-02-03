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
import plotly.graph_objects as go
from dash.dependencies import Output, Input, State

PLOTLY_LOGO = "https://s2.loli.net/2022/01/21/bl8ZS5vzwjA3YaM.png"
external_stylesheets = [dbc.themes.ZEPHYR, ]

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
    color="lightblue",
    dark=True,
)

# assume you have a "long-form" data frame see https://plotly.com/python/px-arguments/ for more options

# ------Import data for visualization------
df = pd.read_csv('data/Prepared_data.csv')

df['Date'] = pd.to_datetime(df['Date'], format="%Y/%m/%d")

df['month'] = df['Date'].dt.month

seasons = df.groupby('Seasons')['Rented Bike Count'].sum().reset_index(
    name='Total Amount')
hour = df.groupby('Hour').sum()['Rented Bike Count'].reset_index(
    name='Total Amount')
temp_rent = df.groupby('Temperature').mean()['Rented Bike Count'].reset_index(
    name='Rented Bike Count')

# Temperature line plot
temp_line = px.line(temp_rent, x='Temperature', y='Rented Bike Count',
                    title='Rented Bike Count vs Temperature')
temp_line.update_layout(title_text='Your title', title_x=0.5)
# Season bar plot
season_total_bar = px.bar(seasons, x='Seasons', y='Total Amount')
season_total_bar.update_layout(title_text='Your title', title_x=0.5)
# Hourly line and bar plot
hour_line_bar = go.Figure()
hour_line_bar.add_trace(
    go.Scatter(
        x=hour['Hour'],
        y=hour['Total Amount'],
    ))

hour_line_bar.add_trace(
    go.Bar(
        x=hour['Hour'],
        y=hour['Total Amount'],

    ))
hour_line_bar.update_layout(
    title={
        'text': "Plot Title",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

# Day and Night Pie plot
day_pie = go.Figure(
    data=[go.Pie(labels=df['Day_night'], values=df['Rented Bike Count'])])
day_pie.update_traces(hole=.4, hoverinfo="label+percent+name")
# day_pie.update_layout(title='Title')

day_pie.update_layout(
    title={
        'text': "Plot Title",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

# Elements in layout
title = html.H1(
    children='DATA DASHBOARD',
    style={'text-align': 'center'}
)

day_night_pie = html.Div(
    children=dcc.Graph(
        id='day pie',
        figure=day_pie,
    )
)
bar_line = html.Div(
    children=dcc.Graph(
        id='bar_line',
        figure=hour_line_bar,
    )

)

season_bar = html.Div(
    children=dcc.Graph(
        id='seasonal amount',
        figure=season_total_bar,

    ))
temperature_line = html.Div(
    children=dcc.Graph(
        id='temp_line',
        figure=temp_line,
    )
)

card = dbc.Card(
    [
        dbc.CardImg(src="/static/images/placeholder286x180.png", top=True),
        dbc.CardBody(
            [
                html.H4("Card title", className="card-title"),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),
                dbc.Button("Go somewhere", color="primary"),
            ]
        ),
    ],
    style={"width": "30rem"},
)

# row of graphs

row1 = dbc.Row([  # row1
    dbc.Col(bar_line, width=6),
    dbc.Col(day_night_pie, width=3),
    dbc.Col(season_bar, width=3),

])
row2 = dbc.Row([  # row2
    dbc.Col(temperature_line, width=5),
    dbc.Col('Figure Expected ', width=4),
    dbc.Col('Figure Expected', width=3),
])

month_dropdown = dcc.Dropdown(id='month-dropdown',
                              options=[{'label': month, 'value': month}
                                       for month in df['month'].unique()],
                              value=1)


# dff = df.copy()
# dff = dff[dff["month"] == 3]
# dff = dff.groupby('Date')['Rented Bike Count'].sum().reset_index('Date')
# fig2 = px.bar(dff, x='Date', y='Rented Bike Count')


app.layout = html.Div(children=[
    navbar,
    title,
    month_dropdown,
    row1,
    row2,
    dcc.Graph(id='out1', figure={}),
    # dcc.Graph(figure=fig2),


])


@app.callback([Output(component_id='out1', component_property='figure')],
              [Input(component_id='month-dropdown',
                     component_property='value')])
def update_month_graph(option_selected):
    print(option_selected)
    print(type(option_selected))
    container = "The month chosen by user was: {}".format(option_selected)
    dff = df.copy()
    dff = dff[dff["month"] == option_selected]
    print(dff.info(3))
    dff = dff.groupby('Date')['Rented Bike Count'].sum().reset_index('Date')
    print(dff.info(3))
    fig = px.bar(dff, x='Date', y='Rented Bike Count')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True,port=3000)
