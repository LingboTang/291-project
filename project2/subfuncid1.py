from validity import *
import os
import time
# Berkeley DB Example

__author__ = "Bing Xu"
__email__ = "bx3@ualberta.ca"

import bsddb3 as bsddb
import random
# Make sure you run "mkdir /tmp/my_db" first!
DA_FILE = "/tmp/my_db/sample_db"
INVERSE_DA_FILE = "/tmp/my_db/sample_db2"
DB_SIZE = 1000
SEED = 10000000

def get_random():
    return random.randint(0, 63)
def get_random_char():
    return chr(97 + random.randint(0, 25))



def subfuncid1():
    select = 'y'
    while select == 'y':
        os.system('cls' if os.name == 'nt' else 'clear')
        os.system('mkdir /tmp/my_db/')
        print('Create and Populate the database')
        #main code start from here
        try:          
            db = bsddb.btopen(DA_FILE, "w")
            inverse_db = bsddb.btopen(INVERSE_DA_FILE,"w")           
        except:
            print("DB doesn't exist, creating a new one")             
            db = bsddb.btopen(DA_FILE, "c")
            inverse_db = bsddb.btopen(INVERSE_DA_FILE,"c")
        random.seed(SEED)
        start_time = time.time()
        for index in range(DB_SIZE):
            krng = 64 + get_random()
            key = ""
            for i in range(krng):
                key += str(get_random_char())
            vrng = 64 + get_random()
            value = ""
            for i in range(vrng):
                value += str(get_random_char())
            print (key)
            print (value)
            print ("")
            key = key.encode(encoding='UTF-8')
            value = value.encode(encoding='UTF-8')
            db[key] = value
            inverse_db[value] = key
        end_time = time.time()
        time_used = end_time - start_time
        time_used *= 1000000
        try:
            db.close()
            inverse_db.close()
        except Exception as e:
            print (e)        
        
        print('Database created')
        print("The program runs %.6f micro seconds"%time_used)
        select = validity("Do you want to repopulate the database? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')
        os.system('cls' if os.name == 'nt' else 'clear')