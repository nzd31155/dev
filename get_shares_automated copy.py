from share_settings import Settings
import share_functions as sf
import portfolio as p

s = Settings()

def main(s):
    """Main programme loop"""
    print("\n\n\t*******   Starting up stocks analysis environment   ******* \n")
    
    df_close_prices = 0
    
    #runs the main program
    df_close_prices = sf.get_stocks(s)
    sf.rec_stocks(s,df_close_prices)
    p.run_main()

main(s)