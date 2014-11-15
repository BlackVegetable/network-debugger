#!/usr/bin/evn python
from scapy.all import *
def packet_summary(pkt):
    if IP in pkt:
        ip_src=pkt[IP].src
        ip_dst=pkt[IP].dst
        
        print " IP src " + str(ip_src)
        print " IP dst " + str(ip_dst)
    #if TCP in pkt:
     #   tcp_sport=pkt[TCP].sport
      #  tcp_dport=pkt[TCP].dport

        #print " IP src " + str(ip_src) + " TCP sport " + str(tcp_sport) 
        #print " IP dst " + str(ip_dst) + " TCP dport " + str(tcp_dport)

    # you can filter with something like that
    if ( ( pkt[IP].src == "10.1.2.2") or ( pkt[IP].dst == "10.1.3.2") ):
        print("!")

#sniff(filter="ip",prn=packet_summary)
# or it possible to filter with filter parameter...!
sniff(filter="ip and host 10.1.2.2",prn=packet_summary)
