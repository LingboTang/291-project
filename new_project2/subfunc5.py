from validity import *
import os

def subfunc5(data):
    DIR = data[0]
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Destroy the database\nDirectory: %s'%(DIR))
    
    result = os.system('rm -rf %s'%(DIR))
    
    if result == 0:
        print("Database destroyed")
    else:
        print("Database not destroyed")
    
    if len(data) < 2:
        input("\nPlease press enter to continue")