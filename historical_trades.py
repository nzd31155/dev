import pandas as pd
import numpy as np 
import share_functions as sf
from share_settings import Settings
s= Settings()

"""    Requires 
    Symbols - Stock symbols that form the portfolio
    bars - Dataframe of prices for stocks
    signals - A pandas dataframe of signals for stocks
    initial capital - how much money to start with.
    """

def load_data (s,sf):
    """Loads data from stored file, filters for prices and buys"""
    tag = []
    tag2=[]
    for stock in s.symbols:
        tag.append(stock)
        tag2.append(stock+'BUY')
    df1 = sf.load_from_file()
    bars = df1[tag]
    signals = df1[tag2]
    return bars, signals

def generate_positions(bars, signals,s):
    """calculate purchases of stock"""
    positions = pd.DataFrame(index = signals.index).fillna(0.0)
    for stock in s.symbols:
        pp = np.where(signals[stock+'BUY']==11,s.buy_value/(bars[stock]/100),False)
        positions[stock] = np.floor(pp)
    return positions

def build_portfolio(s,signals,positions):
    """builds the portfolio table"""
    portfolio = pd.DataFrame(index = signals.index).fillna(0)
    for stock in s.symbols:
        portfolio[stock]=bars[stock]
        portfolio[stock+'HOLD']=positions[stock]
        portfolio['cash'] =s.pot - (portfolio[stock]*portfolio[stock+'HOLD']).sum().cumsum()
    print(portfolio)         
    return portfolio
bars, signals = load_data(s,sf)
positions = generate_positions(bars, signals, s)
portfolio = build_portfolio(s,signals,positions)

#save
sf.save_stocks(portfolio,'historical_trades.xlsx')

