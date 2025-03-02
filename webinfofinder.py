import socket
import os
import requests
import platform
import sys
import subprocess

def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

# 01) IP Finder                                
def IP_Finder(victim): 
    ipAddr = socket.gethostbyname(victim)
    print(ipAddr)

# 02) Port Scanner  
def Port_Scanner(victim, port_choice, port_number):
    try:
        command = ["nmap"]
        if port_choice == '1' and port_number:
            command.extend(["-p", port_number, victim])
        elif port_choice == '2':
            command.extend(["-p-", victim])
    # Run the command and capture the output
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return f"An error occurred: {str(e)}"

# 03) WayBack urls     
def WayBack_urls(victim, status_code_choice):                         
    statusCode = "0"

    if (status_code_choice == "1"):
        statusCode = "200"
    elif (status_code_choice == "2"):
        statusCode = "302"
    elif (status_code_choice == "3"):
        statusCode = "403"
    elif (status_code_choice == "4"):
        statusCode = "404"
    elif (status_code_choice != "5"):
        print("\n\033[91mNot Valid. Kindly fill the between 1-5 ONLY!")

    if (statusCode != "0"):
        pagelink = "http://web.archive.org/cdx/search/cdx?url=*." + victim + \
            "/*&output=text&fl=original&collapse=urlkey&filter=statuscode:" + statusCode
    else:
        pagelink = "http://web.archive.org/cdx/search/cdx?url=*." + \
            victim + "/*&output=text&fl=original&collapse=urlkey"

    info = requests.get(pagelink)
    print('\033[91m', info.text)


# 04) Subdomain Listing (use Sublistr) 
def Subdomain_Listing_by_Sublistr(victim):                         
    clear()
    os.system('cd modules/Sublist3r && python3 sublist3r.py -d ' + victim)
    
# 05) Get robots.txt
def Get_robotstxt(victim):  
    robots = 'http://' + victim + '/robots.txt'
    info = requests.get(robots)
    print('\033[91m', info.text)

# 06) Host Info Scanner (use WhatWeb)         
def Host_Info_Scanner(victim):  
    clear()
    os.system('whatweb -v '+victim)

# 07) DNS Lookup   
def DNS_Lookup(victim):
    dnslook = 'https://api.hackertarget.com/dnslookup/?q='+victim
    info = requests.get(dnslook)
    print('\033[91m', info.text)

# 08) Hosts Search
def Hosts_Search(victim):                            
    host = 'https://api.hackertarget.com/hostsearch/?q='+victim
    info = requests.get(host)
    print('\033[91m', info.text)

# 09) Geo Location
def Geo_Location(victim):
    ipgeo = 'https://api.hackertarget.com/geoip/?q='+victim
    info = requests.get(ipgeo)
    print('\033[91m', info.text)
    info.close()

# 10) Host Information
def Host_Information(victim):
    iplt = 'https://ipinfo.io/'+socket.gethostbyname(victim)+'/json'
    info = requests.get(iplt)
    print('\033[91m', info.text)
    info.close()

# 11) List Shared DNS Servers
def List_Shared_DNS_Servers(victim):
    shared = 'https://api.hackertarget.com/findshareddns/?q='+victim
    info = requests.get(shared)
    print('\033[91m', info.text)

# 12) Dorking
def Dorking(victim, keywords):
    # keywords = input("Enter Keywords: ")
    os.system('cd modules/Dorker && python3 dorker.py search ' +
                keywords + " >> output.txt")
    run = open('modules/Dorker/output.txt', 'r')
    file = run.read()
    for i in file.split(sep="\n"):
        print('site:*.' + victim + " " + i)
    run.close()
    os.system('rm modules/Dorker/output.txt')

# 13) Check if domain email spoofable
def Check_if_domain_email_spoofable(victim):
    clear()
    os.system('cd modules/EmailSpoof && python3 checkSpoofable.py ' + victim)

# 14) DOS Attack
def DOS_Attack(attack_argument):
    os.system('cd modules/dosattack && echo "\n" && python3 dosattack.py')
    os.system('cd modules/dosattack && python3 dosattack.py ' + attack_argument)

# 15) Set New Target
def setNewTarget(isIP):
    clear()
    global victim
    if isIP:
        victim = socket.gethostbyname(victim)

# 16) EXIT                

def iseeverything():
    try: 
        # Skip the first line (address type, not used in analysis)
        _ = sys.stdin.readline()  # Read and discard the first line
    
        # Read the basic parameters
        choose = sys.stdin.readline().strip()
        victim = sys.stdin.readline().strip()
    
        # Handle choices that require additional inputs
        if choose == '2':  # Assuming '2' is for Port Scanner
            port_choice = sys.stdin.readline().strip()
            port_number = sys.stdin.readline().strip() if port_choice == '1' else None
            print(Port_Scanner(victim, port_choice, port_number))
        elif choose == '3':  # Assuming '3' is for WayBack urls
            status_code_choice = sys.stdin.readline().strip()
            WayBack_urls(victim, status_code_choice)
        elif choose == '12':  # Assuming '12' is for Dorking
            keywords = sys.stdin.readline().strip()
            Dorking(victim, keywords)
        elif choose == '14':
            attack_argument = sys.stdin.readline().strip()
            DOS_Attack(attack_argument)
        else:
            if choose == '1':
                IP_Finder(victim)

            elif choose == '4':
                Subdomain_Listing_by_Sublistr(victim)

            elif choose == '5':
                Get_robotstxt(victim)

            elif choose == '6':
                Host_Info_Scanner(victim)

            elif choose == '7':
                DNS_Lookup(victim)

            elif choose == '8':
                Hosts_Search(victim)

            elif choose == '9':
                Geo_Location(victim)

            elif choose == '10':  # Host Information
                Host_Information(victim)

            elif choose == '11':
                List_Shared_DNS_Servers(victim)

            elif choose == '13':
                Check_if_domain_email_spoofable(victim)


            elif choose == '15':
                setNewTarget()

            elif choose == '16' or choose == "exit":
                print("\033[91m\n\nThank You")
                exit

            else:
                print('?')

    except socket.gaierror:
        print('Name or service not known!\033[93m')
        print()
    except UnboundLocalError:
        print('The information you entered is incorrect')
        print()
    except requests.exceptions.ConnectionError:
        print('Your Internet Offline')
        exit
    except IndexError:
        print('?')
        print()


setNewTarget(False)
iseeverything()