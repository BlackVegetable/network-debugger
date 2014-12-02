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
    #msg.actions.append(of.ofp_action_output(port = 1337))
    
    connection.send(msg)

def add_sniff(connection, nw_dst):
    msg = of.ofp_flow_mod()
    msg.match.nw_dst = nw_dst     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 1
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)
    
    msg = of.ofp_flow_mod()
    msg.match.nw_dst = nw_dst     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 6
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)
    
def add_sniff(connection, nw_src):
    msg = of.ofp_flow_mod()
    msg.match.nw_src = nw_src     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 1
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)
    
    msg = of.ofp_flow_mod()
    msg.match.nw_src = nw_src     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 6
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)

def add_sniff(connection, tp_dst):
    msg = of.ofp_flow_mod()
    #msg.match.tp_dst = tp_dst     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 1
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)
    
    msg = of.ofp_flow_mod()
    msg.match.tp_dst = tp_dst     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 6
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)

def add_sniff(connection, tp_src):
    msg = of.ofp_flow_mod()
    #msg.match.tp_src = tp_src     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 1
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)
    
    msg = of.ofp_flow_mod()
    msg.match.tp_src = tp_src     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 6
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)

def add_sniff(connection, nw_dst, nw_src):
    msg = of.ofp_flow_mod()
    msg.match.nw_dst = nw_dst
    msg.match.nw_src = nw_src     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 1
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)
    
    msg = of.ofp_flow_mod()
    msg.match.nw_dst = nw_dst
    msg.match.nw_src = nw_src     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 6
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)
def add_sniff(connection, nw_dst, tp_dst):
    msg = of.ofp_flow_mod()
    msg.match.nw_dst = nw_dst
    #msg.match.tp_dst = tp_dst     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 1
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)
    
    msg = of.ofp_flow_mod()
    msg.match.nw_dst = nw_dst
    msg.match.tp_dst = tp_dst     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 6
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)

def add_sniff(connection, nw_dst, tp_src):
    msg = of.ofp_flow_mod()
    msg.match.nw_dst = nw_dst
    #msg.match.tp_src = tp_src     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 1
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)
    
    msg = of.ofp_flow_mod()
    msg.match.nw_dst = nw_dst
    msg.match.tp_src = tp_src     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 6
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)

def add_sniff(connection, nw_src, tp_dst):
    msg = of.ofp_flow_mod()
    msg.match.nw_src = nw_src
    #msg.match.tp_dst = tp_dst     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 1
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)
    
    msg = of.ofp_flow_mod()
    msg.match.nw_src = nw_src
    msg.match.tp_dst = tp_dst     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 6
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)

def add_sniff(connection, nw_src, tp_src):
    msg = of.ofp_flow_mod()
    msg.match.nw_src = nw_src
    #msg.match.tp_src = tp_src     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 1
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)
    
    msg = of.ofp_flow_mod()
    msg.match.nw_src = nw_src
    msg.match.tp_src = tp_src     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 6
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)

def add_sniff(connection, nw_dst, nw_src, tp_dst):
    msg = of.ofp_flow_mod()
    msg.match.nw_dst = nw_dst
    msg.match.nw_src = nw_src
    #msg.match.tp_dst = tp_dst     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 1
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)
    
    msg = of.ofp_flow_mod()
    msg.match.nw_dst = nw_dst
    msg.match.nw_src = nw_src
    msg.match.tp_dst = tp_dst     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 6
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)

def add_sniff(connection, nw_dst, nw_src, tp_src):
    msg = of.ofp_flow_mod()
    msg.match.nw_dst = nw_dst
    msg.match.nw_src = nw_src
    #msg.match.tp_src = tp_src     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 1
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)
    
    msg = of.ofp_flow_mod()
    msg.match.nw_dst = nw_dst
    msg.match.nw_src = nw_src
    msg.match.tp_src = tp_src     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 6
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)

def add_sniff(connection, nw_dst, nw_src, tp_dst, tp_src):
    msg = of.ofp_flow_mod()
    msg.match.nw_dst = nw_dst
    msg.match.nw_src = nw_src
    #msg.match.tp_dst = tp_dst
    #msg.match.tp_src = tp_src     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 1
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)
    
    msg = of.ofp_flow_mod()
    msg.match.nw_dst = nw_dst
    msg.match.nw_src = nw_src
    msg.match.tp_dst = tp_dst
    msg.match.tp_src = tp_src     
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 6
    msg.actions = []
    msg.actions.append(of.ofp_action_output(port = 1337))
    connection.send(msg)

