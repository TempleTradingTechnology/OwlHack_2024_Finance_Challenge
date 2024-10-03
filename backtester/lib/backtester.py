'''
Main driver class for the backtester

'''
import os
import datetime

import preference
import common as cm

from datamatrix import DataMatrixLoader
from longindex_strategy import LongIndexStrategy

class Driver(object):

    def __init__(self, pref):
        self.pref = pref
        self.start_date = pref.start_date
        self.end_date = pref.end_date
        self.universe_name = pref.universe_name
        self.initial_capital = pref.initial_capital
        self.universe = cm.get_index_components(pref.universe_name, pref.meta_data_dir)
        self.benchmark_etf = cm.get_ETF_by_index(pref.universe_name)
        self.datamatrix_loader = DataMatrixLoader(pref, pref.universe_name, self.universe, pref.start_date, pref.end_date)
        self.strategy_list = []
        self.run_date = None

        print(
    """
+-----------------------------------------------+
|          TTT Stock Backtester v1.0            |
+-----------------------------------------------+
    """)

    def get_info(self):
        '''
        Return all the settings for this backtest
        '''
        info = self.pref.describe()
        info += f"\nRun date: {self.run_date}"
        return(info)

    def run(self, strategy_list):
        self.run_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        self.strategy_list = strategy_list

        for strategy in strategy_list:
            strategy.validate()
            strategy.run_strategy()
            strategy.save_to_csv(self.pref.output_dir)

    def run_benchmark(self):
        '''
        for each backtest, we have index ETF as its benchmark for comparison.
        For example, long SPY for S&P 500 universe
        '''
        etf_universe = [self.benchmark_etf]
        loader = DataMatrixLoader(self.pref, self.pref.universe_name, etf_universe, self.pref.start_date, self.pref.end_date)
        dm = loader.get_daily_datamatrix()

        buyETF = LongIndexStrategy(self.pref, dm, cm.OneMillion, index_name = self.benchmark_etf)
        buyETF.validate()
        buyETF.run_strategy()
        buyETF.save_to_csv(self.pref.output_dir)

        print(f"""
+-----------------------------------------------+
|            Benchmark Performance              |
+-----------------------------------------------+
Output File:      {self.pref.output_dir}
+-----------------------------------------------+ce
Benchmark:        {LongIndexStrategy.__name__} on {self.benchmark_etf}
Start Date:       {self.pref.start_date}
End Date:         {self.pref.end_date}
+-----------------------------------------------+
Initial Value:      ${self.initial_capital:,.3f}
Final Value:        ${buyETF.pnl['cumulative_pnl'].iloc[-1]:,.3f}
Total Return:       ${buyETF.pnl['cumulative_pnl'].iloc[-1] - self.initial_capital:,.3f}
+-----------------------------------------------+
Cumulative Return:     {buyETF.performance['Cumulative Returns']:.3f}%
Sharpe Ratio:          {buyETF.performance['Sharpe Ratio']:.3f}
Max Drawdown:          {buyETF.performance['Maximum Drawdown']:.3f}%
+-----------------------------------------------+
        """)

    def summary(self):
        '''
        print out summary of the result
        '''
        print(f"""
+-----------------------------------------------+
|               Backtester Summary              |
+-----------------------------------------------+
        """, end='')

        for strategy in self.strategy_list:
            print(f"""
=====          {strategy.name}              =====
Trading History:
    {strategy.port.summary()}

Portfolio Value:
    Initial Value:      ${self.initial_capital:,.3f}
    Final Value:        ${strategy.pnl['cumulative_pnl'].iloc[-1]:,.3f}
    Total Return:       ${strategy.pnl['cumulative_pnl'].iloc[-1] - self.initial_capital:,.3f}

Performance:
    Cumulative Return:     {strategy.performance['Cumulative Returns']:.3f}%
    Sharpe Ratio:          {strategy.performance['Sharpe Ratio']:.3f}
    Max Drawdown:          {strategy.performance['Maximum Drawdown']:.3f}%

==================================================
            """)

        print(f"""
+-----------------------------------------------+
|              Backtester Completed             |
+-----------------------------------------------+
        """)


# ==============================================
# Testing
# ==============================================
def _test():
    '''
    unit test
    '''
    parser = preference.get_default_parser()
    parser.add_argument('--universe_name',   dest='universe_name', default = 'OwlHack 2024 Universe', help='Name of the Universe')
    parser.add_argument('--initial_capital', dest='initial_capital', default = cm.OneMillion, help='Initial Capital')
    parser.add_argument('--random_seed', dest='random_seed', default = None, type = int, help='Random Seed')

    args = parser.parse_args()
    pref = preference.Preference(cli_args = args)

    if pref.output_dir is None:
        pref.output_dir = pref.test_output_dir

    driver = Driver(pref)


if __name__ == '__main__':
    import sys
    sys.path.append(os.getcwd())
    _test()




