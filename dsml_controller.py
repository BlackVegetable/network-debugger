
from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from pox.lib.addresses import IPAddr
import pox.misc.arp_responder as arp_responder
from pox.entry_operation import *

from scapy.all import *
import sys
import test_dsm as dsm
import threading
import time

class dsml_controller (object):

    def __init__ (self, connection):
        self.current_timeout_duration = 0
        self.current_timeout_time = time.time()
        self.timeout_lock = threading.Lock()
        self.TIME_GRANULARITY = 5 # Seconds

        self.DEBUG_TIME = True # ENABLE THIS FOR DEBUG TIMING INFO
        self.packet_average = 0
        self.packets_processed = 0
        self.timeout_average = 0
        self.timeouts_processed = 0

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
        
        #add_entry(self.connection, nw_dst="10.1.1.2", nw_src="10.1.1.5", nw_proto=1)
        #add_entry(self.connection, nw_dst="10.1.1.2", nw_src="10.1.1.5", nw_proto=6)
        
        self.start_sniffer ("127.0.0.1", "1337", "tcp")

        self.waiter_thread = threading.Thread(target=self.timeout_waiter, name="Waiter")
        self.waiter_thread.daemon = True
        self.waiter_thread.start()

    def convert_to_scapy_packet(self, pox_packet):
        '''Convert a POX-style packet to a Scapy-style
        packet for use in the DSM.'''
        raw_bytes = pox_packet.raw
        return Ether(raw_bytes)

    def debug_wrapper_handle_packet(self, pkt, timeout=0):
        time_start = None
        return_list = None
        if self.DEBUG_TIME:
            time_start = time.time()
            return_list = self.engine.handle_packet(pkt, timeout)
            time_stop = time.time()
            
            diff_time = time_stop - time_start
            if pkt and self.packets_processed < 5000:
                self.packets_processed += 1
                self.packet_average = self.packet_average * (float(self.packets_processed - 1) /
                                                             float(self.packets_processed)) + \
                                      diff_time * (1.0 / float(self.packets_processed))
            elif timeout > 0 and self.timeouts_processed < 5000:
                self.timeouts_processed += 1
                self.timeout_average = self.timeout_average * (float(self.timeouts_processed - 1) /
                                                               float(self.timeouts_processed)) + \
                                       diff_time * (1.0 / float(self.timeouts_processed))
        else:
            return_list = self.engine.handle_packet(pkt, timeout)
        return return_list

    def timeout_waiter(self):
        '''Calls handle_packet periodically.'''
        while True:
            if self.current_timeout_time <= time.time() - self.TIME_GRANULARITY:
                self.current_timeout_time = time.time()
                with self.timeout_lock:
                    self.current_timeout_duration += self.TIME_GRANULARITY
                return_list = self.debug_wrapper_handle_packet(None, self.current_timeout_duration)
                if return_list[0] == True:
                    with self.timeout_lock:
                        self.current_timeout_duration = 0
                    if len(return_list) > 1:
                        self.write_entry(return_list[1:])
                elif return_list[0] == "Exit":
                    self.cleanup()

    def _handle_PacketIn(self, event):
        pox_packet = event.parsed
        scapy_packet = self.convert_to_scapy_packet(pox_packet)
        return_list = self.debug_wrapper_handle_packet(scapy_packet)
        if return_list[0] == True:
            with self.timeout_lock:
                self.current_timeout_duration = 0
            if len(return_list) > 1:
                self.write_entry(return_list[1:])
        elif return_list[0] == "Exit":
            self.cleanup()

    def cleanup(self):
        # TODO: Reset to default L2 learning switch rules.
        # Otherwise the switch will require a manual reload.
        if self.DEBUG_TIME:
            with open("controller_log.txt", "a") as f:
                f.write("DEBUG information @ " + `time.time()` + "\n")
                f.write("Packets Processed (max 5000): " + `self.packets_processed` + "\n")
                f.write("Average Packet Time: " + `self.packet_average` + "\n")
                f.write("Timeouts Processed (max 5000): " + `self.timeouts_processed` + "\n")
                f.write("Average Timeout Time: " + `self.timeout_average` + "\n\n")
        sys.exit(0)
    
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
