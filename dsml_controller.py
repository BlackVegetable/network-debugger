
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
    
        #match = of.ofp_match.from_packet(packet)       
        msg = of.ofp_flow_mod()
                       
        msg.match.nw_dst = "10.1.1.2"
        msg.match.nw_src = "10.1.1.5"      
        msg.match.dl_type = 0x800
        msg.match.nw_proto = 1
        msg.idle_timeout = 20
        msg.hard_timeout = 20
        msg.actions = []
        msg.actions.append(of.ofp_action_output(port = of.OFPP_NORMAL))
        msg.actions.append(of.ofp_action_output(port = 6633))
        msg.actions.append(of.ofp_action_output(port = 1337))

        self.connection.send(msg)
        
        msg = of.ofp_flow_mod()

        msg.match.nw_dst = "10.1.1.5"
        msg.match.nw_src = "10.1.1.2"      
        msg.match.dl_type = 0x800
        msg.match.nw_proto = 1
        msg.idle_timeout = 20
        msg.hard_timeout = 20
        msg.actions = []
        msg.actions.append(of.ofp_action_output(port = of.OFPP_NORMAL))
        msg.actions.append(of.ofp_action_output(port = 6633))
        msg.actions.append(of.ofp_action_output(port = 1337))

        self.connection.send(msg)
        
        
        
        print "handle packetIn do nothing, just printing"

def launch ():
    arp_responder.launch(no_learn = True)
    def start_switch (event):
        dsml_controller(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)

