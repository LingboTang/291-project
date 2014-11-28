from validity import *
import os
import time
import bsddb3 as bsddb
import random

DA_FILE = "/tmp/my_db/sample_db"
DB_SIZE = 1000
SEED = 10000000


def subfunc3():
    select = 'y'
    while select == 'y':
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Retrieve records with a given data')
        Given_data = validity("Please enter your data: ", "Please select a valid data: ", 300, str)
        Retrieved_key = '' 
        try:
            db = bsddb.btopen(DA_FILE,"r")
        except:
            print("Open method and file does not match to each other")
            break
        Given_data = Given_data.encode(encoding = 'UTF-8')
        try:
            start_time = time.time()
            key_list = []
            for key in db.keys():
                if db[key] == Given_data:
                    Retrieved_key = key
                    Given_data = Given_data.decode(encoding = 'UTF-8')
                    Retrieved_key = Retrieved_key.decode(encoding = 'UTF-8')
                    key_list.append(Retrieved_key)
            end_time = time.time()
            #Given_data = Given_data.decode(encoding = 'UTF-8')
            #Retrieved_key = Retrieved_key.decode(encoding = 'UTF-8')
            time_used = end_time - start_time
            time_used *= 1000000
            db.close()
        except:
            print('data is not found')
            break
        for key in key_list:
            print("Key: ")
            print(key)
        print("The program runs %.6f micro seconds"%time_used)
        select = validity("Do you want find another key by given data? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')
        #os.system('cls' if os.name == 'nt' else 'clear')
        #print()