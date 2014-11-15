from validity import *
import datetime
import sys
import os

def func5(curs, connection):
	again = 'y'
	while again == 'y':
		os.system('cls' if os.name == 'nt' else 'clear')
		print('SEARCH THE DATABASE')	
		print()
		print(' 1 - Driver Info \n 2 - List all violation records received by a person\n 3 - Print out the vehicle_history\n')
		#inp = input(' 1 - Driver Info \n 2 - List all violation records received by a person\n 3 - Print out the vehicle_history\n')
		inp = validity("Please select a search option: ", "Please enter a valid option: ", 1, str, ['1','2','3'])
		#check the kind of search being executed(name, licence searchfor personal info.)
		if inp == '1':
			ppl = []
			#choose the search type, name or licence no
			#selection = input(' 1 - search by name \n 2 - search by licence number \n')
			print(" 1 - search by name \n 2 - search by licence number \n")
			selection = validity("Please select a search option: ", "Please enter a valid option: ", 1, str, ['1','2'])	
			#search by name query
			if selection == '1':
				search_by = input('Please enter name: ')
				searchf10 = ("SELECT name, x.licence_no, addr, birthday, x.class, x.r_id, x.description FROM (SELECT dl.licence_no, dl.sin, dl.class, r.r_id, r.description FROM drive_licence dl left join (SELECT * FROM restriction r, driving_condition dc WHERE r.r_id = dc.c_id) r on dl.licence_no = r.licence_no) x, people p WHERE x.sin = p.sin AND regexp_like(name, '%s', 'i')"%(search_by))
				curs.execute(searchf10)
				v = curs.fetchall()
				#for every driver info, return the correct output
				print()
				os.system('cls' if os.name == 'nt' else 'clear')
				
				print('Results for: %s'%(search_by))
				for i in v:
					#tmpsearch = ("SELECT r_id FROM restriction r WHERE r.licence_no = '%s'"%(i[1].strip())
					#curs.execute(tmpsearch)
					#x = curs.fetchall()
					if i[5] == None:
						res = 'No Restriction'
					else:
						res = i[6]
					dates = i[3].date()
					print('Name: %s \n Drivers licence: %s \n Address: %s \n Birthday: %s \n Class: %s \n Restriction: %s \n ' %(i[0], i[1].strip(), i[2], dates.strftime('%d-%b-%Y'), i[4].strip(), res))	
				if len(v) == 0:
					print('###No results were found matching your search criteria###')						
					print()
			#search by licence query
			if selection == '2':
				search_by = validity("please enter a licence number: ", "Please enter something valid: ", 15, str, [], 'upper')	
				searchf11 = ("SELECT name, x.licence_no, addr, birthday, x.class, x.r_id, x.description FROM (SELECT dl.licence_no, dl.sin, dl.class, r.r_id, r.description FROM drive_licence dl left join (SELECT * FROM restriction r, driving_condition dc WHERE r.r_id = dc.c_id) r on dl.licence_no = r.licence_no) x, people p WHERE x.sin = p.sin AND regexp_like(x.licence_no, '%s', 'i')"%(search_by))
				curs.execute(searchf11)
				v = curs.fetchall()
				print()
				os.system('cls' if os.name == 'nt' else 'clear')
				print('Results for: %s'%(search_by))				
				for i in v:
					if i[5] == None:
						res = 'No Restriction'
					else:
						res = i[6]					
					dates = i[3].date()
					print('Name: %s \n Drivers licence: %s \n Address: %s \n Birthday: %s \n Class: %s \n Restriction: %s \n' %(i[0], i[1].strip(), i[2],dates.strftime('%d-%b-%Y'), i[4].strip(), res))
				if len(v) == 0:
					print('###No results were found matching your search criteria###')	
					print()
		#check the kind of search being executed(SIN, licence search for tickets)
		if inp == '2':
			#selection = input(' 1 - search by SIN \n 2 - search by licence number \n')#choose the search type, SIN or licence no
			print(' 1 - search by SIN \n 2 - search by licence number \n')
			selection = validity("Please select a search option: ", "Please enter a valid option: ", 1, str, ['1','2'])			
			
			#query the database for the required info.
			if selection == '1':
				search_by = validity("please enter a sin: ", "Please enter something valid: ", 15, str)	
				searchf01 = "(SELECT p.name, ticket_no, t.vtype, fine, vdate, descriptions, t.place FROM ticket t, ticket_type tt, people p WHERE t.vtype = tt.vtype AND p.sin = t.violator_no and regexp_like(p.sin, '%s', 'i'))"%(search_by);
				(curs.execute(searchf01))
				v = curs.fetchall()
				print()
				os.system('cls' if os.name == 'nt' else 'clear')
				print('Results for: %s'%(search_by))				
				#for every driver info, return the correct output	
				for i in v:
					#allows us to return only the date and not all the date/time format
					dates = i[4].date()
					print('Name: %s \n Ticket number: %d \n Violation code: %s \n Fine: %d \n Date: %s \n Description: %s \n Place: %s \n ' %(i[0],i[1], i[2].strip(),i[3],dates.strftime('%d-%b-%Y'), i[5], i[6]))
					
				if len(v) == 0:
					print('###No results were found matching your search criteria###')							
					print()
			if selection == '2':#query the database for the required info.
				search_by = validity("please enter a licence number: ", "Please enter something valid: ", 15, str, [], 'upper')	
				searchf02 = "(SELECT p.name, ticket_no, t.vtype, fine, vdate, descriptions, t.place FROM ticket t, ticket_type tt, people p, drive_licence dl WHERE t.vtype = tt.vtype AND p.sin = t.violator_no AND dl.sin = p.sin AND regexp_like(dl.licence_no, '%s', 'i'))"%(search_by);
				
				(curs.execute(searchf02))
				v = curs.fetchall()
				#for every infraction commited, return the correct output
				print()
				os.system('cls' if os.name == 'nt' else 'clear')
				print('Results for: %s'%(search_by))	
				
				for i in v:
					#print(i)
					dates = i[4].date()
					print('Name: %s \n Ticket number: %d \n Violation code: %s \n Fine: %d \n Date: %s \n Description: %s \n Place: %s \n ' %(i[0],i[1], i[2].strip(),i[3],dates.strftime('%d-%b-%Y'), i[5], i[6]))
					
				#curs.execute("select p.name from people p, drive_licence dl where dl.sin = p.sin AND dl.licence_no = '%s'"%((search_by)))
				#person = curs.fetchone()
																		
				if len(v) == 0:
					print('###No results were found matching your search criteria###')
					print()														
		if inp == '3':#query the database for the required info.
			search_by = validity("please enter a vehicle serial number: ", "Please enter something valid: ", 15, str, [], 'upper')	
			searchf03 = "(SELECT vehicle_no, number_sales, average_price, total_tickets FROM ((SELECT v.serial_no as vehicle_no, COUNT(DISTINCT s.transaction_id) AS number_sales , AVG(s.price) AS average_price FROM auto_sale s, vehicle v, vehicle_type vt, ticket t WHERE s.vehicle_id = v.serial_no and v.type_id = vt.type_id and regexp_like(v.serial_no, '%s', 'i') GROUP BY v.serial_no) f left join (SELECT COUNT(t.vtype) as total_tickets, v.serial_no as car FROM vehicle v left join ticket t on v.serial_no = t.vehicle_id GROUP BY v.serial_no) r on f.vehicle_no = r.car))"%(search_by);
			
			(curs.execute(searchf03))
			v = curs.fetchall()							
			#for every vehicle output that vehicle's history
			print()
			os.system('cls' if os.name == 'nt' else 'clear')
			print('Results for: %s'%(search_by))			
			for i in v:#for every result in query, output the result.
				print('Vehicle Serial Number: %s \n Times Sold: %d \n Average sale price: %d \n Total Tickets: %d \n ' %((i[0]), int(i[1]), int(i[2]), int(i[3])))	
				
			#check for outut of the query, otherwise tell user nothing matched
			if len(v) == 0:
				print('###No results were found matching your search criteria###')
				print()
				
		#check if another search is to be made.
		again = validity("Do you want do another search? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')	
		print()