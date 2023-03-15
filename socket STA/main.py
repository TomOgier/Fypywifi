from network import WLAN
import machine
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

nets = wlan.scan()
for net in nets:
    if net.ssid == 'Facto':
        print('Network found!')
        wlan.connect(net.ssid)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

wlan.ifconfig(config=('192.168.4.4', '255.255.255.0', '192.168.4.254', '8.8.8.8'))
#  ------------------------------------

def client_thread(c,address):
    # Receive maxium of 12 bytes from the client
    print(c)
    if (c == b'ack'):
        print("debut attente")
        machine.sleep(10000)
        print("fin attente")
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(b'pspoll',("192.168.4.1", 6543))
        s.close()



# Set up server socket



s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(b'pspoll',("192.168.4.1", 6543))
s.close()

while True:
    # Accept the connection of the clients
    serversocket = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
    serversocket.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
    serversocket.bind(("",6543))
    print("attente")
    (c, address) = serversocket.recvfrom(1024)
    # Start a new thread to handle the client
    serversocket.close()
    _thread.start_new_thread(client_thread, (c,address))
    #_thread.start_new_thread(client_thread, c)
    #c = c+1