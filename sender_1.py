from scapy.all import *
import time

a = IP(dst="10.1.1.2", src="10.1.1.5")/TCP(dport=1337);

while 1:
    send(a);
    print "IP/TCP packet sent from 10.1.1.5 to 10.1.1.2 port=1337"
    time.sleep(1)
    
