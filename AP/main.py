from network import WLAN
import ubinascii
import pycom
import time
import machine


#initialistaion en mode AP 
pycom.heartbeat(False)
wlan = WLAN()
#wlan.init(mode=WLAN.STA)
wlan.init(mode=WLAN.AP, ssid='Facto')
wlan.antenna(WLAN.EXT_ANT)
print("Je suis l'AP")
print('mon adresse MAC est :')
print(ubinascii.hexlify(machine.unique_id(),':').decode())


#  ------------------------------------


#pile de data a envoyé (pas totalement encore utilisé)
dataToSend = []

#permet de savoir si l'AP attend un ack 
waitForAck = False

#permet de définir si une trame nous apprtient avec l'adresse mac source
def accept_pack(pack):
    return pack.data[4]==0xfc and pack.data[5]==0xf5 and pack.data[6] == 0xc4 and pack.data[7]==0x0d and pack.data[8]==0xef and (pack.data[9]==0x64 or pack.data[9]==0x65)

#permet de définir si c'est un acquitement (premier octet de donnée utile a 1)
def accept_ack(pack):
    return len(pack.data) - 28 == 2 and pack.data[24] == 0x01 

#permet de définir si c'est un pspoll (premier octet de donnée utile a 2)
def accept_pspoll(pack):
    return len(pack.data) - 28 == 1 and pack.data[24] == 0x02

#permet de définir si c'est de la data (premier octet de donnée utile a 3)
def accept_data(pack):
    return len(pack.data) - 28 > 1 and pack.data[24] == 0x03

beacon =    b'\x80\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xfc\xf5\xc4\x0d\xef\x64\xfc\xf5\xc4\x0d\xef\x64\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x64\x00\x31\x04\x00\x04\x46\x41\x43\x54\x01\x08\x82\x84\x8B\x96\x0C\x12\x18\x24\x03\x01\x01\x05\x04\x01\x02\x00\x00'
ackNoData = b'\x08\x00\x00\x00\xf0\x08\xd1\xcb\x59\x68\xfc\xf5\xc4\x0d\xef\x65\xfc\xf5\xc4\x0d\xef\x65\x00\x00\x01'
data =      b'\x08\x00\x00\x00\xf0\x08\xd1\xcb\x59\x68\xfc\xf5\xc4\x0d\xef\x65\xfc\xf5\xc4\x0d\xef\x65\x00\x00\x03\xff'


#fonction appelé lorsque l'AP recoit un paquet
#L'ensemble de l'algorithme distribué se trouve dans cette fonction
def monitor(pack):
    pk = wlan.wifi_packet()
    if accept_pack(pk): 
        #deux cas de figure, si l'AP recoit un Ack ou un pspoll
        if accept_ack(pk) and waitForAck:
            # si l'AP recoit un ack et en attend un, la data qui a été envoyé est enlevé de la pile
            waitForAck=False
            dataToSend.pop()

        if accept_pspoll(pk):
            # deux cas de figure s'il y a des data a envoyé ou non
            print("j'ai recu un pspoll")
            #si non l'AP envoit juste un ACK
            if len(dataToSend) == 0:
                wlan.send_raw(Buffer=ackNoData)
                
                print('acknodata envoye')
            #si oui l'AP envoie un data et se met en attente d'un Ack
            else:
                print('jai envoyé des data')
                waitForAck = True
                wlan.send_raw(Buffer=data)

       
        


#wlan.send_raw(Buffer=beacon,interface=WLAN.AP)


wlan.callback(trigger=WLAN.EVENT_PKT_DATA, handler=monitor)
wlan.promiscuous(True)
#wlan.send_raw(Buffer=ackNoData)
machine.idle()
