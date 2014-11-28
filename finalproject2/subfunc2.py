from validity import *
import os
import time
import bsddb3 as bsddb

options = {'btree': bsddb.btopen, 'hash': bsddb.hashopen, 'indexfile': bsddb.btopen}

def subfunc2(data):
    FILE = data[0]
    searchtype = data[1]
    searchresult = data[2]
    filetype = data[3]
    answers = data[4]
    answers = open(answers, 'a')
    
    select = 'y'
    while select == 'y':
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Retrieve records with a given %s\n'%(searchtype))

        try:
            db = options[filetype](FILE,"r")
            Given = validity("Please enter your %s: "%(searchtype), "Please select a valid %s: "%(searchtype), 0, str).encode(encoding = 'UTF-8')
            Retrieved_list = []
            print()
            
            start_time = time.time()
            try:
                        
                        Retrieved = db[Given].decode(encoding = 'UTF-8')
                        end_time = time.time()
                        
                        Retrieved_list = Retrieved.split()
                        Given = Given.decode(encoding = 'UTF-8')                                                                      
                        for data in Retrieved_list:
                            print(Given)
                            answers.write(Given)
                            answers.write('\n')
                            print(data)     
                            answers.write(data)
                            answers.write('\n')
                            print()
                            answers.write('\n')
                            
            except:
                end_time = time.time()
                print('Key is not found\n') 
                
            
            time_used = end_time - start_time
            time_used *= 1000000         
            
            print("Number of records received: %d"%(len(Retrieved_list)))  
            print("The program runs %.6f micro seconds"%time_used)

            try:
                db.close()
                
            except Exception as e:
                print (e)        
      
            select = validity("\nDo you want find another %s? y/n: "%(searchtype), "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')

        except:
            print("Database couldn't be opened")
            select = validity("\nDo you want to try again? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')
        
        os.system('cls' if os.name == 'nt' else 'clear')
    
    answers.close()