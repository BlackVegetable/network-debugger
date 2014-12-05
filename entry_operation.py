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
    msg.command = of.OFPFC_DELETE
    connection.send(msg)
    
def add_entry(connection, nw_dst, nw_src, dl_type = 0x800, nw_proto = 1):
    msg = of.ofp_flow_mod()
    msg.match.nw_dst = nw_dst
    msg.match.nw_src = nw_src      
    msg.match.dl_type = dl_type
    msg.match.nw_proto = nw_proto
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = of.OFPP_NORMAL))
    #msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)

def add_sniff(connection, nw_dst=None, nw_src=None, tp_dst=None, tp_src=None, dl_type=0x800, nw_proto=1):
    msg = of.ofp_flow_mod()
    if not (nw_dst is None):
        msg.match.nw_dst = IPAddr(nw_dst)
    if not (nw_src is None):
        msg.match.nw_src = IPAddr(nw_src)
    if nw_proto != 1:
        if not (tp_dst is None):
            msg.match.tp_dst = tp_dst
        if not (tp_src is None):
            msg.match.tp_src = tp_src
    #if (nw_proto == 1)and((not (nw_dst is None))or(not (nw_src is None))):
        #return
    #    msg.match.tp_dst = None
    #    msg.match.tp_src = None
    msg.match.dl_type = dl_type
    msg.match.nw_proto = nw_proto
    msg.actions = []
    msg.actions.append(of.ofp_action_nw_addr.set_dst(IPAddr("127.0.0.1")))
    msg.actions.append(of.ofp_action_tp_port.set_dst(1337))
    connection.send(msg)
    
def delete_sniff(connection, nw_dst=None, nw_src=None, tp_dst=None, tp_src=None, dl_type=0x800, nw_proto=1):    
    msg = of.ofp_flow_mod()
    if not (nw_dst is None):
        msg.match.nw_dst = IPAddr(nw_dst)
    if not (nw_src is None):
        msg.match.nw_src = IPAddr(nw_src)
    if not (tp_dst is None):
        msg.match.tp_dst = tp_dst
    if not (tp_src is None):
        msg.match.tp_src = tp_src  
    msg.match.dl_type = dl_type
    msg.match.nw_proto = 1
    msg.command =of.OFPFC_DELETE
    connection.send(msg)
    