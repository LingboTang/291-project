from validity import *
import os
from subfunchash import subfunchash
from subfunchash2 import subfunchash2
from subfunc3 import subfunc3
from subfunchash4 import subfunchash4
from subfunc5 import subfunc5


def func2():
    try:
        options = {1: subfunchash, 2: subfunchash2,3:subfunc3, 4: subfunchash4, 5: subfunc5}
        while True:
            #os.system('cls' if os.name == 'nt' else 'clear')
            print('HASH MENU\n')
            print(' 1 - Create and populate the database\n 2 - Retrieve records with a given key\n 3 - Retrieve records with a given data\n 4 - Retrieve records with a given range of key values\n 5 - Destroy the database\n 6 - Quit\n ')
            choice = validity("Please select a number option from the options above: ", "Please select a valid option: ", 1, int, ['1','2','3','4','5','6'])
            try:
                options[choice]()
                
            except:
                break
            
        #os.system('cls' if os.name == 'nt' else 'clear')
    except:
        print('wrong')