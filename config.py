from os import path

# File Configurations
library_directory = ''
library_file = path.join(library_directory, 'sky130nm.lib')
cell_directory = 'custom_stdcell/nand2_1x/'
spice_file = path.join(cell_directory, "vsdcell_nand2_1x.spice")
lef_file = path.join(cell_directory, "vsdcell_nand2_1x.lef")
output_folder =  path.join(cell_directory, "data")

# Simulation Setup
VDD = '1.8'
time_unit = 1e-9 # 1ns
cap_unit = 1e-12 # 1pF
temp = '25C' # TODO: Need to add this into the timing_harness.cir
# With 0.01ns it take approx 2min for 7*7 cases at two input pin part
sim_step = '0.01n' # Controls the speed of Characterization (make sure to have step less than the minimum Input slew rate)
# Y Considered as Output 

# Input Vectors
input_transition_time = '0.01n 0.023n 0.0531329n 0.122474n 0.282311n 0.650743n 1.5n' # Only put the unit(do not include sec suffix)
output_caps = '0.0005p 0.0012105800p 0.002931p 0.00709641p 0.0171815p 0.0415991p 0.100718p' # Only put the unit(do not include Farad suffix)
output_pins = 'Y' # TODO: extract from .lef files
logic_function = 'not (A and B)' # Use keyword 'not', 'and' , 'or'

# Liberty Base File Location
lib_file = 'sta_results/sky130_fd_sc_hd__tt_025C_1v80.lib'
merged_file_file = 'sta_results/sky_mod.lib'