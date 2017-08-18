from datetime import date
from share_settings import Settings
import pandas as pd
import pandas_datareader.data as wb

s = Settings()

#FTSE100 Share list
symbols = ['AAL',	'ABF',	'ADM',	'AHT',	'ANTO',	'AV',	'AZN',	'BA',
'BAB',	'BARC',	'BATS',	'BDEV',	'BLND',	'BLT',	'BNZL',	'BP',	'BRBY',	
'BT.A',	'CCH',	'CCL',	'CNA',	'CPG',	'CRDA',	'CRH',	'CTEC',	'DCC',	
'DGE',	'DLG',	'EXPN',	'EZJ',	'FRES',	'GFS',	'GKN',	'GLEN',	'GSK',	
'HL',	'HMSO',	'HSBA',	'IAG',	'IHG',	'III',	'IMB',	'INF',	'ITRK',	
'ITV',	'JMAT',	'KGF',	'LAND',	'LGEN',	'LLOY',	'LSE',	'MCRO',	'MDC',	
'MERL',	'MKS',	'MNDI',	'MRW',	'NG',	'NXT',	'OML',	'PPB',	'PRU',	
'PSN',	'PSON',	'RB',	'RBS',	'RDSA',	'RDSB',	'REL',	'RIO',	'RMG',	
'RR',	'RRS',	'RSA',	'RTO',	'SBRY',	'SDR',	'SGE',	'SGRO',	'SHP',	
'SKG',	'SKY',	'SLA',	'SMIN',	'SMT',	'SN',	'SSE',	'STAN',	'STJ',	
'SVT',	'TSCO',	'TUI',	'TW','ULVR','UU','VOD','WOS','WPG','WPP','WTB']

#date range for pandas datatable
st_date = date(2017,1,1)
ed_date = date.today().isoformat()

#creates data frame using share tickers, source, date range
stock_list = [symbols]
df_temp = wb.DataReader(symbols, 'google', st_date, ed_date)

#Select field I want and clean the data removing the unwanted fields
field = 'Close'
cleanData = df_temp.ix[field]
df_close_prices=pd.DataFrame(cleanData)
print(df_close_prices.iloc[0])

#calculates moving average for multiple columns
for stock in symbols:
    tag = (stock + '_MA')
    print(tag)
    df_close_prices[tag] = df_close_prices[stock].rolling(window=5).mean()


print(df_close_prices)
#creates pandas excel writer using xlsxwriter as the engine
writer = pd.ExcelWriter('/users/neald/desktop/share_test.xlsx', engine='xlsxwriter')
df_close_prices.to_excel(writer, sheet_name='Sheet1')
