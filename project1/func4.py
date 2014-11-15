from validity import *
import os
import random

def func4(curs, connection):	
	more = 'y'
	curs.execute("select vtype from ticket_type")
	ticks=  curs.fetchall()
	tt = []
	

	while more == 'y':
		os.system('cls' if os.name == 'nt' else 'clear')
		print('VIOLATION RECORD')
		print()
		SIN = {}
		#Insert the vehicle_id into the table, note that the violator_no is a vehicle's serial_no		
		
		vehicle_id = validity("Please enter the car's serial number: ",  "Please enter a valid serial number: ", 15, str, [], '', curs, connection, [["SELECT serial_no FROM vehicle WHERE lower(serial_no) = lower('%s')", 1, 0, True]])
		curs.execute("select serial_no from vehicle where lower(serial_no) = lower('%s')"%(vehicle_id))
		vehicle_id = curs.fetchone()[0].strip()	
		
		inp = validity('Display ticket types? y/n: ' ,'Please pick a valid input: ', 1, str, ['y','n'])
		if inp == 'y':
			for i in ticks:
				print(i[0].strip())
			vtype = validity("Please enter the violation type from the options above: ",  "Please enter a valid violation type: ", 10, str, [], '', curs, connection, [["SELECT vtype FROM ticket WHERE lower(vtype) = lower('%s')", 1, 0, True]])
		else:
			vtype = validity("Please enter the violation type: ",  "Please enter a valid violation type: ", 10, str, [], '', curs, connection, [["SELECT vtype FROM ticket WHERE lower(vtype) = lower('%s')", 1, 0, True]])
			
		curs.execute("select ticket_type.vtype from ticket_type where lower(ticket_type.vtype) = lower('%s')"%(vtype))
		
		#find the original value for the violation
		vtype = curs.fetchone()[0].strip()
		
		identifible = validity("Can you identify the driver? y/n: ", "Please enter a valid option: ",1,str,['y', 'n'],'lower')
		
		if identifible == 'y':
			
			#Insert the violator_No into the table, note that the violator_no is a person's SIN
			#So we need to check the parent key
			#By select the SIN that equals to the violator_no in the table of people
			#See if the query got zero length(Because SIN is also a primary key)
			violator_no = validity("Please enter the violator's SIN: ", "Please enter a valid SIN: ", 15, str, [], '', curs, connection, [["SELECT sin FROM people WHERE lower(sin) = lower('%s')", 0, 0, True, 0]], 'y', SIN)						
				
		if identifible == 'n':
			
			curs.execute("SELECT owner_id from owner where lower(owner.vehicle_id) = lower('%s') and lower(is_primary_owner) = lower('y')"%(vehicle_id))
			primary_owner_SIN = curs.fetchone()
			curs.execute("Select name from people where lower(sin) = lower('%s')"%(primary_owner_SIN))
			name = curs.fetchone()
			primary_owner_l = list(primary_owner_SIN)
			primary_owner_list = primary_owner_l[0].split(' ')
			primary_owner_SIN = ''.join(primary_owner_list)
			print("Primary Owner SIN: %s \nName: %s"%(primary_owner_SIN, name[0]))
			violator_no = primary_owner_SIN
			SIN[violator_no] = 'y'
		
		#Randomly generating ticket_no in the range of (0,99999999)
		#Check it's unique constraint by select all ticket_no that are already in the table and check
		#if the ticket_no is already inside --> yes: generate a new one | no: this is the new one
		office_no = validity("Please enter the officer's SIN: ", [["Please enter a valid SIN: ", 0], "SIN already received, please try another: "], 15, str, [], '', curs, connection, [["SELECT sin FROM people WHERE lower(sin) = lower('%s')", 0, 0, True, 0]], 'y', SIN)
		
		ticket_no = False
		ticket_conflict = 0
		while not ticket_no or ticket_conflict:
			ticket_no = random.randint(0,99999999)
			curs.execute("select ticket_no from ticket where ticket_no = '%s'"%(ticket_no))
			ticket_conflict = len(curs.fetchall())

		#When we insert the violation date, we have to notice that the violation date should be later than the first transaction date
		#Therefore, we select the minimum s_date of the sepecific vehicle in the violation
		#and then check if the time is correct			
		
		curs.execute("SELECT min(s_date) FROM auto_sale WHERE lower(vehicle_id) = lower('%s')"%(vehicle_id))
		prev = curs.fetchall()
		if prev:
			prev_date = prev[0][0].date()
			print('Vehicle %s was last sold on %s'%(vehicle_id, prev_date.strftime("%d-%b-%Y")))
		else:
			prev_date = None
			print('Vehicle %s has never been sold'%(vehicle_id))			
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
		
		curs.execute("Insert into ticket values" 
			     "(%d,'%s','%s','%s','%s','%s','%s','%s')"%(ticket_no,violator_no,vehicle_id,office_no,vtype,vdate.strftime('%d-%b-%Y'),place,descriptions)) 
		connection.commit()
		
		print("Ticket has been recorded as %d" %(ticket_no))
		
		#Ask if there're more tickets to record
		more = validity("Do you want to register another ticket? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')
		print()