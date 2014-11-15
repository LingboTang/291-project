import datetime

# Adds unknown SIN into people table
def SIN(sin, curs, connection):
	# Required info
	name = validity("Please enter person's name: ", "Please enter a valid name: ", 40, str)
	height = validity("Please enter person's height: ", "Please enter a valid height: ", 5, float)
	weight = validity("Please enter person's weight: ", "Please enter a valid weight: ", 5, float)
	eyecolor = validity("Please enter person's eye color: ", "Please enter a valid eye color: ", 10, str)
	haircolor = validity("Please enter person's hair color: ", "Please enter a valid hair color: ", 10, str)
	addr = validity("Please enter person's address: ", "Please enter a valid address: ", 50, str)
	gender = validity("Please enter person's gender m/f: ", "Please enter a valid gender: ", 1, str, ['m', 'f'])
	birthday = validity("Please enter the person's birthday (DD-MON-YYYY): ", "Please enter a valid date: ", 11, datetime.date)
	
	# Insert and commit
	curs.execute("Insert into people "
	             "values('%s', '%s', %f, %f, '%s', '%s', '%s', '%s', '%s')"%(sin, name, height, weight, eyecolor, haircolor, addr, gender, birthday.strftime('%d-%b-%Y')))	
	connection.commit()
	
	# Display successful registration of new SIN
	print("New SIN, %s, has been successfully registered"%(sin))

# Returns 0 if n = 1 else 1
def falsify(n):
	if n == 0:
		return 1
	return 0

#VALIDITY checks the validity of the input provided. if the input has been used or does not exist, it will return nothing
def validity(str1, str2, val, vartype, constraint = [], case = '', curs = [], connection = [], queries = [], newval = '', notlike = ''):
	first = True
	var = ''
	
	while not var:
		# First iteration, use str1 as input message
		if first:
			var = input(str1).strip()
			first = False
			
		else:
			# str2 is a string, use it as input error message
			if type(str2) == str:
				var = input(str2).strip()	
				
			# str2 is a list, iterate through it
			else:
				for i in str2:
					# i is a list, check if condition is true, if so use that i[0] as input error message
					if type(i) == list and ((queries[i[1]][1] == queries[i[1]][2]) == queries[i[1]][3]):
						var = input(i[0]).strip()
						break
					
					# Last element of str2 is a string which will be used as input error message
					elif type(i) == str:
						var = input(i).strip()
						break		
		# Change case of input
		if case == 'upper':
			var = var.upper()
		elif case == 'lower':
			var = var.lower()		

		# Make sure length of input is <= val, and in constraint if a constraint is specified
		if len(var) > val or (constraint and var not in constraint):	
			var = ''	
		
		# Passed first test
		# The input is not expected to be a string
		elif vartype != str:
			try:
				# If vartype == float or vartype == int, convert the input
				if vartype == float or vartype == int:
					var = vartype(var)	
				
					# In the case of a float, make sure the value does not go over 10**(val-2) (size limit of the identifier)
					if vartype == float and var >= 10**(val-2):
						var = ''
				
				# If vartype == datetime.date, convert input into string format of date (DD-MMM-YYYY)	
				elif vartype == datetime.date:
					var = datetime.datetime.strptime(var, '%d-%b-%Y').date()
					
				# If vartype == 'file', try opening the file and return read of the file
				elif vartype == 'file':
					file = open(var, 'rb')
					var = file.read()
					file.close()	
			
			# If an error occured, reset input	
			except:
				var = ''			
		
		# Passed second test
		if var:
			# Iterate through elements in queries
			for i in queries:
				# Execute the sql command and set i[1] = length of result
				curs.execute(i[0]%(var))
				i[1] = len(curs.fetchall())
				
				# Condition to reset input is achieved
				if ((i[1] == i[2]) == i[3]):
					# length of i == 5 means that input is an SIN, and this condition means that input SIN wasn't found in people table
					if len(i) == 5:
						i[1] = falsify(i[1])
						
						# Ask user if they want to register the unknown SIN
						choice = validity("Unknown SIN, do you wish to register it? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')
						
						# Don't register, and reset
						if choice == 'n':
							i[1] = falsify(i[1])
							var = ''
						
						# Register the SIN
						else:
							SIN(var, curs, connection)
							break
						
					# Not SIN input, just reset
					else:
						var = ''
		
		# Tests failed somewhere
		else:
			# Falsify values in queries
			for i in queries:
				# No specified reset value (falsify only if condition to reset if true)
				if len(i) != 5 and ((i[1] == i[2]) == i[3]):
					i[1] == falsify(i[1])
						
				# Reset value is specified
				elif len(i) == 5:
					i[1] = i[4]

		# Makes sure that input doesn't satisfy notlike condition
		# Error message will be last possible one in str2 if it is a list
		if (type(notlike) == dict and var in notlike) or var == notlike:
			var = ''		
			
		# In the case that notlike is a dictionary, and all tests are passed
		# Add var into notlike with value newval
		if var and newval and type(notlike) == dict:
			notlike[var] = newval
			
	return var