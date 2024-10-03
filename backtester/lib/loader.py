'''
Classes for loading data into DataFrame
'''

import os
import datetime
import enum
import pandas as pd
import numpy as np

import common as cm

from preference import Preference

class DataLoader(object):

    '''
    class responsible for loading data from files or database into pandas DataFrame
    '''

    class DataSource(enum.Enum):
        CSV = 1
        SQLITE = 2

    def __init__(self, pref, data_src = DataSource.CSV, data_dir = None, db_connection = None):

        self.pref = pref
        self.data_src = data_src
        self.db_connection = db_connection
        if data_dir is None:
            self.data_dir = self.pref.train_data_dir
        else:
            self.data_dir = data_dir


    def get_daily_hist_price(self, ticker, start_date = None, end_date = None):

        fname = os.path.join(self.data_dir, f"{ticker}_daily.csv")
        if not os.path.exists(fname):
            fname = os.path.join(self.data_dir, f"{ticker}.csv")
        df = pd.read_csv(fname)

        df['Date'] = df['Date'].apply(lambda x: datetime.datetime.strptime(x[:10], '%Y-%m-%d').date())

        if start_date is not None:
            df = df[df['Date'] >= start_date]
        if end_date is not None:
            df = df[df['Date'] <= end_date]

        df = df.set_index('Date')
        return(df)


def _test1():

    from pprint import pprint
    print('Running test1')
    pref = Preference()
    #pprint(vars(pref))

    loader = DataLoader(pref, data_dir = pref.train_data_dir)

    df = loader.get_daily_hist_price('AWO')
    print(df.head())
    print(df.tail())

# ==============================================
# Testing
# ==============================================
def _test():
    _test1()


if __name__ == '__main__':
    import sys
    sys.path.append(os.getcwd())
    _test()
