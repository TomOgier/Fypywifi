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


#  ------------------------------------


s = socket.socket()
host = ''
addr = socket.getaddrinfo("192.168.4.254", 6543)[0][-1]
s.connect(addr)
print('socket connected')
# it is possible to attach additional HTTP headers in the line below, but note to always close with \r\n\r\n
httpreq = 'GET / HTTP/1.1 \r\nHOST: '+ host + '\r\nConnection: close \r\n\r\n'
print('http request: \n', httpreq)
s.send(httpreq)
time.sleep(1)
rec_bytes = s.recv(10000)
print(rec_bytes)
print('end')