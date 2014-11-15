from scapy.all import *

sniff(filter="ip and (port 1337)", prn=lambda x: x.show())
