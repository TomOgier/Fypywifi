from network import WLAN
import ubinascii
import pycom
import time
import machine
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

# Thread for handling a client
def client_thread(c,address):
    # Receive maxium of 12 bytes from the client
    print(c)
    if (c == b'pspoll'):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(b'ack',("192.168.4.4", 6543))
        s.close()




# Set up server socket
serversocket = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
serversocket.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
serversocket.bind(("",6543))


# Accept maximum of 5 connections at the same time
#serversocket.listen()

# Unique data to send back
#c = 0
while True:
    # Accept the connection of the clients
    print("attente")
    (c, address) = serversocket.recvfrom(1024)
    # Start a new thread to handle the client
    _thread.start_new_thread(client_thread, (c,address))
    #c = c+1

