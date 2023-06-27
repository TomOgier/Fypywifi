import socket
import binascii
import time
import os
from numpy import random
from datetime import datetime
from random import randint
'''
socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket1.settimeout(0.2)
result = binascii.b2a_hex(os.urandom(randint(200,1500)))
print(result)


socket1.bind(("",6543))

socket1.sendto(result, ("140.77.178.54",6544))
'''
bg = "1687774415.0077944"
print(random.exponential(1/10,size=1))
