from share_settings import Settings
import pandas as pd
import pandas_datareader.data as wb
import numpy as np 

#this is a test line

s = Settings()

def options(df_close_prices):
    """Startup options"""
    while True:
        #print options
        try:
            print("\n\nSelect from one of the following options...\n"
            "1. See/Change settings\n"
            "2. Plot stock calcs\n"
            "3. TBC\n"
            "4. TBC\n"
            "5. Quit\n"
            )
            #locks to selection of 0-5
            selection = 0
            while selection not in (range(1,6)):
                selection = int(input("type a number from 1-5\n> "))
        except (ValueError, NameError, SyntaxError):
            print("Type a number from 1-5\n> ")
        
        #once entry is acceptible, run the option
        else:
            if selection == 1: #see/change settings
                change_settings(s)
            elif selection == 2: #plot selected stock
                plot_stock(df_close_prices)   
            elif selection == 3: 
                options(df_close_prices)
            elif selection == 4: 
                options(df_close_prices)
            elif selection == 5:
                break


def get_stock_prices(s):
    """Downloads stock prices from google"""
    #creates data frame using share tickers, source, date range
    print('Downloading stocks')
    stock_list = [s.symbols]
    df_temp = wb.DataReader(s.symbols, 'google', s.st_date, s.ed_date)
    return df_temp

def clean_stocks(s, df_temp):
    """ removes unwanted fields and stores all stocks in single df"""
    #Select field I want and clean the data removing the unwanted fields
    print('Cleaning stocks')
    field = 'Close'
    cleanData = df_temp.ix[field]
    df_close_prices=pd.DataFrame(cleanData)
    #print(df_close_prices.iloc[0])
    return df_close_prices

'''
def calc_ma(s,df_close_prices):
    """ calculates MA for Stocks """
    ma_values = s.MA_values
    for ma_value in ma_values:
        print('\nCalculating MA value = ' +str(ma_value))
        for stock in s.symbols:
            tag = (stock + '_MA_' + str(ma_value))
            #print(tag)
            df_close_prices[tag] = df_close_prices[stock].rolling(window=ma_value).mean()
    print('\n\n')
'''

def calc_ema(s,df_close_prices):
    """ Calculates EMA for stocks"""
    ema_values = s.EMA_values
    for ema_value in ema_values:
        print('\nCalculating EMA value = ' +str(ema_value)) 
        for stock in s.symbols:
            tag = (stock + '_EMA_' +str(ema_value))
            print(tag)
            df_close_prices[tag] = df_close_prices[stock].ewm(span=ema_value, min_periods=ema_value, adjust=False).mean()
        

def save_stocks(df_close_prices):
    """Saves data to excel usng xlsxwriter as the engine"""
    writer = pd.ExcelWriter('/users/neald/desktop/share_test.xlsx', engine='xlsxwriter')
    df_close_prices.to_excel(writer, sheet_name='Sheet1')

def stock_calcs(stock, df_close_prices):
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
    df_filtered = stock_calcs(stock,df_close_prices)

    #now make the plot
    from bokeh.charts import TimeSeries
    from bokeh.io import output_file, show
    ts = TimeSeries(df_filtered, x='index')
    show(ts)


def EMA_dw_trigger(s,df_close_prices):
    """downward trigger"""
    for stock in s.symbols:    
        x = (stock +'_EMA_' +str(s.EMA_Sho))
        y = (stock +'_EMA_' +str(s.EMA_Mid))
        z = (stock +'_EMA_' +str(s.EMA_Lon))
        tag = (stock + 'TrigD')
        df_close_prices[tag] = np.where(df_close_prices[x]<df_close_prices[y], np.where(df_close_prices[y]<df_close_prices[z],True,False),False)
        
def EMA_up_trigger(s,df_close_prices):
    """recovery trigger"""
    for stock in s.symbols:    
        x = (stock +'_EMA_' +str(s.EMA_Sho))
        y = (stock +'_EMA_' +str(s.EMA_Mid))
        z = (stock +'_EMA_' +str(s.EMA_Lon))
        tag = (stock + 'TrigU')
        df_close_prices[tag] = np.where(df_close_prices[x]>df_close_prices[y], np.where(df_close_prices[y]>df_close_prices[z],True,False),False)
        print(df_close_prices)

def get_stocks(s):
    """embeds >1 functn to get and format stocks"""
    #download stocks
    df_temp = get_stock_prices(s)
    #Limit to just close prices in single DF
    df_close_prices = clean_stocks(s, df_temp)
    #calc_ma(s,df_close_prices)  don't need these any more as can directly calculate EMA
    #calculate the 3 EMAs
    calc_ema(s,df_close_prices)
    #Calculates triggers
    EMA_dw_trigger(s,df_close_prices)
    EMA_up_trigger(s,df_close_prices)
    #save copy to Excel
    save_stocks(df_close_prices)
    return df_close_prices

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
    
