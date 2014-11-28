from validity import *
import os
import time
import bsddb3 as bsddb
import random

DA_FILE = "/tmp/my_db/sample_db"
DB_SIZE = 1000
SEED = 10000000


def subfunc2():
    select = 'y'
    while select == 'y':
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Retrieve records with a given key')
        Given_key = validity("Please enter your key: ", "Please select a valid key: ", 300, str)
        Retrieved_data = '' 
        try:
            db = bsddb.btopen(DA_FILE,"r")
        except:
            print("Open method and file does not match to each other")
            break
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
        #os.system('cls' if os.name == 'nt' else 'clear')
        #print()