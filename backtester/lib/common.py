'''
Misc utilites
'''

import os
import datetime
import enum
import numpy as np
import pandas as pd

OneThousand = 1000.0
OneHundredThousand = 100000.0
OneMillion = 1000000.0

# should not depend on other library

class TimeFrame(enum.Enum):

    def __str__(self):
        return(str(self.value))

    DAILY = 'daily'
    ONEMIN = '1-min'
    FIVEMIN = '5-min'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

class DataField(str, enum.Enum):

    def __str__(self):
        return(str(self.value))

    open = 'Open'
    high = 'High'
    low = 'Low'
    close = 'Close'
    volume = 'Volume'

    # common moving averages
    SMA_10 = 'SMA_10'
    SMA_20 = 'SMA_20'
    SMA_50 = 'SMA_50'
    SMA_200 = 'SMA_200'

    daily_returns = 'daily_returns'
    weekly_returns = 'weekly_returns'
    monthly_returns = 'monthly_returns'
    fifty_two_high = '52_weeks_high'
    fifty_two_low = '52_weeks_low'

    capitalization = 'Capitalization'

    # common technical indicators
    RSI = 'RSI'


OHLCV_Fields_value = [DataField.open.value, DataField.high.value, DataField.low.value, DataField.close.value, DataField.volume.value]
SMA_Fields_value = [DataField.SMA_10.value, DataField.SMA_20.value, DataField.SMA_50.value, DataField.SMA_200.value]


class TradeAction(enum.Enum):

    def __str__(self):
        return(str(self.value))

    NONE              = ""
    BUY               = "BUY"                   # Buy shares
    SELL              = "SELL"                  # Sell shares
    BUY_TO_CLOSE_ALL  = "BUY_TO_CLOSE_ALL"      # Buy back all short positions
    SELL_TO_CLOSE_ALL = "SELL_TO_CLOSE_ALL"     # Sell all long positions

    # the following are for buying and selling shares without specifying the number of shares
    BUY_TO_CLOSE_50   = "BUY_TO_CLOSE_50"       # buy to close half
    BUY_TO_CLOSE_25   = "BUY_TO_CLOSE_25"       # buy to close a quarter
    SELL_TO_CLOSE_50  = "SELL_TO_CLOSE_50"      # sell 50 percent
    SELL_TO_CLOSE_25  = "SELL_TO_CLOSE_25"      # sell quarter position

def is_a_buy(trade_action):
    return trade_action in [TradeAction.BUY, TradeAction.BUY_TO_CLOSE_ALL, TradeAction.BUY_TO_CLOSE_50, TradeAction.BUY_TO_CLOSE_25,
                            TradeAction.BUY.value, TradeAction.BUY_TO_CLOSE_ALL.value, TradeAction.BUY_TO_CLOSE_50.value,
                            TradeAction.BUY_TO_CLOSE_25.value
                            ]

def is_a_sell(trade_action):
    return trade_action in [TradeAction.SELL, TradeAction.SELL_TO_CLOSE_ALL, TradeAction.SELL_TO_CLOSE_50, TradeAction.SELL_TO_CLOSE_25,
                            TradeAction.SELL.value, TradeAction.SELL_TO_CLOSE_ALL.value,
                            TradeAction.SELL_TO_CLOSE_50.value, TradeAction.SELL_TO_CLOSE_25.value
                            ]

class TradeSignal(enum.Enum):
    SHORT = -1
    HOLD = 0
    LONG = 1

class WeighingScheme(enum.Enum):
    EqualShares = "EQL_SHARE"
    EqualDollarExposure = "EQL_DOLLAR"
    MarketCapitalization = "MKT_CAP"

class RiskAllocation(enum.Enum):
    FIXED_PERCENT_PORT = "FIXED_PERCENT"
    FIXED_DOLLAR = "FIXED_DOLLAR"
    EQUAL_RISK = "EQUAL_RISK"


class DisposalMethod(enum.Enum):
    FIFO = "FIFO"
    LIFO = "LIFO"

def get_index():
    return ['S&P 500', 'NASDAQ 100', 'DJIA', 'RUSSELL 2000', 'OwlHack 2024 Universe', 'Test Universe', 'Small Universe']

def get_ETF_by_index(index):
    _map = {'S&P 500': 'SPY',
            'NASDAQ 100': 'QQQ',
            'DJIA': 'DIA',
            'RUSSELL 2000': 'IWM',
            'OwlHack 2024 Universe': 'SPY',
            'Small Universe': 'SPY',
            'Test Universe': 'SPY'}
    return _map[index]

def get_sector():
    return ['Basic Materials', 'Communication Services', 'Consumer Cyclical',
            'Consumer Defensive', 'Energy', 'Financial', 'Healthcare', 'Industrials',
            'Real Estate', 'Technology', 'Utilities', 'Others']

def get_industry():
    # to be determined
    return []

def get_index_components(index, meta_data_dir):
    fname = os.path.join(meta_data_dir, index.replace(' ', '') + '.txt')
    df = pd.read_csv(fname)
    return(df['Ticker'].tolist())

def parse_date_str(txt):
    try:
        dt = datetime.datetime.strptime(txt, "%Y-%m-%d").date()
    except:
        dt = datetime.datetime.strptime(txt, "%m/%d/%Y").date()
    return(dt)

def calculate_sharpe_ratio(daily_returns, risk_free_rate):
    # Calculate average daily return
    avg_daily_return = np.mean(daily_returns)

    # Calculate daily standard deviation
    daily_std_dev = np.std(daily_returns, ddof=1)

    # Annualized the figures
    annualized_return = (1 + avg_daily_return) ** 252 - 1
    annualized_std_dev = daily_std_dev * np.sqrt(252)

    # Convert annual risk-free rate to daily
    daily_risk_free = (1 + risk_free_rate) ** (1/252) - 1
    annualized_risk_free = (1 + daily_risk_free) ** 252 - 1

    # Calculate Sharpe ratio
    sharpe_ratio = (annualized_return - annualized_risk_free) / annualized_std_dev

    return sharpe_ratio

def calculate_max_drawdown(equity_values):
    """
    Calculate the maximum drawdown of a time series of asset returns.

    :param equity_values: (Pandas Series) Time series of asset returns

    :return: Maximum drawdown of the asset returns in percentage
    """
    # Calculate the running maximum
    running_max = np.maximum.accumulate(equity_values)

    # Calculate drawdowns
    drawdowns = (equity_values - running_max) / running_max

    # Find the maximum drawdown
    max_drawdown = np.min(drawdowns)
    return max_drawdown * 100

# ==============================================
# Testing
# ==============================================
def _test():
    # various unit tests
    equity_values = [100, 110, 105, 95, 100, 90, 100, 110]
    max_dd = calculate_max_drawdown(equity_values)
    print(f"Maximum Drawdown: {max_dd:.2%}")

if __name__ == "__main__":
    import sys
    sys.path.append(os.getcwd())
    _test()
