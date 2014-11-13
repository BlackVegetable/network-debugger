#!/usr/bin/python

import sys
import os.path
from keyword import iskeyword
import re
import shlex

# Meta-State-Machine
#
# Starting state expects: "start variables" or "start filters" or "start state"

GLOBAL_DICT = "__global"
DSML_KEYWORDS = [] #["exit"]

class StateDefinition:
    def __init__(self, name, argument_list=[]):
        self.name = name
        self.argument_list = argument_list
        self.clauses = []
        self.timeout = None
    
    def __str__(self):
        if not self.clauses and not self.timeout:
            raise Exception("State has no string representation with no clauses.")
        s = "\ndef " + self.name + "(self, pkt"
        for arg in self.argument_list:
            s += ", " + arg
        s += "):"
        for clause in self.clauses:
            s += "\n" + str(clause)
        if self.timeout:
            s += "\n" + str(self.timeout)
        # TODO: default argument list should be the parameters given.
        s += "    return (False, [" + self.name + "])"
        return s

    def is_valid(self):
        try:
            s = str(self)
            return True
        except Exception as e:
            return False

class Clause:
    def __init__(self):
        self.matching_functions = []
        self.comparisons = []
        self.side_effects = []
        self.goto = ""

    def __str__(self):
        if not self.matching_functions:
            raise Exception("Clause has no string representation with no matching functions.")
        if not self.goto:
            raise Exception("Clause has no string representation with no goto.")
        s = "    if " + self.matching_functions[0]
        if len(self.matching_functions) > 1:
            for x in self.matching_functions[1:]:
                s += " \\\n       " + str(x)
        s += ":"
        # TODO: print comparisons
        # TODO: print side_effects
        goto_args = shlex.split(self.goto)
        s += "\n        return (True, [" + goto_args[0]
        if len(goto_args) > 1:
            for x in goto_args[1:]:
                s += ", " + x
        s += "])\n"
        return s

    def is_valid(self):
        try:
            s = str(self)
            return True
        except Exception as e:
            return False

class Timeout:
    def __init__(self):
        self.seconds = None
        self.side_effects = []
        self.goto = None

def main(input_path):
    if input_path[-4:] != "dsml":
        print "Compilation failed: Input file not a .dsml file"
        return
    output_path = input_path[:-1]
    with open(input_path, 'r') as input_file:
        try:
            with open(output_path, "w") as output_file:
                in_contents = [s.strip() for s in input_file.read().splitlines()]
                start_parse(in_contents, output_file)
                print "Compilation successful to file: " + output_path
        except Exception as e:
            print "Compilation failed: " + `e`
            if os.path.exists(output_path):
                os.remove(output_path)

def start_parse(in_contents, out_file):
    write_header(out_file)
    write_global_dict(out_file)
    lines_to_skip = 0
    for line_number in range(len(in_contents)):
        line = in_contents[line_number]
        if line.startswith("#") or line == "":
            # Comment or whitespace only.
            continue

        if lines_to_skip > 0:
            lines_to_skip -= 1
            continue
        
        elif line == "start variables":
            lines_to_skip = parse_globals(in_contents, line_number + 1, out_file)
        elif line == "start filters":
            lines_to_skip = parse_of_filters(in_contents, line_number + 1, out_file)
        elif line.startswith("start state"):
            # TODO: Allow for starting state arguments
            words = line.split()
            if len(words) < 3:
                raise Exception('"start state" used not followed by a state name on line: ' + line_number)
            starting_state_name = words[2]
            if not is_valid_identifier(starting_state_name):
                raise Exception("Invalid state name on line: " + `line_number`)
            main_parse(in_contents, line_number + 1, out_file, starting_state_name)
            return

def main_parse(in_contents, start_line_number, out_file, starting_state_name):
    # TODO: If starting state name not found ever, raise Exception.
    lines_to_skip = 0
    starting_state_found = False
    for line_number in range(start_line_number, len(in_contents)):
        line = in_contents[line_number]
        if line.startswith("#") or line == "":
            # Comment or whitespace only.
            continue

        if lines_to_skip > 0:
            lines_to_skip -= 1
            continue

        if line.startswith("define state "):
            words = line.split()
            state_name = words[2] # Known to exist because of trailing space above.
            if not is_valid_identifier(state_name):
                raise Exception("Invalid state definition (bad name) on line: " + `line_number`)
            # TODO: Allow for previously seen state names to compose states.
            
            # Basic State Definition parsing
            args = []
            if len(words) > 3:
                for i in range(3, len(words)):
                    if not is_valid_identifier(words[i]):
                        raise Exception("Invalid state definition (bad arg '" +
                                        words[i] + "') on line: " + `line_number`)
                    args.append(words[i])
            definition = StateDefinition(state_name, args)
            
            # Parse and add Clauses
            lines_to_skip, clauses = parse_clauses(in_contents, line_number + 1, out_file)
            for c in clauses:
                definition.clauses.append(c)

            # Add Timeout if present? TODO
            out_file.write(str(definition) + "\n")

    
def write_header(out_file):
    # TODO: Check if os is linux?
    out_file.write("#!/usr/bin/python")
    # TODO: Machine generated remark
    
def write_global_dict(out_file):
    out_file.write("\n" + GLOBAL_DICT + " = {}") 
    
def is_valid_identifier(word):
    # Expected variable-name: letter + letter/underscore/number*
    return re.match("[_A-Za-z][_a-zA-Z0-9]*", word) and not iskeyword(word) and \
           not word in DSML_KEYWORDS
    
def is_valid_value(value):
    # Expected value: number or string
    return re.match("(\".*\")|(-?\d+)", value)
    
def is_valid_string(word):
    return re.match("\".*\"", word)

def is_valid_number(word):
    try:
        num = int(word, 10)
        return True
    except Exception as e:
        return False

def is_valid_boolean(word):
    if word == "True" or word == "true" or word == "TRUE" or \
       word == "False" or word == "false" or word == "FALSE":
       return True
    return False

def parse_matching_function(s, line_number):
    fname_and_args = s.split("(")
    
    fname = fname_and_args[0].strip()
    args = fname_and_args[1].strip() # Get rid of trailing whitespace.
    args = args[:-1] # Get rid of final parenthesis.
    args = args.split(",") # split into arguments.
    args = map(lambda x: x.strip(), args) # strip whitespace from each.

    arg_string = ""
    if fname == "match_string":
        if len(args) == 4:
            # Protocol, field_name, val, full_match
            if is_valid_string(args[0]) and \
               is_valid_string(args[1]) and \
               is_valid_string(args[2]) and \
               is_valid_boolean(args[3]):
                arg_string += "(pkt, " + args[0] + ", " + args[1] + ", " + \
                              args[2] + ", " + args[3] + ")"
            else:
                raise Exception("Invalid arguments for function " + fname +
                                " on line: " + `line_number`)
        elif len(args) == 3:
            # Protocol, field_name, val
            if is_valid_string(args[0]) and \
               is_valid_string(args[1]) and \
               is_valid_string(args[2]):
                arg_string += "(pkt, " + args[0] + ", " + args[1] + ", " + \
                              args[2] + ")"
            else:
                raise Exception("Invalid arguments for function " + fname +
                                " on line: " + `line_number`)
        else:
            raise Exception("Invalid argument count for function " + fname +
                            " on line: " + `line_number`)
        
    elif fname == "match_atleast" or fname == "match_atmost" or fname == "match_exactly":
        if len(args) == 3:
            # Protocol, field_name, val
            # Should we allow for string <--> number comparisons?
            if is_valid_string(args[0]) and \
               is_valid_string(args[1]) and \
               is_valid_number(args[2]):
                arg_string += "(pkt, " + args[0] + ", " + args[1] + ", " + \
                              `args[2]` + ")"
            else:
                raise Exception("Invalid arguments for function " + fname +
                                " on line: " + `line_number`)
        else:
            raise Exception("Invalid argument count for function " + fname +
                            " on line: " + `line_number`)
    else:
        raise Exception("Invalid matching function name " + fname + " on line: " +
                        `line_number`)

    return fname + arg_string

def parse_matching(in_contents, start_line_number, current_clause):
    if start_line_number is len(in_contents):
        raise Exception('matching used not followed by any matching functions on line: ' +
                        `start_line_number - 1`)
    lines_processed = 0
    for line_number in range(start_line_number, len(in_contents)):
        line = in_contents[line_number]    
        if line.startswith("#") or line == "":
            # Comment or whitespace only.
            continue
        if line.startswith("match_"):
            current_clause.matching_functions.append(parse_matching_function(line,
                                                                             line_number))
            lines_processed += 1
        elif line == "compare" or line == "do" or line == "goto":
            if lines_processed == 0:
                raise Exception('matching used not followed by any matching functions on line: ' +
                                `start_line_number - 1`)
            return lines_processed
        else:
            raise Exception("Invalid matching line: " + `line_number`)

def parse_goto(in_contents, start_line_number, current_clause):
    if start_line_number is len(in_contents):
        raise Exception('goto used not followed by a destination on line: ' + `start_line_number - 1`)
    pass
    goto_str = ""
    for line_number in range(start_line_number, len(in_contents)):
        line = in_contents[line_number]
        if line.startswith("#") or line == "":
            # Comment or whitespace only.
            continue
        line_split = shlex.split(line) # Preserve whitespace in quotes.
        if not is_valid_identifier(line_split[0]):
            raise Exception("Invalid goto identifier on line: " + `line_number`)
        goto_str = line_split[0]
        args = []
        if len(line_split) > 0:
            args = line_split[1:]
        for arg in args:
            # TODO: Support strings as arguments!
            # TODO: Verify that argument identifiers are in scope.
            if not is_valid_identifier(arg) and not is_valid_value(arg):
                raise Exception("Invalid goto argument '" + arg + "' on line: " +
                                `line_number`)
            goto_str += " " + arg
        if goto_str == "":
            raise Exception("goto used not followed by a destination on line: " +
                            `start_line_number - 1`)
        current_clause.goto = goto_str
        break
    return 1 # One non-whitespace line is always processed here.
    # TODO Special case for goto: exit

def parse_clauses(in_contents, start_line_number, out_file):
    if start_line_number is len(in_contents):
        raise Exception('state definition used not followed by any clauses on line: ' + `start_line_number - 1`)
    lines_processed = 0
    lines_to_skip = 0
    clauses = []
    current_clause = None
    for line_number in range(start_line_number, len(in_contents)):
        line = in_contents[line_number]    
        if line.startswith("#") or line == "":
            # Comment or whitespace only.
            continue

        if lines_to_skip > 0:
            lines_to_skip -= 1
            continue

        if line.startswith("define state"):
            break
        if line == "matching":
            current_clause = Clause()
            lines_to_skip = parse_matching(in_contents, line_number + 1, current_clause)
            lines_processed += lines_to_skip + 1
        elif line == "goto":
            lines_to_skip = parse_goto(in_contents, line_number + 1, current_clause)
            clauses.append(current_clause)
            lines_processed += lines_to_skip + 1
        elif line == "do":
            raise NotImplementedError("'do' has not been implemented yet!")
        elif line == "timeout":
            raise NotImplementedError("'timeout' has not been implemented yet!")
            # Timeout handling here TODO
            # Only allow one timeout TODO
        else:
            raise Exception('Invalid clause line: ' + `line_number`)
    return (lines_processed, clauses)

def parse_of_filters(in_contents, start_line_number, out_file):
    if start_line_number is len(in_contents):
        raise Exception('"start filters" used not followed by variable definition(s) on line: ' + `start_line_number - 1`)
    lines_processed = 0
    for line_number in range(start_line_number, len(in_contents)):
        line = in_contents[line_number]
        if line.startswith("#") or line == "":
            # Comment or whitespace only.
            continue
        if line == "start variables" or line == "start state":
            break
        # TODO: Parse OF Filters.
        lines_processed += 1
    
    if lines_processed is 0:
        raise Exception('"start filters" used not followed by filters on line: ' + `start_line_number - 1`)    
    return lines_processed    
    
def parse_globals(in_contents, start_line_number, out_file):
    if start_line_number is len(in_contents):
        raise Exception('"start variables" used not followed by variable definition(s) on line: ' + `start_line_number - 1`)
    lines_processed = 0
    for line_number in range(start_line_number, len(in_contents)):
        line = in_contents[line_number].strip()
        if line.startswith("#") or line.isspace() or not line:
            # Comment or whitespace only.
            continue
        if line is "start filters" or line.startswith("start state"):
            break
            
        # Expected Syntax: variable-name starting-value
        #              OR: variable-name = starting-value        
        words = line.split()
        if len(words) is 3 and words[1] == "=":
            words = [words[0], words[2]]
        if len(words) != 2:
            raise Exception("Invalid variable definition on line: " + `line_number`)
        
        variable_name = words[0]
        if not is_valid_identifier(variable_name):
            raise Exception("Invalid variable definition (bad name) on line: " + `line_number`)
        out_file.write("\n" + GLOBAL_DICT + "['" + variable_name + "'] = ")
        value = words[1]
        if not is_valid_value(value):
            raise Exception("Invalid variable definition (bad value) on line: " + `line_number`)
        out_file.write(value)
        lines_processed += 1
        
    if lines_processed is 0:
        raise Exception('"start variables" used not followed by variable definition(s) on line: ' + `start_line_number - 1`)    
    return lines_processed        

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python dsml_compiler.py <example.dsml>"
    else:        
        main(sys.argv[1])
	