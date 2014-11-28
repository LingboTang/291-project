from validity import *
import os
import time

def subfunc5():
    print('Destroy the database')
    os.system('rm -rf /tmp/my_db')
    print('Database destroyed')

    print("The program runs %.6f seconds"%time.clock())