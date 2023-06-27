import socket
import sys
import time
from datetime import datetime
import binascii
import os
from random import randint


if (len(sys.argv) != 6):
    print("bad argument")  
    exit()


intervalleTempsEveille = int(sys.argv[1])
tempsexp = int(sys.argv[2])
timeout = float(sys.argv[3])
t0 = int(sys.argv[4])
arrivemessage = float(sys.argv[5])

adressIPmachine = "127.0.0.1"


def Traitement(socket1, trame, AdresseIP,donneprint):
    entete = bin(int.from_bytes(trame[0:1] + b'\x01', "little"))[3:]

    match entete[0:3]:
        case "000" : 
            donneprint.append("STA : Data recu, "+ str(time.time())[-11:])
            delai.append(str(time.time()))
            return entete[3] == "1"
        case "010" :
            donneprint.append("STA : NDP recu, "+ str(time.time())[-11:])
            return True
    
    return False

def Serviceperiod(socket1, donneeAEnvoye, adresseIPstation,donneprint):
    debutSP = time.time()
    donneprint.append("STA : debut periode de service, " + str(debutSP)[-11:])
    debutMinWakeDuration = time.time()

    NDPorEOSPrecu = False

    while (time.time() - debutSP < intervalleTempsEveille-0.3 and not NDPorEOSPrecu and time.time() - debutMinWakeDuration < 1):
        try:
            (trame,adressIP) = socket1.recvfrom(1024)
            NDPorEOSPrecu = Traitement(socket1,trame,adressIP,donneprint)
            debutMinWakeDuration = debutMinWakeDuration + 10
        except:
            """Timeout"""
        if(len(donneeAEnvoye) != 0):
            socket1.sendto(b'\x00' + donneeAEnvoye.pop(0),(adresseIPstation,6543))
            donneprint.append("STA : Data envoye," + str(time.time())[-11:])
    donneprint.append("STA: fin de periode de service, "+ str(time.time())[-11:])




socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket1.settimeout(timeout)
socket1.bind(("",6544))

delai = []

donneeAEnvoye = []

donneprint = []

dateAchange = True
tampon = datetime.now().second

while datetime.now().second != t0 :
    """"""
print("STA : debut exp Station " + str(time.time()))
debutexp = time.time()
try: 
    while time.time() - debutexp <= tempsexp:
        if(time.time()%arrivemessage < arrivemessage*0.1):
            donneeAEnvoye.append(binascii.b2a_hex(os.urandom(randint(200,1500))))
        if tampon != datetime.now().second:
            dateAchange = True
        if dateAchange and datetime.now().second%intervalleTempsEveille == 0:
            tampon = datetime.now().second
            dateAchange = False

            Serviceperiod(socket1, donneeAEnvoye, adressIPmachine, donneprint)
except KeyboardInterrupt:
    socket1.close()
    print("socket close")

socket1.close()
print("STA : fin de l'expériance")

fichier = open("STA.txt", "w")
while donneprint != []:
    fichier.write(donneprint.pop(0)+ '\n')
fichier.close()

fichier = open("delaiDSsta.txt","w")
while delai != []:
    fichier.write(delai.pop(0) + "\n")
fichier.close()
