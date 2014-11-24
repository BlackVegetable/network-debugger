from scapy.all import *

sniff(filter="ip and host 10.1.1.2", prn=lambda x: x.show())

sniff(filter="tcp and (port 1337)", prn=lambda x: x.show())
