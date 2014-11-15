import sys
import cx_Oracle
import getpass
import random
import string 
import datetime
from func1 import func1
from func2 import func2
from func3 import func3
from func4 import func4
from func5 import func5
from validity import *
import os

#ADD FUNCTION 4

def main():
	first = True
	check = True
	
	try:	
		while check:
			os.system('cls' if os.name == 'nt' else 'clear')	
			if first:
				print('Please enter your Oracle username and password')
				print()
				first = False
			else:
				print('Please enter correct username/password')
				print()
			user= input('Username: ')
			password = getpass.getpass()			
			try:			
								
				stringconn = user+'/'+password + '@gwynne.cs.ualberta.ca:1521/CRS'
				connection = cx_Oracle.connect(stringconn)
				curs = connection.cursor()
				check = False
			except:
				pass
				
			
		options = {1: func1, 2: func2, 3: func3, 4: func4, 5: func5}
		while True:
			os.system('cls' if os.name == 'nt' else 'clear')
			print('MAIN MENU')
			print()
			print(' 1 - New Vehicle Registration\n 2 - Auto Transaction\n 3 - Driver Licence Registration\n 4 - Violation Record\n 5 - Search the database\n 6 - exit\n')
			choice = validity("Please select a number option from the options above: ", "Please select a valid option: ", 1, int, ['1','2','3','4','5','6'])		
			try:
				options[choice](curs, connection)
			except:
				break
			
			choice = validity("1 - Main Menu \n2 - Exit \nSelection: ", "Please input a valid option: ", 1, str, ['1', '2'])
			
			if choice == '2':
				break
			else:
				print()		
				
		os.system('cls' if os.name == 'nt' else 'clear')	
		curs.close()#deconstruct cursor
		connection.close()#close connection.
		

	#DISPLAY ANY ERROR MESSAGES THAT OCCUR DURING THE EXECUTION OF THE QUERIES AND/OR MANAGEMENT OF THE DATABASE
	except cx_Oracle.DatabaseError as exc:
		error = exc.args
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "Oracle message:", error.message)
	
		
if __name__ == "__main__":
	main()#call main function