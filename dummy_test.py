
from scapy.all import *
import test_dsm as dsm

pkts = sniff(offline="./example_packets/example_packets2.pcap")
pkt = pkts[0]

engine = dsm.Engine()

engine.handle_packet(pkt)
engine.handle_packet(None, 100)
engine.handle_packet(pkt)
engine.handle_packet(None, 100)
engine.handle_packet(pkt)
engine.handle_packet(None, 100)
engine.handle_packet(pkt)
engine.handle_packet(None, 100)
engine.handle_packet(pkt)
engine.handle_packet(None, 100)
engine.handle_packet(pkt)
