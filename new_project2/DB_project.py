import sys
import os
from validity import *
from subfunc1 import subfunc1
from subfunc2 import subfunc2
from subfunc3 import subfunc3
from subfunc4 import subfunc4
from subfunc5 import subfunc5

DIR = "/tmp/my_db1/"
DA_FILE = DIR + "sample_db"
INVERSE_DA_FILE = DIR + "sample_db2"
DB_SIZE = 1000
SEED = 10000000

def main():
	try:
		options = {'btree': {1: subfunc1, 2: subfunc2, 3: subfunc3, 4: subfunc4, 5: subfunc5}, \
		           'hash': {1: subfunc1, 5: subfunc5}, \
		           'indexfile': {1: subfunc1, 2: subfunc2, 3: subfunc2, 4: subfunc4, 5: subfunc5}}
		
		params = {'btree': {1: [[DA_FILE], DIR, DB_SIZE, SEED], 2: [DA_FILE, 'key', 'data'], 3: [DA_FILE], 4: [DA_FILE], 5: [DIR]}, \
		          'hash': {1: [[DA_FILE], DIR, DB_SIZE, SEED], 5: [DIR]}, \
		          'indexfile': {1: [[DA_FILE, INVERSE_DA_FILE], DIR, DB_SIZE, SEED], 2: [DA_FILE, 'key', 'data'], 3:[INVERSE_DA_FILE, 'data', 'key'], 4: [DA_FILE]}, 5: [DIR]}

		while True:
			os.system('cls' if os.name == 'nt' else 'clear')
			
			options[sys.argv[1].lower()]
			
			print('%s MENU\n'%(sys.argv[1].upper()))
			print(' 1 - Create and populate the database\n 2 - Retrieve records with a given key\n 3 - Retrieve records with a given data\n 4 - Retrieve records with a given range of key values\n 5 - Destroy the database\n 6 - Quit\n ')
			
			choice = validity("Please select a number option from the options above: ", "Please select a valid option: ", 1, int, ['1','2','3','4','5','6'])
					
			try:
				try:
					options[sys.argv[1].lower()][choice](params[sys.argv[1].lower()][choice])
				except:
					options[sys.argv[1].lower()][choice]()
			
			except:
				os.system('cls' if os.name == 'nt' else 'clear')
				options[sys.argv[1].lower()][5]([DIR, "END"])
				break
					    
	except:
		print("Not a valid option")
		
if __name__ == "__main__":
	main()#call main function