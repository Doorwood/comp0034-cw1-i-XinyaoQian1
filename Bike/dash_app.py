"""
# @File    :    dash_app.py
# @Time    :    24/02/2022 01:36
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description: 
"""
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import Bike.seoul_bike_chart as Sc
import Bike.seoul_bike_elements as El
from Bike.seoul_bike_data import Data
# ----------------------data processing-------------------#

static_data = Data()
static_data.pre_process_data()

# ----------------------static data plot-------------------#

season_total_bar= Sc.seasonal_bar_plot(
    static_data.seasons_total)
temp_line = Sc.temp_line_plot(static_data.temp_rent_mean)
card_season = El.card('Seasonal Total Bike Rent Count', season_total_bar,
                      '450px', '450px')
card_temp = El.card('Correlation between Temperature and Average Rented Bike '
                    'Count', temp_line, '450px', '700px')

# ----------------------app elements-------------------#
navbar = El.nav_bar()
card_content_dropdwn = El.dropdown()

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
# Create a Dash app
def init_dashboard(flask_app):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(server=flask_app,
                         routes_pathname_prefix="/dash_app/",
                         external_stylesheets=[dbc.themes.ZEPHYR, 'mystyles.css'],
                         )

    dash_app.layout =html.Div(id='parent',
                      children=
                      [
                          navbar,
                          body_app
                      ])
    init_callbacks(dash_app)

    return dash_app.server


def init_callbacks(dash_app):
    # ----------------------app callbacks-------------------#
    @dash_app.callback([Output('card_num1', 'children'),
                   Output('card_num2', 'children'),
                   Output('card_num3', 'children'),
                   Output('card_num4', 'children'),
                   Output('card_num5', 'children'),
                   Output('card_num6', 'children')],
                  [Input('dropdown_base', 'value'),
                   Input('dropdown_comp', 'value')])
    def update_cards(current, reference):
        """

        Args:
            current (int): current month
            reference (int): referencing month

        Returns:
            card_content1:
             shows month1's Total Rented Bike Count compare to that of month2
            card_content2:
             shows month1's functional hours versus total hours
            card_content3:
             shows month1's season
            card_content4:
             Scatter plot of month1 and month2's hourly rent trend
            card_content5:
             pie plot of month1's day-night rent distribution
            card_content6:
             compare month1 and month2's daily rents

        """
        # ----------------------data processing-------------------#
        month1 = Data()  # current month
        month1.pre_process_data()
        month1.process_data_for_given_month(current)
        base_month = month1.month
        rent_number_1 = month1.rent_total

        month2 = Data()  # reference month
        month2.pre_process_data()
        month2.process_data_for_given_month(reference)

        monthly_difference = rent_number_1.sum() - month2.rent_total.sum()
        monthly_change = 0

        # Adapted from Online Course: Interactive python dashboards | Plotly Dash
        # 2022| 3 Projects
        # https://www.udemy.com/course/plotly-dash-python-dashboards/
        if monthly_difference >= 0:
            monthly_change = dcc.Markdown(dangerously_allow_html=True,
                                          children=[
                                              f"<sub>{monthly_difference}</sub>"
                                          ],
                                          style={'textAlign': 'center'})

        elif monthly_difference < 0:

            monthly_change = dcc.Markdown(dangerously_allow_html=True,
                                          children=[
                                              f"<sub>{monthly_difference}</sub>"
                                          ],
                                          style={'textAlign': 'center'})

        total_hour = dcc.Markdown(dangerously_allow_html=True,
                                  children=[
                                      f"<sub>/{base_month['Rented Bike Count'].count()}</sub>"],
                                  style={'textAlign': 'center'})

        # ----------------------plot-------------------#

        # day_bar_base = Sc.daily_rents_bar_plot(month1.rent_daily, current)
        # day_bar_comp = Sc.daily_rents_bar_plot(month2.rent_daily, reference)
        # day_pie = Sc.pie_plot(base_month)
        # hour_scatter = Sc.hour_scatter_plot(month1.hour, month2.hour, current,
        #                                     reference)

        # ----------------------cards-------------------#

        card_content1 = El.card_text('Total Rented Bike Count',
                                     rent_number_1.sum(), monthly_change)
        card_content2 = El.card_text('Total Functional Hours',
                                     month1.working_hour,
                                     total_hour)
        card_content3 = El.card_text('Current Season',
                                     base_month['Seasons'].iloc[0])

        card_content4 = El.card('Hourly Rent Trend',
                                Sc.hour_scatter_plot(month1.hour, month2.hour,
                                                     current,
                                                     reference))
        card_content5 = El.card('Day vs Night Rents',
                                Sc.pie_plot(base_month))
        card_content6 = El.card_double_figure('Daily Rents',
                                              Sc.daily_rents_bar_plot(
                                                  month1.rent_daily, current),
                                              Sc.daily_rents_bar_plot(
                                                  month2.rent_daily,
                                                  reference), )

        return card_content1, card_content2, card_content3, card_content4, \
               card_content5, card_content6

