import sys
import cx_Oracle
import getpass
import random
import string 
import datetime
import time
from func1 import func1
from func2 import func2
from func3 import func3
from validity import *
import os

def main():

	options = {'btree': func1, 'hash': func2, 'indexfile': func3}
	#os.system('cls' if os.name == 'nt' else 'clear')	
	print(sys.argv[1])
	try:
		options[sys.argv[1]]()
		
	except:
		print('not a valid option')
		
if __name__ == "__main__":
	main()#call main function