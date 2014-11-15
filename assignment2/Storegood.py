import sys
import cx_Oracle
import getpass
import random
import string 
import datetime

#converts date number into corresponding month for easy visualisation when output at the end.
monthdic ={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

def validity(str1, str2, val, vartype, constraint = []):
	first = True
	var = ''
	while not var:
		if first:
			var = input(str1)
			first = False
			
		else:
			var = input(str2)
			
		if len(var) > val or (constraint and var not in constraint):	
			var = ''	
				
		elif vartype != str:
			try:
				if vartype == float or vartype == int:
					var = vartype(var)	
				
					if vartype == float and var > 10**(val-2):
						var = ''
						
				elif vartype == datetime.date:
					var = datetime.datetime.strptime(var, '%d-%b-%Y').date()
					
				elif vartype == 'file':
					file = open(var, 'rb')
					var = file.read()
					file.close()	
					
			except:
				var = ''
	
	return var

def erasespace(L):
	for char in L:
		if char == ' ':
			L.remove(char)
	return ''.join(L)

def func1(curs, connection):
	print('NEW VEHICLE REGISTRATION')
	select = 'y'
	
	while select == 'y':#if this option is selected, proceed to fill in all required information in order to fill in the tables.
		# Keeps asking for SIN until a valid one is received
		first = True
		owner_id = ''
		SIN = {}
		
		while not owner_id:
			if first:
				owner_id = (input("Please enter the primary owner's SIN: "))	
				first = False
				
			# If owner_id not in people table was received
			elif len(owner_unknown) == 0:
				owner_id = input("Unknown SIN, please try again: ")
			
			# Check if owner_id is in people table
			# len(owner_unknown) == 0 if owner_id not in people table
			curs.execute("SELECT sin FROM people WHERE sin = '%s'"%(owner_id))
			owner_unknown = curs.fetchall()
			
			if len(owner_unknown) == 0:
				owner_id = ''			
		SIN[owner_id] = 'y'
		
		# Keeps asking for car_id until an unused one is received
		first = True
		car_id = ''
		
		while not car_id:
			if first:
				car_id = (input("Please enter the car's serial number: "))
				first = False
				
			# If car_id in vehicle table was received
			elif len(car_conflict) > 0:
				car_id = input("Serial number already registered, please use another: ")
				
			# Invalid car_id was received
			else:
				car_id = (input("Please enter a valid serial number: "))							
			
			# Check if car_id is in vehicle table
			# len(car_conflict) > 0 if car_id is in vehicle table
			curs.execute("SELECT serial_no FROM vehicle WHERE serial_no = '%s'"%(car_id))
			car_conflict = curs.fetchall()
			
			# Reset car_id if there is a conflict, length of car_id is > 15 or if it is NULL
			if len(car_conflict) > 0 or len(car_id) > 15 or car_id == 'NULL':
				car_id = ''											
		
		maker = validity("Please enter the car's maker: ", "Please enter a valid car maker: ", 20, str)
		model = validity("Please enter the car's model: ", "Please enter a valid car model: ", 20, str)
		year = validity("Please enter the car's year: ", "Please enter a valid year: ", 4, int)
		color = validity("Please enter the car's color: ", "Please enter a valid color: ", 10, str)
		
		# Keeps asking for type_id until a valid one is received
		first = True
		type_id = ''
		
		while not type_id:
			if first:
				type_id = (input("Please enter the car's type_id: "))	
				first = False
		
			else:
				type_id = input("Unknown type_id, please try again: ")
			
			# Convert type_id into int and check if type_id is in vehicle_type table
			# len(type_unknown) == 0 if type_id not in vehicle_type table
			try:
				type_id = int(type_id)
				curs.execute("SELECT type_id FROM vehicle_type WHERE type_id = '%d'"%(type_id))
				type_unknown = curs.fetchall()
			
				if len(type_unknown) == 0:
					type_id = ''
					
			# Error occured, reset type_id
			except:
				type_id = ''
		
		# Keeps asking if there are any other owners to add to the vehicle
		cont = True
		while cont:
			choice = validity("Are there any other (non-primary) owners? y/n: ", "Please input a valid choice: ", 1, str, ['y', 'n'])
			
			if choice == 'n':
				cont = False
			else:
				# Keeps asking for SIN until a valid one is received
				first = True
				secondary_id = ''
				
				while not secondary_id:
					if first:
						secondary_id = (input("Please enter the primary owner's SIN: "))	
						first = False
						
					# If owner_id not in people table was received
					elif len(secondary_unknown) == 0:
						secondary_id = input("Unknown SIN, please try again: ")
					
					else:
						secondary_id = input("SIN already received, please try another: ")
						
					# Check if secondary_id is in people table
					# len(secondary_unknown) == 0 if secondary_id not in people table
					curs.execute("SELECT sin FROM people WHERE sin = '%s'"%(secondary_id))
					secondary_unknown = curs.fetchall()
					
					if len(secondary_unknown) == 0 or secondary_id in SIN:
						secondary_id = ''						
				
				SIN[secondary_id] = 'n'
		
		curs.execute("Insert into vehicle "
                                     "values('%s','%s','%s',%d,'%s','%d')"%(car_id, maker, model, year, color, type_id))#insert statement for vehicle table
		
		for i in SIN:
			curs.execute("Insert into owner "
                                     "values('%s', '%s', '%s')"%(i, car_id, SIN[i]))							
		
		connection.commit()							

		print('New vehicle successfully registered')
		select = validity("Do you want to register another vehicle? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'])

def func2(curs, connection):
	print('AUTO TRANSACTION')
	#auto_sale( transaction_id,seller_id, buyer_id, vehicle_id, s_date, price )
	
	# Get current max transaction_id (transaction_ids increment by 1)
	curs.execute("SELECT max(transaction_id) FROM auto_sale")
	transactions = curs.fetchall()
	transaction_id = int(transactions[0][0])

	more = 'y'
	while more == 'y':
		transaction_id = transaction_id+1
		SIN = {}
		
		# Keeps asking for vehicle_id until a one is received
		first = True
		vehicle_id = ''
		
		while not vehicle_id:
			if first:
				vehicle_id = (input("Please enter the car's serial number: "))
				first = False
				
			# Invalid car_id was received
			else:
				vehicle_id = (input("Please enter a valid serial number: "))							
			
			# Check if vehicle_id is in vehicle table
			# len(car_unknown) == 0 if vehicle_id is not in vehicle table
			curs.execute("SELECT serial_no FROM vehicle WHERE serial_no = '%s'"%(vehicle_id))
			vehicle_unknown = curs.fetchall()
			

			if len(vehicle_unknown) == 0:
				vehicle_id = ''
				
		# Keeps asking for SIN until a valid one is received (person must be the primary owner of the car)
		first =	True	
		seller_id = ''
				
		while not seller_id:
			if first:
				seller_id = (input("Please enter the primary seller's SIN: "))	
				first = False
				
			# If seller_id not in people table was received
			elif len(seller_unknown) == 0:
				seller_id = input("Unknown SIN, please try again: ")
			
			else:
				seller_id = input("This SIN is not the primary owner of this vehicle, please try again: ")
				
			# Check if seller_id is in people table and if seller_id is the primary owner in the owner table
			# len(seller_unknown) == 0 if seller_id not in people table
			curs.execute("SELECT sin FROM people WHERE sin = '%s'"%(seller_id))
			seller_unknown = curs.fetchall()
			
			# len(seller_notprimary) == 0 if seller_id not the primary owner of vehicle_id in owner table
			curs.execute("SELECT owner_id FROM owner where vehicle_id = '%s' and owner_id = '%s' and is_primary_owner = '%s'"%(vehicle_id, seller_id, 'y'))
			seller_notprimary = curs.fetchall()
			
			if len(seller_unknown) == 0 or len(seller_notprimary) == 0:
				seller_id = ''
			
		# Keeps asking for SIN until a valid one is received (person must not be the primary owner of the car)
		first =	True	
		buyer_id = ''
				
		while not buyer_id:
			if first:
				buyer_id = (input("Please enter the primary buyer's SIN: "))	
				first = False
				
			# If buyer_id not in people table was received
			elif len(buyer_unknown) == 0:
				buyer_id = input("Unknown SIN, please try again: ")
			
			else:
				buyer_id = input("SIN already received, please try another: ")
				
			# Check if buyer_id is in people table
			# len(buyer_unknown) == 0 if buyer_id not in people table
			curs.execute("SELECT sin FROM people WHERE sin = '%s'"%(buyer_id))
			buyer_unknown = curs.fetchall()
					
			if len(buyer_unknown) == 0 or buyer_id == seller_id:
				buyer_id = ''		
		SIN[buyer_id] = 'y'
		
		# Get previous sale date of vehicle
		curs.execute("SELECT max(s_date) FROM auto_sale WHERE vehicle_id = '%s'"%(vehicle_id))
		prev = curs.fetchall()
		if prev:
			prev_date = prev[0][0].date()
		s_date = ''
		first = True
		while not s_date:
			if first:
				s_date = validity("Please enter the sale date(DD-MON-YYYY): ", "Please enter a valid date: ", 11, datetime.date)
				first = False
			else:
				s_date = validity("You can't time travel (last sold on: %s), try again: "%(prev_date.strftime('%d-%b-%Y')), "Please enter a valid date: ", 11, datetime.date)
			
			if prev_date and s_date < prev_date:
				s_date = ''
			
		price = validity("Please enter the sale price: ", "Please enter a valid price: ", 9, float)
		
		# Keeps asking if there are any other owners to add to the vehicle
		cont = True
		while cont:
			choice = validity("Are there any other (non-primary) owners? y/n: ", "Please input a valid choice: ", 1, str, ['y', 'n'])
			
			if choice == 'n':
				cont = False
			else:
				# Keeps asking for SIN until a valid one is received
				first = True
				secondary_id = ''
				
				while not secondary_id:
					if first:
						secondary_id = (input("Please enter the primary owner's SIN: "))	
						first = False
						
					# If owner_id not in people table was received
					elif len(secondary_unknown) == 0:
						secondary_id = input("Unknown SIN, please try again: ")
					
					else:
						secondary_id = input("SIN already received, please try another: ")
						
					# Check if secondary_id is in people table
					# len(secondary_unknown) == 0 if secondary_id not in people table
					curs.execute("SELECT sin FROM people WHERE sin = '%s'"%(secondary_id))
					secondary_unknown = curs.fetchall()
					
					if len(secondary_unknown) == 0 or secondary_id in SIN:
						secondary_id = ''						
				
				SIN[secondary_id] = 'n'		
		
		curs.execute("DELETE FROM owner WHERE vehicle_id = '%s'" %(vehicle_id));

		for i in SIN:
			curs.execute("Insert into owner "
			             "values('%s', '%s', '%s')"%(i, vehicle_id, SIN[i]))			
		
		curs.execute("Insert into auto_sale "
                                     "values(%d, '%s', '%s','%s', '%s', %f)"%(transaction_id, seller_id, buyer_id, vehicle_id, s_date.strftime('%d-%b-%Y'), price));
		
		connection.commit()								

		print('Sale successfully completed as transaction_id: %s'%(transaction_id))
		more = validity("Do you want to make another transaction? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'])
	

def func3(curs, connection):
	print('DRIVER LICENCE REGISTRATION')
	#drive_licence( licence_no,sin,class,photo,issuing_date,expiring_date)
	
	cont = 'y'
	while cont == 'y':
		# Keeps asking for SIN until a valid and unused one is received
		first = True
		person_id = ''
		
		while not person_id:
			if first:
				person_id = input("Please input an SIN to register: ")	
				first = False
				
			# If person_id not in people table was received
			elif len(person_unknown) == 0:
				person_id = input("Unknown SIN, please try again: ")
				
			# If person_id in people table but also in drive_licence table was received 
			else:
				person_id = input("SIN already registered, please use another: ")
			
			# Check if person_id is in people table and drive_licence table
			# len(person_unknown) == 0 if person_id not in people table
			curs.execute("SELECT sin FROM people WHERE sin = '%s'"%(person_id))
			person_unknown = curs.fetchall()
			
			# len(person_conflict) > 0 if person_id in drive_licence table
			curs.execute("SELECT sin FROM drive_licence WHERE sin = '%s'"%(person_id))
			person_conflict = curs.fetchall()
			
			if len(person_unknown) == 0 or len(person_conflict) > 0:
				person_id = ''

		drive_class = validity("Please enter the licence class: ", "Please enter a valid licence class: ", 10, str)
		
		# Obtain current time
		# issuing_date = sysdate; expiring_date = issuing_date + 5 years
		issuing_date = datetime.datetime.now().date()
		expiring_date = datetime.date(issuing_date.year+5, issuing_date.month, issuing_date.day)

		photo = validity("Name of image file of driver: ", "Please input a valid photo option: ", float('infinity'), 'file')
			
		# Generates random licence_no until an unused one is received (must be <15 characters long)
		licence_no = False
		while not licence_no or len(licence_conflict) > 0 or len(licence_no) > 15 or licence_no == 'NULL':
			licence_no = ''.join(random.choice(string.ascii_uppercase) for x in range(3))+'-'+''.join(random.choice(string.digits) for x in range(4))
			curs.execute("SELECT licence_no FROM drive_licence WHERE licence_no = '%s'"%(licence_no))
			licence_conflict = curs.fetchall()
		
		curs.setinputsizes(photo=cx_Oracle.BLOB)
		curs.execute("Insert into drive_licence "
                                     "values(:licence_no, :person_id, :class, :photo, :issuing_date, :expiring_date)", {'licence_no':licence_no, 'person_id':person_id, 'class':drive_class, 'photo':photo, 'issuing_date':issuing_date.strftime('%d-%b-%Y'), 'expiring_date':expiring_date.strftime('%d-%b-%Y')})
		connection.commit()
		
		print('Licence registered successfully as %s'%(licence_no))	
		cont = validity("Do you want to register another licence? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'])	

def check_general_errors():
	while True:
		try:
			a = input("Please enter the violator's SIN: ")
			if a == '':
				print("Empty input!")
			else:
				if len(a) > 15:
					print("You have to enter a violator_no in 15 digits!\n")
				else:
					break
		except Exception:
			print("You should enter a valid violator_no")	
	return a		
	
def func4(curs, connection):
	print('VIOLATION RECORD')
	#ticket( ticket_no,violator_no,vehicle_id,office_no,vtype,vdate,place,descriptions)
	#error handling!!!!!!!!!
	ticket_no_list=[]
	violator_no_list = []
	curs.execute("select people.sin from people")
	rows = curs.fetchall()
	for row in rows:
		rowlist = row[0].split(' ')
		violator_no_list.append(erasespace(rowlist))
	curs.execute("select ticket_no from ticket")
	rows = curs.fetchall()
	for row in rows:
		ticket_no_list.append(row[0])
	ticket_no = random.randint(0,99999999)
	while ticket_no in ticket_no_list:
		ticket_no = random.randint(0,99999999)
	print("The ticket_no is already generated!")
	violator_no = check_general_errors()
	while violator_no not in violator_no_list:
		print("Parent key not found!Try it again")
		violator_no = check_general_errors()	
	while True:
		try:
			vehicle_id = input("Please enter the vehicle_id: ")
			if vehicle_id == '':
				print("Empty input!")
			else:
				if len(vehicle_id) > 15:
					print("You have to enter a vehicle_id in 15 digits!\n")
				else:
					break
		except Exception:
			print("Parent key not found")
	while True:
		try:
			office_no = input("Please enter the office_no: ")
			if office_no == '':
				print("Empty input!")
			else:
				if len(office_no) > 15:
					print("You have to enter a office_no in 15 digits!\n")
				else:
					break
		except Exception:
			print("Parent key not found")
	while True:
		try:
			vtype = input("Please enter the violation type: ")
			if vtype == '':
				print("Empty input!")
			else:
				if len(vtype) > 10:
					print("You have to enter a vtype in 10 digits!\n")
				else:
					break
		except Exception:
			print("Parent key not found")						
	while True:
		try:
			vdate = input("Please enter the violation date: ").upper()
			if vdate == '':
				print("Empty input!")
			else:
				if len(vdate) > 12:
					print("You have to enter a datetype date like 'DD-MMM-YYYY'!\n")
				else:
					break
		except Exception:
			print("Parent key not found")
	while True:
		try:
			place = input("Please enter where did the violation take place: ")
			if place == '':
				print("Empty input!")
			else:
				if len(place) > 20:
					print("You have to enter a place in 20 digits!\n")
				else:
					break
		except Exception:
			print("Incorrect input")
	while True:
		try:
			descriptions = input("Please enter the descriptions of the violation: ")
			if descriptions == '':
				print("Empty input!")
			else:
				if len(descriptions) > 1024:
					print("You have to enter a desciption in 1024 digits = !\n")
				else:
					break
		except Exception:
			print("Incorrect input")						
	curs.execute("Insert into ticket values" 
	             "(%d,'%s','%s','%s','%s','%s','%s','%s')"%(ticket_no,violator_no,vehicle_id,office_no,vtype,vdate,place,descriptions)) #insert statement for licence table
	connection.commit()
	more = input('do you want to add another ticket to record y/n: ')
	while more == 'y':
		ticket_no_list = []
		curs.execute("select ticket_no from ticket")
		rows = curs.fetchall()
		for row in rows:
			ticket_no_list.append(row[0])
		ticket_no = random.randint(0,99999999)
		while ticket_no in ticket_no_list:
			ticket_no = random.randint(0,99999999)
		print("The ticket_no is already generated!")
		while True:
			try:
				violator_no = input("Please enter the violator's SIN: ")
				if violator_no == '':
					print("Empty input!")
				else:
					if len(violator_no) > 15:
						print("You have to enter a violator_no in 15 digits!\n")
					else:
						break
			except Exception:
				print("Parents key not found!")
		while True:
			try:
				vehicle_id = input("Please enter the vehicle_id: ")
				if vehicle_id == '':
					print("Empty input!")
				else:
					if len(vehicle_id) > 15:
						print("You have to enter a vehicle_id in 15 digits!\n")
					else:
						break
			except Exception:
				print("Parent key not found")
		while True:
			try:
				office_no = input("Please enter the office_no: ")
				if office_no == '':
					print("Empty input!")
				else:
					if len(office_no) > 15:
						print("You have to enter a office_no in 15 digits!\n")
					else:
						break
			except Exception:
				print("Parent key not found")
		while True:
			try:
				vtype = input("Please enter the violation type: ")
				if vtype == '':
					print("Empty input!")
				else:
					if len(vtype) > 10:
						print("You have to enter a vtype in 10 digits!\n")
					else:
						break
			except Exception:
				print("Parent key not found")						
		while True:
			try:
				vdate = input("Please enter the violation date: ").upper()
				if vdate == '':
					print("Empty input!")
				else:
					if len(vdate) > 12:
						print("You have to enter a datetype date like 'DD-MMM-YYYY'!\n")
					else:
						break
			except Exception:
				print("Parent key not found")
		while True:
			try:
				place = input("Please enter where did the violation take place: ")
				if place == '':
					print("Empty input!")
				else:
					if len(place) > 20:
						print("You have to enter a place in 20 digits!\n")
					else:
						break
			except Exception:
				print("Incorrect input")
		while True:
			try:
				descriptions = input("Please enter the descriptions of the violation: ")
				if descriptions == '':
					print("Empty input!")
				else:
					if len(descriptions) > 1024:
						print("You have to enter a desciption in 1024 digits = !\n")
					else:
						break
			except Exception:
				print("Incorrect input")								
		curs.execute("Insert into ticket values" 
		             "(%d,'%s','%s','%s','%s','%s','%s','%s')"%(ticket_no,violator_no,vehicle_id,office_no,vtype,vdate,place,descriptions))					
		connection.commit()
		more = input('do you want to add another ticket to record y/n: ')
	print("ticket is already recorded")	

def main():
	user= 'lingbo' #input('Username:')(uncomment for final code before submission
	password = 'Tlbo1994' #getpass.getpass()(uncomment in final code before submission
	
	try:
		stringconn = user+'/'+password + '@gwynne.cs.ualberta.ca:1521/CRS'
		connection = cx_Oracle.connect(stringconn)

		curs = connection.cursor()
		print('please select a number option from the options below: ')
		choice = input(' 1 - New Vehicle Registration\n 2 - Auto Transaction\n 3 - Driver Licence Registration\n 4 - Violation Record\n 5 - Search the database\n 6 - exit\n')
		
		while choice != '6':
			while choice not in ['1','2', '3', '4', '5','6']:
				choice = input(' pick a valid number: ')		
				
			#this is what happens when vehicle registration is picked
			if choice == '1':
				func1(curs, connection)
			
			#this is the code that executes when selection 2 is picked
			if choice == '2':
				func2(curs, connection)
				
			#selection of the third choice option(licence registration)
			if choice == '3':
				func3(curs, connection)
				
			if choice == '4':
				func4(curs, connection)
				
			#choice 5 is the search database appication.
			if choice == '5':
				print('SEARCH THE DATABASE')	
				print('Please pick a search option')
				again = 'y'
				while again == 'y':
					inp = input(' 1 - Driver Info \n 2 - List all violation records received by a person\n 3 - Print out the vehicle_history\n')
					
					if inp == '1':#check the kind of search being executed(name, licence searchfor personal info.)
						selection = input(' 1 - search by name \n 2 - search by licence number \n')#choose the search type, name or licence no
						
						if selection == '1':#search by name query
							search_by = input('please enter full name: ')
							searchf10 = ("(SELECT name, dl.licence_no, addr, birthday, class, c_id FROM people p, driving_condition dc, restriction r, drive_licence dl WHERE p.sin = dl.sin AND r.r_id = dc.c_id AND r.licence_no = dl.licence_no AND p.name = '%s')"%(search_by));
							curs.execute(searchf10)
							v = curs.fetchall()
							
							for i in v:
								dates = i[3].date()
								print(' Name: %s \n Drivers licence: %s \n Address: %s \n Birthday: %s \n Class: %s \n Restriction: %s \n' %(i[0], i[1].split()[0], i[2], str(dates.day)+'-'+monthdic[dates.month]+'-'+str(dates.year), i[4].split()[0], i[5]))	
							if len(v) == 0:
								print('###No results were found matching your search criteria###')						
								
						if selection == '2':#search by licence query
							search_by = input('please enter the licence number: ').upper()
							searchf11 = ("(SELECT name, dl.licence_no, addr, birthday, class, c_id FROM people p, driving_condition dc, drive_licence dl, restriction r WHERE p.sin = dl.sin AND r.r_id = dc.c_id AND r.licence_no = dl.licence_no AND dl.licence_no = '%s')"%(search_by));
							(curs.execute(searchf11))
							v = curs.fetchall()
							
							for i in v:
								dates = i[3].date()
								print(' Name: %s \n Drivers licence: %s \n Address: %s \n Birthday: %s \n Class: %s \n Restriction: %s \n' %(i[0], i[1].split()[0], i[2],str(dates.day)+'-'+monthdic[dates.month]+'-'+str(dates.year), i[4].split()[0], i[5]))
							if len(v) == 0:
								print('###No results were found matching your search criteria###')	
						
					if inp == '2':#check the kind of search being executed(SIN, licence search for tickets)
						selection = input(' 1 - search by SIN \n 2 - search by licence number \n')#choose the search type, SIN or licence no
						if selection == '1':
							search_by = input('please enter the SIN: ')
							searchf01 = "(SELECT ticket_no, t.vtype, fine, vdate, descriptions, t.place FROM ticket t, ticket_type tt, people p WHERE t.vtype = tt.vtype AND p.sin = t.violator_no and p.sin = '%s')"%(search_by);
							(curs.execute(searchf01))
							v = curs.fetchall()
						
							for i in v:
								dates = i[3].date()
								print(' Ticket number: %d \n Violation code: %s \n Fine: %d \n Date: %s \n Description: %s \n Place: %s \n ' %(i[0], i[1].split()[0], i[2],str(dates.day)+'-'+monthdic[dates.month]+'-'+str(dates.year), i[4], i[5]))
							curs.execute("select p.name from people p where sin = %s"%((search_by)))
							person = curs.fetchone()
							
							print("%s has %d tickets total"%(person[0], len(v)))
							if len(v) == 0:
								print('###No results were found matching your search criteria###')							
							
						if selection == '2':
							search_by = input('please enter the licence number: ').upper()
							searchf02 = "(SELECT ticket_no, t.vtype, fine, vdate, descriptions, t.place FROM ticket t, ticket_type tt, people p, drive_licence WHERE t.vtype = tt.vtype AND p.sin = t.violator_no AND drive_licence.sin = p.sin AND drive_licence.licence_no = '%s')"%(search_by);
							
							(curs.execute(searchf02))
							v = curs.fetchall()
													
							for i in v:
								dates = i[3].date()
								print(' Ticket number: %d \n Violation code: %s \n Fine: %d \n Date: %s \n Description: %s \n Place: %s \n' %(i[0], i[1].split()[0], i[2],str(dates.day)+'-'+monthdic[dates.month]+'-'+str(dates.year), i[4], i[5]))
							curs.execute("select p.name from people p, drive_licence dl where dl.sin = p.sin AND dl.licence_no = '%s'"%((search_by)))
							person = curs.fetchone()
															
							print("%s has %d tickets total"%(person[0], len(v)))							
							if len(v) == 0:
								print('###No results were found matching your search criteria###')														
					if inp == '3':
						select_by = input('Please enter the vehicle licence plate: ')
						searchf03 = "(SELECT vehicle_no, number_sales, average_price, total_tickets FROM ((SELECT v.serial_no as vehicle_no, COUNT(DISTINCT s.transaction_id) AS number_sales , AVG(s.price) AS average_price FROM auto_sale s, vehicle v, vehicle_type vt, ticket t WHERE s.vehicle_id = v.serial_no and v.type_id = vt.type_id and v.serial_no = '%s' GROUP BY v.serial_no) f left join (SELECT COUNT(t.vtype) as total_tickets, v.serial_no as car FROM vehicle v left join ticket t on v.serial_no = t.vehicle_id GROUP BY v.serial_no) r on f.vehicle_no = r.car))"%(select_by);
						
						(curs.execute(searchf03))
						v = curs.fetchall()
																			
						for i in v:
							print(' Vehicle Serial Number: %s \n Times Sold: %d \n Average sale price: %d \n Total Tickets: %d \n ' %((i[0]), int(i[1]), int(i[2]), int(i[3])))		
						if len(v) == 0:
							print('###No results were found matching your search criteria###')	
					
					again = input('do you want to do another search? y/n: ')
					while again not in ['y', 'n']:
						print('please press "y" or "n"')
						again = input('do you want to do another search?;')
			
				
			if choice == '6':
				break
			#
			x = input('Are you sure you want to exit? y/n: ').lower()
			
			while x not in ['y', 'n']:
				print("please pick a real option")
				x = input('Are you sure you want to exit? y/n: ').lower()
				
			if x == 'n':
				print('please select another number option from the options below: ')
				choice = input(' 1 - New Vehicle Registration\n 2 - Auto Transaction\n 3 - Driver Licence Registration\n 4 - Violation Record\n 5 - Search the database\n 6 - exit\n')
			else:
				choice = '6'
					
		curs.close()
		connection.close()
		print('Have a nice day!')
		

	except cx_Oracle.DatabaseError as exc:
		error = exc.args
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "Oracle message:", error.message)
	
		
if __name__ == "__main__":
	main()