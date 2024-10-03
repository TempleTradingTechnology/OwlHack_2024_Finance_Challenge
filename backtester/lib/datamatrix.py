'''
Class to manage data set for a list of stocks and for a time period
'''

import os
import datetime
import copy
import pandas as pd
import numpy as np

import common as cm

from loader import DataLoader
from stock import Stock

from preference import get_default_parser, Preference

class DataMatrix(pd.DataFrame):

    '''
    DataMatrix is a panda dataframe where the row is index by datetime with a certain fixed Timeframe.
    The columns are index by keys encoded usng {ticker}_{field}
    where field can be open, high, low, close, volume and calculated Technical indicators or fundamental quantities
    such as capitalization
    '''

    def __init__(self, *args, **kwargs):
        _name = kwargs.pop('name', None)
        _temp = kwargs.pop('universe', None)
        _timeframe = kwargs.pop('timeframe', cm.TimeFrame.DAILY)
        super().__init__(*args, **kwargs)
        self._name = _name
        self._universe = _temp
        self._timeframe = _timeframe

    @property
    def timeframe(self):
        return self._timeframe

    @timeframe.setter
    def timeframe(self, value):
        self._timeframe = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def universe(self):
        return self._universe

    @universe.setter
    def universe(self, value):
        self._universe = value

    def get_info(self):
        info = f"Name: {self._name}, Universe: {self._universe}, TimeFrame: {self.timeframe}"
        return(info)


    def extract_price_matrix(self, price_choice = cm.DataField.close):
        '''
        return a datamatrix that has only the ticker_close columns
        '''
        result = self[[f"{ticker}_{price_choice}" for ticker in self.universe]]
        # keep only the ticker as column label
        result.columns = [f"{col.split('_')[0]}" for col in result.columns]
        return(result)


    def copy_and_zero(self):
        dm = self.copy()
        for col in dm.columns:
            dm[col].values[:] = 0
        return(dm)

    def validate(self):
        '''
        TBD
        '''
        result = True
        return result

    def analyse(self):
        '''
        TBD

        '''
        print(f"running analyse in DataMatrix")



class DataMatrixLoader(DataLoader):
    '''
    class responsible for loading data from files or database into DataMatrix which is a derived class from pandas DataFrame
    '''

    def __init__(self, pref, name, universe, start_date, end_date, data_src = DataLoader.DataSource.CSV,
                data_dir = None, db_connection = None):

        super().__init__(pref, data_src, data_dir, db_connection)
        self.name = name
        self.universe = universe
        self.start_date = start_date
        self.end_date = end_date


    def get_daily_datamatrix(self, fields = None):
        '''
        create datamatrix with columns as {ticker_field}
        '''
        df = Stock(self, self.universe[0]).get_daily_hist_price(self.start_date,
                                                                self.end_date).grab_fields(fields)

        for ticker in self.universe[1:]:
            tdf = Stock(self, ticker).get_daily_hist_price(self.start_date,
                                                        self.end_date).grab_fields(fields)
            for col in tdf.columns:
                df[col] = tdf[col]

        df = DataMatrix(df, name = self.name, universe = self.universe, timeframe = cm.TimeFrame.DAILY)
        df.fillna(0, inplace=True)

        return df

# ==============================================
# Testing
# ==============================================
def _test1():

    print('Running Test1')
    pref = Preference()
    fname = os.path.join(pref.data_root_dir, 'train/AWO.csv')
    df = pd.read_csv(fname)

    dm = DataMatrix(df, name = 'test', universe = ['AWO', 'BDJ'])

    print(dm.get_info())
    print(dm.head())

    dm = DataMatrix(data = {'A': [1,2,3], 'B': [4, 5, 6]})
    print(dm.get_info())
    print(dm.head())

    # show how to apply lambda
    # modify column by column
    import math
#    dm = dm.apply(lambda col: np.square(col) if col.name == 'A' else col + 1, axis=0)
#    dm = dm.apply(lambda col: col.index if col.name == 'A' else col + 1, axis=0)
    dm = dm.apply(lambda col: (lambda x: x**3)(col) if col.name == 'A' else col + 1, axis=0)
    print(dm.head())

#    dm = dm.apply(lambda row: col.name , axis=1)

def _test2():

    print('Running test2')
    parser = get_default_parser()
    args = parser.parse_args()

    pref = Preference(cli_args = args)

    universe = ['AWO', 'BDJ', 'BDTC']
    start_date = datetime.date(2010, 1, 1)
    end_date = datetime.date(2022, 1, 1)

    name = 'test'
    loader = DataMatrixLoader(pref, name, universe, start_date, end_date)
    dm = loader.get_daily_datamatrix()
    print(dm.get_info())

    print(dm.extract_price_matrix('Close'))

    if not os.path.exists ("C:/temp"):
        os.mkdir("C:/temp")

    output_fname = f"C:/temp/{name}1.csv"
    print(f"Dumping output file to {output_fname}")
    dm.to_csv(output_fname)

    fields = [cm.DataField.close, cm.DataField.volume, cm.DataField.SMA_200, cm.DataField.daily_returns]

    dm = loader.get_daily_datamatrix(fields)
    output_fname = f"C:/temp/{name}2.csv"
    print(f"Dumping output file to {output_fname}")
    dm.to_csv(output_fname)

    dm2 = dm.copy_and_zero()

    print(dm2.head(), type(dm2))

def _test():
    _test1()
    _test2()

if __name__ == "__main__":
    import sys
    sys.path.append(os.getcwd())
    _test()


