from scapy.all import *
import test_dsm as dsm
import time

class Dsml_sniffer:
    def __init__(self, controller):
        print "Create sniffer\n"
        self.controller = controller
        self.engine = dsm.Engine()
        
    def start_sniffing (self, IP, port, protocol):
        print "Sniffer starts snooping"
        sniff_packet = sniff(filter ="tcp and host 127.0.0.1 and (port 1337)", count = 1)
        rule = self.engine.handle_packet(sniff_packet)
        return rule
        
    #def trigger_controller(self):
	#	self.controller.get_information()
