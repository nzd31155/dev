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
            self.sell_type = ""

        def triggers2(self, df):
            """iterates through the triggers"""
            #long_hold sale date
            lon_s_date = self.p_date + timedelta(days = sf.s.max_days_held)
            iter_date = self.p_date
            looper = True
            lw_trigger1, lw_trigger2, lg_trigger, hi_trigger, cur_held = (False,)*5
            #skips over weekends/holidays not in stock df
            while looper == True:
                
                while lw_trigger1 | lw_trigger2 | lg_trigger | hi_trigger | cur_held == False: 
                    while iter_date not in df.index and iter_date <= df.index.max().date():  
                        #print('loop not in df')
                        iter_date += timedelta(days = 1)
                    #print('loop')
                    
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
                        hi_trigger = ema_s <  ema_l

                    #break out if latest date after trigger tests                
                    cur_held =  iter_date == df.index.max().date()
                        
                    #if not latest date, iterate back through the loop
                    iter_date += timedelta(days = 1)  
                    #print(iter_date)
                if cur_held:
                    break
                else:
                    #set sale price and populate class sell fields
                    #print(self.stock,'adding sales data')
                    fill_sale_data(self,iter_price, iter_date) 
                    looper = False
                  
        def triggers(self, df):
            """iterates through the triggers"""
            #long_hold sale date
            lon_s_date = self.p_date + timedelta(days = sf.s.max_days_held)
            iter_date = self.p_date
            looper = True
            while looper == True:
                while iter_date not in df.index and iter_date <= df.index.max().date():  
                    #passes through weekends/national holiday dates
                    #print('loop not in df')
                    iter_date += timedelta(days = 1)
                #print('loop', stock, iter_date)
                if iter_date <= df.index.max().date():
                    label_l = self.stock + "_EMA_" + str(sf.s.EMA_Lon)
                    ema_l = df.loc[iter_date,[label_l]].values[0]
                    iter_price = df.loc[iter_date,[self.stock]].values[0]
                    #print('in trigger loop')
                    #long trigger. stock held for long time
                    if iter_date>= lon_s_date: 
                        self.sell_type = 'long'
                        fill_sale_data(self,iter_price, iter_date) 
                        break

                    #low trigger1 - if stock drops below low % threshold
                    elif iter_price < (self.p_price * (1-sf.s.l_trig1/100)): 
                        self.sell_type = 'bottom'
                        fill_sale_data(self,iter_price, iter_date) 
                        break

                    #low trigger2 - if stock dips x% below ema_Long
                    elif iter_price < (ema_l*(1-(sf.s.l_trig2/100))):
                        self.sell_type = 'low trend'
                        fill_sale_data(self,iter_price, iter_date) 
                        break

                    #high trigger
                    else:
                        #builds iterative df to find max price over time period
                        #would be great to use a slice rather than keep having to
                        #build a df but this works for now.
                        df2 = df.loc[self.p_date:iter_date][self.stock]
                        max_price = df2.max()
                    
                        #has the stock now grown by x%
                        if max_price > self.p_price * (1+(sf.s.min_gain/100)):
                            label_s = self.stock + "_EMA_" + str(sf.s.EMA_Sho) 
                            ema_s = df.loc[iter_date,[label_s]].values[0]
                            ema_trig = ema_s * ((100-sf.s.h_trig1)/100)
                            #print('has grown enough',iter_price/ema_trig)
                            #if EMA short dips under EMA long
                            if iter_price < ema_s *((100-sf.s.h_trig1)/100):
                                self.sell_type = 'high'
                                #print('high sell', 'iterprice',iter_price, 'ema_s',ema_s)
                                fill_sale_data(self,iter_price, iter_date) 
                                break
                            pass

                    #if not latest date, iterate back through the loop
                    iter_date += timedelta(days = 1)
                    #print('trigger loop after iter_date')  
                else:
                    #print('end of trigger loop')
                    looper = False
                    #print('Date outside of df',iter_date)
                    break

        def triggers2(self, df):
            """iterates through the triggers"""
            #long_hold sale date
            lon_s_date = self.p_date + timedelta(days = sf.s.max_days_held)
            iter_date = self.p_date
            looper = True
            lw_trigger1, lw_trigger2, lg_trigger, hi_trigger, cur_held = (False,)*5
            #skips over weekends/holidays not in stock df
            while looper == True:
                
                while lw_trigger1 | lw_trigger2 | lg_trigger | hi_trigger | cur_held == False: 
                    while iter_date not in df.index and iter_date <= df.index.max().date():  
                        #print('loop not in df')
                        iter_date += timedelta(days = 1)
                    #print('loop')
                    
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
                        hi_trigger = ema_s <  ema_l

                    #break out if latest date after trigger tests                
                    cur_held =  iter_date == df.index.max().date()
                        
                    #if not latest date, iterate back through the loop
                    iter_date += timedelta(days = 1)  
                    #print(iter_date)
                if cur_held:
                    break
                else:
                    #set sale price and populate class sell fields
                    #print(self.stock,'adding sales data')
                    fill_sale_data(self,iter_price, iter_date) 
                    looper = False
                
        triggers(self,df)

    def create_record(self):
        """builds the tuple for the df, check order matehces column list"""
        tp = (self.p_date, self.stock, self.p_price, self.n_stocks, self.is_held, self.days_held, 
        self.s_date, self.s_price, self.profit, self.pctgain)
        return tp 