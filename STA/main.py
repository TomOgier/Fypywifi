from network import WLAN
import machine
from machine import Timer
import ubinascii
import time


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

#trame pspoll (erreur la fipy (AP) change le dernier bit de son adresse MAC)
pspoll =  b'\x08\x00\x00\x00\xfc\xf5\xc4\x0d\xef\x65\xf0\x08\xd1\xcb\x59\x68\xfc\xf5\xc4\x0d\xef\x65\x00\x00\x01'

#trame ACK permetant d'acquiter les data
ackData = b'\x08\x00\x00\x00\xfc\xf5\xc4\x0d\xef\x65\xf0\x08\xd1\xcb\x59\x68\xfc\xf5\xc4\x0d\xef\x65\x00\x00\x01\01\02'



listenIntervalle = 10
waitForPaket = False

#permet de définir si une trame nous apprtient avec l'adresse mac source
def accept_pack(pack):
    return pack.data[4]==0xf0 and pack.data[5]==0x08 and pack.data[6] == 0xd1 and pack.data[7]==0xcb and pack.data[8]==0x59 and pack.data[9]==0x68

#permet de définir si c'est un acquitement (premier octet de donnée utile a 1)
def accept_ack(pack):
    return len(pack.data) - 28 == 1 and pack.data[24] == 0x01 

#permet de définir si c'est un pspoll (premier octet de donnée utile a 2)
def accept_pspoll(pack):
    return len(pack.data) - 28 == 1 and pack.data[24] == 0x02 

#permet de définir si c'est de la data (premier octet de donnée utile a 3)
def accept_data(pack):
    return len(pack.data) - 28 >= 1 and pack.data[24] == 0x03

def more_data(pack):
    return pack.data[1] == 0x30


def ifNoReturn(alarm):
    if waitForPaket:
        wlan.send_raw(Buffer=pspoll)
    else:
        alarm.cancel()


'''

#fonction appelé lorsque la STA recoit un paquet
#L'ensemble de l'algorithme distribué se trouve dans cette fonction
def monitor(pack):
    #récupere le paquet
    pk = wlan.wifi_packet()

    if accept_pack(pk):
        #deux cas de figure si la STA recoit un Ack ou une data
        if accept_ack(pk):
            # si Ack recu, plus de data a recevoir donc la STA s'endort
            print("j'ai recu un ack")
            waitForPaket = False
            machine.idle()
            # A la fin du doze state envoie un pspoll et reste en attente d'une reponse 
            print("je me reveille")
            wlan.send_raw(Buffer=pspoll)
            waitForPaket = True
            #Timer.Alarm(ifNoReturn, 1, periodic=True)

        if accept_data(pk):
            # si data recu, plus de data a recevoir donc la STA s'endort apres avoir envoyé un ack
            print("j'ai recu une data")
            wlan.send_raw(Buffer=ackData)
            waitForPaket = False
            if not more_data(pk):
                machine.idle()
                print(("je suis reveill"))
            # A la fin du doze state envoie un pspoll et reste en attente d'une reponse 
            wlan.send_raw(Buffer=pspoll)
            waitForPaket = True
            #Timer.Alarm(ifNoReturn, 1, periodic=True)





wlan.callback(trigger=WLAN.EVENT_PKT_DATA, handler=monitor)
#wlan.callback(trigger=WLAN.EVENT_PKT_ANY,handler=test)
wlan.promiscuous(True)

 

#time.sleep(2)


wlan.send_raw(Buffer=pspoll)
print("j'ai envoye un pspoll")
waitForPaket = True
while waitForPaket:
    time.sleep(1)
    wlan.send_raw(Buffer=pspoll)
    print(waitForPaket)



wlan.send_raw(Buffer=ackData)
for i in range (10):
    machine.sleep(1000)
    #
    #wlan.send_raw(Buffer=ackData)
    
    print("j'ai envoyé " + str(i))
'''
#Timer.Alarm(ifNoReturn, 1, periodic=True)


def test(pack):
    print(wlan.wifi_packet())


#wlan.callback(trigger=WLAN.EVENT_PKT_DATA,handler=test)
wlan.promiscuous(True)

