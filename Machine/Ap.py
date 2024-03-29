import socket
import sys
import time
import threading
import math
from datetime import datetime
import binascii
import os
from random import randint,random



if (len(sys.argv) != 7):
    print("bad argument")  
    exit()

"""arriver des messages toutes les A Secondes deterministes """

intervalleTempsEveille = int(sys.argv[1])
tempsexp = int(sys.argv[2])
timeout = float(sys.argv[3])
t0 = int(sys.argv[4])
typearrive = int(sys.argv[5])
arrivemessage = float(sys.argv[6])
"""argument durer SP"""

donneprint = []
delai = []

adressIPmachine = "127.0.0.1"
lock = threading.Lock()
donneeAEnvoye = []

def exponential(beta):
    return -(1/beta) * math.log(1.0 - random())


def Traitement(socket1, trame, AdresseIP,donneprint):
    entete = bin(int.from_bytes(trame[0:1] + b'\x01', "little"))[3:] 

    match entete[0:3]:
        case "000" : 
            donneprint.append("AP : Data recu," + str(time.time())[-11:])
        case "100" :
            donneprint.append("AP : envoie," + str(time.time())[-11:])


def Serviceperiod(socket1,donneeAEnvoye,adresseIPstation,donneprint):
    debutSP = time.time()
    donneprint.append("AP : debut periode de service, " + str(debutSP)[-11:])

    NDPaEnvoye = True

    while (time.time() - debutSP < intervalleTempsEveille-0.3 and len(donneeAEnvoye) != 0):
        NDPaEnvoye = False

        if len(donneeAEnvoye) - 1 != 0:
            lock.acquire()
            socket1.sendto(b'\x00'+ donneeAEnvoye.pop(0),(adresseIPstation,6544))
            lock.release()
            donneprint.append("AP : EOSP 0," + str(time.time())[-11:])
        else:
            lock.acquire()
            socket1.sendto(b'\x10' + donneeAEnvoye.pop(0),(adresseIPstation,6544))
            lock.release()
            donneprint.append("AP : EOSP 1," + str(time.time())[-11:])
        try:
            (trame,adressIP) = socket1.recvfrom(1024)
            Traitement(socket1,trame,adressIP,donneprint)
        except:
            """Timeout"""
    
    if NDPaEnvoye:
        socket1.sendto(b'\x40',(adresseIPstation,6544))
        donneprint.append("AP : envoie NDP," + str(time.time())[-11:])
    donneprint.append("AP : fin de periode de service," + str(time.time())[-11:])
        

class Thread_A(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global donneeAEnvoye    #made global here
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket1.settimeout(timeout)

        socket1.bind(("",6543))

        tampon = datetime.now().second

        dateAchange = True

        while datetime.now().second != t0 :
            """"""
        print("AP : debut exp AP " + str(time.time()))
        debutexp = time.time()
        try: 
            while time.time() - debutexp <= tempsexp:
                try:
                    (trame,adressIP) = socket1.recvfrom(1024)
                    Traitement(socket1,trame,adressIP,donneprint)
                except:
                    """Timeout"""
                if tampon != datetime.now().second:
                    dateAchange = True
                if dateAchange and datetime.now().second%intervalleTempsEveille == 0:
                    tampon = datetime.now().second
                    dateAchange = False

                    #print("AP : debut SP, " +str(time.time()))
                    Serviceperiod(socket1, donneeAEnvoye, adressIPmachine,donneprint)
        except KeyboardInterrupt:
            socket1.close()
            print("AP : socket close")
        socket1.close()
        print("AP : fin de l'expériance")

        fichier = open("AP.txt", "w")
        while donneprint != []:
            fichier.write(donneprint.pop(0)+ '\n')
        fichier.close()

        fichier = open("delaiDSap.txt","w")
        while delai != []:
            fichier.write(delai.pop(0) + "\n")
        fichier.close()


class Thread_B(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        
        while datetime.now().second != t0 :
            """"""
        global donneeAEnvoye
        debutexp = time.time()   
        chronomètre = time.time()
        match typearrive:   
            case 1:
                exp = exponential(arrivemessage)
                while time.time() - debutexp <= tempsexp:
                    if(chronomètre + exp < time.time()):
                        chronomètre = time.time()
                        lock.acquire()
                        donneeAEnvoye.append(binascii.b2a_hex(os.urandom(randint(200,1500))))
                        lock.release()
                        exp = exponential(arrivemessage)
                        delai.append(str(time.time()))
            case 2: 
                while time.time() - debutexp <= tempsexp:
                    if(chronomètre + arrivemessage < time.time()):
                        chronomètre = time.time()
                        lock.acquire()
                        donneeAEnvoye.append(binascii.b2a_hex(os.urandom(randint(200,1500))))
                        lock.release()
                        delai.append(str(time.time()))
a = Thread_A("Transmission")
b = Thread_B("Buffurisation")

b.start()
a.start()

a.join()
b.join()




