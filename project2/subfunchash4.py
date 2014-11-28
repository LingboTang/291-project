from validity import *
import os
import time
import bsddb3 as bsddb
import random

DA_FILE = "/tmp/my_db/sample_db"
DB_SIZE = 1000
SEED = 10000000

def subfunchash4():
    select = 'y'
    while select == 'y':
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Retrieve records with a given range of key values')
        try:
            db = bsddb.hashopen(DA_FILE,"r")
        except:
            print("Open method and file does not match to each other")
            break
        lower_bound = validity("Please enter your lower bound: ", "Please select a valid input: ", 300, str)
        upper_bound = validity("Please enter your upper bound: ", "Please select a valid input: ", 300, str)
        if upper_bound < lower_bound:
            print("Upper bound lower than lower bound, you suck")
            break
        elif upper_bound == lower_bound:
            select = 'y'
            while select == 'y':
                os.system('cls' if os.name == 'nt' else 'clear')
                print('Retrieve records with a given key')
                Given_key = upper_bound
                Retrieved_data = '' 
                Given_key = Given_key.encode(encoding = 'UTF-8')
                try:
                    start_time = time.time()
                    Retrieved_data = db[Given_key]
                    end_time = time.time()
                    Given_key = Given_key.decode(encoding = 'UTF-8')
                    Retrieved_data = Retrieved_data.decode(encoding = 'UTF-8')
                    time_used = end_time - start_time
                    time_used *= 1000000
                    db.close()
                except:
                    print('Key is not found')
                    break
                print('Key: %s\n'%Given_key+'Value: %s\n'%Retrieved_data)
                print("The program runs %.6f micro seconds"%time_used)
                select = validity("Do you want find another key? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')
        else:
            upper_bound = upper_bound.encode(encoding = 'UTF-8')
            lower_bound = lower_bound.encode(encoding = 'UTF-8')
            counter = 0 
            try:
                start_time = time.time()
                for key, data in db.items():
                    if key <= upper_bound and key >= lower_bound:
                        if counter == 200:
                            print("too much values, stop now")
                            break
                        counter = counter + 1
                        print('Key: ')
                        print(key.decode(encoding ='UTF-8'))
                        print('Data: ')
                        print(data.decode(encoding = 'UTF-8'))
                end_time = time.time()
                time_used = end_time - start_time
                time_used *= 1000000
                print("Time used: %.6f\n micro seconds"%time_used)
            except:
                print('Key not found, try again')
                db.close()
                break
        select = validity("Do you want to search another range? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')
        os.system('cls' if os.name == 'nt' else 'clear')
        #print()