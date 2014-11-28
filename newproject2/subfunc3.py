from validity import *
import os
import time
import bsddb3 as bsddb

options = {'btree': bsddb.btopen, 'hash': bsddb.hashopen, 'indexfile': bsddb.btopen}

def subfunc3(data):
    FILE = data[0]
    filetype = data[1]
    answers = data[2]
    
    select = 'y'
    while select == 'y':
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Retrieve records with a given data\n')
        os.system('vim answer')

        try:
            db = options[filetype](FILE,"r")
            
            Given = validity("Please enter your data: ", "Please select a valid data: ", 0, str).encode(encoding = 'UTF-8')
            print()
            
            start_time = time.time()
            Retrieved_list = []
            for key in db.keys():
                if db[key] == Given:
                    Retrieved_list.append(key.decode(encoding = 'UTF-8'))
            end_time = time.time()
            time_used = end_time - start_time
            time_used *= 1000000
            
            Given = Given.decode(encoding = 'UTF-8')
            if Retrieved_list:
                
                for key in Retrieved_list:
                    print(key) 
                    answers.write(key)
                    answers.write('\n')
                    print(Given)
                    answers.write(Given)
                    answers.write('\n')                    
                    print()
                    answers.write('\n')
                    
            else:
                print('Data is not found\n') 
            
            print("Number of records received: %d"%(len(Retrieved_list)))
            print("The program runs %.6f micro seconds"%time_used)
            
            try:
                db.close()
                
            except Exception as e:
                print (e)                

            select = validity("\nDo you want find another key by given data? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')
    
        except:
            print("Database couldn't be opened")
            select = validity("\nDo you want to try again? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')