"""
# @File    :    sales_app.py
# @Time    :    02/02/2022 13:52
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description: 
"""
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output
from navbar import nav_bar

PLOTLY_LOGO = "https://s2.loli.net/2022/01/21/bl8ZS5vzwjA3YaM.png"
external_stylesheets = [dbc.themes.ZEPHYR, ]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                # make it responsive to mobile
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )


## reading the dataset

df = pd.read_csv('data/Prepared_data.csv')
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
df['month'] = df['Date'].dt.month

# ----------------------monthly rented bike-------------------#
monthly_sales_df = df.copy()
monthly_sales_df = monthly_sales_df.groupby('Date')[
    'Rented Bike Count'].sum().reset_index()
monthly_sales_df['month'] = monthly_sales_df['Date'].dt.month
seasons = df.groupby('Seasons')['Rented Bike Count'].sum().reset_index(
    name='Total Amount')
temp_rent = df.groupby('Temperature').mean()['Rented Bike Count'].reset_index(
    name='Rented Bike Count')
# ----------------------month content dropdwn-------------------#
card_content_dropdwn = [dbc.CardBody([
    html.H6('Select Months', style={'textAlign': 'center'}),
    dbc.Row([
        dbc.Col([
            html.H6('Current Month'),
            dcc.Dropdown(id='dropdown_base',
                         options=[
                             {'label': i, 'value': i} for i in
                             monthly_sales_df['month'].unique()
                         ],
                         value=1,
                         )
        ]),
        dbc.Col([
            html.H6('Reference Month'),
            dcc.Dropdown(id='dropdown_comp',
                         options=[
                             {'label': i, 'value': i} for i in
                             monthly_sales_df['month'].unique()
                         ],
                         value=1,
                         )
        ]),

    ])

])]
# ----------------------plot-------------------#
# Season bar plot
season_total_bar = px.bar(seasons, x='Seasons', y='Total Amount')
season_total_bar.update_layout( title_x=0.5,plot_bgcolor='white')

card_season = [dbc.Card(
    dbc.CardBody(
        [html.H6('seasonal total',
                 style={'fontWeight': 'lighter', 'textAlign': 'center'}),
         dcc.Graph(figure=season_total_bar,
                   style={'height': '450px', 'width': '450px'})
         ]

    ))
]
# Temperature line plot
temp_line = px.line(temp_rent, x='Temperature', y='Rented Bike Count'
                    )
temp_line.update_layout(plot_bgcolor='white')

card_temp = [dbc.Card(
    dbc.CardBody(
        [html.H6('temp',
                 style={'fontWeight': 'lighter', 'textAlign': 'center'}),
         dcc.Graph(figure=temp_line,
                   style={'height': '450px', 'width': '700px'})
         ]

    ))
]


# ----------------------app body-------------------#
body_app = dbc.Container([

    html.Br(),
    html.Br(),
    html.H1('Compare Months', style={'textAlign': 'center'}),
    dbc.Row([
        dbc.Col([dbc.Card(card_content_dropdwn, style={'height': '150px'})],
                width=4),
        dbc.Col([dbc.Card(id='card_num1', style={'height': '150px'})]),
        dbc.Col([dbc.Card(id='card_num2', style={'height': '150px'})]),
        dbc.Col([dbc.Card(id='card_num3', style={'height': '150px'})]),

    ]),
    html.Br(),
    html.Br(),


    dbc.Row([
        dbc.Col([dbc.Card(id='card_num4', style={'height': '450px'})]),
        dbc.Col([dbc.Card(id='card_num5', style={'height': '450px'})]),
        dbc.Col([dbc.Card(id='card_num6', style={'height': '450px'})]),

    ]),

    html.Br(),
    html.Br(),
    html.H1('More Info', style={'textAlign': 'center'}),
    dbc.Row([
        dbc.Col(card_season,width=5),
        dbc.Col(card_temp,width=7),


    ]),

])

app.layout = html.Div(id='parent',
                      children=[body_app])


@app.callback([Output('card_num1', 'children'),
               Output('card_num2', 'children'),
               Output('card_num3', 'children'),
               Output('card_num4', 'children'),
               Output('card_num5', 'children'),
               Output('card_num6', 'children')],
              [Input('dropdown_base', 'value'),
               Input('dropdown_comp', 'value')])
def update_cards(base, comparison):
    # ----------------------data-------------------#
    base_month = df[df['month'] == base]
    comp_month = df[df['month'] == comparison]
    count = (base_month['Rented Bike Count'] != 0).sum()


    rent_total_base = \
        monthly_sales_df.loc[monthly_sales_df['month'] == base].reset_index()[
            'Rented Bike Count']
    rent_total_comp = \
        monthly_sales_df.loc[
            monthly_sales_df['month'] == comparison].reset_index()[
            'Rented Bike Count']
    rent_daily_base = monthly_sales_df[monthly_sales_df['month'] == base]
    rent_daily_comp = monthly_sales_df[monthly_sales_df['month'] == comparison]
    hour_base = base_month.groupby('Hour').sum()[
        'Rented Bike Count'].reset_index(
        name='Total Amount')
    hour_comp = comp_month.groupby('Hour').sum()[
        'Rented Bike Count'].reset_index(
        name='Total Amount')

    monthly_difference = rent_total_base.sum() - rent_total_comp.sum()
    monthly_change = 0

    if monthly_difference >= 0:
        monthly_change = dcc.Markdown(dangerously_allow_html=True,
                                      children=[
                                          "<sub>+{0}</sub>".format(
                                              monthly_difference)],
                                      style={'textAlign': 'center'})

    elif monthly_difference < 0:

        monthly_change = dcc.Markdown(dangerously_allow_html=True,
                                      children=[
                                          "<sub>{0}</sub>".format(
                                              monthly_difference
                                          )],
                                      style={'textAlign': 'center'})

    working_hour = dcc.Markdown(dangerously_allow_html=True,
                                      children=[
                                          "<sub>/{0}</sub>".format(
                                              base_month['Rented Bike Count'].count()
                                          )],
                                      style={'textAlign': 'center'})


    # ----------------------plot-------------------#

    daily_rents_base = go.Figure([go.Scatter(x=rent_daily_base['Date'],
                                             y=rent_daily_base[
                                                 'Rented Bike Count'],
                                             name='{}'.format(comparison),
                                             orientation='h'),
                                  ])
    daily_rents_base.update_layout(plot_bgcolor='white',
                                   title='{}'.format(base),
                                   title_x=0.5)

    day_bar_base = go.Figure([go.Bar(y=rent_daily_base['Date'],
                                     x=rent_daily_base['Rented Bike Count'],
                                     name='{}'.format(comparison),
                                     orientation='h'),
                              ])
    day_bar_comp = go.Figure([go.Bar(y=rent_daily_comp['Date'],
                                     x=rent_daily_comp['Rented Bike Count'],
                                     name='{}'.format(comparison),
                                     orientation='h'),
                              ])
    day_bar_base.update_layout(plot_bgcolor='white',
                               margin=dict(l=40, r=5, t=60, b=40),
                               )

    day_bar_comp.update_layout(plot_bgcolor='white',
                               margin=dict(l=40, r=5, t=60, b=40),
                               )
    # Day and Night Pie plot
    day_pie = go.Figure(
        data=[go.Pie(labels=base_month['Day_night'],
                     values=base_month['Rented Bike Count'])])
    day_pie.update_traces(hole=.4, hoverinfo="label+percent+name")

    fig = go.Figure(
        data=[go.Scatter(x=hour_comp['Hour'], y=hour_comp['Total Amount'], \

                         name='{}'.format(comparison)),
              go.Scatter(x=hour_base['Hour'], y=hour_base['Total Amount'], \

                         name='{}'.format(base))])
    fig.update_layout(plot_bgcolor='white',
                      margin=dict(l=40, r=5, t=60, b=40),
                      )

    # ----------------------cards-------------------#

    card_content1 = [

        dbc.CardBody(
            [
                html.H6('Total Rented Bike Count',
                        style={'fontWeight': 'lighter', 'textAlign': 'center'}),

                html.H3('{0}'.format(rent_total_base.sum()),
                        style={'color': '#090059', 'textAlign': 'center'}),

                monthly_change,

            ]

        )
    ]
    card_content2 = [

        dbc.CardBody(
            [
                html.H6('Total Functional Hours',
                        style={'fontWeight': 'lighter', 'textAlign': 'center'}),

                html.H3('{0}'.format(count),
                        style={'color': '#090059', 'textAlign': 'center'}),

                working_hour,

            ]

        )
    ]
    card_content3 = [

        dbc.CardBody(
            [
                html.H6('Current Season',
                        style={'fontWeight': 'lighter', 'textAlign': 'center'}),

                html.H3('{0}'.format(base_month['Seasons'].unique()),
                        style={'color': '#090059', 'textAlign': 'center'}),


            ]

        )
    ]

    card_content4 = [
        dbc.CardBody(
            [html.H6('Total sales',
                     style={'fontWeight': 'lighter', 'textAlign': 'center'}),
             dcc.Graph(figure=fig,
                       style={'height': '350px', 'width': '350px'})
             ]

        )
    ]

    card_content5 = [
        dbc.CardBody(
            [
                html.H6('Pie',
                        style={'fontWeight': 'lighter', 'textAlign': 'center'}),
                dcc.Graph(figure=day_pie,
                          style={'height': '400px'}),

            ]

        )
    ]

    card_content6 = [

        dbc.CardBody(
            [
                html.H6('Stores with highest Sales',
                        style={'fontWeight': 'lighter', 'textAlign': 'center'}),

                dbc.Row([
                    dbc.Col([dcc.Graph(figure=day_bar_base,
                                       style={'height': '400px'}),
                             ]),
                    dbc.Col([dcc.Graph(figure=day_bar_comp,
                                       style={'height': '400px'}),
                             ])

                ])

            ]

        )
    ]

    return card_content1, card_content2, card_content3, card_content4,card_content5,card_content6


if __name__ == "__main__":
    app.run_server(debug=True)
