network-debugger
================

A Debugger modeled as a state machine for debugging networking systems.

To use:

Write DSML script according to the dsml_definition.txt file. Save this
script as my_script.dsml.

To compile:

`python dsml_compiler.py my_script.dsml`

To run:

Modify dsml_controller.py to use `import my_script_dsm as dsm` instead
of `import test_dsm as dsm`. Setup Controller to connect to an OpenFlow
enabled switch and begin network traffic.
