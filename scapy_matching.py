
# Typically importing all is a bad practice, but this is the core library we're
# going to be using, so I don't feel too terrible about it.
from scapy.all import *
import re

def main():   
    # Files from Wireshark will need to be passed to the editcap program.
    # To use: `editcap -F libpcap <old_pcap_file> <new_pcap_file>`
    # This will only work if the original pcap file does not capture
    # across more than one interface!
    
    # There are two ways to read from a pcap file. They seem identical in their
    # output. I'll only use the "sniff" one for now, but here is the other:
    # a = rdpcap("./example_packets2.pcap")
    
    pkts = sniff(offline="./example_packets/example_packets2.pcap")
    pkt = pkts[0]
    
    # Here are all of the things a packet object can do:
    # print dir(pkts[0])
    
    # The "fields" of a pcap packet object are the Ethernet frame fields
    # 'src', 'dst', and 'type', which in this case is 0x800, or IPv4.
    #print pkts[0].fields
    
    print "Source MAC: " + pkt.src
    print "Destination MAC: " + pkt.dst
    print "Next protocol (type): " + `pkt.type`
    
    pkt_ip = pkt.getlayer(IP)
    print "Source Address: " + pkt_ip.src
    print "Destination Address: " + pkt_ip.dst
    print "Next protocol: " + `pkt_ip.proto`
    
    pkt_udp = pkt_ip.getlayer(UDP)
    
    print "Source Port: " + `pkt_udp.sport`
    print "Destination Port: " + `pkt_udp.dport`
    print "Payload: " + `pkt_udp.payload`
    
    # Use repr or backticks to get human-readable payloads.
    
    print match_string(pkt, "UDP", "dport", "53")
    print match_string(pkt, "UDP", "payload", "utah.instructure.com", False)
    print match_regex(pkt, "UDP", "payload", ".*instru(c|j).*")
    print match_atleast(pkt, "IP", "len", 12)
    print match_atmost(pkt, "IP", "len", 900)
    print match_exactly(pkt, "IP", "len", 66)
    print get_regex_value(pkt, "UDP", "payload", r"(.*)ins(.*?)e\.com", 2)

def get_value(pkt, protocol, field_name):
    ''' returns the value of the field with the given name in the given packet
    at the given protocol layer. '''
    sub_pkt = pkt.getlayer(protocol)
    if sub_pkt is None:
        return None
    if not hasattr(sub_pkt, field_name):
        return None
    return getattr(sub_pkt, field_name)

def get_regex_value(pkt, protocol, field_name, regex_val, match_index):
    ''' Returns the value matched by the given fields and regex submatch
    indexed by 'match_index'. Remember, a match_index of 0 is an entire
    match. '''
    sub_pkt = pkt.getlayer(protocol)
    if sub_pkt is None:
        # Failed to match protocol.
        return None
    if not hasattr(sub_pkt, field_name):
        # Failed to match field name.
        return None
    m = re.match(regex_val, `getattr(sub_pkt, field_name)`)
    if m:
        return m.group(match_index)
    return None

def match_regex(pkt, protocol, field_name, regex_val):
    ''' Determines if a packet has a field value that returns a match from the
    given regular expression string '''
    sub_pkt = pkt.getlayer(protocol)
    if sub_pkt is None:
        # Failed to match protocol.
        return False
    if not hasattr(sub_pkt, field_name):
        # Failed to match field name.
        return False
    if re.match(regex_val, `getattr(sub_pkt, field_name)`):
        return True
    return False

def match_string(pkt, protocol, field_name, val, full_match=True):
    ''' Determines if a packet has a matching field value.
    pkt: The packet to inspect
    protocol: The protocol within the packet to inspect
    field_name: The name of the field within the protocol to inspect
    val: A string to match against the field value of the packet.
    full_match: If false, the provided val only needs to be a substring of the 
                packet's value of that field.
    returns: True only if the packet has the given protocol, with the given field
             name, with a matching field value. False otherwise. 
    '''
    sub_pkt = pkt.getlayer(protocol)
    if sub_pkt is None:
        # Failed to match protocol.
        return False
    if not hasattr(sub_pkt, field_name):
        # Failed to match field name.
        return False
    if full_match:
        if `getattr(sub_pkt, field_name)` == str(val):
            # Found it (exact)!
            return True
    else:
        if str(val) in `getattr(sub_pkt, field_name)`:
            # Found it (partial)!
            return True
    return False

def match_atleast(pkt, protocol, field_name, val):
    ''' Because values are all numbers underneath, this requires
    careful use to avoid false positives. '''
    return match_cmp(pkt, protocol, field_name, val, lambda x,y: x >= y)

def match_atmost(pkt, protocol, field_name, val):
    ''' Because values are all numbers underneath, this requires
    careful use to avoid false positives. '''
    return match_cmp(pkt, protocol, field_name, val, lambda x,y: x <= y)

def match_exactly(pkt, protocol, field_name, val):
    ''' Because values are all numbers underneath, this requires
    careful use to avoid false positives. '''
    return match_cmp(pkt, protocol, field_name, val, lambda x,y: x == y)

def match_cmp(pkt, protocol, field_name, val, comparator):
    ''' Compares a field value of a packet against a provided value.
    pkt: The packet to inspect
    protocol: The protocol within the packet to inspect
    field_name: The name of the field within the protocol to inspect
    val: An integer to compare against the field value of the packet.
    comparator: A function defining the comparison to perform.

    Returns: True if the value exists and meets the comparison criteria.
             False otherwise.
    '''
    sub_pkt = pkt.getlayer(protocol)
    if sub_pkt is None:
        # Failed to match protocol.
        return False
    if not hasattr(sub_pkt, field_name):
        # Failed to match field name.
        return False
    return comparator(getattr(sub_pkt, field_name), val)

if __name__ == "__main__":
    main()
