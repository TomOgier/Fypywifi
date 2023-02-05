from network import WLAN
import ubinascii
import pycom
import time
import machine

def monitordata(pack):
    pk = wlan.wifi_packet()
    if pk.data[8]==0x59 and pk.data[9] == 0x68: 
        if len(pk.data) - 28 == 1 and pk.data[24] == 0x01:
            print("j'ai recu un pspoll")
            
        

pycom.heartbeat(True)
wlan = WLAN()
wlan.antenna(WLAN.EXT_ANT)
print("Je suis l'AP")


beacon = b'\x80\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xF0\x08\xD1\xCB\x59\x00\xF0\x08\xD1\xCB\x59\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x64\x00\x31\x04\x00\x04\x46\x41\x43\x54\x01\x08\x82\x84\x8B\x96\x0C\x12\x18\x24\x03\x01\x01\x05\x04\x01\x02\x00\x00'



print(ubinascii.hexlify(machine.unique_id(),':').decode())
#wlan.send_raw(Buffer=beacon,interface=WLAN.AP)

wlan.callback(trigger=WLAN.EVENT_PKT_DATA, handler=monitordata)
wlan.promiscuous(True)


