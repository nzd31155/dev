from share_settings import Settings
from datetime import date, datetime, timedelta
import share_functions as sf
class PortfolioRecord():
    """This class defines a single portfolio record"""
    def __init__(self,stock,p_date,p_price,df):
        """for each stock fed into the Class... """
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
        self.n_stocks = int(sf.s.buy_value/(p_price/100))

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
            #long_hold sale date
            lon_s_date = self.p_date + timedelta(days = sf.s.max_days_held)
            iter_date = self.p_date
            looper = True
            lw_trigger1, lw_trigger2, lg_trigger, hi_trigger = (False, False, False, False)
            #skips over weekends/holidays not in stock df
            while looper == True:
                while lw_trigger1 | lw_trigger2 | lg_trigger | hi_trigger == False: 
                    while iter_date not in df.index:
                        #print('loop not in df')
                        iter_date += timedelta(days = 1)                 
                    #long trigger
                    lg_trigger = iter_date >= lon_s_date
                    iter_price = df.loc[iter_date,[self.stock]].values[0]

                    #low trigger1 - if stock drops below 10% sell
                    lw_trigger1 = iter_price < (self.p_price * (1-sf.s.l_trig1/100))                    
                    
                    #low trigger2 - if stock dips x% below ema_Long
                    label_l = self.stock + "_EMA_" + str(sf.s.EMA_Lon)
                    ema_l = df.loc[iter_date,[label_l]].values[0]
                    lw_trigger2 = iter_price < (ema_l*(1-(sf.s.l_trig2/100)))
                    
                    #high trigger
                    #builds iterative df to find max price over time period
                    #would be great to use a slice rather than keep having to
                    #build a df but this works for now.
                    df2 = df.loc[self.p_date:iter_date][self.stock]
                    max_price = df2.max()
                    
                    #has the stock now grown by x%
                    if max_price > self.p_price * (1+(sf.s.min_gain/100)):
                        label_s = self.stock + "_EMA_" + str(sf.s.EMA_Sho) 
                        ema_s = df.loc[iter_date,[label_s]].values[0]
                        #print(self.stock, self.p_date, iter_date, ema_l, ema_s)
                        #if EMA short dips under EMA long
                        if ema_s <  ema_l:
                        #    print('High trigger')
                            hi_trigger = True
                                
                    #iterate back through the loop
                    if iter_date < df.index.max().date():
                        iter_date += timedelta(days = 1)  
                    else:
                        #print(self.stock, ' is currently held')
                        break

                #set sale price and populate class sell fields
                #print("Long -",lg_trigger,"Low -",lw_trigger,"High -",hi_trigger)    
                fill_sale_data(self,iter_price, iter_date) 
                looper = False
                
        triggers(self,df)
        
    def create_record(self):
        """builds the tuple for the df, check order matehces column list"""
        tp = (self.p_date, self.stock, self.p_price, self.n_stocks, self.is_held, self.days_held, 
        self.s_date, self.s_price, self.profit, self.pctgain, self.s_type)
        return tp 