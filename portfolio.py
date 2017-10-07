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
#from share_settings import Settings
from portfolio_record import PortfolioRecord
#global variables
#s = Settings()
p = PortfolioRecord

def run_main():
    #Start with some test data loads portfolio_test file, portfolio_test2 includes 2 stocks
    df_rawdata = sf.load_from_file()  # defaults to share_test.xlsx
    #print(df[20:30])
    df=create_df(df_rawdata)
    #sf.save_stocks(df,'portfolio.xlsx')  #cut this out if using simulation_looper

def build_portfolio(df_rawdata):
    pf_dict = {}
    """load in the stocks from Settings"""
    for stock in sf.s.symbols2:        #Later - replace this with s.symbols
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
    df.columns = ['p_date','stock','p_price','n_stocks','is_held','days_held','s_date','s_price','profit','pctgain','s_type']
    #sorts into chonological order
    df = df.sort_values('p_date')
    print("Low sell % =", sf.s.l_trig1, "EMA_l switch =", sf.s.l_trig2, "Min grow% =", sf.s.min_gain, "Profit =", sum(df.profit),
    'Success rate =', (sum(n > 0 for n in df.profit)/len(df.profit)), "N  completed sales  =", sum(n == False for n in df.is_held),
    'n held =', sum(n==True for n in df.is_held))
    return df
