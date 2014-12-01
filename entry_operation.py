from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from pox.lib.addresses import IPAddr


def delete_entry(connection, nw_dst, nw_src, dl_type = 0x800, nw_proto = 1):
    msg = of.ofp_flow_mod()
    msg.match.nw_dst = nw_dst
    msg.match.nw_src = nw_src      
    msg.match.dl_type = dl_type
    msg.match.nw_proto = nw_proto
    msg.command =of.OFPFC_DELETE
    #print msg
    connection.send(msg)
    
def add_entry(connection, nw_dst, nw_src, dl_type = 0x800, nw_proto = 1):
    msg = of.ofp_flow_mod()
    msg.match.nw_dst = nw_dst
    msg.match.nw_src = nw_src      
    msg.match.dl_type = dl_type
    msg.match.nw_proto = nw_proto
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = of.OFPP_NORMAL))
    msg.actions.append(of.ofp_action_output(port = 6633))
    
    connection.send(msg)
