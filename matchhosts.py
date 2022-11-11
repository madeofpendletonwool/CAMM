import os
import time
from datetime import date, timedelta
import sys, getopt

today = date.today()
print("Today's date:", today)
print(sys.argv)
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
        (Collin's Automated Machine Manager)
        This little program will continually scan a subnet and keep an active list of computer up to date and remove anything it's been unable to contact for more than 90 days.
        The pioneers used to drive this baby for miles.

        A simple way to keep a list up to date is to use a cronjob to kick this script off as often as you'd like. I would recommend running a couple times a day. That way you can collect info from computers that run only at particular times.

        Here's an example of how to run the program:

        "CAMM.py -s <subnetlist> ex. CAMM.py \'10.0.0.0/24 192.168.2.0/24\' 
        Don't forget the quotes. They are a requirment if passing more than one subnet to scan."
        ''')
        sys.exit()
    elif opt in ("-s"):
        subnet_list = arg
        print(subnet_list)
    else:
        print("Not valid program syntax: Try running matchhosts.py -h for help")

print ('Subnets we will scan:', subnet_list)

match_subnet = '10.0.0.0/24'
print (f'Number of arguments:', len(sys.argv), 'arguments.')

def pull_current_list(working_list):
    path = 'Computer_list.txt'
    isExist = os.path.exists(path)
    if isExist == True:
        current_list = open('Computer_list.txt').read().splitlines()
        return current_list
    if isExist == False:
        create_file = open("Computer_list.txt","w")
        create_file.write(str(working_list))
        create_file.close()
        current_list = open('Computer_list.txt').read().splitlines()
        # print(working_list)
        return current_list



# if 
def get_working_list(current_list):
    nmap_search = f"sudo nmap -sP {subnet_list} | awk -F'for ' '{{print $2}}' | sed 's/(.*//' | sed '/^$/d'"
    # found_machines = os.system(nmap_search)
    found_machines = os.popen(nmap_search).read()
    # print(found_machines)

    create_file = open("found.txt","w")
    create_file.write(str(found_machines))
    create_file.close()

    working_list = open('found.txt').read().splitlines()
    for _ in range(len(working_list)):
        working_list[_] = working_list[_] + f", {today}"
    # print(working_list)

    # print(working_list)
    current_list = pull_current_list(working_list)
    #remove old entries that haven't been updated
    remove_old(working_list, current_list)
    #compare new and old lists, updating final list to add on new entries
    compare_lists(working_list, current_list)
    os.remove("found.txt")

def remove_old(working_list, current_list):
    for _ in range(len(current_list)):
        list_dates = current_list[_][-10:]
        # print('Date Only : ', list_dates)
        #Get date as of 90 days prior
        prev = date.strftime(today - timedelta(days=90), '%Y-%m-%d')
        # print(prev)
        # Delete lines that are older than 90 days prior
        if list_dates < prev:
            print(f'{list_dates} older than 90 days. Removing {current_list[_]}')
            with open("Computer_list.txt", "w") as fp:
                for line in current_list:
                    # print(current_list[_])
                    if line.strip("\n") != current_list[_]:
                        fp.write("%s\n" % line)

def compare_lists(working_list, current_list):
    compare1 = set(working_list)
    compare2 = set(current_list)

    missing_machines = list(sorted(compare1 - compare2))

    # print('missing:', missing_machines)

    with open(r'Computer_list.txt', 'a') as write_to:
        for item in missing_machines:
            # write each item on a new line
            write_to.write("%s\n" % item)
        print('Done')
    
current_list = 'null'
get_working_list(current_list)

