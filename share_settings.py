from datetime import date, datetime, timedelta, time

class Settings():
    """contains all the settings for stock program"""
    def __init__(self):
        """Initialise the settings""" 
        
        #Exponential moving average in days
        self.EMA_Sho = 3
        self.EMA_Mid = 10
        self.EMA_Lon = 33
        self.EMA_values = (self.EMA_Sho, self.EMA_Mid, self.EMA_Lon)

        #FTSE100 Share list the selfsymbols is the active list, switch with symbols2/3 when scaling.
        self.symbols1 = ['PRU']
        self.symbols2 = ['AAL',	'ABF',	'ADM',	'AHT',	'ANTO',	'AV']
        self.symbols = ['AAL',	'ABF',	'ADM',	'AHT',	'ANTO',	'AV',	'AZN',	'BA',	'BAB',	'BARC',	'BATS',	'BDEV',	'BLND',	'BLT',	'BNZL',	'BP',	'BRBY',	'BT.A',	'CCH',	'CCL',	'CNA',	'CPG',	'CRDA',	'CRH',	'CTEC',	'DCC',	'DGE',	'DLG',	'EXPN',	'EZJ',	'FRES',	'GFS',	'GKN',	'GLEN',	'GSK',	'HL',	'HMSO',	'HSBA',	'IAG',	'IHG',	'III',	'IMB',	'INF',	'ITRK',	'ITV',	'JMAT',	'KGF',	'LAND',	'LGEN',	'LLOY',	'LSE',	'MCRO',	'MDC',	'MERL',	'MKS',	'MNDI',	'MRW',	'NG',	'NXT',	'OML',	'PPB',	'PRU',	'PSN',	'PSON',	'RB',	'RBS',	'RDSA',	'RDSB',	'REL',	'RIO',	'RMG',	'RR',	'RRS',	'RSA',	'RTO',	'SBRY',	'SDR',	'SGE',	'SGRO',	'SHP',	'SKG',	'SKY',	'SLA',	'SMIN',	'SMT',	'SN',	'SSE',	'STAN',	'STJ',	'SVT',	'TSCO',	'TUI',	'TW','ULVR','UU','VOD','WOS','WPG','WPP','WTB']

        #TimeLag - gap between down trigger and up trigger
        self.ts=1
        
        #date range for pandas datatable
        self.st_date = date(2017,5,1)
        self.ed_date = date.today().isoformat()
        self.date_now = datetime.combine(date.today(),time())
        #DELETE - self.date_yst = date.today() - timedelta(days=self.ts)
        
        #Settings for the purchase model
        self.pot = 10000
        self.buy_value = 1000
        self.sell_trigger = 1.1