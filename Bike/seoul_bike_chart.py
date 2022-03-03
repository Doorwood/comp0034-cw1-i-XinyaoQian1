"""
# @File    :    seoul_bike_chart.py
# @Time    :    03/02/2022 10:22
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description: Functions for creating visualizations in the SeoulBike dashboard
"""

from pathlib import Path
import plotly.express as px
import plotly.graph_objs as go

VENT_DATA_FILEPATH = Path(__file__).parent.joinpath('data', 'Prepared_data.csv')


def seasonal_bar_plot(data):
    """

    Args:
        data (data_frame): The dataframe for plotting the bar chart

    Returns:
         bar plot of the data
    """
    # Season bar plot
    season_total_bar = px.bar(data, x='Seasons', y='Total Amount',text ='Total Amount')
    season_total_bar.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    season_total_bar.update_layout(title_x=0.5, plot_bgcolor='rgba(0,0,0,0)',
                                   paper_bgcolor='rgba(0,0,0,0)',
                                   )
    return season_total_bar


def temp_line_plot(data):
    """

    Args:
        data (data_frame): The dataframe for plotting the line chart

    Returns:
        line plot of the data
    """
    temp_line = px.line(data, x='Temperature', y='Rented Bike Count')
    # temp_line.update_layout(plot_bgcolor='white')
    temp_line.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)')
    return temp_line


def daily_rents_bar_plot(data, month):
    """

    Args:
        data (data_frame): the dataframe for the plot
        month (int): user selected month

    Returns:
        bar plot of the data in the given month

    """
    day_bar = go.Figure([go.Bar(y=data['Date'],
                                x=data['Rented Bike Count'],
                                name=f'{month}',
                                orientation='h',

                                ),
                         ])
    day_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                          paper_bgcolor='rgba(0,0,0,0)',

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
    day_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                          paper_bgcolor='rgba(0,0,0,0)')
    return day_pie


def hour_scatter_plot(base_data, comp_data, base, comparison):
    """

    Args:
        base_data (data_frame):the dataframe for the first plot
        comp_data (data_frame):the dataframe for the second plot
        base (int): current month
        comparison (int): reference Month

    Returns:
        scatter plot of two dataframes

    """
    fig = go.Figure(
        data=[go.Scatter(x=comp_data['Hour'], y=comp_data['Total Amount'],
                         name=f'{comparison}',
                         mode='lines+markers'),
              go.Scatter(x=base_data['Hour'], y=base_data['Total Amount'],
                         name=f'{base}',
                         mode='lines+markers')]
    )
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
                      margin=dict(l=40, r=5, t=60, b=40),
                      )
    return fig
