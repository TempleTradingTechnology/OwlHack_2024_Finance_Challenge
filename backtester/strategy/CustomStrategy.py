# CustomStrategy.py
import common as cm
from strategy import Strategy
from datamatrix import DataMatrix, DataMatrixLoader

class CustomStrategy(Strategy):
    '''
		Write your custom trading strategy below
    '''
    def __init__(self,
	    pref,
	    input_datamatrix: DataMatrix,
	    initial_capital: float,
	    price_choice = cm.DataField.close):

        super().__init__(pref, self.__name__, input_datamatrix, initial_capital, price_choice)
        # You can add more arguments if you feel like your code needs it but the given template is the minimal working
        # code

    def validate(self):
        '''
	      Validate to see if your input has everything your strategy need
        '''
        # validation code goes here

    def run_model(self, model = None):
        '''
        Run the strategy.
        Your strategy would need to return the three variation below.
            tsignal: a panda dataframe with column as being the stock Ticker and the row as the Date
            taction: a panda dataframe with column as being the stock Ticker and the row as the Date
            shares: a panda dataframe with column as being the stock Ticker and the row as the Date
        '''

        taction = self.pricing_matrix.copy()
        tsignal = self.pricing_matrix.copy()

        # shares on trade execution
        shares = self.pricing_matrix.copy()

        # strategy code goes here #

        return(tsignal, taction, shares)