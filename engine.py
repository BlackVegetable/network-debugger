

class Engine:    
    def __init__(self):
        self.stacktrace = []
        self.arguments = []    
    
    def handle_packet(self, packet,time_elipase=0):
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
            self.stacktrace.append([self.next_function.__name__, packet])
        return of_rules_to_send
        
    def get_initial_rules(self):
        return __initial_rules
        
