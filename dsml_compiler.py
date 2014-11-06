#!/usr/bin/python

import sys
import os.path
from keyword import iskeyword
import re

# Meta-State-Machine
#
# Starting state expects: "start variables" or "start filters" or "start state"

GLOBAL_DICT = "__global"

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
        if lines_to_skip > 0:
            lines_to_skip -= 1
            continue
        line = in_contents[line_number]
        if line.startswith("#") or line == "":
            # Comment or whitespace only.
            continue
        elif line == "start variables":
            lines_to_skip = parse_globals(in_contents, line_number + 1, out_file)
        elif line == "start filters":
            lines_to_skip = parse_of_filters(in_contents, line_number + 1, out_file)
        elif line.startswith("start state"):
            # TODO: Indicate starting state function.
            return
    
def write_header(out_file):
    # TODO: Check if os is linux?
    out_file.write("#!/usr/bin/python")
    # TODO: Machine generated remark
    
def write_global_dict(out_file):
    out_file.write("\n" + GLOBAL_DICT + " = {}") 
    
def is_valid_identifier(word):
    dsml_keywords = []
    # Expected variable-name: letter + letter/underscore/number*
    return re.match("[_A-Za-z][_a-zA-Z0-9]*", word) and not iskeyword(word) and not word in dsml_keywords
    
def is_valid_value(value):
    # Expected value: number or string
    return re.match("(\"\S*\")|(-?\d+)", value)
    
def parse_of_filters(in_contents, start_line_number, out_file):
    if start_line_number is len(in_contents):
        raise Exception('"start filters" used not followed by variable definition(s) on line: ' + `start_line_number - 1`)
    lines_processed = 0
    for line_number in range(start_line_number, len(in_contents)):
        line = in_contents[line_number]
        if line.startswith("#") or line == "":
            # Comment or whitespace only.
            continue
        if line is "start variables" or line is "start state":
            break
        # TODO: Parse OF Filters.
        lines_processed += 1
    
    if lines_processed is 0:
        raise Exception('"start variables" used not followed by variable definition(s) on line: ' + `start_line_number - 1`)    
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
	