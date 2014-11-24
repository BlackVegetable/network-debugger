# DSM Engine

from datetime import datetime

class Engine:    
    def __init__(self):
        self.stacktrace = [] # stacktrace list creation
        self.arguments = []    
        self.next_function = __initial_state
        self.current_of_rules = set(__initial_rules)

    def combine_of_rules(self, of_rules_list):
        '''Combines a list of OF rules into an existing set.
        Removes old rules that are given remove commands.'''

        # Awkward iteration ahead, better way to do this? TODO
        for new_rule in of_rules_list:
            should_add = True
            for old_rule in self.current_of_rules:
                if new_rule.is_opposite(old_rule):
                    self.current_of_rules.remove(old_rule)
                    should_add = False
            if should_add:
                self.current_of_rules.add(new_rule)

    def handle_packet(self, packet, time_elapsed=0):
        '''Should be called with either a packet object (scapy)
        or with None for the packet and a positive integer for
        time_elapsed. It is an error to call it with anything else.
        '''
        __pending_of_rules = [] # Clear the list.
        matched, next_function_and_args = self.next_function(packet,
                                                             time_elapsed,
                                                             *self.arguments)
        self.next_function = next_function_and_args[0]
        if len(next_function_and_args) > 1:
            self.arguments = next_function_and_args[1:]
        else:
            self.arguments = [] 
        if matched:
            if packet is None:
                packet = "Timeout"
            self.stacktrace.append([self.next_function.__name__, packet])

        self.combine_of_rules(__pending_of_rules)
        return __pending_of_rules # Mutated within DSML script
        
    def get_initial_rules(self):
        '''Simply returns a list of OFSideEffects that need to be 
        implemented by the controller before the DSM starts up.'''
        return __initial_rules

# Side effects:

def __print(msg):
    '''Print a given message to the console.'''
    print "Engine (print): " + msg
      
def __print_packet(packet):
    '''Print the current packet's contents to the console.'''
    print str(packet)

def __print_time():
    '''Print the current timestamp to the console.'''
    print datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def __print_stacktrace(stacktrace):
    '''Print the network 'stacktrace' to the console.'''
    for i in range(len(stacktrace)):
        print "frame " + str(i) + " " + stacktrace[i][0] + ": " + str(stacktrace[i][1])

def __print_of_rules(self):
    '''Prints the Open Flow filters currently applied to the controller/switch.'''
    for rule in self.current_of_rules:
        print str(rule)

def __log(filename, msg):
    '''Log a given message to a given file.'''
    with open(filename, "a") as logfile:
        logfile.write(msg)

def __log_packet(filename, packet):
    '''Log the current packet's contents to a given file.'''
    with open(filename, "a") as logfile:
        logfile.write(str(packet))

def __log_time(filename):
    '''Log the current timestamp to a given file.'''
    with open(filename, "a") as logfile:
        logfile.write(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

def __log_stacktrace(filename, stacktrace):
    '''Log a network 'stacktrace' to a given file.'''
    with open(filename, "a") as logfile:
        for i in range(len(stacktrace)):
            logfile.write("frame " + str(i) + " " + stacktrace[i][0] + ": " + str(stacktrace[i][1]))

def __log_of_rules(self, filename):
    '''Logs the Open Flow filters currently applied to the controller/switch to a given file.'''
    with open(filename, "a") as logfile:
        for rule in self.current_of_rules:
            logfile.write(str(rule))

def __inc(variable):
    '''Increment a variable'''
    __global[variable] = __global[variable] + 1

def __dec(variable):
    '''Decrement a variable'''
    __global[variable] = __global[variable] - 1

def __set(variable, value):
    '''Set a variable to a value'''
    __global[variable] = value

def __set_to_field_value(packet, variable, protocol, field_name):
    '''Set a variable to a value found in a packet.'''
    __global[variable] = get_value(packet, protocol, field_name)

def __add_of_rule(src_ip, dst_ip, src_port, dst_port):
    '''Request that an OpenFlow filter be added by the controller.'''
    __pending_of_rules.append(OF.OFSideEffect("add", src_ip, dst_ip, src_port, dst_port))

def __remove_of_rule(src_ip, dst_ip, src_port, dst_port):
    '''Request that an OpenFlow filter be removed by the controller.''' 
    __pending_of_rules.append(OF.OFSideEffect("remove", src_ip, dst_ip, src_port, dst_port))
