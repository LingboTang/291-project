from validity import *
import os
import time
import random
import bsddb3 as bsddb

def get_random():
    return random.randint(0, 63)
def get_random_char():
    return chr(97 + random.randint(0, 25))

def subfunc1(data):
    FILES = data[0]
    DIR = data[1]
    DB_SIZE = data[2]
    SEED = data[3]
    
    select = 'y'
    while select == 'y':
        os.system('cls' if os.name == 'nt' else 'clear')
        os.system('mkdir %s'%(DIR))
        
        print('Create and Populate the database\n')
        
        try:
            db = bsddb.btopen(FILES[0], "w")
            
            if len(FILES) > 1:
                inverse_db = bsddb.btopen(FILES[1],"w")
            
        except:
            print("DB doesn't exist, creating a new one")
            db = bsddb.btopen(FILES[0], "c")
            
            if len(FILES) > 1:
                inverse_db = bsddb.btopen(FILES[1],"c")

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
            print ()
            key = key.encode(encoding='UTF-8')
            value = value.encode(encoding='UTF-8')
            db[key] = value
            
            if len(FILES) > 1:
                if inverse_db.has_key(value):
                    inverse_db[value] += " ".encode(encoding='UTF-8') + key
                else:
                    inverse_db[value] = key
            
        end_time = time.time()
        time_used = end_time - start_time
        time_used *= 1000000
        
        try:
            db.close()
            
            if len(FILES) > 1:
                inverse_db.close()
                
        except Exception as e:
            print (e)        
        
        print('\nDatabase created')
        print("The program runs %.6f micro seconds"%time_used)
        
        select = validity("\nDo you want to repopulate the database? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')
        os.system('cls' if os.name == 'nt' else 'clear')