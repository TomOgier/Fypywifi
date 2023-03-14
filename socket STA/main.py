from network import WLAN
import machine
from machine import Timer
import ubinascii
import socket
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


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

addr = socket.getaddrinfo("192.168.4.1", 6543)[0][-1]
print(addr)
print('socket connected')
# it is possible to attach additional HTTP headers in the line below, but note to always close with \r\n\r\n
n="H"
s.sendto(n,("192.168.4.1", 6543))
time.sleep(1)

print('end')