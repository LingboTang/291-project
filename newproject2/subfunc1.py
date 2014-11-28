from validity import *
import os
import time
import random
import bsddb3 as bsddb

options = {'btree': bsddb.btopen, 'hash': bsddb.hashopen, 'indexfile': bsddb.btopen}

def get_random():
    return random.randint(0, 63)
def get_random_char():
    return chr(97 + random.randint(0, 25))

def subfunc1(data):
    FILES = data[0]
    DIR = data[1]
    DB_SIZE = data[2]
    SEED = data[3]
    filetype = data[4]
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print('Create and Populate the database\n')
    
    result = os.system('mkdir %s'%(DIR))
    
    if result != 0:
        print("Could not create or open %s"%(FILES[0]), end = '')

        if len(FILES) > 1:
            print(" and %s"%(FILES[1]))
        else:
            print()
    
    else:
        try:
            db = options[filetype](FILES[0], "w")
            
            if len(FILES) > 1:
                inverse_db = options[filetype](FILES[1],"w")
            
        except:
            print("DB doesn't exist, creating a new one")
            db = options[filetype](FILES[0], "c")
            
            if len(FILES) > 1:
                inverse_db = options[filetype](FILES[1],"c")
    
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
        
    input("\nPlease press enter to continue")