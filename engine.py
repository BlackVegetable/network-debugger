
from datetime import datetime

class Engine:    
    def __init__(self):
        self.stacktrace = []
        self.arguments = []    
        self.next_function = __initial_state

    def handle_packet(self, packet, time_elapsed=0):
        matched, next_function_and_args, of_rules_to_send = \
                                        self.next_function(packet,
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
        return of_rules_to_send
        
    def get_initial_rules(self):
        return __initial_rules

# Side effects:

def __print(text):
    print "Engine (print): " + text
        
def __print_packet(packet):
    print str(packet)

def __print_time():
    print datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def __print_stacktrace(stacktrace):
    for i in range(len(stacktrace)):
        print "frame " + str(i) + " " + stacktrace[i][0] + ": " + str(stacktrace[i][1])

def __log(filename, msg):
    with open(filename, "a") as logfile:
        logfile.write(msg)

def __log_packet(filename, packet):
    with open(filename, "a") as logfile:
        logfile.write(str(packet))

def __log_time(filename):
    with open(filename, "a") as logfile:
        logfile.write(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

def __log_stacktrace(filename, stacktrace):
    with open(filename, "a") as logfile:
        for i in range(len(stacktrace)):
            logfile.write("frame " + str(i) + " " + stacktrace[i][0] + ": " + str(stacktrace[i][1]))

def __inc(variable):
    __global[variable] = __global[variable] + 1

def __dec(variable):
    __global[variable] = __global[variable] - 1

def __set(variable, value):
    __global[variable] = value

def __set_to_field_value(packet, variable, protocol, field_name):
    __global[variable] = get_value(packet, protocol, field_name)



