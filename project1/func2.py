from validity import *
import os

def func2(curs, connection):
	#auto_sale( transaction_id,seller_id, buyer_id, vehicle_id, s_date, price )
	
	# Get current max transaction_id (transaction_ids increment by 1)
	
	more = 'y'
	while more == 'y':
		os.system('cls' if os.name == 'nt' else 'clear')
		print('AUTO TRANSACTION')
		print()
		SIN = {}
		
		vehicle_id = validity("Please enter the car's serial number: ",  "Please enter a valid serial number: ", 15, str, [], '', curs, connection, [["SELECT serial_no FROM vehicle WHERE lower(serial_no) = lower('%s')", 1, 0, True]])
		curs.execute("select serial_no from vehicle where lower(serial_no) = lower('%s')"%(vehicle_id))
		
		vehicle_id = curs.fetchone()[0].strip()
		
		seller_id = validity("Please enter the primary seller's SIN: ", [["Please enter a valid SIN: ", 0], "This SIN does not own vehicle %s, please try again: "%(vehicle_id)], 15, str, [], '', curs, connection, [["SELECT sin FROM people WHERE sin = '%s'", 0, 0, True, 0], ["SELECT owner_id FROM owner WHERE lower(vehicle_id) = " + "lower('%s')"%(vehicle_id) + " AND lower(owner_id) = lower('%s')", 0, 0, True]], 'y', SIN)		
				
		buyer_id = validity("Please enter the primary buyer's SIN: ", [["Please enter a valid SIN: ", 0], "SIN already received, please try another: "], 15, str, [], '', curs, connection, [["SELECT sin FROM people WHERE lower(sin) = lower('%s')", 0, 0, True, 0]], 'y', SIN)
		
		del SIN[seller_id]

		# Get previous sale date of vehicle
		curs.execute("SELECT max(s_date) FROM auto_sale WHERE vehicle_id = '%s'"%(vehicle_id))
		prev = curs.fetchall()
		
		if prev[0][0]:
			prev_date = prev[0][0].date()
			print('Vehicle %s was last ticketed on %s'%(vehicle_id, prev_date.strftime("%d-%b-%Y")))
		else:
			prev_date = None
			print('Vehicle %s has never been sold'%(vehicle_id))

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
				
		curs.execute("SELECT max(transaction_id) FROM auto_sale")
		
		transactions = curs.fetchall()
		try:
			transaction_id = int(transactions[0][0])
		except:
			transaction_id = 0
		transaction_id += 1
		curs.execute("DELETE FROM owner WHERE vehicle_id = '%s'" %(vehicle_id))

		for i in SIN:
			curs.execute("Insert into owner "
			             "values('%s', '%s', '%s')"%(i, vehicle_id, SIN[i]))			
		curs.execute("Insert into auto_sale "
                                     "values(%d, '%s', '%s','%s', '%s', %f)"%(transaction_id, seller_id, buyer_id, vehicle_id, s_date.strftime('%d-%b-%Y'), price));

		connection.commit()								

		print('Sale successfully completed as transaction_id: %s'%(transaction_id))
		more = validity("Do you want to make another transaction? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')
		print()