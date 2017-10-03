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
        self.s_type = None

        """calculates how long stock held for"""
        self.p_date = datetime.strptime(self.p_date,'%Y-%m-%d').date()
        self.days_held = (date.today()-self.p_date).days
        """calculates stock price using settings value and stock price"""
        #checking if enough money in pot
        self.n_stocks = int(s.buy_value/(p_price/100))

        def fill_sale_data(self,iter_price, iter_date):
            """On trigger, add in sales data"""
            self.s_price = iter_price
            self.s_date = iter_date
            self.days_held = self.p_date-self.s_date
            pre = self.n_stocks * self.p_price
            pos = self.n_stocks * self.s_price
            self.profit = (pos-pre)/100
            self.pctgain = round(((pos/pre)-1)*100,1)
            self.is_held = False

        def triggers(self, df):
            """iterates through the triggers"""
            lon_s_date = self.p_date + timedelta(days = s.max_days_held)
            iter_date = self.p_date
            
            #iterate through the days before selling on long_trigger
            while iter_date <= lon_s_date:
                #print('loop', iter_date, self.stock, self.p_date)
                while iter_date not in df.index:
                    #print('loop not in df')
                    iter_date += timedelta(days = 1)                 #skips weekends/bankholidays
                label_s = self.stock + "_EMA_" + str(s.EMA_Lon)
                label_l = self.stock + "_EMA_" + str(s.EMA_Sho) 
                ema_s = df.loc[iter_date,[label_s]].values[0]
                ema_l = df.loc[iter_date,[label_l]].values[0]
                
                #low sell
                iter_price = df.loc[iter_date,[self.stock]].values[0]
                if iter_price < (ema_l*(1-(s.low_sell_pct/100))):
                    #print('lowsell')
                    self.s_type = 'low_sell'
                    fill_sale_data(self, iter_price, iter_date)
                    break

                #high sell
                #if min gain on stock is at least > s.min_gain
                elif max(df.loc[self.p_date:iter_date,[self.stock]].values[0])> self.p_price * (1+(s.min_gain/100)):
                    #EMA switch trigger 
                """ this line doesn't work below"""
                    print(self.stock, ema_l, ema_s)
                    if ema_l > ema_s:
                        #print('high_sell')
                        self.s_type = 'high_sell'
                        fill_sale_data(self, iter_price, iter_date)
                    break     

                #iterate back through the loop    
                elif iter_date < df.index.max().date():
                    #print('iter_date loopback')
                    iter_date += timedelta(days = 1)  
                else:
                    #print('stock_held')
                    #print('stock =', self.stock, 'p_date =', self.p_date, 'iter date =', iter_date, 'long_date =',lon_s_date)
                    break
                    
            #Long sell
            else:
                #print('long sell')
                fill_sale_data(self, iter_price, iter_date)
                self.s_type = 'Long sell'
                pass
            
        triggers(self,df)
        
    def create_record(self):
        """builds the tuple for the df, check order matehces column list"""
        tp = (self.p_date, self.stock, self.p_price, self.n_stocks, self.is_held, self.days_held, 
        self.s_date, self.s_price, self.profit, self.pctgain, self.s_type)
        return tp 