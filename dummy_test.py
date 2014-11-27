
from scapy.all import *
import test_dsm as dsm
import of_side_effect as OF

pkts = sniff(offline="./example_packets/example_packets2.pcap")
pkt = pkts[0]

engine = dsm.Engine()

starting_of_rules = engine.get_initial_rules()
print "List of starting rules: "
for rule in starting_of_rules:
    print str(rule)

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
