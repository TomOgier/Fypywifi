import socket
import binascii
import time
import os
import math
import numpy
from datetime import datetime
from random import randint,random
'''
socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket1.settimeout(0.2)
result = binascii.b2a_hex(os.urandom(randint(200,1500)))
print(result)


socket1.bind(("",6543))

socket1.sendto(result, ("140.77.178.54",6544))
'''

def exponential(beta):
    return -(1/beta) * math.log(1.0 - random())

