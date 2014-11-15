import sys
import cx_Oracle
import getpass
import random

def main():
	user= 'lingbo' #input()(uncomment for final code before submission
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
				print('NEW VEHICLE REGISTRATION')
				select = 'y'
				while select == 'y':#if this option is selected, proceed to fill in all required information in order to fill in the tables.
					owner_id = int(input("Please enter the owner's sin number: "))
					car_id = (input("Please enter the car's serial number: "))
					maker = input("Please enter the car's maker: ")
					model = input("Please enter the car's model: ")
					year = int(input("Please enter the car's year: "))
					color = input("Please enter the car's color: ")
					type_id = int(input("Please enter the car's type_id: "))
					primary_owner = input('Is this person the primary owner?   y or n: ').lower()
					while primary_owner not in ['y', 'n']:#check proper input for primary owner.  database only allows 1 char answers.
						print('invalid input: ')
						primary_owner = input('Is this person the primary owner?   y or n: ').lower()
				
					curs.execute("Insert into vehicle "
						     "values('%s','%s','%s',%d,'%s',%d)"%(car_id, maker, model, year, color, type_id))#insert statement for vehicle table
					connection.commit()
					curs.execute("Insert into owner "
						     "values(%d, '%s','%s')"%(owner_id, car_id, primary_owner))#insert statement for owner table				
					connection.commit()
					select = input("type 'y' to register another vehicle,or 'n' to close session: ")#select option to continue or quit this registration loop
				print('new vehicle(s) successfully registered')#when all required vehicles are registered, print confirmation and quit the loop.
				
			
			#this is the code that executes when selection 2 is picked
			if choice == '2':
				print('AUTO TRANSACTION')
				curs.execute("SELECT transaction_id FROM auto_sale")
				transactions = curs.fetchall()
				num = -1
				for i in transactions:
					if i[0]>num:
						num = i[0]
				more = 'y'
				#auto_sale( transaction_id,seller_id, buyer_id, vehicle_id, s_date, price )
				while more == 'y':
					transaction_id = num+1
					seller_id = int(input("Please enter the seller's SIN: "))
					buyer_id = int(input("Please enter the buyer's SIN: "))
					vehicle_id = (input("Please enter the car's serial number: "))
					s_date = (input("Please enter the sale date(DD-MON-YYYY): "))
					price = float(input("Please enter the sale price: "))
					primary_id = input("is the buyer the primary owner? y/n")
					more = input('do you have any other buyers to register to this same vehicle? y/n: ')
					while more == 'y':
						buyer_id = int(input("Please enter the buyer's SIN: "))
						curs.execute("Insert into owner "
							     "values(%d, '%s','%s')"%(buyer_id, vehicle_id, 'n'))#insert statement for owner table	
						connection.commit()
						more = input('do you have any other buyers to register to this same vehicle? y/n: ')
					if seller_id == buyer_id:
						print('you cannot sell yourself a car')
					curs.execute("DELETE FROM owner WHERE vehicle_id = '%s'" %(vehicle_id));
					connection.commit()
					curs.execute("Insert into owner "
						     "values(%d, '%s','%s')"%(buyer_id, vehicle_id, primary_id))#insert statement for owner table	
					connection.commit()
					#auto_sale( transaction_id,seller_id, buyer_id, vehicle_id, s_date, price )
					curs.execute("Insert into auto_sale "
						     "values(%d, %d, %d,'%s', '%s', %f)"%(transaction_id, seller_id, buyer_id, vehicle_id, s_date, price));
					connection.commit()
					curs.execute("Insert into owner "
						     "values(%d, '%s','%s')"%(buyer_id, vehicle_id, primary_id));
					connection.commit()
					more = input('do you want to make another transaction? y/n')
				print('sale successfully completed')
				
			#selection of the third choice option(licence registration)
			if choice == '3':
				'''print('DRIVER LICENCE REGISTRATION')
				#drive_licence( licence_no,sin,class,photo,issuing_date,expiring_date)
				lincence_no = int(input("Please enter the driver's licence number: "))
				person_id= int(input("Please enter the holder's SIN: "))
				drive_class = (input("Please enter the licence class: "))
				issue_date = (input("Please enter the issue date(DD-MON-YYYY): "))
				exp_date = float(input("Please enter the expiry date (DD-MON-YYYY): "))
				photo = input("photo of the driver:")
				curs.execute("Insert into drive_licence "
				             "values(%d,%d,%d,'%s','%s')"%(licence_no, person_id, drive_class, 'photo', issue_date,exp_date))#insert statement for licence table				
				connection.commit()
				print('licence registered successfully')'''
				
				
				
			if choice == '4':
				print('VIOLATION RECORD')
				#ticket( ticket_no,violator_no,vehicle_id,office_no,vtype,vdate,place,descriptions)
				#error handling!!!!!!!!!
				ticket_no_list=[]
				violator_no_list = []
				curs.execute("select people.sin from people")
				rows = curs.fetchall()
				for row in rows:
					print(row[0])
					violator_no_list.append(row[0])
				print(violator_no_list)
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
				
			if choice == '5':
				print('SEARCH THE DATABASE')	
			if choice == '6':
				break
		
			x = input('do you have any more buisness? y/n: ').lower()
				
			if x in ['y', 'yes', 'yeah']:
				print('please select another number option from the options below: ')
				choice = input(' 1 - New Vehicle Registration\n 2 - Auto Transaction\n 3 - Driver Licence Registration\n 4 - Violation Record\n 5 - Search the database\n 6 - exit\n')
			else:
				choice = '6'
				
		connection.close()
		print('Have a nice day!')
		

	except cx_Oracle.DatabaseError as exc:
		error = exc.args
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "Oracle message:", error.message)
	
		
if __name__ == "__main__":
	main()
