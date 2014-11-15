from validity import *
import cx_Oracle
import random
import string
import os

def func3(curs, connection):
	#drive_licence( licence_no,sin,class,photo,issuing_date,expiring_date)
	
	cont = 'y'
	while cont == 'y':
		os.system('cls' if os.name == 'nt' else 'clear')
		print('LICENCE REGISTRATION')
		print()
		person_id = validity("Please input an SIN to register: ", [["Unknown SIN, please try again: ", 0], "SIN already registered, please use another: "], 15, str, [], '', curs, connection, [["SELECT sin FROM people WHERE lower(sin) = lower('%s')", 0, 0, True, 0], ["SELECT sin FROM drive_licence WHERE lower(sin) = lower('%s')", 0, 0, False]])
		curs.execute("select sin from people where lower(sin) = lower('%s')"%(person_id))
		person_id = curs.fetchone()[0].strip()
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
			curs.execute("SELECT licence_no FROM drive_licence WHERE lower(licence_no) = lower('%s')"%(licence_no))
			licence_conflict = curs.fetchall()
			
		curs.setinputsizes(photo=cx_Oracle.BLOB)
		curs.execute("Insert into drive_licence "
                                     "values(:licence_no, :person_id, :class, :photo, :issuing_date, :expiring_date)", {'licence_no':licence_no, 'person_id':person_id, 'class':drive_class, 'photo':photo, 'issuing_date':issuing_date.strftime('%d-%b-%Y'), 'expiring_date':expiring_date.strftime('%d-%b-%Y')})
		connection.commit()
		print('Licence registered successfully as %s'%(licence_no))	
		cont = validity("Do you want to register another licence? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')	
		print()