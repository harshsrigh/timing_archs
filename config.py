from os import path

# File Configurations
library_directory = ''
library_file = path.join(library_directory, 'sky130nm.lib')
cell_directory = 'custom_stdcell/nand2_1x/'
spice_file = path.join(cell_directory, "nand2.spice")
output_folder =  path.join(cell_directory, "data")

# Simulation Setup
VDD = '1.8'
time_unit = 1e-9 # 1ns
cap_unit = 1e-12 # 1pF
temp = '25C'
# Y Considered as Output 

# Input Vectors
input_delay = '0.06ns 0.18ns 0.42ns 0.6ns 1.2ns'
output_caps = '0.025pF 0.05pF 0.1pF 0.3pF 0.6pF'
input_pins = 'a b' # TODO: extract from .lef files
output_pins = 'y' # TODO: extract from .lef files
logic_function = 'not (a and b)'