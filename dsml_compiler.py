#!/usr/bin/python

import sys
import os.path
from keyword import iskeyword
import re

# Meta-State-Machine
#
# Starting state expects: "start variables" or "start filters" or "start state"

GLOBAL_DICT = "global00"
META_DICT = {}

class StateDefinition:
    def __init__(self, name, argument_list=[]):
        self.name = name
        self.argument_list = argument_list
        self.clauses = []
        self.timeout = None
    
    def __str__(self):
        if not self.clauses and not self.timeout:
            raise Exception("State has no string representation with no clauses.")
        s = "\ndef " + self.name + "(self, packet, time_elapsed00"
        for arg in self.argument_list:
            s += ", " + arg
        s += "):"
        if self.timeout:
            s += "\n" + str(self.timeout)
        else:
            s += "\n    if time_elapsed00:"
            s += "\n        return (False, [" + self.name
            for arg in self.argument_list:
                s += ", " + arg
            s += "])"
        for clause in self.clauses:
            s += "\n" + str(clause)
        s += "    return (False, [" + self.name
        for arg in self.argument_list:
            s += ", " + arg
        s += "])"
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
        self.goto = None

    def __str__(self):
        if not self.matching_functions:
            raise Exception("Clause has no string representation with no matching functions.")
        if not self.goto:
            raise Exception("Clause has no string representation with no goto.")
        s = "    if " + self.matching_functions[0]
        if len(self.matching_functions) > 1:
            for x in self.matching_functions[1:]:
                s += "\\\n    " + str(x)
        s += ":"
        spaces = "        "
        if self.comparisons:
            if len(self.comparisons) > 1:
                s += "\n" + spaces + "if " + self.comparisons[0] + "\\" 
                for x in self.comparisons[1:]:
                    s += "\n" + spaces + x + "\\"
                s = s[:-1] # Remove extra line-continuation character.
            else:
                s += "\n" + spaces + "if " + self.comparisons[0]
            s += ":"
            spaces += "    "
        for x in self.side_effects:
            s += "\n" + spaces + str(x)
        s += "\n        return (True, ["
        for goto_arg in self.goto:
            if isinstance(goto_arg, str):
                s += " " + goto_arg + ","
            else:
                s += " " + `goto_arg` + ","
        s = s[:-1] # Remove extraneous comma
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

    def __str__(self):
        if not self.seconds:
            raise Exception("Timeout has no string representation with no seconds.")
        if self.seconds < 1:
            raise Exception("Timeout cannot have non-positive duration.")
        if not self.goto:
            raise Exception("Timeout has no string representation with no goto.")
        s = "    if time_elapsed00 >= " + `self.seconds` + ":"
        for effect in self.side_effects:
            s += "\n        " + effect
        s += "\n        return (True, ["
        for goto_arg in self.goto:
            if isinstance(goto_arg, str):
                s += " " + goto_arg + ","
            else:
                s += " " + `goto_arg` + ","
        s = s[:-1] # Remove extraneous comma
        s += "])\n"
        return s

def main(input_path):
    if input_path[-4:] != "dsml":
        print "Compilation failed: Input file not a .dsml file"
        return
    output_path = input_path[:-5] + "_dsm.py"
    with open(input_path, 'r') as input_file:
        try:
            with open(output_path, "w") as output_file, open("./engine.py", "r") as engine_file:
                in_contents = [s.strip() for s in input_file.read().splitlines()]
                start_parse(in_contents, output_file)
                engine = engine_file.read()
                output_file.write("\n" + engine)
                print "Compilation successful to file: " + output_path
        except Exception as e:
            print "Compilation failed: " + `e`
            if os.path.exists(output_path):
                os.remove(output_path)

def start_parse(in_contents, out_file):
    write_header(out_file)
    write_global_state(out_file)
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
            # TODO: Allow for starting state arguments (Low priority)
            words = line.split()
            if len(words) < 3:
                raise Exception('"start state" used not followed by a state name on line: ' + line_number)
            starting_state_name = words[2]
            if not is_valid_identifier(starting_state_name):
                raise Exception("Invalid state name on line: " + `line_number`)
            main_parse(in_contents, line_number + 1, out_file, starting_state_name)
            return

def main_parse(in_contents, start_line_number, out_file, starting_state_name):
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
            # TODO: Allow for previously seen state names to compose states. (Low priority)
            
            # Basic State Definition parsing
            args = []
            if len(words) > 3:
                for i in range(3, len(words)):
                    if not is_valid_identifier(words[i]):
                        raise Exception("Invalid state definition (bad arg '" +
                                        words[i] + "') on line: " + `line_number`)
                    args.append(words[i])
            for arg in args:
                if arg in META_DICT:
                    raise Exception("Argument name '" + arg + "' cannot be used as both global " +
                                    "variable and as argument name.")
            definition = StateDefinition(state_name, args)
            
            # Parse and add Clauses
            lines_to_skip, clauses, timeout = parse_clauses(in_contents, line_number + 1,
                                                            out_file, args)
            for c in clauses:
                definition.clauses.append(c)
            if timeout:
                definition.timeout = timeout

            out_file.write(str(definition) + "\n")
            if definition.name == starting_state_name:
                starting_state_found = True

    if not starting_state_found:
        raise Exception("Starting State '" + starting_state_name + "' not found in definitions.")

    out_file.write("\ninitial_state00 = " + starting_state_name + "\n")
    return
    
def write_header(out_file):
    # TODO: Check if os is linux? (Low priority)
    out_file.write("#!/usr/bin/python\n\n")
    out_file.write("# This program is machine generated and should not\n")
    out_file.write("# be altered by hand. To make changes, alter the\n")
    out_file.write("# DSML file with the same name as this file.\n\n")
    
    out_file.write("import of_side_effect as OF\n")
    out_file.write("from datetime import datetime\n")
    out_file.write("from scapy_matching import *\n\n")
 
def write_global_state(out_file):
    out_file.write("\n" + GLOBAL_DICT + " = {}")
    out_file.write("\npending_of_rules00 = []")
    
def is_valid_identifier(word):
    # Expected variable-name: letter + letter/underscore/number*
    return re.match("^[_A-Za-z][\[\]_a-zA-Z0-9]*$", word) \
           and not iskeyword(word)
    
def is_valid_value(value):
    # Expected value: number or string
    return re.match("^(\".*\")|(-?\d+)$", value)
    
def is_valid_string(word):
    return re.match("^'.*'$", word) or re.match('^".*"$', word) 

def is_valid_number(word):
    try:
        num = int(word, 10)
        return True
    except Exception as e:
        return False

def is_valid_boolean(word):
    if word == "True" or word == "False":
       return True
    return False

def apply_global_scope(maybe_variable, def_args, line_number, name_wanted=False):
    '''Replaces a globally scoped variable with its mangled representation.
    If the given "maybe_variable" is defined within the definition's arguments
    instead, it is simply returned unchanged. Will also return any non-variable
    (non-identifier) unchanged. Will throw an exception if the variable is truly
    an identifier and is not contained in any valid scope.'''
    if is_valid_identifier(maybe_variable):
        if maybe_variable in META_DICT:
            if name_wanted:
                return "'" + maybe_variable + "'"
            else:
                return GLOBAL_DICT + "['" + maybe_variable + "']"
        elif not (maybe_variable in def_args or maybe_variable == "None"):
            raise Exception("Unknown variable name '" + maybe_variable + "' near " +
                            "line " + `line_number`)
    return maybe_variable

def parse_matching_function(s, line_number, conjunction, def_args):
    # Remove conjunctions from the line for now.
    if s.startswith("and"):
        s = s[3:]
    elif s.startswith("or"):
        s = s[2:]

    fname_and_args = s.split("(")

    fname = fname_and_args[0].strip()
    args = fname_and_args[1].strip() # Get rid of trailing whitespace.
    args = args[:-1] # Get rid of final parenthesis.
    args = args.split(",") # split into arguments.
    args = map(lambda x: x.strip(), args) # strip whitespace from each.
    
    # Lookup variables in our global scope and resolve by name.
    for i in range(len(args)):
        args[i] = apply_global_scope(args[i], def_args, line_number)

    arg_string = ""
    if fname == "match_string" and len(args) == 4:
        # Protocol, field_name, val, full_match
        #if is_valid_string(args[0]) or is_valid_identifier(args[0]) and \
        #   is_valid_string(args[1]) or is_valid_identifier(args[1]) and \
        #   is_valid_string(args[2]) or is_valid_identifier(args[2]) and \
        #   is_valid_boolean(args[3]):
        arg_string += "(packet, " + args[0] + ", " + args[1] + ", " + \
                        args[2] + ", " + args[3] + ")"
        #else:
        #    raise Exception("Invalid arguments for function " + fname +
        #                    " near line: " + `line_number`)

    elif len(args) == 3 and (fname == "match_string" or fname == "match_regex"):
        # Protocol, field_name, val
        #if is_valid_string(args[0]) or is_valid_identifier(args[0]) and \
        #   is_valid_string(args[1]) or is_valid_identifier(args[1]) and \
        #   is_valid_string(args[2]) or is_valid_identifier(args[2]):
        arg_string += "(packet, " + args[0] + ", " + args[1] + ", " + \
                       args[2] + ")"
        #else:
        #    raise Exception("Invalid arguments for function " + fname +
        #                    "(" + str(args) + ") near line: " + `line_number`)
        
    elif fname == "match_atleast" or fname == "match_atmost" or fname == "match_exactly":
        if len(args) == 3:
            # Protocol, field_name, val
            # Should we allow for string <--> number comparisons?
        #    if is_valid_string(args[0]) or is_valid_identifier(args[0]) and \
        #       is_valid_string(args[1]) or is_valid_identifier(args[1]) and \
        #       is_valid_number(args[2]) or is_valid_identifier(args[2]):
            arg_string += "(packet, " + args[0] + ", " + args[1] + ", " + \
                              `args[2]` + ")"
        #    else:
        #        raise Exception("Invalid arguments for function " + fname +
        #                        " near line: " + `line_number`)
        else:
            raise Exception("Invalid argument count for function " + fname +
                            " near line: " + `line_number`)
    else:
        raise Exception("Invalid matching function name " + fname + " near line: " +
                        `line_number`)

    if conjunction:
        return conjunction + " " + fname + arg_string
    return fname + arg_string

def parse_matching(in_contents, start_line_number, current_clause, def_args):
    if start_line_number is len(in_contents):
        raise Exception('matching used not followed by any matching functions on line: ' +
                        `start_line_number - 1`)
    lines_processed = 0
    first_match = True
    for line_number in range(start_line_number, len(in_contents)):
        line = in_contents[line_number]    
        if line.startswith("#") or line == "":
            # Comment or whitespace only.
            continue
        if line.startswith("match_") or line.startswith("and match_"):
            conjunction = None
            if line.startswith("and") or not first_match:
                conjunction = "and"
            current_clause.matching_functions.append(parse_matching_function(line,
                                                                             line_number,
                                                                             conjunction,
                                                                             def_args))
            first_match = False
            lines_processed += 1
        elif line.startswith("or match_"):
            if first_match:
                raise Exception("'or' used without previous matching function on line: " +
                                `line_number`)
            conjunction = "or"
            current_clause.matching_functions.append(parse_matching_function(line,
                                                                             line_number,
                                                                             conjunction,
                                                                             def_args))
            lines_processed += 1
        elif line == "compare" or line == "do" or line == "goto":
            if lines_processed == 0:
                raise Exception('matching used not followed by any matching functions on line: ' +
                                `start_line_number - 1`)
            return lines_processed
        else:
            raise Exception("Invalid matching line: " + `line_number`)

def parse_timeout(in_contents, start_line_number, timeout, def_args):
    if start_line_number is len(in_contents):
        raise Exception('timeout used not followed by a duration on line: ' + `start_line_number - 1`)
    lines_to_skip = 0
    lines_processed = 0
    for line_number in range(start_line_number, len(in_contents)):
        line = in_contents[line_number].strip()
        if line.startswith("#") or line == "":
            # Comment or whitespace only.
            continue
        if lines_to_skip > 0:
            lines_to_skip -= 1
            continue
        if not timeout.seconds:
            if not is_valid_number(line) or int(line, 10) <= 0:
                raise Exception('timeout duration must be a positive integer (given: ' + `line` +
                                ') on line ' + `line_number`)
            timeout.seconds = int(line, 10)
            lines_processed += 1
        elif line == "goto":
            lines_to_skip = parse_goto(in_contents, line_number + 1, timeout, def_args)
            lines_processed += lines_to_skip + 1
            break
        elif line == "do":
            lines_to_skip = parse_side_effects(in_contents, line_number + 1, timeout, def_args)
            lines_processed += lines_to_skip + 1
    if not timeout.goto:
        raise Exception('timeout must end with a goto.')
    return lines_processed

def parse_comparisons(in_contents, start_line_number, clause, def_args):
    if start_line_number is len(in_contents):
        raise Exception('"compare" used not followed by any comparisons on line: ' + `start_line_number - 1`)
    lines_processed = 0
    first_comparison = True
    for line_number in range(start_line_number, len(in_contents)):
        line = in_contents[line_number]
        if line.startswith("#") or line == "":
            # Comment or whitespace only.
            continue
        if line == "do" or line == "goto":
            if lines_processed == 0:
                raise Exception('"compare" used not followed by any comparisons on line ' +
                                `start_line_number - 1`)
            return lines_processed
        parts = line.split()
        conjunction = ""
        comparator = ""
        if first_comparison:
            if len(parts) != 3:
                raise Exception("Invalid number of comparison operators on line " +
                                `line_number`)
            parts[0] = apply_global_scope(parts[0], def_args, line_number)
            comparator = parts[1]
            parts[2] = apply_global_scope(parts[2], def_args, line_number)
        else:
            if len(parts) < 3 or len(parts) > 4:
                raise Exception("Invalid number of comparison operators on line " +
                                `line_number`)
            if len(parts) == 3:
                parts[0] = apply_global_scope(parts[0], def_args, line_number)
                comparator = parts[1]
                parts[2] = apply_global_scope(parts[2], def_args, line_number)
            elif len(parts) == 4:
                conjunction = parts[0]
                parts[1] = apply_global_scope(parts[1], def_args, line_number)
                comparator = parts[2]
                parts[3] = apply_global_scope(parts[3], def_args, line_number)
                
        if not (comparator in ["<", "<=", "==", ">=", ">"]):
            raise Exception("Invalid comparator on line " + `line_number`)
        if conjunction and not (conjunction in ["and", "or"]):
            raise Exception("Invalid conjunction on line " + `line_number`)
        if not conjunction and not first_comparison:
            # Implicit 'and' needed.
            clause.comparisons.append("and " + line)
        else:
            clause.comparisons.append(line)
  
        lines_processed += 1
        first_comparison = False

def parse_side_effects(in_contents, start_line_number, side_effect_container, def_args):
    if start_line_number is len(in_contents):
        raise Exception('"do" used not followed by any side-effects on line: ' + `start_line_number - 1`)
    side_effect_functions = ["print", "print_packet", "print_stacktrace", "print_of_rules",
                             "print_time", "log", "log_packet", "log_stacktrace", "log_of_rules",
                             "log_time", "set_to_field_value", "set_to_regex_match", "set", "inc",
                             "dec", "add_of_rule", "remove_of_rule"]
    lines_processed = 0
    for line_number in range(start_line_number, len(in_contents)):
        line = in_contents[line_number]
        if line.startswith("#") or line == "":
            # Comment or whitespace only.
            continue
        if line == "goto":
            if lines_processed == 0:
                raise Exception('"do" used not followed by any side-effects on line: ' +
                                `start_line_number - 1`)
            return lines_processed
        fname_and_args = line.split("(")
        fname = fname_and_args[0].strip()
        if not (fname in side_effect_functions):
            raise Exception("Unknown side effect function (" + `fname` + ") on line: " +
                            `line_number`)
        args = []
        if len(fname_and_args) > 1:
            args = fname_and_args[1].strip() # Get rid of trailing whitespace.
            args = args[:-1] # Get rid of final parenthesis.
            args = args.split(",") # split into arguments.
            args = map(lambda x: x.strip(), args) # strip whitespace from each.
            # TODO: Validate inputs to all side effect functions? (Low priority)

        name_wanted = False
        if fname in ["set", "dec", "inc", "set_to_field_value", "set_to_regex_match"]:
            name_wanted = True    
        arg_string = "("
        for i in range(len(args)):
            args[i] = apply_global_scope(args[i], def_args, line_number, name_wanted)
            arg_string += args[i] + ","
        if len(arg_string) > 1:
            arg_string = arg_string[:-1] + ")" # Replace final comma.

        # Needed to transmit stacktrace information, OF rule status via self
        if fname == "print_stacktrace" or fname == "print_of_rules":
            arg_string = "(self)" 
        elif fname == "log_stacktrace" or fname == "log_of_rules":
            # (filename) --> (self, filename)
            arg_string = "(self, " + arg_string[1:]

        side_effect = fname + "00" + arg_string
        side_effect_container.side_effects.append(side_effect)
        lines_processed += 1

def parse_goto(in_contents, start_line_number, goto_container, def_args):
    if start_line_number is len(in_contents):
        raise Exception('"goto" used not followed by a destination on line: ' + `start_line_number - 1`)
    goto = None
    for line_number in range(start_line_number, len(in_contents)):
        line = in_contents[line_number]
        if line.startswith("#") or line == "":
            # Comment or whitespace only.
            continue
        goto = re.findall(r'(?:[^\s"]|"(?:\\.|[^"])*")+', line)
        if not is_valid_identifier(goto[0]):
            raise Exception("Invalid goto identifier on line: " + `line_number`)
        if line == "exit":
            goto = ["exit00"]
        args = []
        if len(goto) > 0:
            args = goto[1:]
        for i in range(len(args)):
            # This could definitely be more readable... clean up (low priority TODO)
            goto[i + 1] = apply_global_scope(args[i], def_args, line_number)
            if not is_valid_identifier(args[i]) and not is_valid_value(args[i]):
                raise Exception("Invalid goto argument '" + args[i] + "' on line: " +
                                `line_number`)
        if not goto:
            raise Exception("goto used not followed by a destination on line: " +
                            `start_line_number - 1`)
        goto_container.goto = goto
        break
    return 1 # One non-whitespace line is always processed here.

def parse_clauses(in_contents, start_line_number, out_file, def_args):
    if start_line_number is len(in_contents):
        raise Exception('state definition used not followed by any clauses on line: ' + `start_line_number - 1`)
    lines_processed = 0
    lines_to_skip = 0
    clauses = []
    current_clause = None
    timeout = None
    for line_number in range(start_line_number, len(in_contents)):
        line = in_contents[line_number]    
        if line.startswith("#") or line == "":
            # Comment or whitespace only.
            continue

        if lines_to_skip > 0:
            lines_to_skip -= 1
            continue

        # TODO: Restrict order (compare/matching before do/goto) (may be done implicitly? Low priority)
        if line.startswith("define state"):
            break
        if line == "matching":
            current_clause = Clause()
            lines_to_skip = parse_matching(in_contents, line_number + 1, current_clause, def_args)
            lines_processed += lines_to_skip + 1
        elif line == "goto":
            lines_to_skip = parse_goto(in_contents, line_number + 1, current_clause, def_args)
            clauses.append(current_clause)
            lines_processed += lines_to_skip + 1
        elif line == "do":
            lines_to_skip = parse_side_effects(in_contents, line_number + 1, current_clause, def_args)
            lines_processed += lines_to_skip + 1
        elif line == "compare":
            lines_to_skip = parse_comparisons(in_contents, line_number + 1, current_clause, def_args)
            lines_processed += lines_to_skip + 1
        elif line == "timeout":
            if timeout:
                raise Exception("Multiple timeouts not allowed. Line: " + `line_number`)
            timeout = Timeout()
            lines_to_skip = parse_timeout(in_contents, line_number + 1, timeout, def_args)
            lines_processed += lines_to_skip + 1
        else:
            raise Exception('Invalid clause line: ' + `line_number`)
    return (lines_processed, clauses, timeout)

def parse_of_filters(in_contents, start_line_number, out_file):
    if start_line_number is len(in_contents):
        raise Exception('"start filters" used not followed by variable definition(s) on line: ' + `start_line_number - 1`)
    lines_processed = 0
    initial_rules = []
    for line_number in range(start_line_number, len(in_contents)):
        line = in_contents[line_number]
        if line.startswith("#") or line == "":
            # Comment or whitespace only.
            continue
        if line == "start variables" or line.startswith("start state"):
            break
        
        if line.startswith("of_filter"):
            no_parens = line.replace("(", " ").replace(")", "").replace(",", " ").split()
            args = no_parens[1:]
            if len(args) != 4:
                raise Exception("Incorrect number of arguments to of_filter near line: " +
                                `line_number`)
            initial_rules.append('OF.OFSideEffect("add", ' + args[0] + ", " + args[1] +
                                 ", " + args[2] + ", " + args[3] + ")")
            lines_processed += 1
            continue
        else:
            raise Exception("Invalid syntax near line: " + `line_number`)
    
    if lines_processed is 0:
        raise Exception('"start filters" used not followed by filters on line: ' + `start_line_number - 1`)    
    out_file.write("\ninitial_rules00 = " + `initial_rules` + "\n")
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
        if line == "start filters" or line.startswith("start state"):
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
        if variable_name in META_DICT:
            raise Exception("Illegal variable re-definition on line: " + `line_number`)
        META_DICT[variable_name] = value
        lines_processed += 1
        
    if lines_processed is 0:
        raise Exception('"start variables" used not followed by variable definition(s) on line: ' + `start_line_number - 1`)    
    return lines_processed        

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python dsml_compiler.py <example.dsml>"
    else:        
        main(sys.argv[1])
	
