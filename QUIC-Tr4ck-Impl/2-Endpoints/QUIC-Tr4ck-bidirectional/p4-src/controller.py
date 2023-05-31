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
TYPE_UPDATE_F = 0x0608
TYPE_UPDATE_B = 0x0618
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

def send_update(rcv_pkt):
    sum = int(snapshot_s1[rcv_pkt[TelemetryHeader].flowid_2]) - int(snapshot_s2[rcv_pkt[TelemetryHeader].flowid_2])
    print(sum)

    print("sending on interface %s" % (iface))
    pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
    pkt = pkt /IP(src="10.0.0.3", dst="10.50.1.6")  / TelemetryHeader(type=TYPE_UPDATE_B, flowid_1=rcv_pkt[TelemetryHeader].flowid_1, flowid_2=rcv_pkt[TelemetryHeader].flowid_2, field=sum)
    pkt.show2()
    sendp(pkt, iface=iface, verbose=False)

    print("sending on interface %s" % (iface2))
    pkt =  Ether(src=get_if_hwaddr(iface2), dst='ff:ff:ff:ff:ff:ff')
    pkt = pkt / IP(src="10.50.1.1", dst="10.50.1.6") / TelemetryHeader(type=TYPE_UPDATE_F, flowid_1=rcv_pkt[TelemetryHeader].flowid_1, flowid_2=rcv_pkt[TelemetryHeader].flowid_2, field=sum)
    pkt.show2()
    sendp(pkt, iface=iface2, verbose=False)

def save_snapshot(pkt):
    #forward switch
    if(pkt[TelemetryHeader].sw == 3):
        snapshot_s1[pkt[TelemetryHeader].flowid_2] = pkt[TelemetryHeader].field
    else:
        #backward switch
        snapshot_s2[pkt[TelemetryHeader].flowid_2] = pkt[TelemetryHeader].field

def read_snapshot(rc_pkt):
    #if came from forward switch
    if(rc_pkt[TelemetryHeader].sw == 3):
        interface = iface
    else:
        interface = iface2

    pkt =  Ether(src=get_if_hwaddr(interface), dst='ff:ff:ff:ff:ff:ff')
    pkt = pkt / IP(src="10.0.0.3", dst="10.50.1.6") / TelemetryHeader(type=TYPE_READ, flowid_1=rc_pkt[TelemetryHeader].flowid_1, flowid_2=rc_pkt[TelemetryHeader].flowid_2, field=rc_pkt[TelemetryHeader].field)
    pkt.show2()
    sendp(pkt, iface=interface, verbose=False)

def handle_pkt(pkt):
    if(TelemetryHeader in pkt):
        if(pkt[TelemetryHeader].type == TYPE_SNAPSHOT):
            print("Got a warning!")
            save_snapshot(pkt)
            read_snapshot(pkt)
        elif(pkt[TelemetryHeader].type == TYPE_EXPORT):
            print("exported!")
            save_snapshot(pkt)
            if((snapshot_s2[pkt[TelemetryHeader].flowid_2] - snapshot_s1[pkt[TelemetryHeader].flowid_2]) > 10):
                print("warning")
            else:
                print("update")
            send_update(pkt)
            print("should be updated")

    sys.stdout.flush()

def receive(iface_):
    interface = iface_
    print("sniffing on %s" % interface)
    #sys.stdout.flush()

    build_lfilter = lambda r: TelemetryHeader in r and (r[TelemetryHeader].type == TYPE_SNAPSHOT or r[TelemetryHeader].type == TYPE_EXPORT)
    sniff(lfilter=build_lfilter, iface = interface, prn = lambda x: handle_pkt(x))
    #sniff(iface = interface, prn = lambda x: handle_pkt(x))

def main():
    receivethread = threading.Thread(target=receive, args=(iface,))
    receivethread.daemon=True
    receivethread.start()

    receivethread2 = threading.Thread(target=receive, args=(iface2,))
    receivethread2.daemon=True
    receivethread2.start()

    #send(iface, iface2)
    while True:
        continue

if __name__ == '__main__':
    main()
