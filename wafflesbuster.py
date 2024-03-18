#!/bin/python3 
# Made by WafflesExploits
import concurrent.futures
import time
import requests
import re
import urllib3
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from datetime import datetime
import logging
logging.getLogger("urllib3").setLevel(logging.ERROR)

urllib3.disable_warnings()

parser = argparse.ArgumentParser(description='-> Directory Brute-forcer')
parser.add_argument('-u', '--url', type=str, help="Target URL.")
parser.add_argument('-w', '--wordlist', type=str, help="Wordlist containing the URLs to scan.")
parser.add_argument('-p', '--pause', type=str, help="Pauses based on status. Default: 429", default='429')
parser.add_argument('-s', '--status', type=str, nargs='?', help="Specifies the Status code to match. Example:'200-299,301,302'", default='200-299,301,302,307,401,403,405,500')
parser.add_argument('-t', '--threads', type=int, nargs='?',help="Number of threads to use. Default: 5", default=5)
parser.add_argument('-o', '--output', type=str, nargs='?',help="Outputs results to a file.")
parser.add_argument('-v', '--verify',action='store_true', help='Set to false if the website doesn\'t use SSL.')
parser.add_argument('-c', '--color',action='store_true', help='Colorize output. Default=false')

args = parser.parse_args()

# Parameters
directory_file = args.wordlist
url = args.url
threads_num = args.threads # Number of threads to run
status = args.status
status_pause = args.pause
output = args.output
verify = not(args.verify)
color = args.color

# Functions

def parse_token(data): # Matches text from data based on regex pattern.
	pattern = 'request_token":"(.*)"'
	return re.findall(pattern, data)
	
def CheckSlash(url1):
	pattern = '/$'
	slash = re.findall(pattern, url1)
	if (not slash):
		url1 = url1 + '/'
		
	return url1
	
def Colors(stat_code):
    if ( 200 <= stat_code < 299):
        color_code = '\033[32m'
    elif ( stat_code == 302):
        color_code = '\033[32m'
    elif ( 300 <= stat_code < 399):
        color_code = '\033[34m'
    elif ( 400 <= stat_code < 499):
        color_code = '\033[33m'
    elif ( 500 <= stat_code < 599):
        color_code = '\033[31m'
    colored_stat = color_code + str(stat_code) + '\033[0;37m'
    return colored_stat
	
def GetStatusCode(status_string):
    status = []
    var1 = status_string.split(",")
    for str1 in var1:
        if ("-" in str1):
            tmp_list = str1.split("-")
            start = int(tmp_list[0])
            end = int(tmp_list[1])
            for i in range(start, end+1):
                status.append(i)
        else:
            status.append(int(str1))
            
    return status


def replace_output(new_text):
    # Move the cursor to the beginning of the line
    sys.stdout.write('\r')
    # Clear the line
    sys.stdout.write('\033[K')
    # Print the new text
    sys.stdout.write(str(new_text))
    # Flush the output to ensure it's displayed immediately
    sys.stdout.flush()

def printrep(string1):
    replace_output('')
    print(string1)

count_dir = 0
def GetRequest(url1, dir1, event):
    global count_dir
    try:
        if (output): 
            file = open(output, "w+")
        while True:
            url2 = url1 + dir1
            res = requests.get(url2, verify=verify)
            stat_code = res.status_code
            if (color):
                stat_code = Colors(stat_code)
            if (res.status_code in status): # Sucess if status code is e.g. 302/200
                output_string = f"Found {dir1} [{stat_code}]"
                replace_output('')
                printrep(output_string)
                if (output): 
                    file.write(output_string)
                
                break
            elif (res.status_code in status_pause):
                printrep(f"{url2} triggered Pause status: [{stat_code}]")
                printrep("If this is due to IP block, then change your IP first.")
                event.clear() # Pauses threads
                input("Press any key to try again..")
                event.set() # Unpauses threads
                
            else:
                #print(f"{url2} Not success [{stat_code}]")
                break
        
        count_dir = count_dir + 1    
        replace_output(f'Running - {count_dir} of {dir_num}')
        if (output): 
            file.close()
            
    except Exception as ex:
        printrep(ex)

def create_threads(url_string, direc_list, max_threads):
    event = Event()
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for directory in direc_list:
            executor.submit(GetRequest, url_string, directory, event)

# Checks
currentDate = str(datetime.now())
StartTime = time.perf_counter()

NumberOfArgs = len(sys.argv)
if (NumberOfArgs==1): # If there is no arguments, prints out the Script's Usage.
	parser.print_usage()
	sys.exit()

if (not directory_file):
	print("Error: Missing wordlist")
	parser.print_usage()
	sys.exit()


dir_list = open(directory_file).read().split('\n') # Opens directory wordlist and transforms it into a list ['dir1','dir2',..]    	
dir_num = len(dir_list)
url = CheckSlash(url) # Check if url has slash, if not added it.
status = GetStatusCode(status)
status_pause = GetStatusCode(status_pause)

for stat in status:
    if (stat in status_pause):
        print("It seems there is a status code assigned to --pause and --status. Remove one of them and try again.")
        sys.exit()

# Start
print("* \033[33mStarting WafflesBuster\033[37m *")
print(f"- Settings:\n| URL: '{url}'\n| Wordlist: '{directory_file}'\n| Status Codes: {args.status}\n| Status Pause: {args.pause}\n| Threads: {threads_num} ")
if (output):
	print(f"| Output: {output}")

print("-")
create_threads(url, dir_list, threads_num)


EndTime = time.perf_counter()
RunTime = EndTime - StartTime
printrep(f"* Finished scan in {round(RunTime, 3)}s.")
