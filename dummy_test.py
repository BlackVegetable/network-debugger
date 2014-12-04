
from scapy.all import *
import test_dsm as dsm
import of_side_effect as OF
import sys
import threading

pkts = sniff(offline="./example_packets/example_packets2.pcap")
pkt = pkts[0]

# Pretend the pkt is originally a POX packet converted to bytes.
pkt_bytes = str(pkt)

# Convert the raw bytes to a new packet compatible with Scapy.
pkt = Ether(pkt_bytes)

engine = dsm.Engine()

starting_of_rules = engine.get_initial_rules()
print "List of starting rules: "
for rule in starting_of_rules:
    print str(rule)

def invoke_with_packet_or_timeout(pkt, timeout=0):
    ret_list = []
    if pkt:
        ret_list = engine.handle_packet(pkt)
    else:
        ret_list = engine.handle_packet(None, timeout)

    if ret_list[0] == "Exit":
        print "DSM Complete!"
        sys.exit(0)
    if ret_list[0] == True:
        print "We matched a packet!"
    else:
        print "Nothing matched..."
    if len(ret_list) > 1:
        print "OF rules to apply: " + str(ret_list[1:])



invoke_with_packet_or_timeout(pkt)
invoke_with_packet_or_timeout(None, 100)
invoke_with_packet_or_timeout(pkt)
invoke_with_packet_or_timeout(None, 100)
invoke_with_packet_or_timeout(pkt)
invoke_with_packet_or_timeout(None, 100)
invoke_with_packet_or_timeout(pkt)
invoke_with_packet_or_timeout(None, 100)
invoke_with_packet_or_timeout(pkt)
invoke_with_packet_or_timeout(None, 100)
invoke_with_packet_or_timeout(pkt)
invoke_with_packet_or_timeout(None, 100)
invoke_with_packet_or_timeout(pkt)
invoke_with_packet_or_timeout(None, 100)
