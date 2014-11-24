
from pox.core import core
import pox.openflow.libopenflow_01 as of
#from engine import *

class OF_module (object):
    def __init__ (self, connection):
        self.connection = connection

        connection.addListeners(self)
        core.openflow.clear_flows_of_connect = 1
    # Handles packet in messages from the switch.
    def _handle_PacketIn (self, event):
        print str(event.data).decode('utf-16')
        #engine.handle_packet(event.data)
        packet = event.parsed # This is the parsed packet data.
        #print "print packet  below ====>"
        #print packet
        
        packet_in = event.ofp # The actual ofp_packet_in message.
        print "print evnet.ofp below =======>"
        print packet_in
        
        #msg = of.ofp_packet_out()
        #print "print msg below ======>"
        #print msg
        #msg.buffer_id = event.ofp.buffer_id
	    #msg.in_port = packet_in.in_port

        # Add an action to send to the specified port
        #action = of.ofp_action_output(port = of.OFPP_FLOOD)
        #msg.actions.append(action)

        # Send message to switch
        #self.connection.send(msg)
        print "handle packetIn do nothing, just printing"

def launch ():
    def start_switch (event):
        OF_module(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)

