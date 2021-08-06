from scapy.all import *

interface = "wlan0"
ip_range = "192.168.1.0/24"
broadcastMac = "ff:ff:ff:ff:ff:ff"

packet = Ether(dst=broadcastMac)/ARP(pdst = ip_range) 

ans, unans = srp(packet, timeout =5, iface=interface, inter=0.9)

for send,receive in ans:
        print (receive.sprintf(r"%Ether.src% - %ARP.psrc%")) 