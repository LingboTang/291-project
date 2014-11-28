from validity import *
import os

def subfunc5(data):
    DIR = data[0]
    
    if DIR != 'answer':
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Destroy the database\nDirectory: %s\n'%(DIR))
    else:
        print('\nDestroy the answers')
    
    result = os.system('rm -rf %s'%(DIR))
    
    if result == 0:
        print("%s destroyed"%(DIR))
    else:
        print("\n%s not destroyed"%(DIR))
    
    if len(data) < 2:
        input("\nPlease press enter to continue")