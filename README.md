# Custom Standard Cell Design using Skywater 130nm PDK
This repository provides a flow for doing custom standard cell design for Skywater 130nm PDK using open-source tools. The proposed flow uses NGSPICE for simulation, Magic for layout, and python scripts in conjunction with NGSPICE control commands to generate timing liberty files.
<p align="center"><img src="images/custom_cell_design_flow.jpg" alt="Proposed flow" width="250" /></p>     

#### Under Development
- [Custom Standard Cell Design using Skywater 130nm PDK](#custom-standard-cell-design-using-skywater-130nm-pdk)
      - [Under Development](#under-development)
  - [What is Non Linear Delay Model(NLDM)?](#what-is-non-linear-delay-modelnldm)
    - [Fall Time](#fall-time)
    - [Rise Time](#rise-time)
    - [Fall Transition](#fall-transition)
    - [Rise Transition](#rise-transition)
  - [Custom Standard Cell List and Results](#custom-standard-cell-list-and-results)
  - [Schematic and spice file generation using Xschem (Optional)](#schematic-and-spice-file-generation-using-xschem-optional)
  - [Instruction to Generate Timing Liberty file](#instruction-to-generate-timing-liberty-file)
  - [Verification of generated liberty file with OpenSTA](#verification-of-generated-liberty-file-with-opensta)
  - [Verification of generated Liberty File with OpenLane](#verification-of-generated-liberty-file-with-openlane)
    - [OpenLane Requirements](#openlane-requirements)
    - [Custom Cells and Skywater 130nm Cells:](#custom-cells-and-skywater-130nm-cells)
    - [Synthesis](#synthesis)
    - [Floor-planning](#floor-planning)
    - [Placement](#placement)
    - [CTS](#cts)
    - [Routing:](#routing)
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
Calculate the Fall time, Rise time, Fall Transition and Rise Transition.

### Fall Time
        Measuring Cell Fall Time @ 50% of VDD(1.8V) 
        meas tran tinfall when v(A)=0.9 FALL=1 
        meas tran tofall when v(X)=0.9 FALL=1
        let cfall = (tofall-tinfall)/1e-9
### Rise Time
        Measuring Cell Rise Time @ 50% of VDD(1.8V) 
        meas tran tinrise when v(in1)=0.9 RISE=1 
        meas tran torise when v(out)=0.9 RISE=1
        let crise = (torise-tinrise)/1e-9
### Fall Transition        
        Measuring Fall Transion Time @ 80-20% of VDD(1.8V) 
        meas tran ft1 when v(out)=1.44 FALL=1 
        meas tran ft2 when v(out)=0.36 FALL=1
        let fall_tran = (ft2-ft1)/1e-9
### Rise Transition        
        Measuring Rise Transion Time @ 20-80% of VDD(1.8V) 
        meas tran rt1 when v(out)=1.44 RISE=1 
        meas tran rt2 when v(out)=0.36 RISE=1
        let rise_tran = (rt1-rt2)/1e-9

 
## Custom Standard Cell List and Results     
   [Pre-layout nand2_1x ](custom_stdcell/nand2_1x/nand2_1x.spice) | [Post-layout nand2_1x ](custom_stdcell/nand2_1x/vsdcell_nand2_1x.spice) | [ Timing Lib File](custom_stdcell/nand2_1x/timing.lib) | [Modified Liberty File](sta_results/sky_mod.lib)         
      <img src="custom_stdcell/nand2_1x/nand2_1x_out.png" alt="nand2_1x" width="500"/>
      <img src="custom_stdcell/nand2_1x/nand2_1x_layout.png" alt="nand2_1x_layout" width="250"/>    
      
## Schematic and spice file generation using Xschem (Optional)
   * Software Requirement: Xschem 
   * Use this command to install Xschem `sudo apt install xschem` 
   * Design the circuit with the help of pmos and nmos from the library models and change the W and L values according to specification.
   * Generate spice file with the help of netlist button.(You can choose the type of netlist from 1.spice 2.VHDL 3.Verilog).


## Instruction to Generate Timing Liberty file
**Step 0: Perquisites based on Ubuntu OS**      
  * Software Requirements: NGSPICE and python 3   
  * Numpy module download: `$ pip3 install numpy`   
  * Clone the repository: `$ git clone https://github.com/harshsrigh/timing_archs.git`        
  * Change Directory to timing_arch: `$ cd timing_arch`
  * All the commands need to be run from the root directory i.e `user_name@PC_name:~/timing_archs$`

**Step 1: Edit config.py**
   * Enter custom cell folder and spice file that needs to be characterized.
   * Mention input vectors for input delay and load capacitor.
   * Mention Input and Output pins.
   * Enter Logic function.
   * Enter Base Liberty File and output Liberty File

**Nand3_2x example:**  [nand2_1x config.py](config.py)      
                 
  * Replace 'custom_stdcell/nand2_1x/' directory with your cell working directory in config.py file.
  * Similarly replace spice file name 'nand2_1x.spice' with your spice file name. Make sure the spice format has the subckt inside it with proper scaling factor.     
    
    File Configuration:
    ``` py
    library_directory = ''
    library_file = path.join(library_directory, 'sky130nm.lib')
    cell_directory = 'custom_stdcell/nand2_1x/' # Enter cell folder
    spice_file = path.join(cell_directory, "nand3_1x.spice") # Enter .spice file
    output_folder =  path.join(cell_directory, "data")
    ```             
    Input Vector:
    ``` py
    input_transtion_time = '0.01n 0.023n 0.0531329n 0.122474n 0.282311n 0.650743 1.5n' # Only put the unit(do not include sec suffix)
    output_caps = '0.0005p 0.0012105800p 0.002931p 0.00709641p 0.0171815 0.0415991p 0.100718p' # Only put the unit(do not include Farad suffix)
    input_pins = 'A B' # TODO: extract from .lef files
    output_pins = 'Y' # TODO: extract from .lef files
    logic_function = 'not (A and B)' # Use keyword 'not', 'and' 'or'
    ```         

**Step 2: Execute python file**       
    Enter command into terminal: `$ python3 combchar.py`

**Step 3: Ideal Run Final Output**:                             
    <img src="images/script_out.png" alt="script_out" width="350"/>

## Verification of generated liberty file with OpenSTA
* Perquisites openSTA software. You could install using `sudo apt-get install openSTA`
* Change directory to sta_results: `$ cd sta_results`
* Replace `picorv32a.synthesis.txt` file name to `picorv32a.synthesis.v`    
* Edit the sta.conf and my_base.sdc as per your requirement.
* Run OpenSTA using command: `$ sta sta.conf`.
* Verify your cell of interest and make sure there is no warning due the liberty files.       
    <img src="images/sta_nand32.png" alt="sta_nand32" width="450"/>
## Verification of generated Liberty File with OpenLane
### OpenLane Requirements
* Install OpenLane as mentioned in repo [OpenLANE Built Script](https://github.com/nickson-jose/openlane_build_script)
* [OpenLane Workshop repo for tool flow](https://github.com/harshsrigh/openlane_sky130nm_vsdworkshop)
### Custom Cells and Skywater 130nm Cells:
All of the custom cells used are combination cell(as shown below) and Sequential cell like D Flip-Flop is taken from Skywater 130nm Library for now.
  * **Skywater Library cells**: sky130_fd_sc_hd__dfxtp_4,  sky130_fd_sc_hd__buf_2, and sky130_fd_sc_hd__conb_1.
  * **Custom cells**: sky130_vsdbuf_1x, sky130_vsdbuf_2x, sky130_vsdclkbuf_4x, sky130_vsdinv_1x, sky130_vsdinv_8x, sky130_vsdnand2_1x, sky130_vsdnand3_1x, sky130_vsdnand4_1x and sky130_vsdo21ai_1x.     
* **Liberty File**: [sky_mod1.lib](sta_results/sky_mod1.lib)    

### Synthesis
* Designed used for verification: picorv32a   
* Edit config.tcl to -      
  <img src="images/configtcl.png" alt="config" width="450"/>
* Synthesis Result:   
  <img src="images/synthesis.png" alt="config" width="300"/>

### Floor-planning
* Command: `run_floorplan`   
* Layout can be viewed in magic with predefined taps, io pins and decoupling Caps: `magic -T ~/sky130A.tech lef read ~/merged.lef def read picorv32a.floorplan.def`

### Placement
 * Command: `run_placement`
 * Layout:    
  <img src="images/placement.png" alt="placement" width="450"/>

### CTS
* Command: `run_cts`
* Layout:   
<img src="images/cts.png" alt="placement" width="250"/>

### Routing:
* Command: `run_routing`
* Facing High congestion issue need to add more cells in to the library and re-check port position in the custom cells.
  
## Future Works: 
* Improve the layout of custom cells for the routing(375 iter-> 81 Overflows)
* Work on Simple D-Flip Flop characterization using Bisection method for determining the setup time, hold and minimum pulse width.

