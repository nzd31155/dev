from share_settings import Settings
from datetime import date, datetime, timedelta
s = Settings()

class PortfolioRecord():
    """This class defines a single portfolio record"""
    def __init__(self,stock,p_date,p_price,df):
        """initialising the portfolio record"""
        self.p_date = p_date
        self.p_price= p_price
        self.stock = stock
        self.s_date = None
        self.s_price = None
        self.is_held = True
        self.profit = None
        self.pctgain = None

        """calculates how long stock held for"""
        self.p_date = datetime.strptime(self.p_date,'%Y-%m-%d').date()
        self.days_held = (date.today()-self.p_date).days
        """calculates stock price using settings value and stock price"""
        #checking if enough money in pot
        self.n_stocks = int(s.buy_value/(p_price/100))
        
        def add_sales_data(self, df):
            """Insert sales data"""
            #Conditional for if long sell
            dateid = self.p_date + timedelta(days = s.max_days_held)
            if dateid < (s.date_now.date()):
                long_trigger(self,dateid,df)
            #add conditional for low sell
            elif self.p_price > 1:
                low_trigger(self,df)    
            #add conditional for high sell
            else:
                print('Fails current conditionals')
            
            #calc sell fields.
            pre = self.n_stocks * self.p_price
            pos = self.n_stocks * self.s_price
            self.profit = (pos-pre)/100
            self.pctgain = round(((pos/pre)-1)*100,1)
                
        def long_trigger(self,dateid,df):
            """Defines the trigger if stock held too long"""
            #iterate until we find the next date after s.max threshold days
            print('long_trigger active')
            while dateid not in df.index:
                dateid += timedelta(days =1)
            else:
                self.s_price =(df.loc[dateid,[self.stock]].values[0])
                self.s_date = dateid
                self.is_held = False
            
        def low_trigger(self,df):
            
            #stuck on here, trying to loop through days between purchase date and max held days.
            #if stockprice is < EMALO*.94 then sell
            #maybe iterate through the Low_sell while loop?
            """defines a trigger for if stock drops too much"""
            print('Low_trigger active')
            print(self.stock, self.p_price)
            temp = (stock +'_EMA_' +str(s.EMA_Lon))
            temp_date = self.p_date
            print(temp_date)
            iter_price = (df.loc[temp_date,[temp]].values[0]) 
            print(self.p_price, iter_price)

            while self.p_price > iter_price*(1-(s.low_sell_pct/100)) :
                while temp_date not in df.index:
                    temp_date += timedelta(days =1)
                    print(temp_date)
                    if temp_date == date.today():
                        print('boom')
                        
                    else:
                        iter_price = (df.loc[temp_date,[temp]].values[0])
                        print(iter_price)
                        
                
            #print(df.ix[-1,[temp]].values[0])
        add_sales_data(self, df)

    
        
    def create_record(self):
        """builds the tuple for the df, check order matehces column list"""
        tp = (self.p_date, self.stock, self.p_price, self.n_stocks, self.is_held, self.days_held, 
        self.s_date, self.s_price, self.profit, self.pctgain)
        return tp 