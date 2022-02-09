"""
# @File    :    SeoulBike_data.py
# @Time    :    03/02/2022 12:42
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description: 
"""
from pathlib import Path

import pandas as pd


class Data:
    def __init__(self):
        self.df = pd.DataFrame()
        self.get_data()
        self.month = pd.DataFrame()
        self.daily_total = pd.DataFrame()
        self.seasons_total = pd.DataFrame()
        self.temp_rent_mean = pd.DataFrame()
        self.hour = pd.DataFrame()
        self.working_hour = 0
        self.rent_daily = pd.DataFrame()

    def get_data(self):
        datafolder = Path('data')
        csvfile = 'Prepared_data.csv'
        self.df = pd.read_csv(datafolder / csvfile)
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%Y-%m-%d')
        self.df['month'] = self.df['Date'].dt.month


    def pre_process_data(self):
        self.daily_total = self.df.copy()
        self.daily_total = self.daily_total.groupby('Date')[
            'Rented Bike Count'].sum().reset_index()
        self.daily_total['month'] = self.daily_total['Date'].dt.month
        self.seasons_total = self.df.groupby('Seasons')[
            'Rented Bike Count'].sum().reset_index(
            name='Total Amount')
        self.temp_rent_mean = self.df.groupby('Temperature').mean()[
            'Rented Bike Count'].reset_index(
            name='Rented Bike Count')

    def process_data_for_given_month(self, month):
        self.month = self.df[self.df['month'] == month]
        self.hour = self.month.groupby('Hour').sum()[
            'Rented Bike Count'].reset_index(
            name='Total Amount')
        self.working_hour = (self.month['Rented Bike Count'] != 0).sum()
        self.rent_total = \
        self.month.loc[self.month['month'] == month].reset_index()[
            'Rented Bike Count']
        self.rent_daily = self.daily_total[self.daily_total['month'] == month]
