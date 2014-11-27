# DSM Engine

class Engine:    
    def __init__(self):
        self.stacktrace = []
        self.arguments = []
        self.next_function = initial_state00
        self.current_of_rules = set(self.get_initial_rules())

    def combine_of_rules(self, of_rules_list):
        '''Combines a list of OF rules into an existing set.
        Removes old rules that are given remove commands.'''
        combined_set = set()
        for rule in of_rules_list:
            if rule.opposite() not in self.current_of_rules:
                combined_set.add(rule)
        for rule in self.current_of_rules:
            if rule.opposite() not in of_rules_list:
                combined_set.add(rule)
        self.current_of_rules = combined_set

    def handle_packet(self, packet, time_elapsed=0):
        '''Should be called with either a packet object (scapy)
        or with None for the packet and a positive integer for
        time_elapsed. It is an error to call it with anything else.
        '''
        pending_of_rules00 = [] # Clear the list.
        previous_function = self.next_function # Store for stacktrace
        matched, next_function_and_args = self.next_function(self,
                                                             packet,
                                                             time_elapsed,
                                                             *self.arguments)
        if not next_function_and_args:
            # We are supposed to terminate the debugger.
            self.next_function = exit00
            return ["Exit"]
        self.next_function = next_function_and_args[0]
        if len(next_function_and_args) > 1:
            self.arguments = next_function_and_args[1:]
        else:
            self.arguments = [] 
        if matched:
            if packet is None:
                packet = "Timeout"
            self.stacktrace.append([previous_function.__name__, packet])

        self.combine_of_rules(pending_of_rules00)
        return [matched].extend(pending_of_rules00) # Mutated within DSML script
        
    def get_initial_rules(self):
        '''Simply returns a list of OFSideEffects that need to be 
        implemented by the controller before the DSM starts up.'''
        rule_list = []
        for rule in initial_rules00:
            rule_list.append(eval(rule))
        return rule_list

def exit00(self, packet, time_elapsed=0):
    '''Signal the end of this debugging session.
    Arguments are ignored.'''
    return (False, []) 
    
# Side effects:

def print00(msg):
    '''Print a given message to the console.'''
    print str(msg)
      
def print_packet00(packet):
    '''Print the current packet's contents to the console.'''
    print `packet`

def print_time00():
    '''Print the current timestamp to the console.'''
    print datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def print_stacktrace00(stack_object):
    '''Print the network 'stacktrace' to the console.'''
    stacktrace = stack_object.stacktrace
    for i in range(len(stacktrace)):
        print "frame " + str(i) + " " + stacktrace[i][0] + ": " + `stacktrace[i][1]`

def print_of_rules00(self):
    '''Prints the Open Flow filters currently applied to the controller/switch.'''
    for rule in self.current_of_rules:
        print str(rule)

def log00(filename, msg):
    '''Log a given message to a given file.'''
    with open(filename, "a") as logfile:
        logfile.write(msg)

def log_packet00(filename, packet):
    '''Log the current packet's contents to a given file.'''
    with open(filename, "a") as logfile:
        logfile.write(`packet`)

def log_time00(filename):
    '''Log the current timestamp to a given file.'''
    with open(filename, "a") as logfile:
        logfile.write(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

def log_stacktrace00(stack_object, filename):
    '''Log a network 'stacktrace' to a given file.'''
    stacktrace = stack_object.stacktrace
    with open(filename, "a") as logfile:
        for i in range(len(stacktrace)):
            logfile.write("frame " + str(i) + " " + stacktrace[i][0] + ": " + `stacktrace[i][1]`)

def log_of_rules00(self, filename):
    '''Logs the Open Flow filters currently applied to the controller/switch to a given file.'''
    with open(filename, "a") as logfile:
        for rule in self.current_of_rules:
            logfile.write(str(rule))

def inc00(variable):
    '''Increment a variable'''
    global00[variable] = global00[variable] + 1

def dec00(variable):
    '''Decrement a variable'''
    global00[variable] = global00[variable] - 1

def set00(variable, value):
    '''Set a variable to a value'''
    global00[variable] = value

def set_to_field_value00(packet, variable, protocol, field_name):
    '''Set a variable to a value found in a packet.'''
    global00[variable] = get_value(packet, protocol, field_name)

def set_to_regex_match00(packet, variable, protocol, field_name, regular_expression, sub_index):
    '''Set a variable to the result from a regular expression match (including a
        sub-match index. Remember, 0 indicates an entire match.)'''
    global00[variable] = get_regex_value(packet, protocol, field_name,
                                         regular_expression, sub_index)

def add_of_rule00(src_ip, dst_ip, src_port, dst_port):
    '''Request that an OpenFlow filter be added by the controller.'''
    pending_of_rules00.append(OF.OFSideEffect("add", src_ip, dst_ip, src_port, dst_port))

def remove_of_rule00(src_ip, dst_ip, src_port, dst_port):
    '''Request that an OpenFlow filter be removed by the controller.''' 
    pending_of_rules00.append(OF.OFSideEffect("remove", src_ip, dst_ip, src_port, dst_port))
