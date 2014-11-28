from validity import *
import os
from subfunc1 import subfunc1
from subfunc2 import subfunc2
from subfunc3 import subfunc3
from subfunc4 import subfunc4
from subfunc5 import subfunc5

def func1():
    
    
    try:
	    options = {1: subfunc1, 2: subfunc2,3:subfunc3, 4: subfunc4, 5: subfunc5}
	    while True:
		    #os.system('cls' if os.name == 'nt' else 'clear')
		    print('BTREE MENU')
		    print()
		    print(' 1 - Create and populate the database\n 2 - Retrieve records with a given key\n 3 - Retrieve records with a given data\n 4 - Retrieve records with a given range of key values\n 5 - Destroy the database\n 6 - Quit\n ')
		    choice = validity("Please select a number option from the options above: ", "Please select a valid option: ", 1, int, ['1','2','3','4','5','6'])		
		    try:
			    options[choice]()
		    except:
			    break
		    
		    choice = validity("1 - SUB Menu \n2 - Exit \nSelection: ", "Please input a valid option: ", 1, str, ['1', '2'])
		    
		    if choice == '2':
			    break
		    else:
			    print()		
			    
	    #os.system('cls' if os.name == 'nt' else 'clear')
    except:
	    print('wrong')