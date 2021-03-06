from share_settings import Settings
import latest_prices as lp
import pandas as pd
import pandas_datareader.data as wb
import numpy as np 
import portfolio as p
import simulation_looper as sim  
import datetime, requests
from io import StringIO
from pandas.io.common import urlencode

s = Settings()
df_close_prices = 0

def options(df_close_prices):
    """Startup options"""
    while True:
        #print options
        try:
            print("\n\nSelect from one of the following options...\n"
            "1. load/download historical stocks\n"
            "2. View data\n"
            "3. See/Change settings\n"
            "4. Plot stock calcs\n"
            "5. List watch/buy stocks\n"
            "6. List sells and calc portfolio \n"            
            "7. Run portfolio simulation\n"
            "8. Quit\n"
            )
            
            selection = 0
            while selection not in (range(1,9)):
                selection = int(input("type a number from 1-8\n> "))
        except (ValueError, NameError, SyntaxError):
            print("Type a number from 1-8\n> ")
        
        #once entry is acceptible, run the option
        else:
            if selection == 1: 
                df_close_prices = dl_or_load()
            elif selection == 2: 
                print(df_close_prices)
            elif selection == 3: 
                change_settings(s)   
            elif selection == 4: 
                plot_stock(df_close_prices)
            elif selection == 5:
                rec_stocks(s,df_close_prices)
            elif selection == 6:
                p.run_main()
            elif selection == 7:
                sim.looper()
            elif selection == 8:
                break


def dl_stocks(s,start_d,end_d):
    """Downloads stock prices from google"""
    #creates data frame using share tickers, source, date range
    print('Downloading stocks since -',s.st_date)
    stock_list = [s.symbols]
    df_temp = wb.DataReader(s.symbols, 'google', start_d, end_d)
    return df_temp

def dl_stocks_temp(s,start_d, end_d):
    """ temp fix for when google.finance API down  this plays instead of dl_stocks above"""
    BASE = 'http://finance.google.com/finance/historical'
    df_close_prices = pd.DataFrame()

            
    def build_url(symbol, start, end):
        params = {
        'q': symbol,
        'startdate': start,
        'enddate': end,
        'output': "csv"
        }
        return BASE + '?' + urlencode(params)

    for stock in s.symbols:
        url = build_url(stock, start_d, end_d)
        #print(url)
        data = requests.get(url).text
        data = pd.read_csv(StringIO(data), index_col='Date', parse_dates=True)
        #filters for 'close'
        df_close_prices[stock] = data['Close']
    #print(df_close_prices)
    return df_close_prices

def clean_stocks(field, df_temp):
    """ selects specific 'fields' and stores all stocks in single df"""
    #Select field I want and clean the data removing the unwanted fields
    print('Cleaning stocks')
    cleanData = df_temp.ix[field]
#    cleanData = df_temp.loc[:,[field]]  when ix is depreciated
    df_close_prices=pd.DataFrame(cleanData)
    for stock in s.symbols:
        df_close_prices[stock].fillna((df_close_prices[stock].mean()),inplace=True) #gets stocks and fills gaps with mean.
    return df_close_prices

def get_latest_prices(df_close_prices,s):
    """downloads todays latest prices - use before close"""
    print('Downloading latest prices')
    df_close_prices.ix[s.date_now]=lp.get_lp(s)
#   df_close_prices.loc[[s.date_now],:]=lp.get_lp(s) when iX is depreciated

def calc_columns(s,df_close_prices):
    """Calculates triggers"""
    print('Searching for stocks to watch/buy')
    df_close_prices = df_close_prices.sort_index(axis=0, ascending=True)
    for stock in s.symbols:    
        print('\t' + stock)
        x = (stock +'_EMA_' +str(s.EMA_Sho))
        y = (stock +'_EMA_' +str(s.EMA_Mid))
        z = (stock +'_EMA_' +str(s.EMA_Lon))
        tagu = (stock + 'TrigU')
        tagd = (stock + 'TrigD')
        tagb = (stock + 'BUY')
        tagm = (stock + 'MACD')
        ema_values = s.EMA_values
        
        #calc EMAs
        for ema_value in ema_values:
            tage = (stock + '_EMA_' +str(ema_value))
            df_close_prices[tage] = df_close_prices[stock].ewm(span=ema_value, min_periods=ema_value, adjust=False).mean()
        #calc MACD
        macd = ((df_close_prices[z]-df_close_prices[x])/df_close_prices[stock])*100
        df_close_prices[tagm] = macd
        
        #Calculating the triggers
        up = np.where(df_close_prices[x]>df_close_prices[y], np.where(df_close_prices[y]>df_close_prices[z],10,False),False)
        down = np.where(df_close_prices[x]<df_close_prices[y], np.where(df_close_prices[y]<df_close_prices[z],1,False),False)
        df_close_prices[tagd] = down
        df_close_prices[tagu] = up
        
        #adding recommend tag
        x = df_close_prices[tagu] +  df_close_prices[tagd].shift(s.ts)
        df_close_prices[tagb] = x

    return df_close_prices

def rec_stocks(s,df_close_prices):
    """Calculates watch/buy stocks only works if last date is today"""
    watch = []
    nearly = []
    buy = []
    for stock in s.symbols:
        tag = (stock + 'BUY')
        u_tag = (stock + 'TrigU')
        d_tag = (stock + 'TrigD')
        m_tag = (stock + 'MACD')
        
        #Calculates Reco dict for today
        up = df_close_prices.ix[-1,u_tag]
        down = df_close_prices.ix[-2,d_tag]
        down2 = df_close_prices.ix[-1,d_tag]
        macd = df_close_prices.ix[-1,m_tag]
        macd2 = df_close_prices.ix[-2,m_tag]
        y = up + down 
        #Watch are if EMAs are in correct order going down
        if down == 1.0 and macd<4:
            watch.append(stock)
            #Nearly if Watch is true, MACD < 0% and < yesterday
            if down2 == 0 and macd<0 and macd2>macd:
                    nearly.append(stock)
        #Buy if down and up triggers are both true
        if y ==11.0:
            buy.append(stock)
        else:
            continue            
    print("\nToday's stocks to watch and buy are as follows....")
    print('Watch = ',watch)
    print('Nearly = ',nearly)
    print('Buy = ',buy)

def save_stocks(df_close_prices,filename):
    """Saves data to excel usng xlsxwriter as the engine"""
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    df_close_prices.to_excel(writer, sheet_name='Sheet1')
    print('File saved')

def save_MACD(df_close_prices):
    """Saves data to MACD excel file xlsxwriter as the engine"""
    path = '/Users/neald/Dropbox/'
    filename = 'downloadprices.xlsx'
    writer = pd.ExcelWriter(path+filename, engine='xlsxwriter')
    df = df_close_prices.sort_index(ascending=False)
    df.to_excel(writer, sheet_name='Prices', startrow=1)
    writer.save()
    print('MACD_prices saved')

def get_stocks(s):
    """embeds >1 functn to download, format and save"""
    #download stocks
    df_close_prices = dl_stocks_temp(s,s.st_date,s.ed_date)
    #Limit to just close prices in single DF
    #df_close_prices = clean_stocks('Close',df_temp)
    #add in todays pricing
    df_close_prices.ix[s.date_now]=lp.get_lp(s)
    #saves to file
    save_MACD(df_close_prices)
    #Calculates EMAs, triggers and watch/buy figures
    df_close_prices = calc_columns(s,df_close_prices)
    #save copy to Excel
    save_stocks(df_close_prices,'share_test.xlsx')
    print('Completed')
    return df_close_prices

def load_from_file(xlsx_file='share_test.xlsx'):
    """Load data from file"""
    data = pd.ExcelFile(xlsx_file, parse_dates = True, index_col=0)
    df_close_prices = data.parse('Sheet1')
    df_close_prices.set_index('Date', inplace = True)
    return df_close_prices

def dl_or_load():
    """Select to download or load previously saved stock data"""
    while True:
        try:
            print('\nDo you want to' 
            '\n1. Load last used data'  
            '\n2. Download new data')
            dls = 0
            while dls not in (range(1,3)):
                dls = int(input('> '))
        except (ValueError, NameError, SyntaxError):
            print("Select '1' or '2'\n>")
        else:
            if dls ==1:
                print('Loading dataframe from file')
                df_close_prices = load_from_file()
                return df_close_prices
                break
            elif dls ==2:
                print('Downloading latest prices to dataframe')
                df_close_prices = get_stocks(s)
                return df_close_prices
                break          

def chart_filtering(stock, df_close_prices):
    """For a selected stock, filter columns for plotting"""
    #Shows list of all columns
    #stock_col = [col for col in df_close_prices.columns if stock in col]
    # print(list(df_close_prices.columns))
    #Returns list of selected columns
    #print(stock_col)

    #This filters out columns to just the EMA and pricing cols
    stk = stock + '_'
    df_filtered = df_close_prices.filter(regex=(stk))
    return (df_filtered)

def plot_stock(df_close_prices):
    """Plot chart for selected stocks"""
    #name the stock
    print (s.symbols)
    stock = input('Enter stock ticker to plot  >').upper()
    
    #get stock and calcs
    df_filtered = chart_filtering(stock,df_close_prices)

    #now make the plot
    from bokeh.charts import TimeSeries
    from bokeh.io import output_file, show
    ts = TimeSeries(df_filtered, x='index')
    show(ts)

def change_settings(s):
    """view hard-coded program settings"""
    print ("\nEMA settings")
    print('\tEMA_short = ' + str(s.EMA_Sho))
    print('\tEMA_mid = ' + str(s.EMA_Mid))
    print('\tEMA_long = ' + str(s.EMA_Lon))
    print("\nDate settings")
    print('\tStart date = ',s.st_date)
    print('\tEnd date = ',s.ed_date)
    print("\nStocks included")
    print('\tStocks = ',s.symbols)
    
