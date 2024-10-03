'''
Main script to run the backtester
'''

# import native libraries
import os
import sys

# append the lib directory to the path
os.environ["ROOT_DATA_DIR"] = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir ,'data'))
os.environ["ROOT_DIR"] = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.environ["ROOT_DIR"], "lib"))
sys.path.append(os.path.join(os.environ["ROOT_DIR"], "strategy"))

# import the internal libraries
import preference
import common as cm
import backtester

# import YOUR strategies here
from RSI_strategy import RSIStrategy
from random_strategy import RandomStrategy

def create_strategy_list(pref, datamatrix_loader):
    result = []

    dm = datamatrix_loader.get_daily_datamatrix()

    rsi = RSIStrategy(pref, dm, pref.initial_capital)
    result.append(rsi)

    random = RandomStrategy(pref, dm, pref.initial_capital, lower_bound = 0.1, upper_bound = 0.9)
    result.append(random)

    return (result)

def run():

    parser = preference.get_default_parser()
    parser.add_argument('--universe_name',   dest='universe_name', default = 'OwlHack 2024 Universe', help='Name of the Universe')
    parser.add_argument('--initial_capital', dest='initial_capital', default = cm.OneMillion, help='Initial Capital')
    parser.add_argument('--random_seed', dest='random_seed', default = None, type = int, help='Random Seed')

    args = parser.parse_args()
    pref = preference.Preference(cli_args = args)

    if pref.output_dir is None:
        pref.output_dir = pref.test_output_dir

    driver = backtester.Driver(pref)

    # first run the bechnmark ETF first
    driver.run_benchmark()

    # create the list of strategies that we want to back-test
    strategy_list = create_strategy_list(pref, driver.datamatrix_loader)

    driver.run(strategy_list)
    driver.summary()

if __name__ == "__main__":
    run()
