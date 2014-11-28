from validity import *
import os
import time
import bsddb3 as bsddb

def subfunc2(data):
    FILE = data[0]
    searchtype = data[1]
    searchresult = data[2]
    
    select = 'y'
    while select == 'y':
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Retrieve records with a given %s\n'%(searchtype))

        try:
            db = bsddb.btopen(FILE,"r")
            Given = validity("Please enter your %s: "%(searchtype), "Please select a valid %s: "%(searchtype), 0, str).encode(encoding = 'UTF-8')
            print()
            
            try:
                        start_time = time.time()
                        Retrieved = db[Given].decode(encoding = 'UTF-8')
                        end_time = time.time()
            
                        time_used = end_time - start_time
                        time_used *= 1000000
                        
                        print("Retrieved %s(s):"%(searchresult))
                        Retrieved_list = Retrieved.split()
                        for data in Retrieved_list:
                            print(data)      
                        
                        print("The program runs %.6f micro seconds"%time_used)
                        
            except:
                print('Key is not found')          
             
            try:
                db.close()
                
            except Exception as e:
                print (e)        
      
            select = validity("\nDo you want find another %s? y/n: "%(searchtype), "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')

        except:
            print("Database couldn't be opened")
            select = validity("\nDo you want to try again? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')
        
        os.system('cls' if os.name == 'nt' else 'clear')