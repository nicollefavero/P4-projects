from scapy.all import *
import sys, os

TYPE_FOR = 0x600

class TelemetryHeader(Packet):
    fields_desc = [    IntField("type", 0),
                       IntField("sw", 0),
                       IntField("flowid_1", 0),
                       IntField("flowid_2", 0),
                       IntField("field", 0)]

bind_layers(IP, TelemetryHeader, proto=18)
#bind_layers(ForensicsHeader, Gradient, action=0)
