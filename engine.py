
from datetime import datetime
import traceback

class Engine:    
    def __init__(self):
        self.stacktrace = []
        self.arguments = []    
        self.next_function = None # Need an initial function here TODO
    
    def handle_packet(self, pkt,time_elipase=0):
        matched, next_function_and_args, of_rules_to_send = \
                                        self.next_function(packet,
                                                           time_elipase,
                                                           *self.arguments)
        self.next_function = next_function_and_args[0]
        if len(next_function_and_args) > 1:
            self.arguments = next_function_and_args[1:]
        else:
            self.arguments = [] 
        if matched:
            self.stacktrace.append([self.next_function.__name__, pkt])
        return of_rules_to_send
        
    def get_initial_rules(self):
        return __initial_rules

# Side effects:


# print time and date to console 

print datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def __print(text):
    print "Engine (print): " + text
        
with open(file_path, "w") as logfile:
 #    Do some stuff, yeah!
  #  logfile.write("Some text")


# print the current packet
def __print(packet):
    print " Packet: " + str(pkt) 


# print OF rules
#TODO when finish with OF module


#traceback
def another_function():
    stack()

def stack():
    traceback.print_stack()
    print repr(traceback.extract_stack())
    print repr(traceback.format_stack())
