#!/usr/bin/env python3
import random
import socket
import sys
import logging

from scapy.all import IP, TCP, Ether, get_if_hwaddr, get_if_list, sendp

SENDER = "[SENDER]"

def get_if():
    ifs=get_if_list()
    iface=None # "h1-eth0"
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print("Cannot find eth0 interface")
        exit(1)
    return iface

def main():
    logging.basicConfig(
        filename="./packets-log/logs.log",
        filemode="a+",
        format="%(asctime)s %(message)s",
        level=logging.INFO,
    )

    if len(sys.argv)<3:
        print('pass 2 arguments: <destination> "<message>"')
        exit(1)

    addr = socket.gethostbyname(sys.argv[1])
    iface = get_if()

    logging.info(f"{SENDER} Trying to send a packet to {sys.argv[1]} with the message \"{sys.argv[2]}\"")

    print("sending on interface %s to %s" % (iface, str(addr)))
    pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
    pkt = pkt / IP(dst=addr) / TCP(dport=1234, sport=random.randint(49152,65535)) / sys.argv[2]
    pkt.show2()
    logging.info(f"{SENDER} Packet sent to IP address {sys.argv[1]}")
    sendp(pkt, iface=iface, verbose=False)


if __name__ == '__main__':
    main()
