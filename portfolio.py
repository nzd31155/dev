"""
This module is about purchasing, holding and selling stocks from get_shares.py
will include the following
will monitor historic/most recent prices and on sell triggers collect sell price, date and calculate profit and store in df.portfolio
will have hold/sell strategies - or point to strategy file which has these?
Can save/export history to excel.abs
""" 
import pandas as pd 
from datetime import date, datetime, timedelta
import share_functions as sf
from portfolio_record import PortfolioRecord
#global variables
p = PortfolioRecord

def run_main():
    #Start with some test data loads portfolio_test file, portfolio_test2 includes 2 stocks
    df_rawdata = sf.load_from_file()  # defaults to share_test.xlsx
    df=create_df(df_rawdata)
    sf.save_stocks(df,'portfolio.xlsx')  #cut this out if using simulation_looper

def build_portfolio(df_rawdata):
    pf_dict = {}
    """load in the stocks from Settings"""
    for stock in sf.s.symbols:        #Later - replace this with s.symbols
        stock_price = stock + "BUY"
        n=0
        for index, row in df_rawdata.iterrows():
            if row[stock_price] == 11.0:
                pfr = p(stock, date.isoformat(index), row[stock],df_rawdata)
                pf_dict[stock+str(n)]= p.create_record(pfr) 
                n+=1
    return pf_dict

def create_df(df_rawdata): 
    """Take pf data and insert into a df, transposes and adds colum titles"""
    pf_dict = build_portfolio(df_rawdata)
    df = pd.DataFrame(pf_dict).transpose().fillna(0)
    df.columns = ['p_date','stock','p_price','n_stocks','is_held','days_held','s_date','s_price','profit','pctgain','sell_type']
    print("bottom sell % =", sf.s.l_trig1, "low trend switch =", sf.s.l_trig2, "EMA switch low = ", sf.s.l_trig3, "Min grow% =", sf.s.min_gain, "H-sell%", sf.s.h_trig1, "Profit =", sum(df.profit),'Success rate =', (sum(n > 0 for n in df.profit)/(sum(n == False for n in df.is_held))), 
    "N  completed sales  =", sum(n == False for n in df.is_held),'n held =', sum(n==True for n in df.is_held))    
    
    #sorts into chonological order
    df = df.sort_values('p_date', ascending = False)
    #returns list of stocks to sell
    try:
        sell = df.loc[df['s_date'] == date.today()]['stock'].values[:]
        if sell == []:
            print('No sells today')
            print('Holds = ', df.loc[df['s_price'] == 0]['stock'].values)    
        else:
            print( "sell the following - ", sell)
            print('Remaining holds = ', df.loc[df['s_date'] == 0]['stock'].values)
    except IndexError:
        print('no df error')

    return df
