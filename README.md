# Custom Standard Cell Design with a automated Non-Linear-Delay-Model Generator
The flow uses control commands based on ngspice to construct the Non-Linear Delay Model(NLDM) for the custom standard cell. This repo aims to introduce an approach of using open-source resources to do custom cell characterization.
#### Under Development
- [Custom Standard Cell Design with a automated Non-Linear-Delay-Model Generator](#custom-standard-cell-design-with-a-automated-non-linear-delay-model-generator)
      - [Under Development](#under-development)
  - [What is Non Linear Delay Model(NLDM)?](#what-is-non-linear-delay-modelnldm)
  - [Custom Standard Cell List and Pre-layout Results](#custom-standard-cell-list-and-pre-layout-results)
  - [Instruction to generate Timing liberty file](#instruction-to-generate-timing-liberty-file)
    - [To Configure config.py](#to-configure-configpy)
    - [Execute 'combchar.py'](#execute-combcharpy)
    - [Ideal Run Output](#ideal-run-output)
  - [Future Works:](#future-works)

## What is Non Linear Delay Model(NLDM)?

NLDM is derived from SPICE characterizations and is a highly reliable timing model. The table model is referred to as an NLDM and is used to measure the
delay, performance slew, or other timing checks. Most of the cell libraries used table models to specify the delay and timing checks for different cell timing arcs.

For different combinations of input at the cell input pin and multiple output capacitance at the cell output pin, the table provides the delay through the
cell. In a two-dimensional array, where the two independent variables are the input transition and the capacitance of the output load and the entries in the table 
are the delays.
The characterization is performed using the ngspice open source circuit simulator.        
<img src="images/rise_fall_wave.jpg" alt="rise_fall_wave" width="350"/> 

The time taken by a signal to increase from 20 percent to 80 percent of its maximum value is known as transition delay or slew. This is referred to as "rise time".
Similarly, it is possible to describe "fall time" as the time taken by a signal to fall from 80 to 20 percent of its maximum value.

The time taken for a signal to propagate through a gate or net is the propagation delay.
Therefore, you can call it a "Gate or Cell Delay" if it is a cell.
The time it takes for a signal at the input pin to impact the output signal at the output pin is the propagation delay of a gate or cell.
A delay of 50 percent of the input transition to the corresponding 50 percent of the output transition is calculated for any gate propagation.

Considering the rise/fall of both input and output, we are faced with four propagation delays: 
  1. 50% of input rise to 50% of output rise.
  2. 50% of input rise to 50% of output fall.
  3. 50% of input fall to 50% of output rise.
  4. 50% of input fall to 50% of output fall.
  
All the delays will have different values, or in some cases same values.
 
## Custom Standard Cell List and Pre-layout Results
  1. [nand2_1x](custom_stdcell/nand2_1x/nand2.spice) |  [ Timing Lib File](custom_stdcell/nand2_1x/timing.lib)          
      <img src="custom_stdcell/nand2_1x/nand2_1x_out.png" alt="nand2_1x" width="350"/>        
  2. [nand2_2x](custom_stdcell/nand2_2x/nand2_2x.spice) |  [ Timing Lib File](custom_stdcell/nand2_2x/timing.lib)     
      <img src="custom_stdcell/nand2_2x/nand2_2x_out.png" alt="nand2_2x" width="350"/>  
  3. [nand3_1x](custom_stdcell/nand3_1x/nand3_1x.spice) |  [ Timing Lib File](custom_stdcell/nand3_1x/timing.lib)             
      <img src="custom_stdcell/nand3_1x/nand3_1x_out.png" alt="nand3_1x" width="350"/>      
  4. [nand3_2x](custom_stdcell/nand3_2x/nand3_2x.spice) |  [ Timing Lib File](custom_stdcell/nand3_2x/timing.lib)       
      <img src="custom_stdcell/nand3_2x/nand3_2x_out.png" alt="nand3_2x" width="350"/>   
  5. [nand4_1x](custom_stdcell/nand4_1x/nand4_1x.spice) |  [ Timing Lib File](custom_stdcell/nand4_1x/timing.lib)     
      <img src="custom_stdcell/nand4_1x/nand4_1x_out.png" alt="nand4_1x" width="350"/>   
  6. [nand4_2x](custom_stdcell/nand4_2x/nand4_2x.spice) |  [ Timing Lib File](custom_stdcell/nand4_2x/timing.lib)     
      <img src="custom_stdcell/nand4_2x/nand4_2x_out.png" alt="nand4_2x" width="350"/>      
  7. [o21ai_1x](custom_stdcell/o21ai_1x/o21ai_1x.spice) |  [ Timing Lib File](custom_stdcell/o21ai_1x/timing.lib)     
      <img src="custom_stdcell/o21ai_1x/o21ai_1x_out.png" alt="o21ai_1x" width="350"/>
  8. [o22ai_1x](custom_stdcell/o22ai_1x/o22ai_1x.spice)  |  [ Timing Lib File](custom_stdcell/o22ai_1x/timing.lib)      
      <img src="custom_stdcell/o22ai_1x/o22ai_1x_out.png" alt="o22ai_1x_out" width="350"/>
  9.  [o221ai_1x](custom_stdcell/o221ai_1x/o221ai_1x.spice)  |  [ Timing Lib File](custom_stdcell/o221ai_1x/timing.lib)       
      <img src="custom_stdcell/o221ai_1x/o221ai_1x_out.png" alt="o221ai_1x_out" width="350"/>       
  10.  [o2111ai_1x](custo_stdcell/../custom_stdcell/o2111ai_1x/o2111ai_1x.spice)  |  [ Timing Lib File](custom_stdcell/o2111ai_1x/timing.lib)     
      <img src="custom_stdcell/o2111ai_1x/o2111ai_1x_out.png" alt="o2111ai_1x_out" width="350"/>      

## Instruction to generate Timing liberty file

### To Configure config.py
1. Enter custom cell folder and spice file that needs to be characterized.
2. Mention input vectors for input delay and load capacitor.
3. Mention Input and Output pins.
4. Enter Logic function.

**Nand4_2x example:**           
File Configuration: [nand4_2x config.py](config.py)         
``` py
library_directory = ''
library_file = path.join(library_directory, 'sky130nm.lib')
cell_directory = 'custom_stdcell/nand4_2x/' # Enter cell folder
spice_file = path.join(cell_directory, "nand4_2x.spice") # Enter .spice file
output_folder =  path.join(cell_directory, "data")
```             
Input Vector:
``` py
input_delay = '0.01n 0.023n 0.0531329n 0.122474n 0.282311n 0.650743n 1.5n' # Only put the unit(do not include sec suffix)
output_caps = '0.0005p 0.0012105800p 0.002931p 0.00709641p 0.0171815p 0.0415991p 0.100718p' # Only put the unit(do not include Farad suffix)
input_pins = 'A B C D' # TODO: extract from .lef files
output_pins = 'Y' # TODO: extract from .lef files
logic_function = 'not (A and B and C and D)' # Use keyword 'not', 'and' , 'or'
```         

### Execute 'combchar.py'       
Enter command into terminal: `python3 combchar.py`

### Ideal Run Output        
``` 
Finished Simulation
Check:  custom_stdcell/nand4_2x/timing.lib
```
## Future Works: 
**(Focused on Combination circuits only without tri-state/HiZ)**
* Perform Layout on these 10 cells.
* Setup Power calculation harness for leakage power and internal power(total power - dynamic power)
* Internal pin capacitance calculations
