from share_settings import Settings
import share_functions as sf
import portfolio as p 


def looper():
    """Runs the simulation using range of 
    values for set arguments"""

#add in calculations for number and %success of purchases
#also limit purchases to pot size.

    loop = range(1,11)
    for n in loop:
        sf.s.loop_iter1(n)
        for n in loop:
            sf.s.loop_iter2(n)
            for n in loop:
                sf.s.loop_iter3(n)
                p.run_main()
                