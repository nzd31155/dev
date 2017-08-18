from share_settings import Settings
import urllib.request
import json
s = Settings()

class GoogleFinanceAPI:
    def __init__(self):
        self.prefix = "http://finance.google.com/finance/info?client=ig&q="
    
    def get(self,symbol,exchange):
        url = self.prefix+"%s:%s"%(exchange,symbol)
        u = urllib.request.urlopen(url)
        content = u.read().decode('utf-8')
        obj = json.loads(content[3:])
        return obj[0]

def get_lp(s):
    """gets latest prices from google"""
    sl = []  
    for stock in s.symbols:        
        #creates a list of latest stock prices
        c = GoogleFinanceAPI()
        quote = c.get(stock,"LON")
        #changes string to integer and removes ','
        x = (quote['l']).replace(',','')
        x = float(x)
        sl.append(x)
    return sl