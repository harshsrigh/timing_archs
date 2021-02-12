# Semi-Automated Non Linear Delay Model Generator using NGSPICE
The flow uses control commands based on ngspice to construct the Non-Linear Delay Model(NLDM) for the custom standard cell. This repo aims to introduce an approach of using open-source resources to do custom cell characterization.

- [Semi-Automated Non Linear Delay Model Generator using NGSPICE](#semi-automated-non-linear-delay-model-generator-using-ngspice)
  - [Prerequisite](#prerequisite)
  - [What is Non Linear Delay Model(NLDM)?](#what-is-non-linear-delay-modelnldm)
    - [Define Cell Rise, Cell Fall, Rise Transition and Fall Transition?](#define-cell-rise-cell-fall-rise-transition-and-fall-transition)
  - [Proposed Flow for Timing Characterization?](#proposed-flow-for-timing-characterization)
  - [Explaining Flow using OR Gate example](#explaining-flow-using-or-gate-example)
    - [NGSPICE File Setup](#ngspice-file-setup)
    - [Process for Text File Creation](#process-for-text-file-creation)
    - [Timing Block .lib Format Generation](#timing-block-lib-format-generation)
    - [Comparison of Timing values from Skywater130nm PDK](#comparison-of-timing-values-from-skywater130nm-pdk)

## Prerequisite 

## What is Non Linear Delay Model(NLDM)?

### Define Cell Rise, Cell Fall, Rise Transition and Fall Transition? 

## Proposed Flow for Timing Characterization?

## Explaining Flow using OR Gate example
Start with simple schematic design using Xcircuit or any schematic capture tool and generate spice file subckt as shown below               
![Spice File](images/spice_file.png)

Once this file is created, we are ready to perform NGSPICE simulation.

### NGSPICE File Setup
This setup is divided into three sections:
* **Adding Required Libraries and Sub-circuit:** '.include' commands are used for adding the subcircuit and skywater nfet and pfet libraries.
* **Setting up Power Supplies and loads:** Power Supplies VDD and VSS as per the .lib file voltage requirement(1.8V). The Pulse supply type should be provided to the input pin which is considered related to the Output and other input pins need to be biased as they are not affecting the output. Assign a load capacitor(c1) as shown below:
![Test Harness(File Name: or2.cir](images/test_harness.png)

* **Control Commands:** These are the commands provided by ngspice to do sequence simulation with different sets of device parameter values and also helps in post-simulation analysis. Commands shown below for measuring different timing figures:
![Timing Measurement Commands(File Name: or2.cir](images/timing_measure.png)

Also, these commands store these values in a .txt( in 'text_files' folder) for verification and generating .lib based timing format.
### Process for Text File Creation
Follow the Steps:
  1. Make sure text_files folder is empty, otherwise delete the files using `rm` command.
  2. `cd` to the root folder(in which sky130nm.lib exists) and type on the terminal `ngspice ngspice or2_custom/or2_0/or2.cir'.
  3. Check all the five files are generated into the text_files folder. This particular folder consisting of different timing .txt file is used by the python file for generating      the .lib type timing block. 
### Timing Block .lib Format Generation

### Comparison of Timing values from Skywater130nm PDK
