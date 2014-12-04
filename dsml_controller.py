
from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from pox.lib.addresses import IPAddr
import pox.misc.arp_responder as arp_responder
from pox.entry_operation import *

from scapy.all import *
import sys
import test_dsm as dsm
import time

class dsml_controller (object):

    def __init__ (self, connection):
        self.connection = connection
        self.connection.addListeners(self)
        #clear all previous rules
        core.openflow.clear_flows_of_connect = 1
        
        self.engine = dsm.Engine()
        starting_of_rules = self.engine.get_initial_rules()
        print starting_of_rules[0]
        print starting_of_rules[1]
        for item in starting_of_rules:
            if item.command == "add":
                if item.destination_port != None:
                    tp_dst = int(item.destination_port)
                else:
                    tp_dst = None
                if item.source_port != None:
                    tp_src = int(item.source_port)
                else:
                    tp_src = None
                add_sniff(self.connection, nw_dst=item.destination_ip, nw_src=item.source_ip, tp_dst=tp_dst, tp_src=tp_src)
        #for i in xrange(len(starting_of_rules)):     
        #    if starting_of_rules[i].command == "add":
        #        #add_entry(connection, nw_dst, nw_src, dl_type = 0x800, nw_proto = 1)
        #        add_entry(self.connection, nw_dst=starting_of_rules[i+1].destination_ip, nw_src=starting_of_rules[i].source_ip, nw_proto=1)
        #        add_entry(self.connection, nw_dst=starting_of_rules[i+1].destination_ip, nw_src=starting_of_rules[i].source_ip, nw_proto=6)
        #    else:
        #        #delete_entry(connection, nw_dst, nw_src, dl_type = 0x800, nw_proto = 1)
        #        delete_entry(self.connection, nw_dst=starting_of_rules[i+1].destination_ip, nw_src=starting_of_rules[i].source_ip, nw_proto=1)
        #        delete_entry(self.connection, nw_dst=starting_of_rules[i+1].destination_ip, nw_src=starting_of_rules[i].source_ip, nw_proto=6)
        
        """This is the test part rules:"""
        #add_entry(self.connection, nw_dst="10.1.1.2", nw_src="10.1.1.5", nw_proto=1)
        #add_entry(self.connection, nw_dst="10.1.1.2", nw_src="10.1.1.5", nw_proto=6)
        
        self.start_sniffer ("127.0.0.1", "1337", "tcp")
        
    def convert_to_scapy_packet(self, pox_packet):
        '''Convert a POX-style packet to a Scapy-style
        packet for use in the DSM.'''
        raw_bytes = pox_packet.raw
        return Ether(raw_bytes)

    # TODO: Replace this Pseudo-code
    # --- Function to receive packets ---
    # scapy_packet = self.convert_to_scapy_packet(pox_packet)
    # return_list = self.engine.handle_packet(scapy_packet)
    # if return_list[0] == True:
    #     if len(return_list) > 1:
    #         self.write_entry(return_list[1:])
    #     pass # Later, we will reset the timer.
    # elif return_list[0] == "Exit":
    #     Cleanup resources gracefully.
    #     Will probably finish by calling sys.exit(0) 
    
    def write_entry(self, rules):
        for item in rules:
            if item.command == "add":
                if item.destination_port != None:
                    tp_dst = int(item.destination_port)
                else:
                    tp_dst = None
                if item.source_port != None:
                    tp_src = int(item.source_port)
                else:
                    tp_src = None
                add_sniff(self.connection, nw_dst=item.destination_ip, nw_src=item.source_ip, tp_dst=tp_dst, tp_src=tp_src)
    
def launch ():
    arp_responder.launch(no_learn = True)
    def start_switch (event):
        dsml_controller(event.connection)
        
    core.openflow.addListenerByName("ConnectionUp", start_switch)
