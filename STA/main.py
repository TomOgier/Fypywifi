from network import WLAN
import machine
import ubinascii

listenIntervalle = 1000

def accept_pack(pack):
    return pack.data[4]==0xf0 and pack.data[5]==0x08 and pack.data[6] == 0xd1 and pack.data[7]==0xcb and pack.data[8]==0x59 and pack.data[9]==0x68

def accept_ack(pack):
    return len(pack.data) - 28 == 1 and pack.data[24] == 0x01 

def accept_pspoll(pack):
    return len(pack.data) - 28 == 1 and pack.data[24] == 0x02 

def accept_data(pack):
    return len(pack.data) - 28 >= 1 and pack.data[24] == 0x03

pspoll = b'\x08\x00\x00\x00\xfc\xf5\xc4\x0d\xef\x64\xf0\x08\xd1\xcb\x59\x68\xfc\xf5\xc4\x0d\xef\x64\x00\x00\x02'
ackData = b'\x08\x00\x00\x00\xfc\xf5\xc4\x0d\xef\x64\xf0\x08\xd1\xcb\x59\x68\xfc\xf5\xc4\x0d\xef\x64\x00\x00\x01'




def monitor(pack):
    pk = wlan.wifi_packet()
    if accept_pack(pk):
        if accept_ack(pk):
            print("j'ai recu un ack")
            #machine.sleep(listenIntervalle,True)
            wlan.send_raw(Buffer=pspoll)
        if accept_data(pk):
            print("j'ai recu une data")
            #wlan.send_raw(Buffer=ackData)
            machine.sleep(listenIntervalle)
            print(("je suis reveill"))
            #wlan.send_raw(Buffer=pspoll)


print("Je suis la STA")
wlan = WLAN(antenna=WLAN.EXT_ANT)

print(ubinascii.hexlify(machine.unique_id(),':').decode())


wlan.callback(trigger=WLAN.EVENT_PKT_DATA, handler=monitor)
#wlan.callback(trigger=WLAN.EVENT_PKT_ANY,handler=test)
wlan.promiscuous(True)


wlan.send_raw(Buffer=pspoll)



