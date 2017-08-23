from share_settings import Settings
import latest_prices as lp
import pandas as pd
import pandas_datareader.data as wb
import numpy as np 

#this is a test line

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
            "6. Quit\n"
            )
            
            selection = 0
            while selection not in (range(1,7)):
                selection = int(input("type a number from 1-6\n> "))
        except (ValueError, NameError, SyntaxError):
            print("Type a number from 1-6\n> ")
        
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
                break


def dl_stocks(s,start_d,end_d):
    """Downloads stock prices from google"""
    #creates data frame using share tickers, source, date range
    print('Downloading stocks')
    stock_list = [s.symbols]
    df_temp = wb.DataReader(s.symbols, 'google', start_d, end_d)
    return df_temp

def clean_stocks(field, df_temp):
    """ selects specific 'fields' and stores all stocks in single df"""
    #Select field I want and clean the data removing the unwanted fields
    print('Cleaning stocks')
    cleanData = df_temp.ix[field]
    df_close_prices=pd.DataFrame(cleanData)
    return df_close_prices

def get_latest_prices(df_close_prices,s):
    """downloads todays latest prices - use before close"""
    print('Downloading todays current prices')
    df_close_prices.ix[s.date_now]=lp.get_lp(s)

def calc_ema(s,df_close_prices):
    """ Calculates EMA for stocks"""
    ema_values = s.EMA_values
    for ema_value in ema_values:
        print('Calculating EMA value = ' +str(ema_value)) 
        for stock in s.symbols:
            tag = (stock + '_EMA_' +str(ema_value))
            df_close_prices[tag] = df_close_prices[stock].ewm(span=ema_value, min_periods=ema_value, adjust=False).mean()
        
def EMA_trigger(s,df_close_prices):
    """Calculates triggers"""
    print('Calculating up/down triggers and adds to df')
    for stock in s.symbols:    
        x = (stock +'_EMA_' +str(s.EMA_Sho))
        y = (stock +'_EMA_' +str(s.EMA_Mid))
        z = (stock +'_EMA_' +str(s.EMA_Lon))
        tagd = (stock + 'TrigD')
        tagu = (stock + 'TrigU')

        #Calculating the triggers
        down = np.where(df_close_prices[x]>df_close_prices[y], np.where(df_close_prices[y]>df_close_prices[z],1,False),False)
        up = np.where(df_close_prices[x]<df_close_prices[y], np.where(df_close_prices[y]<df_close_prices[z],10,False),False)
        
        #adding to the dataframe
        df_close_prices[tagd] = down
        df_close_prices[tagu] = up
        

def buy_stock(s,df_close_prices):
    """Buy stocks that meet this criteria"""
    print("Searching for a day's winners")
    for stock in s.symbols:
        tag = (stock + 'BUY')
        u_tag = (stock + 'TrigU')
        d_tag = (stock + 'TrigD')
        #Calculates Reco column for df
        x = df_close_prices[u_tag] +  df_close_prices[d_tag].shift(s.ts)
        df_close_prices[tag] = x

def rec_stocks(s,df_close_prices):
    """Calculates watch/buy stocks"""
    reco_stocks = {}
    watch = []
    buy = []
    for stock in s.symbols:
        tag = (stock + 'BUY')
        u_tag = (stock + 'TrigU')
        d_tag = (stock + 'TrigD')
        #Calculates Reco dict for today
        up = df_close_prices.loc[s.date_now,u_tag]
        down = df_close_prices.loc[(s.date_yst),d_tag]
        y = up + down 
        reco_stocks[stock]= y
    
        for key, value in reco_stocks.items():
            if value == 10:
                watch.append(key)
            elif value == 11:
                buy.append(key)
            else:
                break
    #print(reco_stocks)
    print("\nToday's stocks to watch and buy are as follows....")
    print('Watch = ',watch)
    print('Buy = ',buy)

def save_stocks(df_close_prices,filename):
    """Saves data to excel usng xlsxwriter as the engine"""
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    df_close_prices.to_excel(writer, sheet_name='Sheet1')
    print('File saved')


def get_stocks(s):
    """embeds >1 functn to download, format and save"""
    #download stocks
    df_temp = dl_stocks(s,s.st_date,s.ed_date)
    #Limit to just close prices in single DF
    df_close_prices = clean_stocks('Close',df_temp)
    #add in todays pricing
    df_close_prices.ix[s.date_now]=lp.get_lp(s)
    #calculate the 3 EMAs
    calc_ema(s,df_close_prices)
    #Calculates triggers
    EMA_trigger(s,df_close_prices)
    #Identifies the stocks to buy
    buy_stock(s,df_close_prices)
    #save copy to Excel
    save_stocks(df_close_prices,'share_test.xlsx')
    print('Completed')
    return df_close_prices

def load_from_file():
    """Load data from file"""
    data = pd.ExcelFile('share_test.xlsx', parse_dates = True, index_col=0)
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
    
