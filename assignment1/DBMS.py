import sys
import cx_Oracle
import getpass
import random
import string 
import datetime

#converts date number into corresponding month for easy visualisation when output at the end.
monthdic ={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}


#VALIDITY checks the validity of the input provided. if the input has been used or does not exist, it will return nothing
def validity(str1, str2, val, vartype, constraint = [], case = '', curs = [], connection = [], queries = [], newval = '', notlike = ''):
	first = True
	var = ''
	quote = "'"
	double_quote = '"'	
	while not var:
		if first:
			var = input(str1).strip()
			first = False
			
		else:
			if type(str2) == str:
				var = input(str2).strip()	
			else:
				for i in str2:
					if type(i) == list and ((queries[i[1]][1] == queries[i[1]][2]) == queries[i[1]][3]):
						var = input(i[0]).strip()
						break
					
					elif type(i) == str:
						var = input(i).strip()
						break		
		
		varlist = list(var)
		if (quote in varlist) or (double_quote in varlist) or (quote and double_quote in varlist):
			var = ''		

		if case == 'upper':
			var = var.upper()
		elif case == 'lower':
			var = var.lower()		

		if len(var) > val or (constraint and var not in constraint):	
			var = ''	
							
		elif vartype != str:
			try:
				if vartype == float or vartype == int:
					var = vartype(var)	
				
					if vartype == float and var >= 10**(val-2):
						var = ''
						
				elif vartype == datetime.date:
					var = datetime.datetime.strptime(var, '%d-%b-%Y').date()
					
				elif vartype == 'file':
					file = open(var, 'rb')
					var = file.read()
					file.close()	
					
			except:
				var = ''			

		if var:
			for i in queries:
				curs.execute(i[0]%(var))
				i[1] = len(curs.fetchall())
				
				if ((i[1] == i[2]) == i[3]):
					var = ''				
		else:
			for i in queries:
				if len(i) != 5 and ((i[1] == i[2]) == i[3]):
					if i[1] == 0:
						i[1] = 1
					else:
						i[1] = 0
						
				elif len(i) == 5:
					i[1] = i[4]

		if (type(notlike) == dict and var in notlike) or var == notlike:
			var = ''		

		if var and newval and type(notlike) == dict:
			notlike[var] = newval
			
	return var

def func1(curs, connection):
	print('NEW VEHICLE REGISTRATION')

	select = 'y'
	while select == 'y':#if this option is selected, proceed to fill in all required information in order to fill in the tables.
		SIN = {}		
		owner_id = validity("Please enter the primary owner's SIN: ", "Unknown SIN, please try again: ", 15, str, [], '', curs, connection, [["SELECT sin FROM people WHERE sin = '%s'", 1, 0, True]], 'y', SIN)	
		
		car_id = validity("Please enter the car's serial number: ", [["Serial number already registered, please use another: ", 0], "Please enter a valid serial number: "], 15, str, [], '', curs, connection, [["SELECT serial_no FROM vehicle WHERE serial_no = '%s'", 0, 0, False]], '', 'NULL')
		
		maker = validity("Please enter the car's maker: ", "Please enter a valid car maker: ", 20, str)
		model = validity("Please enter the car's model: ", "Please enter a valid car model: ", 20, str)
		year = validity("Please enter the car's year: ", "Please enter a valid year: ", 4, int)
		color = validity("Please enter the car's color: ", "Please enter a valid color: ", 10, str)
		
		type_id = validity("Please enter the car's type_id: ", "Unknown type_id, please try again: ", 10, int, [], '', curs, connection, [["SELECT type_id FROM vehicle_type WHERE type_id = '%d'", 1, 0, True]])
		
		# Keeps asking if there are any other owners to add to the vehicle
		while True:
			choice = validity("Are there any other (non-primary) owners? y/n: ", "Please input a valid choice: ", 1, str, ['y', 'n'], 'lower')
			
			if choice == 'n':
				break
			
			else:
				secondary_id = validity("Please enter the non-primary owner's SIN: ", [["Unknown SIN, please try again: ", 0], "SIN already received, please try another: "], 15, str, [], '', curs, connection, [["SELECT sin FROM people WHERE sin = '%s'", 0, 0, True, 0]], 'n', SIN)	
		
		curs.execute("Insert into vehicle "
                                     "values('%s','%s','%s',%d,'%s','%d')"%(car_id, maker, model, year, color, type_id))#insert statement for vehicle table
	
		for i in SIN:
			curs.execute("Insert into owner "
                                     "values('%s', '%s', '%s')"%(i, car_id, SIN[i]))							
			
		connection.commit()							
		
		print('New vehicle, %s, successfully registered'%(car_id))
		select = validity("Do you want to register another vehicle? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')

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
		
		vehicle_id = validity("Please enter the car's serial number: ",  "Please enter a valid serial number: ", 15, str, [], '', curs, connection, [["SELECT serial_no FROM vehicle WHERE serial_no = '%s'", 1, 0, True]])
				
		seller_id = validity("Please enter the primary seller's SIN: ", [["Unknown SIN, please try again: ", 0], "This SIN is not the primary owner of this vehicle, please try again: "], 15, str, [], '', curs, connection, [["SELECT sin FROM people WHERE sin = '%s'", 0, 0, True, 0], ["SELECT owner_id FROM owner where vehicle_id = " + "'%s'"%(vehicle_id) + " and owner_id = '%s' and is_primary_owner = 'y'", 0, 0, True]], 'y', SIN)		
		
		buyer_id = validity("Please enter the primary buyer's SIN: ", [["Unknown SIN, please try again: ", 0], "SIN already received, please try another: "], 15, str, [], '', curs, connection, [["SELECT sin FROM people WHERE sin = '%s'", 0, 0, True, 0]], 'y', SIN)
		
		del SIN[seller_id]
		
		# Get previous sale date of vehicle
		curs.execute("SELECT max(s_date) FROM auto_sale WHERE vehicle_id = '%s'"%(vehicle_id))
		prev = curs.fetchall()
		
		if prev[0][0]:
			prev_date = prev[0][0].date()
		else:
			prev_date = None

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
		while True:
			choice = validity("Are there any other (non-primary) owners? y/n: ", "Please input a valid choice: ", 1, str, ['y', 'n'], 'lower')
			
			if choice == 'n':
				break
			else:
				secondary_id = validity("Please enter the non-primary owner's SIN: ", [["Unknown SIN, please try again: ", 0], "SIN already received, please try another: "], 15, str, [], '', curs, connection, [["SELECT sin FROM people WHERE sin = '%s'", 0, 0, True, 0]], 'n', SIN)		
		
		curs.execute("DELETE FROM owner WHERE vehicle_id = '%s'" %(vehicle_id));

		for i in SIN:
			curs.execute("Insert into owner "
			             "values('%s', '%s', '%s')"%(i, vehicle_id, SIN[i]))			
		
		curs.execute("Insert into auto_sale "
                                     "values(%d, '%s', '%s','%s', '%s', %f)"%(transaction_id, seller_id, buyer_id, vehicle_id, s_date.strftime('%d-%b-%Y'), price));
		
		connection.commit()								

		print('Sale successfully completed as transaction_id: %s'%(transaction_id))
		more = validity("Do you want to make another transaction? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')
	

def func3(curs, connection):
	print('DRIVER LICENCE REGISTRATION')
	#drive_licence( licence_no,sin,class,photo,issuing_date,expiring_date)
	
	cont = 'y'
	while cont == 'y':
		person_id = validity("Please input an SIN to register: ", [["Unknown SIN, please try again: ", 0], "SIN already registered, please use another: "], 15, str, [], '', curs, connection, [["SELECT sin FROM people WHERE sin = '%s'", 0, 0, True, 0], ["SELECT sin FROM drive_licence WHERE sin = '%s'", 0, 0, False]])

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
		cont = validity("Do you want to register another licence? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')	

def func4(curs, connection):
	#subroutine header
	
	print('VIOLATION RECORD')
	
	#ticket( ticket_no,violator_no,vehicle_id,office_no,vtype,vdate,place,descriptions) <-- table
	#error handling!!!!!!!!!
	
	more = 'y'
	while more == 'y':
		
		#Randomly generating ticket_no in the range of (0,99999999)
		#Check it's unique constraint by select all ticket_no that are already in the table and check
		#if the ticket_no is already inside --> yes: generate a new one | no: this is the new one		
		ticket_no_list=[]
		curs.execute("select ticket_no from ticket")
		rows = curs.fetchall()
		for row in rows:
			ticket_no_list.append(row[0])
		ticket_no = random.randint(0,99999999)
		while ticket_no in ticket_no_list:
			ticket_no = random.randint(0,99999999)
			
		#Insert the violator_No into the table, note that the violator_no is a person's SIN
		#So we need to check the parent key
		#By select the SIN that equals to the violator_no in the table of people
		#See if the query got zero length(Because SIN is also a primary key)		
			
		violator_no = validity("Please enter the violator's SIN: ", "Please enter a valid violator's SIN in 15 digits: ", 15, str)
		curs.execute("select people.sin from people where people.sin = '%s'"%(violator_no))
		parentkeys = curs.fetchall()
		while len(parentkeys) == 0:
			print("Parent key not found!Try it again")
			violator_no = validity("Please enter the violator's SIN: ", "Please enter a valid violator's SIN in 15 digits: ", 15, str)
			curs.execute("select people.sin from people where people.sin = '%s'"%(violator_no))
			parentkeys = curs.fetchall()
		
		#Insert the vehicle_id into the table, note that the violator_no is a vehicle's serial_no
		#So we need to check the parent key
		#By select the vehicle_id that equals to the serial_no in the table of vehicle
		#See if the query got zero length(Because serial_no is also a primary key)			
		
		vehicle_id = validity("Please enter the vehicle serial_no: ", "Please enter a valid vehicle serial_no in 15 digits: ", 15, str)
		curs.execute("select serial_no from vehicle where serial_no = '%s'"%(vehicle_id))
		parentkeys = curs.fetchall()
		while len(parentkeys) == 0:
			print("Parent key not found!Try it again")
			vehicle_id = validity("Please enter the vehicle serial_no: ", "Please enter a valid vehicle serial_no in 15 digits: ", 15, str)
			curs.execute("select serial_no from vehicle where serial_no = '%s'"%(vehicle_id))
			parentkeys = curs.fetchall()
			
		#Same as what we did above,but note that the office_no shouldn't be the same as violator_no
		#Thus we have to check if the office_no == violator_no
			
		office_no = validity("Please enter the officer's SIN: ", "Please enter a valid officer's SIN in 15 digits: ", 15, str)
		curs.execute("select people.sin from people where people.sin = '%s'"%(office_no))
		parentkeys = curs.fetchall()
		while (len(parentkeys) == 0) or (office_no == violator_no):
			if (len(parentkeys) == 0):
				print("Parent key not found!Try it again")
			if (office_no == violator_no):
				print("You shouldn'd be the same person as the violator")
			office_no = validity("Please enter the officer's SIN: ", "Please enter a valid officer's SIN in 15 digits: ", 15, str)
			curs.execute("select people.sin from people where people.sin = '%s'"%(office_no))
			parentkeys = curs.fetchall()		
			
		#Same as what we did above
			
		vtype = validity("Please enter the violation type: ", "Please enter a valid violation type in 10 digits: ", 10, str)
		curs.execute("select ticket_type.vtype from ticket_type where ticket_type.vtype = '%s'"%(vtype))
		parentkeys = curs.fetchall()
		while len(parentkeys) == 0:
			print("Parent key not found!Try it again")
			vtype = validity("Please enter the violation type: ", "Please enter a valid violation type in 10 digits: ", 10, str)
			curs.execute("select ticket_type.vtype from ticket_type where ticket_type.vtype = '%s'"%(vtype))		
			parentkeys = curs.fetchall()
			
		#When we insert the violation date, we have to notice that the violation date should be later than the first transaction date
		#Therefore, we select the minimum s_date of the sepecific vehicle in the violation
		#and then check if the time is correct			
		
		
		
		curs.execute("SELECT min(s_date) FROM auto_sale WHERE vehicle_id = '%s'"%(vehicle_id))
		prev = curs.fetchall()
		if prev:
			prev_date = prev[0][0].date()
		vdate = ''
		first = True
		while not vdate:
			if first:
				vdate = validity("Please enter the violation date (DD-MON-YYYY): ", "Please enter a valid date: ", 11, datetime.date)
				first = False
			else:
				vdate = validity("You can't time travel (last sold on: %s), try again: "%(prev_date.strftime('%d-%b-%Y')), "Please enter a valid date: ", 11, datetime.date)
						
			if prev_date and vdate < prev_date:
				vdate = ''	
				
		#Place and descriptions is not primary key nor an attribute with parent key, so we only need to check general exceptions
		
		place = validity("Please enter the location of the violation: ", "Please enter a valid place in 20 digits: ", 20, str)
		descriptions = validity("Please enter the descriptions of the violation: ", "Please enter a valid description in 1024 digits: ", 1024, str)	
		
		
		#After get all the data correct, just insert ,note that we have to convert the date datatype
		curs.execute("SELECT owner_id from owner where owner.vehicle_id = '%s' and is_primary_owner = 'y'"%(vehicle_id))
		primary_owner = curs.fetchone()
		curs.execute("Select name from people where SIN = '%s'"%(primary_owner))
		name = curs.fetchone()
		primary_owner_l = list(primary_owner)
		primary_owner_list = primary_owner_l[0].split(' ')
		primary_owner = ''.join(primary_owner_list)
		print("The primary owner id of this car is '%s'"%(primary_owner))
		print("His name is '%s'"%(name))
		print(vtype)
		if primary_owner != violator_no:
			print("The violator is not the primary owner! We have to register another person")
		else:
			print("That's it! He's the right person")
			
		if vtype in ['Parking','Speeding','Crossing','Accrosing']:
			violator_no = primary_owner
		
		curs.execute("Insert into ticket values" 
			     "(%d,'%s','%s','%s','%s','%s','%s','%s')"%(ticket_no,violator_no,vehicle_id,office_no,vtype,vdate.strftime('%d-%b-%Y'),place,descriptions)) 
		connection.commit()
		print("ticket is already recorded as %d" %(ticket_no))
		
		#Ask if there're more tickets to record
		
		more = validity("Do you want to register another ticket? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')
	

def func5(curs, connection):
	print('SEARCH THE DATABASE')	
	print('Please pick a search option')
	again = 'y'
	while again == 'y':
		print(' 1 - Driver Info \n 2 - List all violation records received by a person\n 3 - Print out the vehicle_history\n')
		inp = validity("Please select a number option from the options above: ", "Please select a valid option: ", 1, str, ['1','2','3'])
		
		#check the kind of search being executed(name, licence searchfor personal info.)
		if inp == '1':
			#choose the search type, name or licence no
			selection = input(' 1 - search by name \n 2 - search by licence number \n')
			
			#search by name query
			if selection == '1':
				search_by = validity('Please enter name: ', 'Please enter a valid name: ', 40, str)					
				
				searchf10 = ("(SELECT name, dl.licence_no, addr, birthday, class, c_id FROM people p, driving_condition dc, restriction r, drive_licence dl WHERE p.sin = dl.sin AND r.r_id = dc.c_id AND r.licence_no = dl.licence_no AND (p.name like '%s' or p.name like '%s'))"%('%'+search_by+'%', \
				                                                                                                                                                                                                                                                                  '%'+search_by.title()+'%'))
				curs.execute(searchf10)
				v = curs.fetchall()
				
				#for every driver info, return the correct output
				for i in v:
					dates = i[3].date()
					print(' Name: %s \n Drivers licence: %s \n Address: %s \n Birthday: %s \n Class: %s \n Restriction: %s \n' %(i[0], i[1].split()[0], i[2], str(dates.day)+'-'+monthdic[dates.month]+'-'+str(dates.year), i[4].split()[0], i[5]))	
				if len(v) == 0:
					print('###No results were found matching your search criteria###')						
				print('thanks')
			#search by licence query
			if selection == '2':
				search_by = input('please enter the licence number: ').upper()
				searchf11 = ("(SELECT name, dl.licence_no, addr, birthday, class, c_id FROM people p, driving_condition dc, drive_licence dl, restriction r WHERE p.sin = dl.sin AND r.r_id = dc.c_id AND r.licence_no = dl.licence_no AND dl.licence_no like '%s'" %('%'+search_by+'%'));
				(curs.execute(searchf11))
				v = curs.fetchall()
				
				for i in v:
					dates = i[3].date()
					print(' Name: %s \n Drivers licence: %s \n Address: %s \n Birthday: %s \n Class: %s \n Restriction: %s \n' %(i[0], i[1].split()[0], i[2],str(dates.day)+'-'+monthdic[dates.month]+'-'+str(dates.year), i[4].split()[0], i[5]))
				if len(v) == 0:
					print('###No results were found matching your search criteria###')	
					
		#check the kind of search being executed(SIN, licence search for tickets)
		if inp == '2':
			selection = input(' 1 - search by SIN \n 2 - search by licence number \n')#choose the search type, SIN or licence no
			
			#query the database for the required info.
			if selection == '1':
				search_by = input('please enter the SIN: ')
				searchf01 = "(SELECT ticket_no, t.vtype, fine, vdate, descriptions, t.place FROM ticket t, ticket_type tt, people p WHERE t.vtype = tt.vtype AND p.sin = t.violator_no and p.sin = '%s')"%(search_by);
				(curs.execute(searchf01))
				v = curs.fetchall()
			
				#for every driver info, return the correct output	
				for i in v:
					###allows us to return only the date and not all the date/time format
					dates = i[3].date()
					print(' Ticket number: %d \n Violation code: %s \n Fine: %d \n Date: %s \n Description: %s \n Place: %s \n ' %(i[0], i[1].split()[0], i[2],str(dates.day)+'-'+monthdic[dates.month]+'-'+str(dates.year), i[4], i[5]))
				curs.execute("select p.name from people p where sin = %s"%((search_by)))
				person = curs.fetchone()
				
				print("%s has %d tickets total"%(person[0], len(v)))
				if len(v) == 0:
					print('###No results were found matching your search criteria###')							
				
			if selection == '2':#query the database for the required info.
				search_by = input('please enter the licence number: ').upper()
				searchf02 = "(SELECT ticket_no, t.vtype, fine, vdate, descriptions, t.place FROM ticket t, ticket_type tt, people p, drive_licence WHERE t.vtype = tt.vtype AND p.sin = t.violator_no AND drive_licence.sin = p.sin AND drive_licence.licence_no = '%s')"%(search_by);
				
				(curs.execute(searchf02))
				v = curs.fetchall()
				#for every infraction commited, return the correct output						
				for i in v:
					dates = i[3].date()
					print(' Ticket number: %d \n Violation code: %s \n Fine: %d \n Date: %s \n Description: %s \n Place: %s \n' %(i[0], i[1].split()[0], i[2],str(dates.day)+'-'+monthdic[dates.month]+'-'+str(dates.year), i[4], i[5]))
				curs.execute("select p.name from people p, drive_licence dl where dl.sin = p.sin AND dl.licence_no = '%s'"%((search_by)))
				person = curs.fetchone()
												
				print("%s has %d tickets total"%(person[0], len(v)))							
				if len(v) == 0:
					print('###No results were found matching your search criteria###')
					
		if inp == '3':#query the database for the required info.
			select_by = input('Please enter the vehicle licence plate: ').upper()
			searchf03 = "(SELECT vehicle_no, number_sales, average_price, total_tickets FROM ((SELECT v.serial_no as vehicle_no, COUNT(DISTINCT s.transaction_id) AS number_sales , AVG(s.price) AS average_price FROM auto_sale s, vehicle v, vehicle_type vt, ticket t WHERE s.vehicle_id = v.serial_no and v.type_id = vt.type_id and v.serial_no = '%s' GROUP BY v.serial_no) f left join (SELECT COUNT(t.vtype) as total_tickets, v.serial_no as car FROM vehicle v left join ticket t on v.serial_no = t.vehicle_id GROUP BY v.serial_no) r on f.vehicle_no = r.car))"%(select_by);
			
			(curs.execute(searchf03))
			v = curs.fetchall()
																
			#for every vehicle output that vehicle's history
			for i in v:#for every result in query, output the result.
				print(' Vehicle Serial Number: %s \n Times Sold: %d \n Average sale price: %d \n Total Tickets: %d \n ' %((i[0]), int(i[1]), int(i[2]), int(i[3])))	
				
			#check for outut of the query, otherwise tell user nothing matched
			if len(v) == 0:
				print('###No results were found matching your search criteria###')	
				
		#check if another search is to be made.
		again = input('do you want to do another search? y/n: ')
		while again not in ['y', 'n']:#check for proper output.
			print('please press "y" or "n"')
			again = input('do you want to do another search?:')
			

def main():
	#username and password.  This will be general access for anyone wanting to query the database.
	user= input('Username:')
	password = getpass.getpass()
	
	try:	
		#connection string
		stringconn = user+'/'+password + '@gwynne.cs.ualberta.ca:1521/CRS'
		connection = cx_Oracle.connect(stringconn)
		curs = connection.cursor()

		options = {1: func1, 2: func2, 3: func3, 4: func4, 5: func5}
		while True:
			print(' 1 - New Vehicle Registration\n 2 - Auto Transaction\n 3 - Driver Licence Registration\n 4 - Violation Record\n 5 - Search the database\n 6 - exit\n')
			choice = validity("Please select a number option from the options above: ", "Please select a valid option: ", 1, int, ['1','2','3','4','5','6'])		
			try:
				options[choice](curs, connection)
			except:
				break
			
			choice = validity("Do you want to continue? y/n: ", "Please input a valid option: ", 1, str, ['y', 'n'])
			
			if choice == 'n':
				break
			else:
				print()		
			
		print('Have a nice day!')#print exit message		
		curs.close()#deconstruct cursor
		connection.close()#close connection.
		

	#DISPLAY ANY ERROR MESSAGES THAT OCCUR DURING THE EXECUTION OF THE QUERIES AND/OR MANAGEMENT OF THE DATABASE
	except cx_Oracle.DatabaseError as exc:
		error = exc.args
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "Oracle message:", error.message)
	
		
if __name__ == "__main__":
	main()#call main function