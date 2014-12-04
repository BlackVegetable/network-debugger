# This is a test controller for flow rules test. the dst, src, dl_type, dw_proto and out port are all hard coded.  

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from pox.lib.addresses import IPAddr
import pox.misc.arp_responder as arp_responder

from pox.entry_operation import *


import thread
from dsml_sniffer import *

from scapy.all import *

import test_dsm as dsm

import time
log = core.getLogger()

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
        #try:
        #    thread.start_new_thread( self.start_sniffer, ("127.0.0.1", "1337", "tcp",) )
        #except Exception as e:
        #    print type(e).__name__
        #    print "Error: unable to start sniffer"
    
    def start_sniffer(self, IP, port, protocol):
        sniffer = Dsml_sniffer(self)
        sniffer.start_sniffing(IP, port, protocol)
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
    
    # sniff and change rules of switch
    #def rules_changing (self, connection):
    #    print "test if we can go to this stage"
    #    rule = []
    #    a = sniff(filter="tcp and (port 1337)",count =1)
    #    print a
    #    while (a)!=0:
    #        print a
    #        rule = self.engine.handle_packet(a)
    #        print rule
    #        a = sniff(filter="tcp and (port 1337)",count =1)
def launch ():
    arp_responder.launch(no_learn = True)
    def start_switch (event):
        dsml_controller(event.connection)
        

    core.openflow.addListenerByName("ConnectionUp", start_switch)
