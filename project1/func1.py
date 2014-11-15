from validity import *
import os
def func1(curs, connection):

	select = 'y'
	while select == 'y':#if this option is selected, proceed to fill in all required information in order to fill in the tables.
		os.system('cls' if os.name == 'nt' else 'clear')
		print('NEW VEHICLE REGISTRATION')
		print()
		SIN = {}		
		owner_id = validity("Please enter the primary owner's SIN: ", "Unknown SIN, please try again: ", 15, str, [], '', curs, connection, [["SELECT sin FROM people WHERE lower(sin) = lower('%s')", 1, 0, True, 0]], 'y', SIN)	
		
		car_id = validity("Please enter the car's serial number: ", [["Serial number already registered, please use another: ", 0], "Please enter a valid serial number: "], 15, str, [], '', curs, connection, [["SELECT serial_no FROM vehicle WHERE lower(serial_no) = lower('%s')", 0, 0, False]], '', 'NULL')
		
		maker = validity("Please enter the car's maker: ", "Please enter a valid car maker: ", 20, str)
		model = validity("Please enter the car's model: ", "Please enter a valid car model: ", 20, str)
		year = validity("Please enter the car's year: ", "Please enter a valid year: ", 4, int)
		color = validity("Please enter the car's color: ", "Please enter a valid color: ", 10, str)
		
		type_id = validity("Please enter the car's type_id: ", "Unknown type_id, please try again: ", 10, int, [], '', curs, connection, [["SELECT type_id FROM vehicle_type WHERE lower(type_id) = lower('%d')", 1, 0, True]])
		
		# Keeps asking if there are any other owners to add to the vehicle
		while True:
			choice = validity("Are there any other (non-primary) owners? y/n: ", "Please input a valid choice: ", 1, str, ['y', 'n'], 'lower')
			
			if choice == 'n':
				break
			
			else:
				secondary_id = validity("Please enter the non-primary owner's SIN: ", [["Unknown SIN, please try again: ", 0], "SIN already received, please try another: "], 15, str, [], '', curs, connection, [["SELECT sin FROM people WHERE lower(sin) = lower('%s')", 0, 0, True, 0]], 'n', SIN)	
		
		curs.execute("Insert into vehicle "
                                     "values('%s','%s','%s',%d,'%s','%d')"%(car_id, maker, model, year, color, type_id))#insert statement for vehicle table
	
		for i in SIN:
			curs.execute("Insert into owner "
                                     "values('%s', '%s', '%s')"%(i, car_id, SIN[i]))							
			
		connection.commit()							
		
		print('New vehicle, %s, successfully registered'%(car_id))
		select = validity("Do you want to register another vehicle? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')
		print()
