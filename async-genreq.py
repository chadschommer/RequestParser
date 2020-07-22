import asyncio
import pycurl
import sys 
import json
import asyncio
import time
import concurrent.futures

HOSTS = sys.argv[1]
uptimeUnbroken = True
RequestsPerCycle = 10
TotalRequests = 1000

def call(x):
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

# Borrowed from http://curio.readthedocs.org/en/latest/tutorial.html.
@asyncio.coroutine
def genreq(n):
    while n > 0:
        call(n)
        n -= 1

# while uptimeUnbroken:
loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(genreq(RequestsPerCycle))]
try:
    loop.run_forever(asyncio.wait(tasks))
except KeyboardInterrupt:
    pass
# loop.close()