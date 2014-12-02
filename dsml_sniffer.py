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
        #sniff_packet = sniff(filter = "%s and host %s and (port %s)"%(protocol,IP,port), count = 1)
        #print str(sniff_packet[0])
        #return_list = self.engine.handle_packet(sniff_packet[0])
        #print return_list
        return_list = [False]
        sniff_packet = sniff(offline="./example_packets/example_packets2.pcap", prn= self.process_packet)
        #sniff_packet = sniff(filter = "%s and host %s and (port %s)"%(protocol,IP,port), prn=self.process_packet) 
        #while return_list[0] == False:
            #print "in while"
            #sniff_packet = sniff(filter = "%s and host %s and (port %s)"%(protocol,IP,port), prn=lambda x: self.process_packet(x))
            #print sniff_packet[0]
            
    def process_packet (self, asYK):
        return_list = self.engine.handle_packet(asYK)
        if return_list[0] == True:
            print "return_list[0] == True"
            if len(return_list) > 1:
                self.controller.write_entry(return_list[1:])
            else:
                return "Empty True return_list"
    
        
               
        
    #def trigger_controller(self):
	#	self.controller.get_information()
