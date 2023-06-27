from network import WLAN
import machine
from machine import RTC
from machine import Timer
import ubinascii
import socket
import usocket
import _thread
import time
import uerrno
import uselect


#initialistaion en mode station 
wlan = WLAN()
wlan = WLAN(mode=WLAN.STA)
wlan.antenna(WLAN.EXT_ANT)
print("Je suis la STA")
print('mon adresse MAC est :')
print(ubinascii.hexlify(machine.unique_id(),':').decode())

#connection à l'AP avec le ssid Facto
ssid = ''
nets = wlan.scan()
for net in nets:
    if net.ssid == 'Facto':
        print('Network found!')
        ssid = net.ssid
        wlan.connect(ssid)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

wlan.ifconfig(config=('192.168.4.4', '255.255.255.0', '192.168.4.254', '8.8.8.8'))
#  ------------------------------------


serversocket = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
serversocket.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
serversocket.settimeout(.1)
serversocket.bind(("",6543))


Date = RTC()

dataToSend = []

# data \x01
# pspoll \x02
# ack niveau 4 \x04
# frame association \x20
# frame Nul data \x40
# frame date \x80


def client_thread(socket1, frame,adresse):

    flag = bin(int.from_bytes(frame[0:1] + b'\x01', "little"))[3:]
    frame = frame[1:] 
    
    if (flag[0:3] == '010'):
        print("debut attente")
        machine.sleep(10000)
        print("fin attente")
        socket1.sendto(b'\x20',("192.168.4.1", 6543))
    if (flag[0:3] == '000'):
        print("ca marche")
    if (flag[0:3] == '101'):
        # recu une date 
        buf = []
        for i in (0,2,4,6,8,10):
            buf.append(int.from_bytes(frame[i:(i+2)], 'little'))
        buf.append(int.from_bytes(frame[12:16],'little') + 140)
        buf.append(0)
        Date.init(buf)
    
    if (flag[0:3] == '100'):
        return True
    
    return False
    



# Set up clock


#envoie une trame d'association
serversocket.sendto(b'\x60',("192.168.4.1", 6543))
(c, address) = serversocket.recvfrom(1024)
client_thread(serversocket, c,address)



time.sleep(5)

nuldata = False

chrono = Timer.Chrono()

change = True
date = None
while True:  

    chrono.reset()
    chrono.start()
    if (date != Date.now()[5]%5):
        change = True
    if (Date.now()[5]%5 == 0 and change):
        change = False
        while( True):
            date = Date.now()[5]%5
            try:
                (c, address) = serversocket.recvfrom(1024)
                nuldata = client_thread(serversocket, c,address)
                chrono.reset()
            except:
                ''''''
            if (len(dataToSend) != 0):
                serversocket.sendto(b'\x00' + dataToSend.pop(),("192.168.4.4", 6543))
        
            if((nuldata or chrono.read_ms() > 500) and len(dataToSend) == 0 ):
                chrono.stop()
                print("ca")
                break



        
        
    
    
    