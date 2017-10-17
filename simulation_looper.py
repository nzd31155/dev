from share_settings import Settings
import share_functions as sf
import portfolio as p 
import csv

def looper():
    """Runs the simulation using range of 
    values for set arguments"""

#add in calculations for number and %success of purchases
#also limit purchases to pot size.
    list=[]
    loop = range(1,22)
    loop2 = range(1,11)
    for n in loop:
        n_value = ((n-21)/5)
        sf.s.loop_iter4(n_value)
        for n in loop2:
            sf.s.loop_iter3(n)
            for n in loop2:
                sf.s.loop_iter2(n)
                p.run_main()
'''
        for n in loop:
            sf.s.loop_iter2(n)
            for n in loop:
                sf.s.loop_iter3(n)
                p.run_main()
'''