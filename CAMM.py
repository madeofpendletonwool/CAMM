import os
import time
from datetime import date, timedelta
import sys, getopt
import csv
import re

today = date.today()
print("Today's date:", today)
argument = sys.argv[1:]

subnet_list = ''
try:
    opts, args = getopt.getopt(argument,"hs:o:",["ifile="]) 
except getopt.GetoptError:
    print ('matchhosts.py -s <subnetlist> ex.')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print ('''
        Welcome to CAMM!
        (Collin's Automated Machine Monitor)
        This little program will continually scan a subnet and keep an active list of computer up to date and remove anything it's been unable to contact for more than 90 days.
        The pioneers used to drive this baby for miles.

        A simple way to keep a list up to date is to use a cronjob to kick this script off as often as you'd like. I would recommend running a couple times a day. That way you can collect info from computers that run only at particular times.

        Here's an example of how to run the program:

        "CAMM.py -s <subnetlist> ex. CAMM.py -s \'10.0.0.0/24 192.168.2.0/24\' 
        Don't forget the quotes. They are a requirment if passing more than one subnet to scan."
        ''')
        sys.exit()
    elif opt in ("-s"):
        subnet_list = arg
    else:
        print("Not valid program syntax: Try running matchhosts.py -h for help")

print ('Subnets we will scan:', subnet_list)

match_subnet = '10.0.0.0/24'

def pull_current_list(working_lines):
    test_data = ''
    isExist = os.path.exists('/data/Computer_list.txt')
    if isExist == True:
        current_list = open('/data/Computer_list.txt').read().splitlines()
        return current_list
    if isExist == False:
        create_file = open("/data/Computer_list.txt","w")
        create_file.write(str(working_lines))
        create_file.close()
        current_list = open('/data/Computer_list.txt').read().splitlines()
        return current_list



# if 
def get_working_list(current_list):
    # The nmap search command
    nmap_search = f"nmap -sn {subnet_list} | awk -F'for ' '{{print $2}}' | sed 's/(.*//' | sed '/^$/d'"

    # found_machines = os.system(nmap_search)
    found_machines = os.popen(nmap_search).read()
    # found_machines_strip = [x.strip(' ') for x in found_machines]

    create_file = open("/data/found.txt","w")
    create_file.write(str(found_machines))
    create_file.close()

    working_pre_list = open('/data/found.txt').read().splitlines()
    working_list = [x.strip(' ') for x in working_pre_list]

    for _ in range(len(working_list)):
        working_list[_] = working_list[_] + f", {today}"
    # Break working list into lines
    working_lines = ('\n'.join(working_list))

    create_file = open("/data/found_dates.txt","w")
    create_file.write(str(working_lines))
    create_file.close()

    #Get Current Saved List
    current_list = pull_current_list(working_lines)
    
    #Removing Duplicates (When machines are found 2 days in a row for example)
    # final_dup_list = remove_dups(working_list)
    clean_dict = remove_dup_dates(working_lines)
    #Remove any entries on final list that are ip addresses. We really only want things that have a hostname
    remove_ips()
    #remove old entries that haven't been updated
    remove_old(clean_dict)
    # Cleaning up!
    os.remove("/data/found.txt")
    os.remove("/data/Computer_listtemp.txt")
    os.remove("/data/edit.txt")
    os.remove("/data/found_dates.txt")

def remove_ips():
    rm_list = open('/data/Computer_list.txt').read().splitlines()

    # my_list = [('10.0.0.1', '2022-12-05'), ('collincomputer', '2022-12-05')]
    os.remove("/data/Computer_list.txt")


    ip_regex = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')

    filtered_list = list(filter(lambda x: not ip_regex.match(x.split(',')[0].strip()), rm_list))

    # join all the elements in the list into a single string
    data = "\n".join(filtered_list)
    # print(filtered_list)cd 

    # write the string to the file
    with open('/data/Computer_list.txt', 'w') as f:
        f.write(data)


def remove_old(clean_dict):

        #Get date as of 90 days prior
    prev = date.strftime(today - timedelta(days=90), '%Y-%m-%d')
        # Open current working file
    rm_list = open('/data/edit.txt').read().splitlines()

    for _ in range(len(rm_list)):
        list_dates = rm_list[_][-10:]
        
        # Delete lines that are older than 90 days prior
        if list_dates < prev:
            with open("/data/Computer_list.txt", "w") as fp:
                for line in rm_list:
                    print(f'{list_dates} older than 90 days. Removing {rm_list[_]}')
                    if line.strip("\n") != rm_list[_]:
                        fp.write("%s\n" % line)

def remove_dup_dates(working_lines):
    # print(working_lines)
    current_dict = {}

    #Remove double quotes
    with open('/data/Computer_list.txt', 'r') as infile, \
        open('/data/edit.txt', 'w') as outfile:
        data = infile.read()
        outfile.write(data)

    #Remove new lines

    f = open('/data/edit.txt', 'r')
    for line in f.readlines():
        name,dates = line.split(",")
        current_dict[name] = str(dates)

    new_dict = {}
    f = open('/data/found_dates.txt', 'r')
    for line in f.readlines():
        name,dates = line.split(",")
        new_dict[name] = str(dates)

    current_dict.update(new_dict)

    clean_dict = {key.strip(): item.strip() for key, item in current_dict.items()}

    with open('/data/Computer_listtemp.txt', 'w') as csv_file:  
        writer = csv.writer(csv_file, delimiter=',', quotechar='\"')
        for key, value in current_dict.items():
            writer.writerow([key, value])
    
    #Remove double quotes that writing dict creates
    with open('/data/Computer_listtemp.txt', 'r') as infile, \
        open('/data/Computer_list.txt', 'w') as outfile:
        data = infile.read()
        data = data.replace('"', "")
        data = data.replace('\n\n', "\n")
        outfile.write(data)

    return clean_dict
    
current_list = 'null'
get_working_list(current_list)

