"""
# @File    :    sales_chart.py
# @Time    :    03/02/2022 10:22
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description: 
"""
import json

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from pathlib import Path
import dash_bootstrap_components as dbc
from dash import html, dcc

VENT_DATA_FILEPATH = Path(__file__).parent.joinpath('data', 'Prepared_data.csv')


def seasonal_bar_plot(data):
    """

    Args:
        data (data_frame): The dataframe for plotting the bar chart

    Returns:
         bar plot of the data
    """
    # Season bar plot
    season_total_bar = px.bar(data, x='Seasons', y='Total Amount')
    season_total_bar.update_layout(title_x=0.5, plot_bgcolor='white')
    return season_total_bar


def temp_line_plot(data):
    """

    Args:
        data (data_frame): The dataframe for plotting the line chart

    Returns:
        line plot of the data
    """
    temp_line = px.line(data, x='Temperature', y='Rented Bike Count')
    temp_line.update_layout(plot_bgcolor='white')
    return temp_line


def card(title, figure, height='390px', width='390px'):
    """

    Args:
        title (str): title of the card
        figure (figure): figure included in the card
        height (str): height of the figure
        width (str): width of the figure

    Returns:
        card-body containing given parameters

    """
    new_card = [dbc.Card(
        dbc.CardBody(
            [html.H6(title,
                     style={'fontWeight': 'lighter', 'textAlign': 'center'}),
             dcc.Graph(figure=figure,
                       style={'height': height, 'width': width})
             ]

        ))
    ]
    return new_card


def daily_rents_bar_plot(data,month):
    """

    Args:
        data (data_frame): the dataframe for the plot
        month (int): user selected month

    Returns:
        bar plot of the data in the given month

    """
    day_bar = go.Figure([go.Bar(y=data['Date'],
                                     x=data['Rented Bike Count'],
                                     name='{}'.format(month),
                                     orientation='h'),
                              ])
    day_bar.update_layout(plot_bgcolor='white',
                               margin=dict(l=40, r=5, t=60, b=40),
                               )
    return day_bar


def pie_plot(data):
    """

    Args:
        data (data_frame): the dataframe for the plot

    Returns:
        pie plot of the data

    """
    # Day and Night Pie plot
    day_pie = go.Figure(
        data=[go.Pie(labels=data['Day_night'],
                     values=data['Rented Bike Count'])])
    day_pie.update_traces(hole=.4, hoverinfo="label+percent+name")
    return day_pie


def hour_scatter_plot(base_data,comp_data,base,comparasion):
    """

    Args:
        base_data (data_frame):the dataframe for the first plot
        comp_data (data_frame):the dataframe for the second plot
        base (int): current month
        comparasion (int): reference Month

    Returns:
        scatter plot of two dataframes

    """
    fig = go.Figure(
        data=[go.Scatter(x=comp_data['Hour'], y=comp_data['Total Amount'],name='{}'.format(comparasion)),
              go.Scatter(x=base_data['Hour'], y=base_data['Total Amount'],name='{}'.format(base))])
    fig.update_layout(plot_bgcolor='white',
                      margin=dict(l=40, r=5, t=60, b=40),
                      )
    return fig


def card_text(title, text, subtext= None):
    """

    Args:
        title (str): title of the card body
        text (Object): main text on the card
        subtext (Object): subtext on the card

    Returns:
        card-body containing title, text and subtext

    """
    new_card = [dbc.CardBody(
        [
            html.H6(title,
                    style={'fontWeight': 'lighter', 'textAlign': 'center'}),

            html.H3('{0}'.format(text),
                    style={'color': '#090059', 'textAlign': 'center'}),

            subtext

        ]

    )]
    return new_card


def card_double_figure(title, fig1, fig2, height='400px'):
    """
    Args:
        title (str): title of the card body
        fig1 (figure): first figure
        fig2 (figure): second figure
        height (str): height of the figures

    Returns:
        card-body containing title, fig1 and fig2

    """
    new_card=[

        dbc.CardBody(
            [
                html.H6(title,
                        style={'fontWeight': 'lighter', 'textAlign': 'center'}),

                dbc.Row([
                    dbc.Col([dcc.Graph(figure=fig1,
                                       style={'height': height}),
                             ]),
                    dbc.Col([dcc.Graph(figure=fig2,
                                       style={'height': height}),
                             ])

                ])

            ]

        )
    ]
    return new_card