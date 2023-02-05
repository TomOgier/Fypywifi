'''
# main.py -- put your code here!
from network import WLAN
import ubinascii
import machine

def pack_cb(pack):
    mac = bytearray(6)
    pk = wlan.wifi_packet()
    control = pk.data[0]
    subtype = (oxF0 & control) >> 4
    type = 0x0C & control
    print('camarche')
    print(pack)
    

wlan = WLAN()
#print(wlan.wifi_packet())
wlan.init(mode=WLAN.STA,antenna=WLAN.EXT_ANT)

wlan.init(power_save=True)
nets = wlan.scan()
for net in nets:
    if net.ssid == "FACT":
        print("network trouve")
        wlan.connect(net.ssid,auth=(net.sec,"motdepasse"))
        while not wlan.isconnected():
            machine.idle()
        print('WLAN est bien connecte')
        break


wlan.ifconfig(config=('192.168.4.10','255.255.255.0','192.168.4.1','8.8.8.8'))
print(wlan.ifconfig())
print(wlan.mac())


machine.sleep(20000)

wlan.callback(trigger=WLAN.EVENT_PKT_ANY,handler=pack_cb)
wlan.promiscuous(True)

pk = wlan.wifi_packet()
print(pk)
wlan.send_raw(Buffer=b'010110010101010101010101010101010101010101010101010101')

test = b'\x00\x00\x12\x00\x2e\x48\x00\x00\x10\x02\x99\x09\xa0\x00\xb4\x00\x80\x00\xac\xb5}\x8d;0<F\xd8~\x0e\xdd\xc2U0\xde'
test2= b'\x00\x00\x12\x00\x2e\x48\x00\x00\x10\x02\x99\x09\xa0\x00\xbb\x03\x00\x00\x40\x00\x00\x00\xff\xff\xff\xff\xff\xff\xfc\xf5\xc4\x0d\xef\x64\xff\xff\xff\xff\xff\xff\xa0\x6c\x00\x05\x46\x41\x43\x54\x4f\x01\x08\x8b\x96\x82\x84\x0c\x18\x30\x60\x32\x04\x6c\x12\x24\x48\xe6\x0e\x51\x07'

wlan.send_raw(Buffer=test2)

'''
from network import WLAN
import machine
import ubinascii

pspoll = b'\x08\x00\x00\x00\xf0\x08\xd1\xcb\x59\x68\xfc\xf5\xc4\x0d\xef\x64\xf0\x08\xd1\xcb\x59\x68\x00\x00\x01'
       

print("Je suis la STA")
wlan = WLAN(mode=WLAN.STA, antenna=WLAN.EXT_ANT)

wlan.send_raw(Buffer=pspoll)


wlan.callback(trigger=WLAN.EVENT_PKT_DATA, handler=pack_cb)
print(ubinascii.hexlify(machine.unique_id(),':').decode())
wlan.promiscuous(True)



