from network import WLAN
import ubinascii
import pycom
import time
import machine
from machine import RTC
from machine import Timer
import usocket
import socket
import _thread


#initialistaion en mode AP 
pycom.heartbeat(False)
wlan = WLAN()
#wlan.init(mode=WLAN.STA)
wlan.init(mode=WLAN.AP, ssid='Facto')
wlan.antenna(WLAN.EXT_ANT)
print("Je suis l'AP")
print('mon adresse MAC est :')
print(ubinascii.hexlify(machine.unique_id(),':').decode())

print(wlan.ifconfig(config=('192.168.4.1', '255.255.255.0', '192.168.4.254', '8.8.8.8')))

print(wlan.ifconfig())



#  ------------------------------------


# Les trois premiers bits sont pour dsesigner le type de paquet
# 000 data
# 001 pspoll
# 010 ack niveau 4
# 011 frame association
# 100 frame nul data 
# 101 frame datation
# le quatrième bit permer de spécifier le Flag EOSP



# Thread for handling a client
def client_thread(socket1, frame,address):
    # Receive maxium of 12 bytes from the client
    
    flag = bin(int.from_bytes(frame[0:1] + b'\x01', "little"))[3:]
    frame = frame[1:]
    print(flag[0:3])
    if (flag[0:3] == '001'):
        socket1.sendto(b'\x40',("192.168.4.4", 6543))
    
    if (flag[0:3] == '011'):
        chain = b''
        for i in range(6):
            chain = chain + Date.now()[i].to_bytes(2,"little")
        chain = chain + Date.now()[6].to_bytes(4,"little")
        chain = b'\xa0' + chain 
        print(Date.now())
        socket1.sendto(chain,("192.168.4.4", 6543))
    if (flag[0:3] == '000'):
        print("data recu")
       
def PeriodService(serversocket,dataToSend):
    chrono = Timer.Chrono()
    chrono.start()
    while (True):
        if (len(dataToSend) != 0):
            if (len(dataToSend) - 1 !=0):
                serversocket.sendto(b'\x10' + dataToSend.pop(),("192.168.4.4", 6543))
            else:
                serversocket.sendto(b'\x00' + dataToSend.pop(),("192.168.4.4", 6543))
        else:
            serversocket.sendto(b'\x80',("192.168.4.4", 6543))
            return
            break



Date = RTC()
Date.init()

# Set up server socket
serversocket = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
serversocket.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
serversocket.settimeout(.01)
serversocket.bind(("",6543))


# Accept maximum of 5 connections at the same time
#serversocket.listen()

# Unique data to send back
#c = 0
change = True
date = None
dataToSend = []
while True:
    # Accept the connection of the clients
    if (date != Date.now()[5]%5):
        change = True
    if (Date.now()[5]%5 == 0):
        date=Date.now()[5]%5
        change = False
        _thread.start_new_thread(PeriodService, (serversocket, dataToSend))
    
    try:
        (c, address) = serversocket.recvfrom(1024)
        _thread.start_new_thread(client_thread, (serversocket, c,address))
    except:
        '''hello'''
        
    
    # Start a new thread to handle the client
    
    #c = c+1

