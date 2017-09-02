"""

Script contains functions for interacting with the Google finance API, makes use of the googlefinance.client
Information on the package can be found here https://pypi.python.org/pypi/googlefinance.client/1.3.0
*Supersedes latest_prices.py*

"""

__author__ = 'Neal Dunkinson, Joe Mullen'
__version__ = '0.1'


from googlefinance.client import get_prices_data
from datetime import datetime
import joe.config as _cfg


def today_date():
    """
    Returns today's date.
    
    :return: 
    """
    return datetime.now().strftime('%Y-%m-01')


def get_today_close():
    """
    
    Method gets close data for all stocks in the FTSE.
    Returns a simple dictionary { STOCK_SYM : CLOSE }
    
    :return: 
    """

    today_close= {}
    todays_date = today_date()

    for stock in _cfg.STOCKS:
            param = [{
                'q': stock,  # Stock symbol (ex: "AAPL")
                'x': "LON"  # Stock exchange symbol on which stock is traded (ex: "NASD")
            }]
            df = get_prices_data(param, _cfg.PERIOD)
            df.reset_index(level=0, inplace=True)
            for index, row in df.iterrows():
                if str(row['index']) == str(todays_date):
                    today_close[stock] = row[stock + '_Close']

    return today_close


def get_three_months():
    """
    Function enables the extraction of three months of data, required when first populating the database.
    
    :return: 
    """


print(get_today_close())
