from validity import *
import os
import time
import bsddb3 as bsddb
        
options = {'btree': bsddb.btopen, 'hash': bsddb.hashopen, 'indexfile': bsddb.btopen}

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
    filetype = data[1]
    answers = data[2]
    
    select = 'y'
    while select == 'y':
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Retrieve records with a given range of key values\n')
        
        try:
            db = options[filetype](FILE,"r")
            
            lower_bound = validity("Please enter your lower bound: ", "Please select a valid input: ", 0, str).encode(encoding = 'UTF-8')
            upper_bound = validity("Please enter your upper bound: ", "Please select a valid input: ", 0, str).encode(encoding = 'UTF-8')           
            print()
            
            if upper_bound < lower_bound:
                print("The upper bound is lower than lower bound")
                         
            elif upper_bound == lower_bound:
                Given = upper_bound
                Retrieved_list = []
                
                start_time = time.time()
                try:
                    Retrieved_list = db[Given].decode(encoding = 'UTF-8')
                    end_time = time.time()
                    Given = Given.decode(encoding = 'UTF-8')
                    
                    Retrieved_list = Retrieved_list.split()                                                                      
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

            else:
                key_list = db.keys()
                Retrieved_list = []
                
                start_time = time.time()  
                if filetype == 'hash':  
                    for i in key_list:          
                        if i<= upper_bound and i>= lower_bound:                 
                            Retrieved_list.append(i)     
                    
                else:
                    
                    lower = binary_search_lower_bound(lower_bound,key_list)
                    
                    while key_list[lower] <= upper_bound:
                            Retrieved_list.append(key_list[lower])  
                            lower += 1               

                end_time = time.time()
                
                if Retrieved_list:
                                                                  
                    for data in Retrieved_list:
                        print(data.decode(encoding ='UTF-8'))
                        answers.write(data.decode(encoding ='UTF-8'))
                        answers.write('\n')
                        print(db[data].decode(encoding ='UTF-8'))     
                        answers.write(db[data].decode(encoding ='UTF-8'))
                        answers.write('\n')
                        print()
                        answers.write('\n')                     
                    
                else:                              
                    print("No matching results were found\n")                                        
                    
            time_used = end_time - start_time
            time_used *= 1000000 
            
            print("Number of records received: %d"%(len(Retrieved_list))) 
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