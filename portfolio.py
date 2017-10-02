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
from share_settings import Settings
from portfolio_record import PortfolioRecord
import pprint as pprint
#global variables
s = Settings()
p = PortfolioRecord

#Start with some test data loads portfolio_test file, portfolio_test2 includes 2 stocks
df_rawdata = sf.load_from_file('portfolio_test2.xlsx')
#print(df[20:30])

def build_portfolio():
    pf_dict = {}
    """load in the stocks from Settings"""
    for stock in s.symbols2:        #Later - replace this with s.symbols
        stock_price = stock + "BUY"
        n=0
        for index, row in df_rawdata.iterrows():
            if row[stock_price] == 11.0:
                pfr = p(stock, date.isoformat(index), row[stock],df_rawdata)
                pf_dict[stock+str(n)]= p.create_record(pfr) 
                n+=1
    return pf_dict

def create_df(): 
    """Take pf data and insert into a df, transposes and adds colum titles"""
    pf_dict = build_portfolio()
    df = pd.DataFrame(pf_dict).transpose().fillna(0)
    df.columns = ['p_date','stock','p_price','n_stocks','is_held','days_held','s_date','s_price','profit','pctgain']
    #sorts into chonological order
    df = df.sort_values('p_date')
    return df

df=create_df()
#if long sell - calculate sell price
#if low_sell - calculate sell price
#if high_sell - calculate sell price
#if none of these - what's current value

'''
for index, row in df.iterrows():
    dateid = datetime.strptime(row['p_date'],'%Y-%m-%d').date()
    #print(dateid)
    dateid2 = dateid + timedelta(days = s.max_days_held)
    
    #iterate until we find the next date after s.max threshold days
    while dateid2 not in df_rawdata.index:
        dateid2 += timedelta(days =1)
    else:

        row['s_date'] = dateid2
        df.loc[index,['s_date']] = dateid2
        sp = df_rawdata.loc[dateid2,row['stock']]
        df.loc[index,['s_price']] = sp
        pre = row['n_stocks']*row['p_price']
        pos = row['n_stocks']*sp
        df.loc[index,['profit']] = (pos-pre)/100
        df.loc[index,['pctgain']] = round(((pos/pre)-1)*100,1)
'''
print(df)