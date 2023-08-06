import os
import random
from time import sleep
def lgo():

    colors = ['\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;34m', '\033[1;35m', '\033[1;36m']
    W = '\033[0m'

    def clr():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def logo():
        clr()
        sleep(1)
        lg = """\033[1;34m
              .888888888.               888                         
              0000    0000              000                              
              888      888              888
              888           R8888888R   888                            
              000           R8888888R   000                               
              888     000               888          88  
              0000   0000               0000        000                    
              "000000000"               88888888888888     
       \033[1;0m"""
        print(lg)
        sleep(1)

    def banner():
        clr()
        logo = """" 
              .888888888.               888                         
              0000    0000              000                              
              888      888              888
              888           R8888888R   888                            
              000           R8888888R   000                               
              888     000               888          88  
              0000   0000               0000        000                    
              "000000000"               88888888888888     

          \033[1;34m        Developed By :\033[1;34m Al Jabir   """
        print(random.choice(colors) + logo + W)
        print("\n")

    logo()
    banner()
lgo()