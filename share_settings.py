from datetime import date, datetime, timedelta, time

class Settings():
    """contains all the settings for stock program, needs to be run from UK or via VPN
    or the stock codes are wrong.  Included is some list comprehension to allow for 
    this but would need a little tweaking to parse out the location information before
    adding to dataframes or gets messy.  Easiest solution to run from VPN"""

    def __init__(self):
        """Initialise the settings""" 
        
        #Exponential moving average in days
        self.EMA_Sho = 3
        self.EMA_Mid = 9
        self.EMA_Lon = 11
        self.EMA_values = (self.EMA_Sho, self.EMA_Mid, self.EMA_Lon)

        #FTSE100 Share list the selfsymbols is the active list, switch with symbols2/3 when scaling.
        #added_US and list comprehension to allow for US-based running - DEPRECIATED
        self.symbols1 = ['ADM']
        self.symbols2 = ['ADM',	'BA']
        self.symbols = ['AAL',	'ABF',	'ADM',	'AHT',	'ANTO',	'AV',	'AZN',	'BA',	'BAB',	'BARC',	'BATS',	'BDEV',	'BLND',	'BLT',	'BNZL',	'BP',	'BRBY',	'BT.A',	'CCH',	'CCL',	'CNA',	'CPG',	'CRDA',	'CRH',	'CTEC',	'DCC',	'DGE',	'DLG',	'EXPN',	'EZJ',	'FRES',	'GFS',	'GKN',	'GLEN',	'GSK',	'HL',	'HMSO',	'HSBA',	'IAG',	'IHG',	'III',	'IMB',	'INF',	'ITRK',	'ITV',	'JMAT',	'KGF',	'LAND',	'LGEN',	'LLOY',	'LSE',	'MCRO',	'MDC',	'MERL',	'MKS',	'MNDI',	'MRW',	'NG',	'NXT',	'OML',	'PPB',	'PRU',	'PSN',	'PSON',	'RB',	'RBS',	'RDSA',	'RDSB',	'REL',	'RIO',	'RMG',	'RR',	'RRS',	'RSA',	'RTO',	'SBRY',	'SDR',	'SGE',	'SGRO',	'SHP',	'SKG',	'SKY',	'SLA',	'SMIN',	'SMT',	'SN',	'SSE',	'STAN',	'STJ',	'SVT',	'TSCO',	'TUI',	'TW','ULVR','UU','VOD','WOS','WPG','WPP','WTB']
        """
        s = ":LON"
        self.symbols_US = [stock + s for stock in self.symbols] #comprehension to allow for US markets
        """
        #TimeLag - gap between down trigger and up trigger
        self.ts=1
        
        #date range for pandas datatable
        #self.st_date = date(2015,1,1)
        self.st_date = date.today() - timedelta(days=self.EMA_Lon+365)
        self.ed_date = date.today().isoformat()
        self.date_now = datetime.combine(date.today(),time())
        #DELETE - self.date_yst = date.today() - timedelta(days=self.ts)
        
        #Settings for the purchase model
        self.pot = 10000
        self.buy_value = 1000
        
        #selling triggers
        self.max_days_held = 70
        self.l_trig1 = 0 #Low sell normally 10
        self.l_trig2 = 0  #EMA_l switch normally 5
        self.min_gain = 0  #normally 4

    def loop_iter1(self,n):
        self.l_trig1 = n
    
    def loop_iter2(self,n):
        self.l_trig2 = n

    def loop_iter3(self,n):
        self.min_gain = n

        #6,3 = 364.6
        #5,3 = 375.9
        #4,3 = 332.9
        #3,3 = 278.7
        #6,4 = 380.1
        #5,4 = 391.4
        #4,4 = 359.2
        #3,4 = 319.9
        #6,5 = 366.4
        #5,5 = 388.9
        #4,5 = 356.7
        #3,5 = 338.7
        