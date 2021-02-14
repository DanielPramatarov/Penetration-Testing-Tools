import socket
import os
import sys
import binascii
import struct
import time

sock_created = False
sniffer_socket = 0

def analyze_ip_header(data_recv):
    ip_hrd = struct.unpack('!6H4s4s',data_recv[:20])
    ver = ip_hrd[0] >> 12
    ihl = (ip_hrd[0] >> 8) & 0x0f
    tos = ip_hrd[0] & 0x00ff
    tos_len = ip_hrd[1]
    ip_id = ip_hrd[2]
    flags = ip_hrd[3] >> 13
    frag_offset = ip_hrd[3] & 0x1fff
    ip_ttl = ip_hrd[4] >> 6
    ip_proto = ip_hrd[4] & 0x00f
    checksum = ip_hrd[5]
    src_address = socket.inet_ntoa(ip_hrd[6])
    dst_address = socket.inet_ntoa(ip_hrd[7])
    data = data_recv[20:]
    print(f"________________IP HEADER________________")
    print(f"Version: {ver}")
    print(f"IHL: {ihl}")
    print(f"TOS: {tos}")
    print(f"Lenght: {tos_len}")
    print(f"ID: {ip_id}")
    print(f"Offset: {frag_offset}")
    print(f"TTL: {ip_ttl}")
    print(f"Proto: {ip_proto}")
    print(f"Checksum: {checksum}")
    print(f"Source IP: {src_address}")
    print(f"Destination IP: {dst_address}")

    if ip_proto == 6:
        tcp_udp = "TCP"
    elif ip_proto == 17:
        tcp_udp = "UDP"
    else:
        tcp_udp = "OTHER"

    return data, tcp_udp

def analyze_ether_header(data_recv):
    ip_bool = False

    eth_hdr = struct.unpack('!6s6sH',data_recv[:14])
    dest_mac = binascii.hexlify(eth_hdr[0])
    src_mac = binascii.hexlify(eth_hdr[1])
    proto = eth_hdr[2] >> 8
    data = data_recv[14:]

    print(f"________________ETHERNET HEADER________________")
    print(f"Destionation MAC: {dest_mac[0:2]}:{dest_mac[2:4]}:{dest_mac[4:6]}:{dest_mac[6:8]}:{dest_mac[8:10]}:{dest_mac[10:12]}")
    print(f"Source MAC: {src_mac[0:2]}:{src_mac[2:4]}:{src_mac[4:6]}:{src_mac[6:8]}:{src_mac[8:10]}:{src_mac[10:12]}")
    print(f"PROTOCOL: {proto}")

    if proto == 0x08:
        ip_bool = True
    return data, ip_bool
def main():

    global sock_created
    global sniffer_socket
    if sock_created == False:
        sniffer_socket = socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x0003))
        sock_created = True
    data_recv = sniffer_socket.recv(2048)
    os.system("clear")

    data_recv, ip_bool = analyze_ether_header(data_recv)

    if ip_bool:
        data_recv, tcp_udp = analyze_ip_header(data_recv)
    else: 
        return


while(True):
    time.sleep(0.5)
    main()