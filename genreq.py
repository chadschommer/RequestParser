import pycurl
import sys 
import json
import asyncio
import time
import concurrent.futures

# """ Simple Python Script for testing uptime.
# Prints statistics on each request and evaluates if 200.
# If request returns non 200, break script.
# Written using Pycurl which is not ideal but only way I know to get fine-grain statistics.
# """

HOSTS = sys.argv[1]
uptimeUnbroken = True

def main():

    while uptimeUnbroken:
        genreq()

def genreq():

    CycleSleep = 1
    RequestsPerCycle = 100

    for i in range(RequestsPerCycle):
        c = pycurl.Curl()
        c.setopt(pycurl.URL, HOSTS)                #set url
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.WRITEFUNCTION, lambda x: None) #mute output

        c.perform()                                  #execute 
        dns_time = c.getinfo(pycurl.NAMELOOKUP_TIME) #DNS time
        conn_time = c.getinfo(pycurl.CONNECT_TIME)   #TCP/IP 3-way handshaking time
        ttfb = c.getinfo(pycurl.STARTTRANSFER_TIME)  #time-to-first-byte
        ttlb = c.getinfo(pycurl.TOTAL_TIME)    #time-to-last-byte
        status_code = c.getinfo(c.RESPONSE_CODE)

        if status_code != 200:
            uptimeUnbroken = False


        data = json.dumps({'dns_lookup_time':dns_time,         
                            'connection_time':conn_time,        
                            'time_to_first_byte':ttfb,    
                            'time_to_last_byte':ttlb,
                            'status_code':status_code})
        print(data)
        c.close()
    time.sleep(CycleSleep)

if __name__ == "__main__":
    print("Starting load test")
    main()