"""
# @File    :    sales_app.py
# @Time    :    02/02/2022 13:52
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description: 
"""
from typing import Union, Any

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc
from dash.dependencies import Input, Output
from plotly.graph_objs import Figure
from datapre import Data
import navbar as nav
import sales_chart as cc
data = Data()


external_stylesheets = [dbc.themes.ZEPHYR, ]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                # make it responsive to mobile
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

# ----------------------data processing-------------------#

df = pd.read_csv('data/Prepared_data.csv')
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
df['month'] = df['Date'].dt.month

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

season_total_bar: Union[Figure, Any] = cc.seasonal_bar_plot(seasons)
temp_line = cc.temp_line_plot(temp_rent)
card_season = cc.card('seasonal total', season_total_bar, '450px', '450px')
card_temp = cc.card('temp', temp_line, '450px', '700px')

# ----------------------app elements-------------------#
navbar = nav.nav_bar()
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
        dbc.Col(card_season, width=5),
        dbc.Col(card_temp, width=7),
    ]),

])

app.layout = html.Div(id='parent',
                      children=[navbar,
                                body_app])


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
    hour_count = (base_month['Rented Bike Count'] != 0).sum()

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

    day_bar_base = cc.daily_rents_bar_plot(rent_daily_base, base)
    day_bar_comp = cc.daily_rents_bar_plot(rent_daily_comp, comparison)
    day_pie = cc.pie_plot(base_month)
    hour_scatter = cc.hour_scatter_plot(hour_base, hour_comp, base, comparison)

    # ----------------------cards-------------------#

    card_content1 = cc.card_text('Total Rented Bike Count',
                                 rent_total_base.sum(), monthly_change)
    card_content2 = cc.card_text('Total Functional Hours', hour_count,
                                 working_hour)
    card_content3 = cc.card_text('Current Season',
                                 base_month['Seasons'].unique())

    card_content4 = cc.card('Total sales', hour_scatter)
    card_content5 = cc.card('Pie', day_pie, )
    card_content6 = cc.card_double_figure('Daliy Rents', day_bar_base,
                                          day_bar_comp, )

    return card_content1, card_content2, card_content3, card_content4, card_content5, card_content6


if __name__ == "__main__":
    app.run_server(debug=True, port=8100)
