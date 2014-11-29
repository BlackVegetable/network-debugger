# This is a test controller for flow rules test. the dst, src, dl_type, dw_proto and out port are all hard coded.  

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from pox.lib.addresses import IPAddr
import pox.misc.arp_responder as arp_responder
#from engine import *
import time
from pox.entry_operation import *
log = core.getLogger()

class delete_controller (object):
    def __init__ (self, connection):
        self.connection = connection

        self.connection.addListeners(self)
        
        core.openflow.clear_flows_of_connect = 1
        
        #add_entry(connection, nw_dst, nw_src, dl_type = 0x800, nw_proto = 1)
        add_entry(self.connection, nw_dst="10.1.1.2", nw_src="10.1.1.5", nw_proto=1)
        add_entry(self.connection, nw_dst="10.1.1.2", nw_src="10.1.1.5", nw_proto=6)
        add_entry(self.connection, nw_dst="10.1.1.5", nw_src="10.1.1.2", nw_proto=1)
        add_entry(self.connection, nw_dst="10.1.1.5", nw_src="10.1.1.2", nw_proto=6)
        
        #raw_input("\n\nPress enter key to exit.")
        time.sleep(5)
        
        delete_entry(self.connection, nw_dst="10.1.1.2", nw_src="10.1.1.5", nw_proto=1)
        delete_entry(self.connection, nw_dst="10.1.1.2", nw_src="10.1.1.5", nw_proto=6)

        
    # Handles packet in messages from the switch.
    def _handle_PacketIn (self, event):
        packet = event.parsed
        
        print "incoming packets"
        
        
        
        
def launch ():
    arp_responder.launch(no_learn = True)
    def start_switch (event):
        delete_controller(event.connection)
        

    core.openflow.addListenerByName("ConnectionUp", start_switch)
