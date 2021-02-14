import multiprocessing, sys, netaddr, argparse, logging
from scapy.all import *
from datetime import datetime
import optparse
import pyfiglet 
from colorama import Fore, Back, Style 

def banner():
    first = f"""{Fore.WHITE}
    _   _______________       ______  ____  __ __
   / | / / ____/_  __/ |     / / __ \/ __ \/ //_/
  /  |/ / __/   / /  | | /| / / / / / /_/ / ,<   
 / /|  / /___  / /   | |/ |/ / /_/ / _, _/ /| |  
/_/ |_/_____/ /_/    |__/|__/\____/_/ |_/_/ |_|     
{Style.RESET_ALL}  
"""
    second = f"""{Fore.GREEN}
    ____  _________ __________ _    ____________     
   / __ \/  _/ ___// ____/ __ \ |  / / ____/ __ \    
  / / / // / \__ \/ /   / / / / | / / __/ / /_/ /    
 / /_/ // / ___/ / /___/ /_/ /| |/ / /___/ _, _/     
/_____/___//____/\____/\____/ |___/_____/_/ |_|     
{Style.RESET_ALL}  
"""

    third = f"""{Fore.RED}
   __________  ____  __ 
 /_  __/ __ \/ __ \/ / 
  / / / / / / / / / /  
 / / / /_/ / /_/ / /___
/_/  \____/\____/_____/
                          
{Style.RESET_ALL}  
"""

    text = first +second + third
    print(text)


conf.verb = 0

class const:
    ARP = 0
    PING = 1
    TCP = 2

def arpScan(subnet):
    ans,unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=subnet), timeout=2)
    for snd,rcv in ans:
        print(rcv.sprintf(r"[ARP] Online: %ARP.psrc% - %Ether.src%"))

def ping(ip):
    reply = sr1(IP(dst=str(ip)) / ICMP(), timeout = 3)
    if reply is not None:
        print(f"[PING]{Fore.GREEN} Online{Style.RESET_ALL}: " + str(ip))

def tcp(ip):
    port = 53
    srcp = RandShort()
    pkt = sr1(IP(dst = str(ip)) / TCP(sport = srcp, dport = port, flags = "S"), timeout = 5)
    if pkt is not None and pkt.getlayer(TCP) is not None: 
        try:
            flag = pkt.getlayer(TCP).flags

            
            if flag is not None:
                if flag == 0x12: 
                    print("[TCP] Online:" + str(ip) + " - replied with syn,ack")
                    send(IP(dst = str(ip)) / TCP(sport = srcp, dport = port, flags = "R"))
                elif flag == 0x14: 
                    print("[TCP] Online: " + str(ip) + " - replied with rst,ack")
        except:
            pass

def scan(subnet, typ):
    jobs = []
    for ip in subnet:
        if typ == const.PING:
            p = multiprocessing.Process(target=ping, args=(ip,))
            jobs.append(p)
            p.start()
        else:
            p = multiprocessing.Process(target=tcp, args=(ip,))
            jobs.append(p)
            p.start()
    
    for j in jobs:
        j.join()    

def main(subnet_to_scan, typeNUM):
    subnet = netaddr.IPNetwork(subnet_to_scan)
    start = datetime.now()
    print ("==================================================")
    print ("Scanning " + str(subnet[0]) + " to " + str(subnet[-1]))
    print ("Started  " + str(start))
    print ("==================================================")

    if typeNUM == const.ARP:
        arpScan(subnet_to_scan)
    elif typeNUM == const.PING:
        scan(subnet, const.PING)
    elif typeNUM == const.TCP:
        scan(subnet, const.TCP)
    else:
        arpScan(subnet_to_scan)
        scan(subnet, const.PING)
        scan(subnet, const.TCP)

    stop = datetime.now()
    print ("==================================================")
    print ("Scan Duration: " + str(stop - start))
    print ("Completed  " + str(stop))
    print ("==================================================")


help_text = """ sudo Python3 NetDiscover.py -s [subnet mask] or [IP] -t [Type Scan]
"""
parser = optparse.OptionParser(usage=help_text)
parser.add_option("-s", "--Subnet", dest="Subnet",help="Subnet to scan for hosts", type=str)
parser.add_option("-t","--type",dest="type_scan", default=3, help="Type of scan: [0 = Arp, 1 = Ping, 2 = TCP, 3 = ALL]" , type=int)


if len(sys.argv[1:])==0:
    parser.print_help()
    parser.exit()

banner()
(options, arguments) = parser.parse_args()

main(options.Subnet, options.type_scan)
