#!/usr/bin/env python3
import random
import socket
import sys
import threading
import time

from scapy.all import IP, TCP, UDP, Ether, get_if_hwaddr, get_if_list, sendp

from scapy.all import sniff

from telemetry_header import TelemetryHeader

from warnings import filterwarnings
filterwarnings("ignore")


TYPE_READ = 0x0606
TYPE_SNAPSHOT = 0x0607
TYPE_UPDATE = 0x0608
TYPE_EXPORT = 0x0609


iface = 'eth0'
iface2 = 'h3-eth1'

snapshot_s1 = {}
snapshot_s2 = {}

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

def send_update():
    print("sending on interface %s" % (iface))
    pkt =  Ether(src=get_if_hwaddr(iface1), dst='ff:ff:ff:ff:ff:ff')
    pkt = pkt /IP(src="10.50.1.1", dst="10.50.1.6")  / TelemetryHeader(type=TYPE_UPDATE, sw=0, flowid=1, field=0)
    pkt.show2()
    sendp(pkt, iface=iface1, verbose=False)

    print("sending on interface %s" % (iface2))
    pkt =  Ether(src=get_if_hwaddr(iface2), dst='ff:ff:ff:ff:ff:ff')
    pkt = pkt / IP(src="10.50.1.1", dst="10.50.1.6") / TelemetryHeader(type=TYPE_UPDATE, sw=1, flowid=1, field=0)
    pkt.show2()
    sendp(pkt, iface=iface2, verbose=False)

def save_snapshot(pkt):
    if(pkt[TelemetryHeader].sw == 0):
        snapshot_s1[pkt[TelemetryHeader].flowid] = pkt[TelemetryHeader].field
    else:
        snapshot_s2[pkt[TelemetryHeader].flowid] = pkt[TelemetryHeader].field

def read_snapshot(rc_pkt):
    if(rc_pkt[TelemetryHeader].sw == 0):
        interface = iface
    else:
        interface = iface2

    pkt =  Ether(src=get_if_hwaddr(interface), dst='ff:ff:ff:ff:ff:ff')
    pkt = pkt / IP(src="10.50.1.1", dst="10.50.1.6") / TelemetryHeader(type=TYPE_READ, sw=1, flowid=1, field=0)
    pkt.show2()
    sendp(pkt, iface=interface, verbose=False)

def handle_pkt(pkt):
    print("teste")
    if(TelemetryHeader in pkt):
        print("this is telemetry!")
        if(pkt[TelemetryHeader].type == TYPE_SNAPSHOT):
            print("Got a warning!")
            save_snapshot(pkt)
            read_snapshot(pkt)
        elif(pkt[TelemetryHeader].type == TYPE_EXPORT):
            save_snapshot(pkt)
            if((snapshot_s2[pkt[TelemetryHeader].flowid] + snapshot_s1[pkt[TelemetryHeader].flowid]) > 10):
                print("warning")
            send_update(pkt)

    sys.stdout.flush()

def receive(iface_):
    interface = iface_
    print("sniffing on %s" % interface)
    sys.stdout.flush()

    build_lfilter = lambda r: TelemetryHeader in r and (r[TelemetryHeader].type == TYPE_SNAPSHOT or r[TelemetryHeader].type == TYPE_EXPORT)
    #sniff(lfilter=build_lfilter, iface = interface, prn = lambda x: handle_pkt(x))
    sniff(iface = interface, prn = lambda x: handle_pkt(x))

def main():
    receivethread = threading.Thread(target=receive(iface))
    receivethread.start()

    receivethread2 = threading.Thread(target=receive(iface2))
    receivethread2.start()

    #send(iface, iface2)

if __name__ == '__main__':
    main()
