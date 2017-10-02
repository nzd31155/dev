from share_settings import Settings
import urllib.request,json
import pprint as p
s = Settings()

prefix = "http://finance.google.com/finance?client=ig&output=json&q="
    
def get(symbol,exchange):
    url = prefix+"%s:%s"%(exchange,symbol)
    u = urllib.request.urlopen(url)
    #translates url to string
    c = u.read().decode('utf-8')
    #slices string to remove characters at start/end of string
    con=(c[5:-2])
    #removes '\' from the text
    cont=con.replace("\\","")
    content = json.loads(cont)
    result = (content['l'])
    return result

def get_lp(s):
    """gets latest prices from google"""
    sl = []  
    for stock in s.symbols:          
        #creates a list of latest stock prices
        quote = get(stock,"LON")
        #changes string to integer and removes ','
        x = (quote.replace(',',''))
        x = float(x)
        sl.append(x)
    return sl

#print(get_lp(s))