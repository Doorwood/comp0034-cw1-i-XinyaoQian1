"""
# @File    :    seoul_bike_data.py
# @Time    :    03/02/2022 12:42
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description: Data class for processing required datasets
"""
from pathlib import Path

import pandas as pd


class Data:
    """
    Data class to represent and process data for visualizations
    """

    def __init__(self):
        self.data = pd.DataFrame()
        self.get_data()
        self.month = pd.DataFrame()
        self.daily_total = pd.DataFrame()
        self.rent_total = pd.DataFrame()
        self.seasons_total = pd.DataFrame()
        self.temp_rent_mean = pd.DataFrame()
        self.hour = pd.DataFrame()
        self.working_hour = 0
        self.rent_daily = pd.DataFrame()

    def get_data(self):
        """
        get data from csv file

        """
        datafolder = Path('../data')
        csvfile = 'Prepared_data.csv'
        self.data = pd.read_csv(datafolder / csvfile)
        self.data['Date'] = pd.to_datetime(self.data['Date'], format='%Y-%m-%d')
        self.data['month'] = self.data['Date'].dt.month

    def pre_process_data(self):
        """
        Processing data for static plots
        """
        self.daily_total = self.data.copy()
        self.daily_total = self.daily_total.groupby('Date')[
            'Rented Bike Count'].sum().reset_index()
        self.daily_total['month'] = self.daily_total['Date'].dt.month
        self.seasons_total = self.data.groupby('Seasons')[
            'Rented Bike Count'].sum().reset_index(
            name='Total Amount')
        self.temp_rent_mean = self.data.groupby('Temperature').mean()[
            'Rented Bike Count'].reset_index(
            name='Rented Bike Count')

    def process_data_for_given_month(self, month):
        """
        Processing data for interactive plots
        """
        self.month = self.data[self.data['month'] == month]
        self.hour = self.month.groupby('Hour').sum()[
            'Rented Bike Count'].reset_index(
            name='Total Amount')
        self.working_hour = (self.month['Rented Bike Count'] != 0).sum()
        self.rent_total = \
            self.month.loc[self.month['month'] == month].reset_index()[
                'Rented Bike Count']
        self.rent_daily = self.daily_total[self.daily_total['month'] == month]
