# this is engine code

from datetime import datetime

class Engine:    
    def __init__(self):
        self.stacktrace = [] # stacktrace list creation
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

# print text to console
def __print(text):
    print "Engine (print): " + text
   
#print packet to console     
def __print_packet(packet):
    print str(packet)

#print time to console
def __print_time():
    print datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#print stacktrace to console using loop
def __print_stacktrace(stacktrace):
    for i in range(len(stacktrace)):
        print "frame " + str(i) + " " + stacktrace[i][0] + ": " + str(stacktrace[i][1])

#log to a file ( mesaages only)
def __log(Message_logfile.log, msg):
    with open(Message_logfile.log, "a") as logfile:
        logfile.write(msg)

#log to a file (packets only)

def __log_packet(Packet_logfile.log, packet):
    with open(Packet_logfile.log, "a") as logfile:
        logfile.write(str(packet))

#log to a file (time only)

def __log_time(time_logfile.log):
    with open(time_logfile.log, "a") as logfile:
        logfile.write(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

#log to a file ( stacktrace only)
def __log_stacktrace(stacktrace_logfile.log, stacktrace):
    with open(stacktrace_logfile.log, "a") as logfile:
        for i in range(len(stacktrace)):
            logfile.write("frame " + str(i) + " " + stacktrace[i][0] + ": " + str(stacktrace[i][1]))
