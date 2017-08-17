from share_settings import Settings
import share_functions as sf

s = Settings()

def main(s):
    """Main programme loop"""
    print("\n\n\t*******   Starting up stocks analysis environment   ******* \n")
    
    df_close_prices = 0
    
    #runs the main program
    sf.options(df_close_prices)
    
main(s)