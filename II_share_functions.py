from share_settings import Settings
import pandas_datareader.data as pdr

s = Settings()

def get_bars(s):
    """Downloads the stocks and drops into panel"""
    #Gets shares from Google stores in panel - bars
    bars = pdr.DataReader(s.symbols,'google',s.st_date,s.ed_date)
    return bars

def get_tickers(symbol,bars):
    """Gets the required df using stock"""
    #prints the data per stock
    '''
    for symbol in bars.minor_axis:
        print(symbol)
        print(bars.minor_xs (symbol))
        #shows all panels
        #print(symbol)
        #print(bars.minor_xs (symbol))
    '''
    return(bars.minor_xs (symbol))

bars = get_bars(s)
get_tickers('ADM',bars)