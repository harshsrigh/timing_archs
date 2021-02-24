#!/usr/bin/python3
from config import *
from os import path
from os import makedirs
import os, re
import scripts.truths as truths
import scripts.timing as timing
import subprocess

logic_operator = {'and':'&',
                  'or': '|',
                  'not': '!'}

def ng_postscript(meas_type, active_pin):
    """ Generate ngspice control commands for timing_harness"""
    
    if meas_type == 'timing':
        
        working_folder = path.join(output_folder,'timing')
        # TODO: Shift this text based template to Jinja Templates if necessary
        control_str = \
                        f"""
                                let run  = 0
                                foreach in_delay {input_delay}

                            * Initiating Text Files in folder data
                            echo "input_delay:$in_delay" >> {working_folder}/input_delay.txt
                            echo "input_delay:$in_delay" >> {working_folder}/cell_fall.txt
                            echo "input_delay:$in_delay" >> {working_folder}/cell_rise.txt
                            echo "input_delay:$in_delay" >> {working_folder}/fall_transition.txt
                            echo "input_delay:$in_delay" >> {working_folder}/rise_transition.txt

                            * 1.666 to match the slew rate
                            let actual_rtime = $in_delay*1.666   
                        
                            * Input Vector - Load Cap values(index2)
                            foreach out_cap {output_caps}
                                reset
                                
                                * Changing the V2 Supply Rise time as per the Input Rise Time vector
                                alter @V{active_pin}[pulse] = [ 0 {VDD} 0 $&actual_rtime $&actual_rtime 50ns 100ns ]
                                
                                * Changing the C1 value as per the foreach list
                                alter CLOAD $out_cap
                                
                                tran {sim_step} 300ns
                                run

                                reset
                                * Verification of INPUT RISE TIME
                                meas tran ts1 when v({active_pin})=1.44 RISE=1 
                                meas tran ts2 when v({active_pin})=0.36 RISE=1
                                meas tran ts3 when v({active_pin})=1.44 FALL=1 
                                meas tran ts4 when v({active_pin})=0.36 FALL=1
                                let RISE_IN_SLEW = (ts1-ts2)/{time_unit}
                                let FALL_IN_SLEW = (ts4-ts3)/{time_unit}
                                echo "actual_rise_slew:$&RISE_IN_SLEW" >> {working_folder}/input_delay.txt
                                echo "actual_fall_slew:$&FALL_IN_SLEW" >> {working_folder}/input_delay.txt


                                print run
                                * Measuring Cell Fall Time @ 50% of VDD(1.8V) 
                                meas tran tinfall when v({active_pin})=0.9 FALL=1 
                                meas tran tofall when v(Y)=0.9 FALL=1
                                let cfall = (tofall-tinfall)/{time_unit}
                                if abs(cfall)>20
                                    meas tran tinfall when v({active_pin})=0.9 Rise=1 
                                    meas tran tofall when v(Y)=0.9 FALL=1
                                    let cfall = abs(tofall-tinfall)/{time_unit}
                                end
                                print cfall
                                echo "out_cap:$out_cap:cell_fall:$&cfall" >> {working_folder}/cell_fall.txt

                                * Measuring Cell Rise Time @ 50% of VDD(1.8V) 
                                meas tran tinrise when v({active_pin})=0.9 RISE=1 
                                meas tran torise when v(Y)=0.9 RISE=1
                                let crise = (torise-tinrise)/{time_unit}
                                if abs(crise)>20
                                    meas tran tinrise when v({active_pin})=0.9 FALL=1 
                                    meas tran torise when v(Y)=0.9 RISE=1
                                    let crise = abs(tinrise-torise)/{time_unit}
                                end
                                print crise
                                echo "out_cap:$out_cap:cell_rise:$&crise" >> {working_folder}/cell_rise.txt

                                * Measuring Fall Transion Time @ 80-20% of VDD(1.8V) 
                                meas tran ft1 when v(Y)=1.44 FALL=2 
                                meas tran ft2 when v(Y)=0.36 FALL=2
                                let fall_tran = (ft2-ft1)/{time_unit}
                                print fall_tran
                                echo "out_cap:$out_cap:fall_transition:$&fall_tran" >> {working_folder}/fall_transition.txt
                                
                                * Measuring Rise Transion Time @ 20-80% of VDD(1.8V) 
                                meas tran rt1 when v(Y)=1.44 RISE=2 
                                meas tran rt2 when v(Y)=0.36 RISE=2
                                let rise_tran = ((rt1-rt2)/{time_unit})
                                print rise_tran
                                echo "out_cap:$out_cap:rise_transition:$&rise_tran" >> {working_folder}/rise_transition.txt
                                let run = run + 1
                                * plot a y
                            end
                        end"""
    
    elif meas_type == 'input_caps':
        working_folder = path.join(output_folder,'input_caps')
        control_str = \
            f"""foreach case 1.8 0

                if $case=0
                    * Fall Condition
                    reset
                    alter @V{active_pin}[PWL] = [ 0 1.8 1.25n 0.9 2.5n 0 ]
                    tran 0.01n 2.5n
                    run
                    let fall_caps = abs(avg(v{active_pin}#branch))*2.5n/(1.8)
                    let fall_cap = fall_caps[length(fall_caps)-1]/1p
                    echo "{active_pin}:fall_capacitance:$&fall_cap" >> {working_folder}/input_pins_caps.txt
                else
                    * Rise Condition
                    reset
                    alter @V{active_pin}[PWL] = [ 0ns 0 1.25ns 0.9 2.5ns 1.8 ]
                    tran 0.01n 2.5n
                    run
                    let rise_caps = abs(avg(v{active_pin}#branch))*2.5n/(1.8)
                    let rise_cap = rise_caps[length(rise_caps)-1]/1p
                    echo "{active_pin}:rise_capacitance:$&rise_cap" >> {working_folder}/input_pins_caps.txt 
                end
            end"""
    return control_str, working_folder

def voltage_deductions(in_pins, out_pins, logic_function, active_pin, netlist_pins):
    """ Setup the Supply voltage and Logic Signal as per the logic function """

    in_pins = in_pins.replace(active_pin, '') + ' ' + active_pin
    
    pos_unate, pins_voltages = truths.Truths(in_pins.split(), [logic_function]).truth_table()
    # print(pos_unate, pins_voltages)

    # Setting up Power Supplies Voltages
    power_supplies = ['VPWR', 'VDD', 'VPB']
    gnd_supplies = ['VGND', 'VNB', 'VSS']
    power_str = '\n'.join([f'V{net} {net} 0 DC {VDD}' for net in power_supplies if net in netlist_pins])
    gnd_str = '\n'.join([f'V{net} {net} 0 DC 0' for net in gnd_supplies if net in netlist_pins])
    
    # Setting Up Signal Voltages
    active_pin_voltage = f'V{active_pin} {active_pin} 0 PULSE(0 {VDD} 0 0.01n 0.01n 50ns 100ns)'
    other_pins_voltage = []
    for net, logic in pins_voltages.items():
        if logic == 0:
            other_pins_voltage.append(f'V{net} {net} 0 DC 0')
        elif logic == 1:
            other_pins_voltage.append(f'V{net} {net} 0 DC {VDD}')
    
    other_pins_vol_str = '\n'.join(other_pins_voltage)
    
    power_supplies = power_str + '\n' + gnd_str
    signal_supplies = active_pin_voltage + '\n' + other_pins_vol_str
    
    return power_supplies, signal_supplies, pos_unate

def read_spice():
    """ Reads the .spice file specified in config.py 
        Returns: Pins (str) 
                 Spice Card Name  (str)"""
    
    with open(spice_file, "r") as file_object:
    # read file content
        spice_txt = file_object.read()
    
    subckt = [line for line in spice_txt.split('\n') if '.subckt' in line][0].split()
    spice_card = subckt[1]
    pins = ' '.join(subckt[2:])
    
    return pins, spice_card 

def Simulation_env(netlist_pins, spice_card, active_pin, sim_type = 'timing'):
    """Creates timing_harness.cir file"""
    
    include_statements = f".include '{library_file}' \n.include '{spice_file}'"
    power, signal, pos_unate = voltage_deductions(input_pins, output_pins, logic_function, active_pin, netlist_pins)
    control_text, working_folder = ng_postscript(sim_type, active_pin)
    harness_name = f"{sim_type}_harness.cir"
    harness_file = path.join(cell_directory, harness_name)
    final_text = \
                    f"""Test Harness  for {spice_card}\n{include_statements}
                    X1 {netlist_pins} {spice_card}
                    * Power Supplies
                    {power}
                    * Signal Supplies
                    {signal}
                    * CLoad 
                    CLoad {output_pins} 0 1f
                    * Control Generations
                    .control
                    {control_text}
                    rusage
                    quit
                    .endc"""
    
    with open(harness_file, "w") as file_doc:
        file_doc.write(final_text)

    return harness_file, working_folder, pos_unate

def ngspice_lunch(file_loc, working_folder):
    """Launches NGspice and delete old simulation files from the working_folder"""
    
    try:
        makedirs(working_folder)
    except OSError:
        print ("Creation of the directory %s failed" % working_folder)
        try:
            for root, dirs, files in os.walk(working_folder):
                for file in files:
                    os.remove(os.path.join(root, file))
            # print(f'Deleted Files in {working_folder}')
        except OSError:
            print(f'Manually delete Files in {working_folder}')
            exit()
    else:
        print ("Successfully created the directory %s " % working_folder)

    subprocess.call(["ngspice", '-b', '-r rawfile.raw' , file_loc])
    print('Finished Simulation')

def conv_logical(logic_func):
    for exp in logic_operator.keys():
        logic_func = logic_func.replace(exp, logic_operator[exp])
    return logic_func

def timing_lib(card, timing_list, inpin_list):
    """ Generate .lib file """

    logic_func = conv_logical(logic_function)
    lib_file = path.join(cell_directory, 'timing.lib')
    timing_txt = '\n\t'.join(timing_list)
    input_pin_txt = '\n\t'.join(inpin_list)    
    cell_card = f"""cell("{card}"){{
        {input_pin_txt}
        pin ("{output_pins}") {{
        direction: "output";
        function: "{logic_func}";
        power_down_function : "(!VPWR + VGND)";
        related_ground_pin : "VGND";
        related_power_pin : "VPWR";
        {timing_txt}  
        }}
    }}    
    """
    with open(lib_file, "w") as file_doc:
        file_doc.write(cell_card)

    print(f'Check:  {lib_file}')

if __name__ == '__main__':
    pins, card = read_spice()
    timing_list = []
    pins_list = []
    for active_pin in input_pins.split():

        # Launching Timing simulation
        timing_cir_file, timing_folder, pos_unate = Simulation_env(pins, card, active_pin, sim_type='timing')
        ngspice_lunch(timing_cir_file, timing_folder)
        # Launching Input Capacitance simulation
        caps_cir_file, caps_folder, pos_unate = Simulation_env(pins, card, active_pin, sim_type='input_caps')
        ngspice_lunch(caps_cir_file, caps_folder)
        
        undte_value = 'positive_unate' if pos_unate == True else 'negative_unate'
        pin_info = timing.input_pins(caps_folder, active_pin, '1.5') 
        pins_list.append(pin_info)
        timing_info = timing.timing_generator(timing_folder, unate=undte_value, related_pin=active_pin)
        timing_list.append(timing_info)

    timing_lib(card, timing_list, pins_list)   
       
