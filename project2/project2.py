
import bsddb3 as bsddb
import os
import time
from ctypes import cdll
lib = cdll.LoadLibrary('./libfoo.so')

global alpha
alpha="abcdefghijklmnopqrstuvwxyz"

global DB_SIZE
DB_SIZE=100000

global PATH
PATH="/tmp/yufei_db/db"

global INVERTED_PATH
INVERTED_PATH="/tmp/yufei_db/inverted_db"

def main():
    fo=open("answers","w")
    fo.close()
    Created=False
    data_type=select_data_type()
    while True:
        print("=================================================================================")
        print("Enter 1: Create and populate the database")
        print("Enter 2: Retrieve records with a given key")
        print("Enter 3: Retrieve records with a given data")
        print("Enter 4: Retrieve records with a given range of key values")
        print("Enter 5: Destroy the database")
        print("Enter 6: Quit")
        print("Enter 7: Destroy the current database (if exist) and go back to choose a new data type")
        print("=================================================================================")
        try:
            cmd=int(input("Please Enter your command:  "))
        except ValueError:
            print("Invalid command, enter again")
        else:
            if cmd>7 or cmd<1:
                print("Invalid command, enter again")
            else:
                if cmd==6:
                    print("Thank you for using our project!")
                    break
                elif cmd==1:
                    if Created==False:
                        try:
                            os.system("mkdir /tmp/yufei_db")
                        except:
                            pass
                        create_and_populate(data_type)
                        print("DATABASE populated")
                        Created=True
                    else:
                        print("Please destroy the database before create a new one")
                elif cmd==2:
                    if Created==True:
                        time=key_search()
                        print("Time used during the search in microseconds: "+str(time))
                    else:
                        print("Database not created, cannot search")
                elif cmd==3:
                    if Created==True:
                        time=data_search(data_type)
                        print("Time used during the search in microseconds: "+str(time))
                    else:
                        print("Database not created, cannot search")
                elif cmd==4:
                    if Created==False:
                        print("Database not created, cannot search")
                    else:
                        time=range_search(data_type)
                        print("Time used during the search in microseconds: "+str(time))
                elif cmd==5:
                    if Created==True:
                        try:
                            db.close()
                            os.system("rm /tmp/yufei_db/db")
                            if data_type==3:
                                inverted_db.close()
                                os.system("rm /tmp/yufei_db/inverted_db")
                                path="/tmp/yufei_db/index_file/db"
                                for i in range(26):
                                    ALL_DB[alpha[i]].close()
                                    os.system("rm "+path+str(i))
                                os.system("rmdir /tmp/yufei_db/index_file")                                
                            os.system("rmdir /tmp/yufei_db")
                        except Exception as Error:
                            print(Error)
                        print("database destroyed")
                        Created=False
                    else:
                        print("database is not created!")
                elif cmd==7:
                    fo=open("answers","w")
                    fo.close()                    
                    if Created==True:
                        try:
                            db.close()
                            os.system("rm /tmp/yufei_db/db")
                            if data_type==3:
                                inverted_db.close()
                                os.system("rm /tmp/yufei_db/inverted_db")
                                path="/tmp/yufei_db/index_file/db"
                                for i in range(26):
                                    ALL_DB[alpha[i]].close()
                                    os.system("rm "+path+str(i))
                                os.system("rmdir /tmp/yufei_db/index_file")
                            os.system("rmdir /tmp/yufei_db")
                        except Exception as Error:
                            print(Error)
                        print("database destroyed")
                        Created=False
                    data_type=select_data_type()
    
    if Created==True:
        try:
            db.close()
            os.system("rm /tmp/yufei_db/db")
            if data_type==3:
                inverted_db.close()
                os.system("rm /tmp/yufei_db/inverted_db")
                path="/tmp/yufei_db/index_file/db"
                for i in range(26):
                    ALL_DB[alpha[i]].close()
                    os.system("rm "+path+str(i))
                os.system("rmdir /tmp/yufei_db/index_file")                
            os.system("rmdir /tmp/yufei_db")
        except Exception as Error:
            print(Error)
        print("Database droped")


def select_data_type():
    print("Enter 'btree' for DB_BTREE datatype;")
    print("Enter 'hash' for DB_HASH datatype;")
    print("Enter 'index' for improved database;")
    print("=================================================================================")
    db_type_option=str(input("Please choose one of the data type above: "))
    if db_type_option.lower()=="btree":
        return 1
    elif db_type_option.lower()=="hash":
        return 2
    elif db_type_option.lower()=="index":
        return 3
    else:
        print("Invalid input, enter again")
        return select_data_type()

def create_index_file():
    global ALL_DB
    try:
        os.system("mkdir /tmp/yufei_db/index_file")
    except:
        pass
    INDEX_PATH="/tmp/yufei_db/index_file/db"
    ALL_DB=dict()
    for i in range(26):
        try:
            db = bsddb.btopen(INDEX_PATH+str(i), "w")
        except:
            db = bsddb.btopen(INDEX_PATH+str(i), "c")
        ALL_DB[alpha[i]]=db

def create_and_populate(data_type):
    global db
    global inverted_db
    try:
        if data_type==1:
            db = bsddb.btopen(PATH, "w")
        elif data_type==2:
            db = bsddb.hashopen(PATH, "w")
        elif data_type==3:
            db = bsddb.btopen(PATH, "w")
            inverted_db = bsddb.btopen(INVERTED_PATH, "w")
            create_index_file()
    except:
        print("DB doesn't exist, creating a new one")
        if data_type==1:
            db = bsddb.btopen(PATH, "c")
        elif data_type==2:
            db = bsddb.hashopen(PATH, "c")
        elif data_type==3:
            db = bsddb.btopen(PATH, "c")
            inverted_db = bsddb.btopen(INVERTED_PATH, "c")            
    SEED = 10000000
    lib.set_seed(SEED)
    index=0
    while index<DB_SIZE:
        krng = 64 + lib.get_random() % 64
        key = ""
        for i in range(krng):
            key += str(chr(lib.get_random_char()))
        vrng = 64 + lib.get_random() % 64
        value = ""
        for i in range(vrng):
            value += str(chr(lib.get_random_char()))
        #print(key)
        #print(value)
        #print("")
        if data_type==3:
            ALPHA=key[0]
            #split_index=alpha.index(ALPHA)
        
        key = key.encode(encoding='UTF-8')
        value = value.encode(encoding='UTF-8')            
        if db.has_key(key):
            pass
        else:
            db[key] = value
            index+=1
            if data_type==3:
                if inverted_db.has_key(value):
                    new_key=inverted_db[value].decode(encoding='UTF-8')
                    new_key+=(","+key.decode(encoding='UTF-8'))
                    inverted_db[value]=new_key.encode(encoding='UTF-8')
                else:
                    inverted_db[value]=key
                ALL_DB[ALPHA][key]=value

def key_search():
    Key=str(input("Please Enter the key value: "))
    fout=open("answers","a")
    start=time.time()
    Key=Key.encode(encoding='UTF-8')
    if db.has_key(Key):
        Value=db[Key]
        print("Key: "+Key.decode(encoding='UTF-8')+" ; \nValue:"+Value.decode(encoding='UTF-8'))
        fout.write(Key.decode(encoding='UTF-8')+"\n")
        fout.write(Value.decode(encoding='UTF-8')+"\n\n")        
        print("number of records retrieved: 1")
    else:
        print("This key is not in the database")
    end=time.time()       
    fout.close()
    return (end-start)*1000000
        
def data_search(data_type):
    Data=str(input("Please Enter the data value: "))
    fout=open("answers","a")
    if data_type==3:
        start=time.time()
        Data=Data.encode(encoding='UTF-8')
        if inverted_db.has_key(Data):
            Keys=inverted_db[Data].decode(encoding='UTF-8').split(",")
            print("Key refering to this data  :"+Data.decode(encoding='UTF-8')+" is listed below: ")
            print("=================================================================================")
            for Key in Keys:
                print(Key)
                fout.write(Key+"\n")
                fout.write(Data.decode(encoding='UTF-8')+"\n\n")
            print("=================================================================================")
            print("number of records retrieved: "+str(len(Keys)))
            print("=================================================================================")
        else:
            print("This data is not in the database")
        end=time.time()
    else:
        start=time.time()
        Data=Data.encode(encoding='UTF-8')
        Pair=db.first()
        print("Key refering to this data  :"+Data.decode(encoding='UTF-8')+" is listed below: ")
        print("=================================================================================")
        cnt=0
        while True:
            if Data==Pair[1]:
                print(Pair[0].decode(encoding='UTF-8'))
                fout.write(Pair[0].decode(encoding='UTF-8')+"\n")
                fout.write(Data.decode(encoding='UTF-8')+"\n\n")
                cnt+=1
            try:
                Pair=db.next()
            except:
                break
        end=time.time()
        print("=================================================================================")
        print("number of records retrieved: "+str(cnt))
        print("=================================================================================")        
    fout.close()
    return (end-start)*1000000

def range_search(data_type):
    Upper_bound=str(input("Please Enter the upper bound value: ")).encode(encoding='UTF-8')
    Lower_bound=str(input("Please Enter the lower bound value: ")).encode(encoding='UTF-8')
    if Upper_bound<Lower_bound:
        print("Invalid input.")
        return ("As input is invalid, no search time printed")
    fout=open("answers","a")
    if data_type==1: # B-Tree
        start=time.time()
        KEYS=db.keys()
        Up=binary_search_upper_bound(Upper_bound,KEYS)
        Lo=binary_search_lower_bound(Lower_bound,KEYS)
        if type(Up)==bool or type(Up)==bool:
            print("Empty range")
            fout.close()
            return ("As range is empty, no search time printed")
        print("====================================================================================")
        print("All key value pairs in range is listed below:")
        for i in range(Lo,Up+1):
            Key=KEYS[i].decode(encoding='UTF-8')
            Value=db[KEYS[i]].decode(encoding='UTF-8')
            print("Key: "+Key+" ; \nValue: "+Value)
            fout.write(Key+"\n")
            fout.write(Value+"\n\n")
        end=time.time()
        print("number of records retrieved: "+str(Up-Lo+1))
    elif data_type==2: # Hesh-Table
        start=time.time()
        print("====================================================================================")
        print("All key value pairs in range is listed below:")
        Pair=db.first()
        cnt=0
        while True:
            Key,Value=Pair[0],Pair[1]
            if Lower_bound<=Key and Key<=Upper_bound:
                print("Key: "+Key.decode(encoding='UTF-8')+" ;\nValue: "+Value.decode(encoding='UTF-8'))
                fout.write(Key.decode(encoding='UTF-8')+"\n")
                fout.write(Value.decode(encoding='UTF-8')+"\n\n")
                cnt+=1
            try:
                Pair=db.next()
            except:
                break
        end=time.time()
        print("number of records retrieved: "+str(cnt))
    elif data_type==3: # indexfile
        start=time.time()
        upper_alpha=Upper_bound.decode(encoding='UTF-8')[0]
        lower_alpha=Lower_bound.decode(encoding='UTF-8')[0]
        #----------------------------------------------------------------------
        upper_key_set=ALL_DB[upper_alpha].keys()
        lower_key_set=ALL_DB[lower_alpha].keys()
        #----------------------------------------------------------------------
        Up=binary_search_upper_bound(Upper_bound,upper_key_set)
        if (type(Up)==bool or Up==None) and upper_alpha=='a':
            print("Empty range")
            return "As range is empty, no search_time recorded"
        elif (type(Up)==bool and upper_alpha!='a') or Up==None:
            while True:
                upper_alpha=alpha[alpha.index(upper_alpha)-1]
                upper_key_set=ALL_DB[upper_alpha].keys()
                Up=len(upper_key_set)-1
                if len(upper_key_set)==0 and upper_alpha=='a':
                    print("Empty range")
                    return "As range is empty, no search_time recorded" 
                elif len(upper_key_set)>0:
                    break                
        #print(Up)
        #----------------------------------------------------------------------
        Lo=binary_search_lower_bound(Lower_bound,lower_key_set)
        if (type(Lo)==bool or Lo==None) and lower_alpha=='z':
            print("Empty range")
            return "As range is empty, no search_time recorded"
        elif (type(Lo)==bool and lower_alpha!='z') or Lo==None:
            while True:
                Lo=0
                lower_alpha=alpha[alpha.index(lower_alpha)+1]
                lower_key_set=ALL_DB[lower_alpha].keys()
                if len(lower_key_set)==0 and lower_alpha=='z':
                    print("Empty range")
                    return "As range is empty, no search_time recorded" 
                elif len(lower_key_set)>0:
                    break
                        
        #print(Lo)
        #----------------------------------------------------------------------
        if upper_alpha==lower_alpha:
            for i in range(Lo,Up+1):
                Key=upper_key_set[i].decode(encoding='UTF-8')
                Value=ALL_DB[upper_alpha][upper_key_set[i]].decode(encoding='UTF-8')
                print("Key: "+Key+"\nValue:"+Value)
                fout.write(Key+"\n")
                fout.write(Value+"\n\n")
            end=time.time()
            print("number of records retrieved: "+str(Up-Lo+1))
        else:
            u_pos=alpha.index(upper_alpha)
            l_pos=alpha.index(lower_alpha)
            cnt=0
            for i in range(l_pos,u_pos+1):
                if i==l_pos:
                    for j in range(Lo,len(lower_key_set)):
                        Key=lower_key_set[j].decode(encoding='UTF-8')
                        Value=ALL_DB[lower_alpha][lower_key_set[j]].decode(encoding='UTF-8')
                        print("Key: "+Key+"\nValue:"+Value)
                        fout.write(Key+"\n")
                        fout.write(Value+"\n\n")
                        cnt+=1
                elif i==u_pos:
                    for j in range(Up+1):
                        Key=upper_key_set[j].decode(encoding='UTF-8')
                        Value=ALL_DB[upper_alpha][upper_key_set[j]].decode(encoding='UTF-8')
                        print("Key: "+Key+"\nValue:"+Value)
                        fout.write(Key+"\n")
                        fout.write(Value+"\n\n")
                        cnt+=1
                else:
                    current_db=ALL_DB[alpha[i]]
                    try:
                        Pair=current_db.first()
                    except:
                        continue
                    while True:
                        Key=Pair[0].decode(encoding='UTF-8')
                        Value=Pair[1].decode(encoding='UTF-8')
                        print("Key: "+Key+"\nValue:"+Value)
                        fout.write(Key+"\n")
                        fout.write(Value+"\n\n")
                        cnt+=1
                        try:
                            Pair=current_db.next()
                        except:
                            break
            print("number of records retrieved: "+str(cnt))
            end=time.time()
    fout.close()           
    return (end-start)*1000000
    
def binary_search_upper_bound(key,List):
    left,right=0,len(List)-1
    if left>right:
        return None
    while left<=right:
        mid=(left+right)//2
        if key==List[mid]:
            return mid
        elif key<List[mid]:
            right=mid-1
            if right<0:
                return False
            bound=mid-1
        else:
            left=mid+1
            if left>len(List)-1:
                return len(List)-1
            bound=mid
    return bound

def binary_search_lower_bound(key,List):
    left,right=0,len(List)-1
    if left>right:
        return None
    while left<=right:
        mid=(left+right)//2
        if key==List[mid]:
            return mid
        elif key<List[mid]:
            right=mid-1
            if right<0:
                return 0
            bound=mid
        elif key>List[mid]:
            left=mid+1
            if left>len(List)-1:
                return False
            bound=mid+1
    return bound
    
    
main()