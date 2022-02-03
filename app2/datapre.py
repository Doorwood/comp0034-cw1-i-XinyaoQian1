"""
# @File    :    datapre.py
# @Time    :    03/02/2022 12:42
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description: 
"""
from pathlib import Path

import pandas as pd
class Data:
    def __init__(self):
        self.df=pd.DataFrame()
        self.get_data()
        self.month=[]

    def get_data(self):
        datafolder = Path('data')
        csvfile = 'Prepared_data.csv'
        self.df = pd.read_csv(datafolder/csvfile)
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%Y-%m-%d')
        self.df['month'] = self.df['Date'].dt.month

    def process_data_for_month(self, month):
        self.month = self.df[self.df['month'] == month]
        self.month= self.df.copy()
        self.month = self.month.groupby('Date')[
            'Rented Bike Count'].sum().reset_index()





