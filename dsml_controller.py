
# This is a test controller for flow rules test. the dst, src, dl_type, dw_proto and out port are all hard coded.  

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from pox.lib.addresses import IPAddr
import pox.misc.arp_responder as arp_responder
#from engine import *

log = core.getLogger()

class dsml_controller (object):
    def __init__ (self, connection):
        self.connection = connection

        self.connection.addListeners(self)
        
        core.openflow.clear_flows_of_connect = 1

    # Handles packet in messages from the switch.
    def _handle_PacketIn (self, event):
  
        packet = event.parsed
        print packet.type
    
        match = of.ofp_match.from_packet(packet)       
        print match
        msg = of.ofp_flow_mod()
        
        msg.match.nw_dst = "10.1.1.2"
        msg.match.nw_src = "10.1.1.5"      
        
        #IP packet type
        msg.match.dl_type = 0x800
        
        #nw_port = {1,6,17} for TCP/UDP/ICMP
        msg.match.nw_proto = 6
        msg.actions = []
        msg.actions.append(of.ofp_action_output(port = of.OFPP_NORMAL))
        
        #adding this port seems can once agin send packet back to the controller
        #msg.actions.append(of.ofp_action_output(port = 6633))
        
        #port for listen
        msg.actions.append(of.ofp_action_output(port = 1337))

        self.connection.send(msg)
        
        msg = of.ofp_flow_mod()

        msg.match.nw_dst = "10.1.1.5"
        msg.match.nw_src = "10.1.1.2"      
        msg.match.dl_type = 0x800
        msg.match.nw_proto = 6
        msg.actions = []
        msg.actions.append(of.ofp_action_output(port = of.OFPP_NORMAL))
        #msg.actions.append(of.ofp_action_output(port = 6633))
        msg.actions.append(of.ofp_action_output(port = 1337))

        self.connection.send(msg)

        print "Rules set 10.1.1.5 <--> 10.1.1.2"

def launch ():
    arp_responder.launch(no_learn = True)
    def start_switch (event):
        dsml_controller(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)

