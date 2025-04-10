import socket
import os
import requests
import platform

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
def Port_Scanner(victim): 
    clear()
    print("""
    1) Enter port number
    2) All ports (may take long time)
    """)

    portInput = input("Select: ")

    if portInput == '1':
        pn = input("PORT NUMBER: ")
        os.system("nmap -p" + pn + " " + victim)

    if portInput == '2':
        os.system("nmap -p- " + victim)

# 03) WayBack urls     
def WayBack_urls(victim):                         
    statusCode = "0"

    option = input("""
    1) Status Code 200
    2) Status Code 302
    3) Status Code 403
    4) Status Code 404
    5) ALL Urls
    
    INPUT: """)

    if (option == "1"):
        statusCode = "200"
    elif (option == "2"):
        statusCode = "302"
    elif (option == "3"):
        statusCode = "403"
    elif (option == "4"):
        statusCode = "404"
    elif (option != "5"):
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
def Dorking(victim):
    keywords = input("Enter Keywords: ")
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
def DOS_Attack(victim):
    os.system('cd modules/dosattack && echo "\n" && python3 dosattack.py')
    argument = input('\nEnter a valid argument for DOS attack: ')
    os.system('cd modules/dosattack && python3 dosattack.py ' + argument)

# 15) Set New Target
def setNewTarget(isIP):
    clear()
    global victim
    if isIP:
        victim = socket.gethostbyname(victim)

# 16) EXIT                

def iseeverything(choose, victim):
    
    try:
        if choose == '1':
            IP_Finder(victim)

        elif choose == '2':
            Port_Scanner(victim)

        elif choose == '3':
            WayBack_urls(victim)

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

        elif choose == '12':
            Dorking(victim)

        elif choose == '13':
            Check_if_domain_email_spoofable(victim)

        elif choose == '14':
            DOS_Attack(victim)

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

# example
choose = "1"
victim = "www.baidu.com"  # or ip
setNewTarget(False)
iseeverything(choose, victim)