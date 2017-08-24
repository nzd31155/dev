import pandas as pd
import numpy as np 
import share_functions as sf
from share_settings import Settings

s= Settings()

tag = []

def load_data (s,sf):
    """Loads data from stored file, filters for prices and buys"""
    for stock in s.symbols:
        tag.append(stock)
        tag.append(stock+'BUY')

    df1 = sf.load_from_file()
    df = df1[tag]
    
    return df

def buybuy (s,df):
    """If buy trigger then buy a stock and add it to list"""
    #down = np.where(df_close_prices[x]>df_close_prices[y], np.where(df_close_prices[y]>df_close_prices[z],1,False),False)
    for stock in s.symbols:
        df[stock+'nHELD']=0
        #Number of stocks bought
        nh = np.where(df[stock+'nHELD'].shift(1)>0,df[stock+'nHELD'].shift(1),(np.where(df[stock+'BUY']==11,1000/(df[stock]/100),False)))

        #Populates the *nHELD field with numb shares
        #df[stock+'nHELD'] = np.floor(nh)
        df[stock+'nHELD'] = nh
        
        #Populates the *pp field with purchase price
        pp = np.where(df[stock+'BUY']==11,df[stock],False)
        df[stock+'PP'] = pp

        df[stock+'test'] = 0
        df[stock+'test'] = 0
        df[stock+'test'][df[stock+'nHELD'].shift(1)>0] = 1
        
        
def sell(s,df):
    """Calculates a sale price"""
    #needs purchase price, number held, sell trigger to calculate the sale

df = load_data(s,sf)
buybuy(s,df)
sf.save_stocks(df,'historical_trades.xlsx')

print(df)