'''
Class to model user preferences
'''
import os
import sys
import getpass
import argparse
import warnings
import pandas as pd

import common as cm


warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action="ignore", category=pd.errors.PerformanceWarning)




class Preference(object):

    '''
    Storing user preference as attribute.
    '''

    _file_dir = os.path.dirname(os.path.realpath(__file__))

    if os.getenv("ROOT_DATA_DIR") is not None:
        _data_root = os.environ["ROOT_DATA_DIR"]
    else:
        _data_root = os.path.abspath(os.path.join(os.pardir, os.pardir ,'data'))

    # root directory for storing various unit and integration tests
    _test_root = os.path.join(_data_root ,'test')
    _default_option = { 'environ': 'dev', 'verbose': False,
                        'start_date': None, 'end_date': None,
                        'data_root_dir': _data_root,
                        'train_data_dir': os.path.join(_data_root, 'train'),
                        'test_data_dir': os.path.join(_data_root, 'test'),
                        'meta_data_dir': os.path.join(_data_root, 'meta'),
                        'test_input_dir': os.path.join(_test_root, 'output'),
                        'test_output_dir': os.path.join(os.environ["ROOT_DIR"], os.pardir, 'output'),
                        'tickers': None, 'port_name': None,
                        'random_seed': None,
                        'risk_free_rate': 0.0,
                    }

    def __init__(self, name = None, user = None, cli_args = None):

        self.name = name
        self.user = user

        # set defaults
        for k, v in Preference._default_option.items():
            setattr(self, k, v)

        # set from CLI
        if cli_args is not None:
            for k, v in vars(cli_args).items():
                setattr(self, k, v)

        if self.name is None:
            self.name = 'standard'

        if self.user is None:
            self.user = getpass.getuser()

        # convert str to date object
        if self.start_date is not None:
            self.start_date = cm.parse_date_str(self.start_date)
        if self.end_date is not None:
            self.end_date = cm.parse_date_str(self.end_date)


    def describe(self, format_or_not = False):
        '''
        Return a well-for
        '''
        txt = ''

        return( txt if format_or_not else vars(pref))


def get_default_parser():
    #
    parser = argparse.ArgumentParser()
    parser.add_argument('--environ', dest='environ', default='dev', help='runtime environment')
    parser.add_argument('--verbose', action='store_true', dest='verbose', default=False, help='verbose')
    parser.add_argument('--user', dest='user', default=None, help='user name')

    parser.add_argument('--start_date', dest='start_date', default="2001-01-01", help='start date (YYYY-MM-DD)')
    parser.add_argument('--end_date', dest='end_date', default="2020-01-01", help='end date (YYYY-MM-DD)')
    parser.add_argument('--risk_free_rate', dest='risk_free_rate', default=0.0, type =float, help='Risk Free Rate')

    parser.add_argument('--tickers', dest='tickers', default=None, help='Tickers with | separator')

    parser.add_argument('--data_dir', dest = 'data_dir', default=None, help='data dir')
    parser.add_argument('--output_dir', dest = 'output_dir', default=None, help='output dir')

    return(parser)

# ==============================================
# Testing
# ==============================================
def _test():
    # test default
    pref = Preference()
    pprint(vars(pref))

    pref = Preference(name = "yahoo application",  user = "John Doe")
    pprint(vars(pref))

    parser = get_default_parser()
    parser.add_argument('--foo', dest='foo', default = 'whatever', help='a parameter')
    parser.add_argument('--apikey', dest='api_key_file', help='a parameter')
    args = parser.parse_args()

    pref = Preference(name = "from cli", cli_args = args)
    pprint(vars(pref))

if __name__ == "__main__":
    import sys
    from pprint import pprint
    sys.path.append(os.getcwd())
    _test()
