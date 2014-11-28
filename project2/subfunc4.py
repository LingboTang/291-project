from validity import *
import os
import time
import bsddb3 as bsddb
import random

DA_FILE = "/tmp/my_db/sample_db"
DB_SIZE = 1000
SEED = 10000000


    

def subfunc4():
    select = 'y'
    while select == 'y':
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Retrieve records with a given range of key values')
        try:
            db = bsddb.btopen(DA_FILE,"r")
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
            key_list = db.keys()
            lower = binary_search_lower_bound(lower_bound,key_list)
            upper = upper_bound
            counter = 0 
            try:
                start_time = time.time()     
                while key_list[lower] <= upper_bound:
                        if counter == 200:
                            print("too much values, stop now")
                            break
                        counter = counter + 1
                        print('Key: ')
                        print(key_list[lower].decode(encoding ='UTF-8'))
                        print('Data: ')
                        print(db[key_list[lower]].decode(encoding = 'UTF-8'))
                        lower = lower + 1
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
        
        
        
        
        
        
def binary_search_lower_bound(key,L):
    left,right=0,len(L)-1
    if left>right:
        return None
    while left<=right:
        mid=(left+right)//2
        if key==L[mid]:
            return mid
        elif key<L[mid]:
            right=mid-1
            if right<0:
                return 0
            lower_b=mid
        elif key>L[mid]:
            left=mid+1
            if left>len(L)-1:
                return False
            lower_b=mid+1
    return lower_b