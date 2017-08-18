from datetime import date

class Settings():
    """contains all the settings for stock program"""
    def __init__(self):
        """Initialise the settings""" 
        '''
        #Moving average length in days.
        self.MA_Sho = 5
        self.MA_Mid = 15
        self.MA_Lon = 30
        self.MA_values = (self.MA_Sho, self.MA_Mid, self.MA_Lon)
        '''
        #Exponential moving average in days
        self.EMA_Sho = 5
        self.EMA_Mid = 12
        self.EMA_Lon = 26
        self.EMA_values = (self.EMA_Sho, self.EMA_Mid, self.EMA_Lon)

        #FTSE100 Share list the selfsymbols is the active list, switch with symbols2/3 when scaling.
        self.symbols1 = ['AAL']
        self.symbols = ['AAL','ABF','BP','AV']
        self.symbols2 = ['AAL',	'ABF',	'ADM',	'AHT',	'ANTO',	'AV',	'AZN',	'BA',	'BAB',	'BARC',	'BATS',	'BDEV',	'BLND',	'BLT',	'BNZL',	'BP',	'BRBY',	'BT.A',	'CCH',	'CCL',	'CNA',	'CPG',	'CRDA',	'CRH',	'CTEC',	'DCC',	'DGE',	'DLG',	'EXPN',	'EZJ',	'FRES',	'GFS',	'GKN',	'GLEN',	'GSK',	'HL',	'HMSO',	'HSBA',	'IAG',	'IHG',	'III',	'IMB',	'INF',	'ITRK',	'ITV',	'JMAT',	'KGF',	'LAND',	'LGEN',	'LLOY',	'LSE',	'MCRO',	'MDC',	'MERL',	'MKS',	'MNDI',	'MRW',	'NG',	'NXT',	'OML',	'PPB',	'PRU',	'PSN',	'PSON',	'RB',	'RBS',	'RDSA',	'RDSB',	'REL',	'RIO',	'RMG',	'RR',	'RRS',	'RSA',	'RTO',	'SBRY',	'SDR',	'SGE',	'SGRO',	'SHP',	'SKG',	'SKY',	'SLA',	'SMIN',	'SMT',	'SN',	'SSE',	'STAN',	'STJ',	'SVT',	'TSCO',	'TUI',	'TW','ULVR','UU','VOD','WOS','WPG','WPP','WTB']

        #date range for pandas datatable
        self.st_date = date(2016,1,1)
        self.ed_date = date.today().isoformat()
        
        #TimeLag - gap between down trigger and up trigger
        ts=1

        