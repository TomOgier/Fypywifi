from network import WLAN
import ubinascii
import pycom
import time
import machine


dataToSend = [1]

waitForAck = False

def accept_pack(pack):
    return pack.data[10]==0xfc and pack.data[11]==0xf5 and pack.data[12] == 0xc4 and pack.data[13]==0x0d and pack.data[14]==0xef and pack.data[15]==0x64

def accept_ack(pack):
    return len(pack.data) - 28 == 2 and pack.data[24] == 0x01 

def accept_pspoll(pack):
    return len(pack.data) - 28 == 1 and pack.data[24] == 0x02

def accept_data(pack):
    return len(pack.data) - 28 > 1 and pack.data[24] == 0x03

beacon = b'\x80\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xF0\x08\xD1\xCB\x59\x00\xF0\x08\xD1\xCB\x59\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x64\x00\x31\x04\x00\x04\x46\x41\x43\x54\x01\x08\x82\x84\x8B\x96\x0C\x12\x18\x24\x03\x01\x01\x05\x04\x01\x02\x00\x00'
ackNoData = b'\x08\x00\x00\x00\xfc\xf5\xc4\x0d\xef\x64\xf0\x08\xd1\xcb\x59\x68\xf0\x08\xd1\xcb\x59\x68\x00\x00\x01'
data = b'\x08\x00\x00\x00\xfc\xf5\xc4\x0d\xef\x64\xf0\x08\xd1\xcb\x59\x68\xf0\x08\xd1\xcb\x59\x68\x00\x00\x03\xff'

def monitor(pack):
    pk = wlan.wifi_packet()
    if accept_pack(pk): 
        if accept_ack(pk) and waitForAck:
            waitForAck=False
            dataToSend.pop()

        if accept_pspoll(pk):
            print("j'ai recu un pspoll")
            if len(dataToSend) == 0:
                wlan.send_raw(Buffer=ackNoData)
                
                print('acknodata envoye')
            else:
                #print('jai envoyé des data')
                waitForAck = True
                wlan.send_raw(Buffer=data)

       
        

pycom.heartbeat(False)
wlan = WLAN()
wlan.antenna(WLAN.EXT_ANT)
print("Je suis l'AP")


print(ubinascii.hexlify(machine.unique_id(),':').decode())
#wlan.send_raw(Buffer=beacon,interface=WLAN.AP)

wlan.callback(trigger=WLAN.EVENT_PKT_DATA, handler=monitor)
wlan.promiscuous(True)

wlan.send_raw(Buffer=ackNoData)