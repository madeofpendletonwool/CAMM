text = "test : match this."
import re
from sh import awk, sed
import os
import time

match_subnet = '10.0.0.0/24'

def pull_current_list(found_machines):
    path = 'Computer_list.txt'
    isExist = os.path.exists(path)
    if isExist == True:
        current_list = open('Computer_list.txt').read().splitlines()
        return current_list
    if isExist == False:
        create_file = open("Computer_list.txt","w")
        create_file.write(str(found_machines))
        create_file.close()
        current_list = open('Computer_list.txt').read().splitlines()
        # print(working_list)
        return current_list



# if 
def get_working_list(current_list):
    nmap_search = f"sudo nmap -sP {match_subnet} | awk -F'for ' '{{print $2}}' | sed 's/(.*//' | sed '/^$/d'"
    # found_machines = os.system(nmap_search)
    found_machines = os.popen(nmap_search).read()
    # print(found_machines)

    create_file = open("found.txt","w")
    create_file.write(str(found_machines))
    create_file.close()

    working_list = open('found.txt').read().splitlines()
    # print(working_list)
    current_list = pull_current_list(found_machines)
    compare_lists(working_list, current_list)
    time.sleep(5)
    os.remove("found.txt")

def compare_lists(working_list, current_list):
    compare1 = set(working_list)
    compare2 = set(current_list)

    missing = list(sorted(compare1 - compare2))

    print('missing:', missing)
    
current_list = 'null'
get_working_list(current_list)

