from validity import *
import os
import time
import bsddb3 as bsddb

def subfunc3(data):
    FILE = data[0]
    
    select = 'y'
    while select == 'y':
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Retrieve records with a given data\n')

        try:
            db = bsddb.btopen(FILE,"r")
            
            Given_data = validity("Please enter your data: ", "Please select a valid data: ", 0, str).encode(encoding = 'UTF-8')
            print()
            
            start_time = time.time()
            key_list = []
            for key in db.keys():
                if db[key] == Given_data:
                    key_list.append(key.decode(encoding = 'UTF-8'))
            end_time = time.time()
            time_used = end_time - start_time
            time_used *= 1000000

            if key_list:
                print("Results:")
                for key in key_list:
                    print(key)  
            else:
                print("No matching results were found")
                
            print("The program runs %.6f micro seconds"%time_used)
            
            try:
                db.close()
                
            except Exception as e:
                print (e)                

            select = validity("\nDo you want find another key by given data? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')
    
        except:
            print("Database couldn't be opened")
            select = validity("\nDo you want to try again? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')