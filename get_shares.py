from share_settings import Settings
import share_functions as sf

s = Settings()

def main(s):
    """Main programme loop"""
    print("\n\n\t*******   Starting up stocks analysis environment   ******* \n")
    
    #downloads the stocks and creates the initial dataframe.
    df_close_prices = sf.get_stocks(s)
    
    #runs the main program
    sf.options(df_close_prices)
    
main(s)