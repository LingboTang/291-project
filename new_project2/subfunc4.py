from validity import *
import os
import time
import bsddb3 as bsddb
        
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

def subfunc4(data):
    FILE = data[0]
    
    select = 'y'
    while select == 'y':
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Retrieve records with a given range of key values\n')
        
        try:
            db = bsddb.btopen(FILE,"r")
            
            lower_bound = validity("Please enter your lower bound: ", "Please select a valid input: ", 0, str).encode(encoding = 'UTF-8')
            upper_bound = validity("Please enter your upper bound: ", "Please select a valid input: ", 0, str).encode(encoding = 'UTF-8')           
            print()
            
            if upper_bound < lower_bound:
                print("The upper bound is lower than lower bound")
                         
            elif upper_bound == lower_bound:
                Given_key = upper_bound
                
                try:
                    start_time = time.time()
                    Retrieved_data = db[Given_key]
                    end_time = time.time()
                    Given_key = Given_key.decode(encoding = 'UTF-8')
                    Retrieved_data = Retrieved_data.decode(encoding = 'UTF-8')
                    time_used = end_time - start_time
                    time_used *= 1000000
                    
                    print('Key: %s\n'%Given_key+'Value: %s\n'%Retrieved_data)
                    print("The program runs %.6f micro seconds"%time_used)                    

                except:
                    print('Key is not found')

            else:
                key_list = db.keys()
                lower = binary_search_lower_bound(lower_bound,key_list)
                counter = 0 
                
                start_time = time.time()     
                while key_list[lower] <= upper_bound:
                        if counter == 200:
                            print("Too many results, stop search")
                            break
                        
                        counter = counter + 1
                        lower = lower + 1
                        
                        print('Key: ')
                        print(key_list[lower].decode(encoding ='UTF-8'))
                        print('Data: ')
                        print(db[key_list[lower]].decode(encoding = 'UTF-8'))
                
                if counter == 0:
                    print("No matching results were found")
                    
                end_time = time.time()
                time_used = end_time - start_time
                time_used *= 1000000
                print("The program runs %.6f micro seconds"%time_used)           
            
            try:
                db.close()
                
            except Exception as e:
                print (e)    
                
            select = validity("\nDo you want to search another range? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')
            
        except:
            print("Database couldn't be opened")
            select = validity("\nDo you want to try again? y/n: ", "Please enter a valid option: ", 1, str, ['y', 'n'], 'lower')
        
        
        os.system('cls' if os.name == 'nt' else 'clear')