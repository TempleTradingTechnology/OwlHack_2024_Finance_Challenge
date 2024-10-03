'''
Classes for Buy and Hold
'''

import enum
import datetime
import pandas as pd

import common as cm
from strategy import Strategy
from datamatrix import DataMatrix, DataMatrixLoader
from preference import Preference

class LongIndexStrategy(Strategy):

    def __init__(self, pref, input_datamatrix: DataMatrix, initial_capital: float, price_choice = cm.DataField.close, index_name = 'SPY'):
        super().__init__(pref, f'Long{index_name}', input_datamatrix, initial_capital, price_choice)
        self.index_name = index_name

    def validate(self):
        '''
        validate if the input_dm has everything the strategy needs
        '''
        columns = self.input_dm.columns
        col = f"{self.index_name}_{self.price_choice}"
        if col not in columns:
            raise Exception(f"Cannot found {col} in input data")


    def run_model(self, model = None):
        '''
        No external prediction model needed, just buy the index on day 1 and sell at the end
        '''
        taction = self.pricing_matrix.copy()
        tsignal = self.pricing_matrix.copy()
        shares = self.pricing_matrix.copy()

        taction = taction.applymap(lambda x: cm.TradeAction.NONE.value)
        tsignal *= 0
        shares  *= 0


        col_index = self.pricing_matrix.columns.get_loc(self.index_name)

        # buy on first day
        tsignal.iloc[0, col_index] = 1
        taction.iloc[0, col_index] = cm.TradeAction.BUY.value
        shares.iloc[0, col_index] = int (self.initial_capital / self.pricing_matrix.iloc[0, col_index])

        # sell on last day
        tsignal.iloc[-1, col_index] = -1
        taction.iloc[-1, col_index] = cm.TradeAction.SELL_TO_CLOSE_ALL.value
        shares.iloc[-1, col_index] = shares.iloc[0, col_index]

        return(tsignal, taction, shares)



def _test1():

    pref = Preference()
    # pick some random name
    universe = ['SPY', 'AWO']
    start_date = datetime.date(2001, 1, 1)
    end_date = datetime.date(2023, 1, 1)

    name = 'test'
    fields = [cm.DataField.close, cm.DataField.volume, cm.DataField.SMA_200, cm.DataField.daily_returns]

    loader = DataMatrixLoader(pref, name, universe, start_date, end_date)
    dm = loader.get_daily_datamatrix(fields)

    print(dm.get_info())
    print(dm.head())

    buyIndex = LongIndexStrategy(pref, dm, cm.OneMillion, index_name = 'SPY')
    buyIndex.validate()
    tradesignal, tradeaction, shares = buyIndex.run_model()

    print(tradeaction.head())
    print(shares)

    buyIndex.run_strategy()
    print(buyIndex.performance)

    buyIndex.save_to_csv(pref.test_output_dir)


def _test():
    _test1()


if __name__ == "__main__":
    _test()
