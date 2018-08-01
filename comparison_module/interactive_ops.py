# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 14:44:17 2018

@author: User
"""
from alt_az_functions import get_location
from alt_az_functions import interactive_get_location
from alt_az_functions import get_object
from alt_az_functions import interactive_get_object

from reading_functions import read_var_file

from io_functions import set_out_dir

import os.path

def interactive_operation(modes, model_df, scope_df):
    """
    This function controls interactive elements of the software system and 
    enables iterative use of the system
    """
    continue_option=True
    menu_choice = "X"
    


    while continue_option:
        print("""
              INTERACTIVE MODE MENU
                
        1: Cropping Options
        2: Normalisation Options
        3: Animation/3D Options
        4: Location/Target Options
        5: Plotting Options
        6: File Input/Output Options
        7: Frequency Options
        8: Other Options
        
        9: Plot with current options
        
        0: Exit
              """)
    

        menu_choice=raw_input("Please enter your selection from the menu above:\t")


        
        if "1" == menu_choice:
            set_crop_options(modes)
        elif "2" == menu_choice:
            set_norm_options(modes)
        elif "3" == menu_choice:
            set_3d_options(modes)
        elif "4" == menu_choice:
            set_coordinate_options(modes)
        elif "5" == menu_choice:
            set_plotting_options(modes)
        elif "6" == menu_choice:
            set_file_io_options(modes, model_df, scope_df)
        elif "7" == menu_choice:
            set_frequency_options(modes)
        elif "8" == menu_choice:
            set_other_options(modes)

            
        elif "9" == menu_choice:
            continue_option=False #finish the loop
            
                                
        elif "0" == menu_choice:
            modes['interactive']=0 #terminates the interactions which will exit
            continue_option=False #finish the loop

        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")
            
def set_crop_options(modes):
    """
    This function modifies the cropping options in the modes
    """
    menu_choice = "X"
    continue_option=True
    #menu_options=range(0,num_options)
    
    while continue_option:

        print("""
              CROPPING MODE MENU
      
      1: Set Crop Level
      2: Set Crop Basis (Frequency/Overall)
      3: Set Crop Data (Model/Scope)
      4: Set Crop Operation Type
      
      0: Return to previous menu
              """)

        menu_choice=raw_input("Please enter your selection from the menu above:\t")

            
            
        if "0" == menu_choice:
            continue_option=False #finish the loop
        
        elif "1" == menu_choice:
            set_crop_level(modes)
            
        elif "2" == menu_choice:
            set_crop_basis(modes)
                        
        elif "3" == menu_choice:
            set_crop_data(modes)
               
        elif "4" == menu_choice:
            set_crop_type(modes)
               
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")
    
def set_crop_level(modes):
    """
    This function modifies the cropping level options in the modes variable
    """
    crop_level = 0.0


    print(("""
              CROPPING LEVEL MENU
              Current cropping Level {0}
          
      Crop level mode indicates the numerical factor for cropping. 
      Depending on the crop operation, the crop level is implemented differently.
      
      In "median" or "mean" crop operation, the crop level is the multiplier by
      which those values are multiplied to generate the maximum permitted value
      
      In "percentile" crop operation, the crop level is the pecentile level to
      crop to.  Percentiles higher than 100 are ignored
          """).format(modes["crop"]))
    try:#read in the choice as an int
        crop_level=float(raw_input("Please the crop level desired:\t"))
        modes["crop"]=crop_level
    except ValueError: #can't be converted to a float
        print("Warning: invalid crop level, please try again.") #print a warning
        set_crop_level(modes)

def set_crop_basis(modes):
    """
    This function modifies the cropping basis options in the modes
    """
    menu_choice = "X"
    continue_option=True
    #menu_options=['n', 'N', 'o', 'O', 'f', 'F', '0']
    
    while continue_option:

        print(("""
              CROPPING BASIS MENU
              Current: {0}
              
      n: No Cropping
      o: Crop Overall
      f: Crop by Frequency
      
      
      0: Return to previous menu
              """).format(modes["crop_basis"]))
        
        
        menu_choice=raw_input("Please enter your selection from the menu above:\t")
        
        
        if '0' == menu_choice:
            continue_option=False #finish the loop
        
        elif menu_choice in ['n', 'N']:
            modes["crop_basis"]='n'
            
        elif menu_choice in ['f', 'F']:
            modes["crop_basis"]='f'
                       
        elif menu_choice in ['o', 'O']:
            modes["crop_basis"]='o'
            
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")

def set_crop_data(modes):
    """
    This function modifies the cropping basis options in the modes
    """
    menu_choice = "X"
   
    #menu_options=['n', 'N', 's', 'S', 'm', 'M', 'b', 'B', '0']
    continue_option=True
    while continue_option:

        print(("""
              CROPPING DATA MENU
              Current: {0}
              
      n: Crop Neither
      s: Crop Scope
      m: Crop Model
      b: Crop Both
      
      
      0: Return to previous menu
              """).format(modes["crop_data"]))
        
        
        menu_choice=raw_input("Please enter your selection from the menu above:\t")
        
        
        if '0' == menu_choice:
            continue_option=False #finish the loop
        
        elif menu_choice in ['n', 'N']:
            modes["crop_data"]='n'
            
        elif menu_choice in ['s', 'S']:
            modes["crop_data"]='s'
                       
        elif menu_choice in ['m', 'M']:
            modes["crop_data"]='m'
            
        elif menu_choice in ['b', 'B']:
            modes["crop_data"]='b'
            
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")

def set_crop_type(modes):
    """
    This function modifies the cropping operation type options in the modes
    """
    menu_choice = "X"
    continue_option=True
    #menu_options=range(0,num_options)
    
    while continue_option:

        print(("""
              CROPPING MODE MENU
              Current: {0}
      
      1: Median
      2: Mean
      3: Percentile
      
      0: Return to previous menu
              """).format(modes["crop_type"]))
        menu_choice=raw_input("Please enter your selection from the menu above:\t")
            
        if "0" == menu_choice:
            continue_option=False #finish the loop
        
        elif "1" == menu_choice:
            modes["crop_type"]="median"
            
        elif "2" == menu_choice:
            modes["crop_type"]="mean"
                        
        elif "3" == menu_choice:
            modes["crop_type"]="percentile"
               

        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")


def validate_options(user_input, valid_options, permit_partial=True):
    """
    This function is used to validate options input by the user to interactive 
    operations.  User input is compared with a list of valid options and the
    valid options in the user input are returned.  
    
    The "permit partial" option allows for valid options to be retained if the 
    user submits a mix of valid and invalid options
    """
    output_options = []
    
    #if all are valid
    if all (opt in valid_options for opt in user_input):
        #pass them all to output
        output_options = user_input
        
    else : #not all options are valid
        #check if partial matches are permitted
        if True==permit_partial:
            
            #Setup the output variable by making a copy of the input
            output_options=list(user_input)
            
            #if so, go through the input
            for opt in user_input:
                #and reove invalid inputs from the output
                if opt not in valid_options:
                    output_options.remove(opt)
                    print("Option: "+str(opt)+
                          " is invalid, continuing with remainder")
            

        else:
            output_options=[]
            print("Some options are invalid.  Stopping.")
    return(output_options)
                
    
def set_norm_options(modes):
    """
    This function modifies the cropping options in the modes
    """
    menu_choice = "X"
    continue_option=True
    #menu_options=range(0,num_options)
    
    while continue_option:

        print("""
              NORMALISATION MODE MENU
      
      1: Set Normalisation Basis (Frequency/Overall)
      2: Set Normalisation Data (Model/Scope)
      
      0: Return to previous menu
              """)
        menu_choice=raw_input("Please enter your selection from the menu above:\t")
            
        if "0" == menu_choice:
            continue_option=False #finish the loop
        
        elif "1" == menu_choice:
            set_norm_basis(modes)
            
        elif "2" == menu_choice:
            set_norm_data(modes)
                        
 
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")


def set_norm_basis(modes):
    """
    This function modifies the normalisation basis options in the modes
    """
    menu_choice = "X"
   
    #menu_options=['n', 'N', 'o', 'O', 'f', 'F', '0']
    continue_option=True
    while continue_option:

        print(("""
              NORMALISATION BASIS MENU
              Current: {0}
              
      n: No Normalisation
      o: Normalisation Overall
      f: Normalisation by Frequency
      
      
      0: Return to previous menu
              """).format(modes["norm"]))
        
        
        menu_choice=raw_input("Please enter your selection from the menu above:\t")
        
        
        if '0' == menu_choice:
            continue_option=False #finish the loop
        
        elif menu_choice in ['n', 'N']:
            modes["norm"]='n'
            
        elif menu_choice in ['f', 'F']:
            modes["norm"]='f'
                       
        elif menu_choice in ['o', 'O']:
            modes["norm"]='o'
            
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")

def set_norm_data(modes):
    """
    This function modifies the normalisation basis options in the modes
    """
    menu_choice = "X"
    continue_option=True
    #menu_options=['n', 'N', 's', 'S', 'm', 'M', 'b', 'B', '0']
    
    while continue_option:

        print(("""
              NORMALISATION DATA MENU
              Current: {0}
              
      n: Normalise Neither
      s: Normalise Scope
      m: Normalise Model
      b: Normalise Both
      
      
      0: Return to previous menu
              """).format(modes["norm_data"]))
        
        
        menu_choice=raw_input("Please enter your selection from the menu above:\t")
        
        
        if '0' == menu_choice:
            continue_option=False #finish the loop
        
        elif menu_choice in ['n', 'N']:
            modes["norm_data"]='n'
            
        elif menu_choice in ['s', 'S']:
            modes["norm_data"]='s'
                       
        elif menu_choice in ['m', 'M']:
            modes["norm_data"]='m'
            
        elif menu_choice in ['b', 'B']:
            modes["norm_data"]='b'
            
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")

def set_3d_options(modes):
    """
    This function modifies the 3d plotting options in the modes
    """
    menu_choice = "X"
    continue_option=True
    #menu_options=range(0,num_options)
    
    while continue_option:

        print("""
              3D/ANIMATION MODE MENU
      
      1: Set 3d plotting Options
      2: Set frame rate
      
      0: Return to previous menu
              """)
        menu_choice=raw_input("Please enter your selection from the menu above:\t")
            
        if "0" == menu_choice:
            continue_option=False #finish the loop
        
        elif "1" == menu_choice:
            set_3d_plotting(modes)
            
        elif "2" == menu_choice:
            set_frame_rate(modes)
                        
 
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")

def set_3d_plotting(modes):
    """
    This function modifies the 3d plotting options in the modes
    """
    menu_choice = "X"
    continue_option=True
    #menu_options=range(0,num_options)
    current_name=""
    
    while continue_option:
        
        if modes["three_d"] in ["colour","color"]:
            current_name="3-D Colour Plots"
        elif "anim" == modes["three_d"]:
            current_name="Animated plots against time"
        elif "animf" == modes["three_d"]:
            current_name="Animated plots against frequency"            
        
        print(("""
              3D/ANIMATION PLOTTING MENU
              Current: {0}
      
      1: Plot in 3-d colour plots
      2: Plot animated against time
      3: Plot animated against frequency
      4: Plot contour 3d plot
      
      0: Return to previous menu
              """).format(current_name))
        
        
        menu_choice=raw_input("Please enter your selection from the menu above:\t")
            
        if "0" == menu_choice:
            continue_option=False #finish the loop
        
        elif "1" == menu_choice:
            modes["three_d"]='colour'
            
        elif "2" == menu_choice:
            modes["three_d"]='anim'
                
        elif "3" == menu_choice:
            modes["three_d"]='animf'
                
        elif "4" == menu_choice:
            modes["three_d"]='contour'
               
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")
                    
def set_frame_rate(modes):
    """
    This function modifies the cropping level options in the modes variable
    """
    frame_rate = 0.0


    print(("""
          FRAME RATE MENU
          Current Frame Rate {0}
          
      Sets the frame rate for animated operations in frames per second.
          """).format(modes["frame_rate"]))
    try:#read in the choice as an int
        frame_rate=float(raw_input("Please the frame rate desired:\t"))
        modes["frame_rate"]=frame_rate
    except ValueError: #can't be converted to a float
        print("Warning: invalid crop level, please try again.") #print a warning
        set_frame_rate(modes)
        
def set_coordinate_options(modes):
    """
    This function modifies the observatory location and target options
    """
    menu_choice = "X"
    continue_option=True
    #menu_options=range(0,num_options)
    
    while continue_option:

        print(("""
              COORDINATE MODE MENU
              Current Location Name: {0} 
              Current Location Coordinates: Lat: {1} Long: {2} Elev {3}m
              
              Current Target Name: {4}
              Current Target Coordinates: RA: {5}deg Dec: {6}deg
      
      1: Set Observing Location Options
      2: Set Target Coordinate Options
      
      0: Return to previous menu
              """).format(modes['location_name'],
                          modes['location_coords'][0], #latitude
                          modes['location_coords'][1], #longitude
                          modes['location_coords'][2], #height,
                          modes['object_name'],
                          modes['object_coords'][0], #RA
                          modes['object_coords'][1] #Dec
                          ))
        
        menu_choice=raw_input("Please enter your selection from the menu above:\t")
            
        if "0" == menu_choice:
            continue_option=False #finish the loop
        
        elif "1" == menu_choice:
            modes = interactive_get_location(modes)
            modes = get_location(modes)
            
        elif "2" == menu_choice:
            modes = interactive_get_object(modes)
            modes = get_object(modes)
                        
 
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")
            

def set_plotting_options(modes):
    """
    This function modifies the plotting options in the modes
    """
    menu_choice = "X"
    continue_option=True
    #menu_options=range(0,num_options)
    
    while continue_option:

        print("""
              PLOTTING MODE MENU
      
      1: Set graphs to plot
      2: Set variables to plot
      
      0: Return to previous menu
              """)
        
        menu_choice=raw_input("Please enter your selection from the menu above:\t")
            
        if "0" == menu_choice:
            continue_option=False #finish the loop
        
        elif "1" == menu_choice:
            set_plotting(modes)
            
        elif "2" == menu_choice:
            set_values(modes)
                        
 
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")            

def set_plotting(modes):
    """
    This functionsets the graphs to be plotted.
    """
    menu_choice = "X"
    continue_option=True
    #menu_options=range(0,num_options)
    
#    ["rmse", "corr", "spectra", 
#                                 "file",
#                                 "alt","az","ew", "stn", "split",
#                                 "values","model","scope", "diff", 
#                                 "overlay"]
    
    while continue_option:
        overlay_status="overlay" in modes['plots']
        spectra_status="spectra" in modes['plots']
        print(("""
              GRAPH SELECTION MENU
      
      1: Set figure of merit for closeness of fit
      2: Set alt-azimuth plotting options
      3: Set whether to plot model, scope or difference values
      4: Toggle single-channel overlay options.  Currently: {0}
      5: Toggle time series plots. Currently {1}
          
      0: Return to previous menu
              """).format(gen_overlay_boolean(overlay_status),
                          gen_plotting_boolean(spectra_status)))
        
        menu_choice=raw_input("Please enter your selection from the menu above:\t")
            
        if "0" == menu_choice:
            continue_option=False #finish the loop
        
        elif "1" == menu_choice:
            set_fom(modes)
            
        elif "2" == menu_choice:
            set_alt_az(modes)
                        
        elif "3" == menu_choice:
            set_msd_vals(modes)
                   
        elif "4" == menu_choice:
            if overlay_status:
                modes['plots'].remove("overlay")
            else:
                modes['plots'].append("overlay")
                   
        elif "5" == menu_choice:
            if spectra_status:
                modes['plots'].remove("spectra")
            else:
                modes['plots'].append("spectra")
                 
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")

def set_fom(modes):
    """
    This function sets the figures of merit to be plotted.
    """
    menu_choice = "X"
    continue_option=True
    #menu_options=range(0,num_options)
    
#    ["rmse", "corr" 
    
    while continue_option:
        rmse_status="rmse" in modes['plots']
        corr_status="corr" in modes['plots']
        print(("""
              FIGURE OF MERIT SELECTION MENU
      
      1: Toggle Root Mean Squared Error Plotting. Currently: {0}
      2: Toggle Pearson's Correlation Plotting. Currently: {1}

          
      0: Return to previous menu
              """).format(gen_plotting_boolean(rmse_status),
                          gen_plotting_boolean(corr_status),))
        
        menu_choice=raw_input("Please enter your selection from the menu above:\t")
            
        if "0" == menu_choice:
            continue_option=False #finish the loop
        
        elif "1" == menu_choice:
            if rmse_status:
                modes['plots'].remove("rmse")
            else:
                modes['plots'].append("rmse")
            
            
        elif "2" == menu_choice:
            if corr_status:
                modes['plots'].remove("corr")
            else:
                modes['plots'].append("corr")
                        
            
        else:
            
            print("Input: "+str(menu_choice)+" not valid or not implemented.")

def set_alt_az(modes):
    """
    This function sets the plotting options for Alt/Az plots.
    """
    menu_choice = "X"
    continue_option=True
    #menu_options=range(0,num_options)
    
#    ["alt","az","ew", "stn", "split"
    
    while continue_option:
        alt_status="alt" in modes['plots']
        az_status="az" in modes['plots']
        ew_status="ew" in modes['plots']
        stn_status="stn" in modes['plots']        
        split_status="split" in modes['plots']        
        print(("""
              ALT-AZIMUTH OPTION SELECTION MENU
      
      1: Toggle Altitude Plotting. Currently: {0}
      2: Toggle Azimuth Plotting. Currently: {1}
      3: Toggle Plotting Azimuth on an East West basis instead of 0-360. Currently: {2}
      4: Toggle Use of LOFAR Station Coordinates. Currently: {3}
      5: Toggle splitting of looping plots. Currently: {4}
          
      0: Return to previous menu
              """).format(gen_plotting_boolean(alt_status),
                          gen_plotting_boolean(az_status),
                          gen_plotting_boolean(ew_status),
                          gen_plotting_boolean(stn_status),
                          gen_plotting_boolean(split_status)))
        
        menu_choice=raw_input("Please enter your selection from the menu above:\t")
            
        if "0" == menu_choice:
            continue_option=False #finish the loop
        
        elif "1" == menu_choice:
            if alt_status:
                modes['plots'].remove("alt")
            else:
                modes['plots'].append("alt")
            
            
        elif "2" == menu_choice:
            if az_status:
                modes['plots'].remove("az")
            else:
                modes['plots'].append("az")
            
        
        elif "3" == menu_choice:
            if ew_status:
                modes['plots'].remove("ew")
            else:
                modes['plots'].append("ew")
            
            
        elif "4" == menu_choice:
            if stn_status:
                modes['plots'].remove("stn")
            else:
                modes['plots'].append("stn")
            
        
        elif "5" == menu_choice:
            if split_status:
                modes['plots'].remove("split")
            else:
                modes['plots'].append("split")
            
            
        else:   
                        
            print("Input: "+str(menu_choice)+" not valid or not implemented.")

def set_msd_vals(modes):
    """
    This function sets Whether to plot Model, scope or difference data.
    """
    menu_choice = "X"
    continue_option=True
    #menu_options=range(0,num_options)
    
#    ["alt","az","ew", "stn", "split"
    
    while continue_option:
        model_status="model" in modes['plots']
        scope_status="scope" in modes['plots']
        diff_status="diff" in modes['plots']
      
        print(("""
              PLOTTING DATA SELECTION MENU
      
      1: Toggle Model Data Plotting. Currently: {0}
      2: Toggle Scope Data Plotting. Currently: {1}
      3: Toggle Difference Plotting. Currently: {2}

          
      0: Return to previous menu
              """).format(gen_plotting_boolean(model_status),
                          gen_plotting_boolean(scope_status),
                          gen_plotting_boolean(diff_status)))
        
        menu_choice=raw_input("Please enter your selection from the menu above:\t")
            
        if "0" == menu_choice:
            continue_option=False #finish the loop
        
        elif "1" == menu_choice:
            if model_status:
                modes['plots'].remove("model")
            else:
                modes['plots'].append("model")
            
            
        elif "2" == menu_choice:
            if scope_status:
                modes['plots'].remove("scope")
            else:
                modes['plots'].append("scope")
            
        
        elif "3" == menu_choice:
            if diff_status:
                modes['plots'].remove("diff")
            else:
                modes['plots'].append("diff")
            
            
            
        else:   
                        
            print("Input: "+str(menu_choice)+" not valid or not implemented.")



def set_values(modes):
    """
    This function modifies the values to plot in the modes
    """
    menu_choice = "X"


    list_linear=["xx","xy","yy"]
    list_stokes=["U","V","I","Q"]
    list_all=["xx","xy","yy","U","V","I","Q"]
    dict_lists={"linear":list_linear,
                "stokes":list_stokes,
                "all":list_all}

    continue_option=True
    
    
    while continue_option:
        dict_set=set_dict(modes,dict_lists)
        
        if "each" in modes["values"]:
            each_status = True
        else:
            each_status = False
        
        print(("""
              CHANNEL SELECTION MENU
      
      Linear Polarisations (to Toggle all enter "linear")
      xx: Currently: {0}
      xy: Currently: {1}
      yy: Currently: {2}
      
      Stokes Parameters (to Toggle all enter "stokes")
      U: Currently: {3}
      V: Currently: {4}
      I: Currently: {5}
      Q: Currently: {6}
      
      To toggle all channels simultaneously, enter "all"
      
      Channels are currently plotted {7} one another
      To toggle to plotting {8} one another enter "each"
      
      0: Return to previous menu
              """).format(gen_plotting_boolean(dict_set['xx']),
                          gen_plotting_boolean(dict_set['xy']),
                          gen_plotting_boolean(dict_set['yy']),
                          gen_plotting_boolean(dict_set['U']),
                          gen_plotting_boolean(dict_set['V']),
                          gen_plotting_boolean(dict_set['I']),
                          gen_plotting_boolean(dict_set['Q']),
                          gen_overlay_boolean(each_status),
                          gen_overlay_boolean(not each_status)
              ))

        menu_choice=raw_input("Please enter your (case sensitive) selection to toggle the option on the menu above:\t")
            
            
        if "0" == menu_choice:
            continue_option=False #finish the loop
        
        #if it's a single value
        elif menu_choice in list_all:
            process_single_values_menu(menu_choice, modes, dict_lists)
            
            
        #if a group value
        elif menu_choice in dict_lists:
            process_group_values_menu(menu_choice, modes, dict_lists)
            
            
        #to toggle the overlay/separate plots
        elif menu_choice == "each":
            
            if each_status:
                modes["values"].remove("each")
            else:
                modes["values"].append("each")
     
        #if nonse
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")   


def gen_plotting_boolean(bool_in):
    """
    generates a string which looks better for the status of a plot
    """
    out_str = ""
    if bool_in:
        out_str="Plotting"
    else:
        out_str="Not Plotting"
    return(out_str)
    
def gen_overlay_boolean(bool_in):
    """
    generates a string which looks better for the status of each
    """
    out_str = ""
    if bool_in:
        out_str="Separate from"
    else:
        out_str="Overlaid upon"
    return(out_str)

def process_single_values_menu(menu_choice, modes, dict_lists):
    """
    this function responds when a single channel value is set in the interactive
    mode.  It toggles the channel on or off, and if the channel is part of a 
    group that is set, the group is toggled off and the remaining channels in 
    the group are toggled on.
    """
    relevant_group=False
    
    #if the chosen option is currently on, then turn it off
    if menu_choice in modes["values"]:
        modes["values"].remove(menu_choice)
    
    
    #if any of the groups are set
    elif any(group_list in modes["values"] for group_list in dict_lists):
        
        #go through the groups
        for group_list in dict_lists:
            #if a group is set and applies to the menu choice
            if group_list in modes["values"] and menu_choice in dict_lists[group_list]:
                #set the flag indicating that the group was relevant
                relevant_group=True

                #remove the group
                modes["values"].remove(group_list)
                

                
                #create a list of the remaining elements of that collective
                new_list=list(dict_lists[group_list])#makes a copy
                new_list.remove(menu_choice)
                
                #and set them to on
                for channel in new_list:
                    if channel not in modes["values"]:
                        modes["values"].append(channel)
    elif False== relevant_group: #was not in a group or single setting
        modes["values"].append(menu_choice) #toggle it on


def process_group_values_menu(menu_choice, modes, dict_lists):
    """
    this function responds when a group channel value is set in the interactive
    mode.  If all of the channels in the group are on, it toggles them off,
    otherwise it toggles the channels on.
    """
    #if the menu choice is all, toggle on if any are off
  
    dict_set=set_dict(modes,dict_lists)
    
    #always drop the groups and to be replaced with individual flags
    for group in dict_lists:
        if group in modes["values"]:
            modes["values"].remove(group)
    
    #always clear out the channels to simplify later logic
    for channel in dict_lists["all"]:
        if channel in modes["values"]:
            modes["values"].remove(channel)


    small_dict=dict((k, dict_set[k]) for k in (dict_lists[menu_choice]))
    #if they're all on
    if all(set_value for set_value in small_dict.values()):
        #go through the list
        for channel in dict_lists[menu_choice]:
            #and turn them off
            dict_set[channel] = False
    else:#at least some are off
        #go through the list
         for channel in dict_lists[menu_choice]:
            #and turn them on
            dict_set[channel] = True
       

    #goes through the modified dictionary
    for channel in dict_set:
        #checks if the flag is set in the dictionary
        if dict_set[channel]:
            #adds it to the modes variable
            modes["values"].append(channel)
            
        

            
def set_dict(modes, dict_lists):
    
    """
    Creates a dictionary of the channels which are set
    """
    dict_set={"xx":False,
              "xy":False,
              "yy":False,
              "U":False,
              "V":False,
              "I":False,
              "Q":False}
        
    for channel in dict_lists["all"]:
        if channel in modes["values"]:
            dict_set[channel]=True
    for group in dict_lists:
        if group in modes["values"]:
            for channel in dict_lists[group]: 
                dict_set[channel]=True

    return(dict_set)
    
    
    
def set_file_io_options(modes, model_df, scope_df):
    """
    This function modifies the File I/O options in the modes
    """
    menu_choice = "X"
    continue_option=True
    #menu_options=range(0,num_options)
    
    while continue_option:
        file_status = "file" in modes["plots"]
        print(("""
              FILE I/O MENU
      
      1: Set Input Model File
      2: Set Input Scope File
      3: Set Output File Type
      4: Set Output File Directory
      5: Toggle Output data file. Current {0}
      
      0: Return to previous menu
              """).format(gen_plotting_boolean(file_status)))
        
        menu_choice=raw_input("Please enter your selection from the menu above:\t")
            
        if "0" == menu_choice:
            continue_option=False #finish the loop
        
        elif "1" == menu_choice:
            set_in_file(modes, model_df, "model")
            
        elif "2" == menu_choice:
            set_in_file(modes, scope_df, "scope")
                        
        elif "3" == menu_choice:
            set_out_file_type(modes)
               
        elif "4" == menu_choice:
            #sets up the output directory based on the input
            modes['out_dir']=set_out_dir(modes)
               
        elif "5" == menu_choice:
            if file_status:
                modes['plots'].remove("file")
            else:
                modes['plots'].append("file")
            
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")
            
def set_in_file(modes, in_df, name):
    """
    This function reads in a new file specified by the user
    """
    out_df=in_df
    dir_file_name="in_file_"+name
    chosen_file_name=raw_input("Please enter the file name you want to use for "+name)
    try:
        out_df=read_var_file(modes[dir_file_name], modes)
        modes[dir_file_name] = chosen_file_name
    except IOError:
        print("Warning, unable to read file "+ chosen_file_name+", returning original data")
    
    return(out_df)
    

def set_out_file_type(modes):
    """
    This function allows the user to choose the file type for output data
    """

    menu_choice = "X"
    continue_option=True
    #menu_options=range(0,num_options)
    
    while continue_option:

        print(("""
              OUTPUT FILE TYPE MENU
              Current: {0}
      
      1: .png
      2: .gif
      3: .jpeg
      4: .tiff
      5: .sgi
      6: .bmp
      7: .raw
      8: .rgba
      9: .html
      
      0: Return to previous menu
              """).format(modes['image_type']))
        
        menu_choice=raw_input("Please enter your selection from the menu above:\t")
            
        if "0" == menu_choice:
            continue_option=False #finish the loop
        
        elif "1" == menu_choice:
            modes['image_type']="png"
            
        elif "2" == menu_choice:
            modes['image_type']="gif"
                        
        elif "3" == menu_choice:
            modes['image_type']="jpeg"
               
        elif "4" == menu_choice:
            modes['image_type']="tiff"
               
        elif "5" == menu_choice:
            modes['image_type']="sgi"
            
        elif "6" == menu_choice:
            modes['image_type']="bmp"
                        
        elif "7" == menu_choice:
            modes['image_type']="raw"
               
        elif "8" == menu_choice:
            modes['image_type']="rgba"
               
        elif "9" == menu_choice:
            modes['image_type']="html"
               
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")

def set_frequency_options(modes):
    """
    This function allows the user to select frequencies to plot
    """
    menu_choice = "X"
    continue_option=True
    #menu_options=range(0,num_options)
    
    while continue_option:

        print("""
              FREQUENCY SETTINGS MENU
      
      1: Set frequencies individually
      2: Set frequency by file

      0: Return to previous menu
              """)
        
        menu_choice=raw_input("Please enter your selection from the menu above:\t")
            
        if "0" == menu_choice:
            continue_option=False #finish the loop
        
        elif "1" == menu_choice:
            set_freq(modes)
            
        elif "2" == menu_choice:
            set_freq_file(modes)
                        

        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")

def set_freq(modes):
    """
    This function allows the user to manually add frequencies to the list of
    frequencies to be plotted
    """
    


    menu_choice = "X"
    continue_option=True
    #menu_options=range(0,num_options)
    
    while continue_option:
        print("""
                  FREQUENCY ENTRY MENU
                  Currently selected frequencies (Hz):
              """)
        
        freq_status = (len(modes["freq"])==1) and (0.0 in modes["freq"])
            
        if freq_status:
            print("None")
        else:
            for freq in modes["freq"]:
                print("\t\t"+str(freq))
    
        print("\n\n")
        print("""
                    
      1: Clear frequency selection (all frequencies plotted)
      2: Add new frequencies to plotting list

      0: Return to previous menu
              """)
        
        menu_choice=raw_input("Please enter your selection from the menu above:\t")
            
        if "0" == menu_choice:
            continue_option=False #finish the loop
        
        elif "1" == menu_choice:
            modes["freq"]=[0.0]
            
        elif "2" == menu_choice:
            freq_loop=True
            while freq_loop:
                input_freq_str =raw_input("Please enter the next frequency in Hz.\n"+
                                          "Enter \"0\" to stop entering frequencies:\t")
                if "0" ==input_freq_str:
                    freq_loop = False
                else:
                    try:
                        input_freq = float(input_freq_str)
                        modes["freq"].append(input_freq)
                    except ValueError:
                        print("Warning: unable to process input frequency: "+input_freq_str)
            if (len(modes["freq"])>1) and (0.0 in modes["freq"]):
                modes["freq"].remove(0.0)
                
                        

        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")

def set_freq_file(modes):
    """
    This function allows the user to input the name of a csv file containing 
    the frequencies to be filtered
    """
    
    continue_flag = True
    
    while continue_flag:
                
        print("""
              FREQUENCY FILE SELECTION MENU
              Currently selected file for frequencies:
              {0}
              
          At this screen you may
          Enter a file name in which frequencies may be found
          Enter "0" to return to the previous menu
          Enter "X" to remove the frequency file
            
            """).format(str(modes["freq_file"]))
        
        in_file = raw_input("Please enter your selection now:\n\t")
        
        if "0" == in_file:
            continue_flag = False
        elif in_file in ["X","x"]:
            modes["freq_file"]=None
        elif os.path.isfile(in_file):
            modes["freq"]=[0.0]#clears the manual entry of frequencies
            modes["freq_file"]=in_file
        else:
            print("ERROR: File \""+in_file+"\" not found.")
        

def set_other_options(modes):
    """
    This function allows the user to set a number of miscellaneous options
    """
    menu_choice = "X"
    continue_option=True
    #menu_options=range(0,num_options)
    
    while continue_option:

        print("""
              MISCELLANEOUS SETTINGS MENU
      
      1: Set time offset between scope and frequency
      2: Set graph and file title prefix
      3: Set difference mode

      0: Return to previous menu
              """)
        
        menu_choice=raw_input("Please enter your selection from the menu above:\t")
            
        if "0" == menu_choice:
            continue_option=False #finish the loop
        
        elif "1" == menu_choice:
            set_offset(modes)
            
        elif "2" == menu_choice:
            set_title(modes)
                        
        elif "3" == menu_choice:
            set_diff(modes)
               
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")


def set_offset(modes):
    """
    This function allows the user to set the number of seconds of offset that 
    exists between the start time of the scope and model observations
    """

    loop_condition=True
    while loop_condition:
        print(("""
              OFFSET MENU
              Current offset: {0}s
              
      Offset is the number of seconds between the start time of the scope and 
      model observations.  Offset is subtracted from the scope timestamps to
      allow the scope and model observations to match.
      
      Offsets MUST be an integer number of seconds.
              """).format(modes["offset"]))
        
        str_offset=raw_input("\tPlease Enter the offset time in seconds"+
                             "\n\t\tLeave Blank to return to previous menu:\t")
        if ""==str_offset:
            loop_condition=False
        else:
            try:
                offset=int(str_offset)
                modes["offset"]=offset
            except ValueError:
                print('Warning: Value: "'+str_offset+'" not valid.  Please try again!')

def set_title(modes):
    """
    This function allows the user to set the titles for graphs and files
    """
    
    continue_flag = True
    
    while continue_flag:
                
        print("""
              GRAPH AND FILE TITLE PREFIX MENU
              Currently selected Title prefix:
              {0}
              
          At this screen you may
          Enter a title prefix for the graphs
          Enter "0" to return to the previous menu
          Enter "X" to remove the title prefix
            
            """).format(str(modes["title"]))
        
        in_title = raw_input("Please enter your selection now:\n\t")
        
        if "0" == in_title:
            continue_flag = False
        elif in_title in ["X","x"]:
            modes["title"]=None
            modes["title_"]=None
        else:
            modes["title"]=in_title
            modes["title_"]="_".join(in_title.split(" "))


def set_diff(modes):
    """
    This function allows the user to determine the difference operation to be 
    used when comparing model with scope.
    """
    menu_choice = "X"
    continue_option=True
    #menu_options=range(0,num_options)
    
    while continue_option:

        print(("""
              DIFFERENCE MODE MENU
              Current: {0}
      
      1: Subtraction (model-scope)
      2: Division (model/scope)
      3: Inverse Division (scope/model)
      
      0: Return to previous menu
              """).format(gen_diff_name(modes["diff"])))
        
        menu_choice=raw_input("Please enter your selection from the menu above:\t")
            
        if "0" == menu_choice:
            continue_option=False #finish the loop
        
        elif "1" == menu_choice:
            modes["diff"]="sub"
            
        elif "2" == menu_choice:
            modes["diff"]="div"
                        
        elif "3" == menu_choice:
            modes["diff"]="idiv"
               

        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")

def gen_diff_name(abbreviation):
    """
    This function is used to generate pretty names for the difference options
    """
    diff_name = ""
    if "sub"==abbreviation:
        diff_name="Subtraction"
    elif "div"==abbreviation:
        diff_name="Division"
    elif "idiv"==abbreviation:
        diff_name="Inverse Division" 
    elif ""==abbreviation:
        diff_name="None"
    else:
        print("Warning: Unknown difference name used!")
    return (diff_name)
#looks like this was already done.  Partial version left for records
#def set_loc_options(modes):
#    """
#    This function modifies the observatory location options
#    """
#    menu_choice = "X"
#    continue_option=True
#    #menu_options=range(0,num_options)
#    location_name=""
#    
#    while continue_option:
#
#        print(("""
#              COORDINATE MODE MENU
#              Current: Lat: {0}deg, Long: {1}deg, Elev: {2}m
#      1: Set Observing Location by name
#      2: Set Observing Location by Coordinates
#      
#      0: Return to previous menu
#              """).format(modes["location_coords"][0],
#                          modes["location_coords"][1],
#                          modes["location_coords"][2]))
#        try:#read in the choice as an int
#            menu_choice=int(raw_input("Please enter your selection from the menu above:\t"))
#            
#        except ValueError: #can't be converted to an int
#            print("Warning: invalid menu choice.") #print a warning
#            menu_choice="X" #set the option back to default
#            
#        if "0" == menu_choice:
#            continue_option=False #finish the loop
#        
#        elif "1" == menu_choice:
#            location_name=raw_input("Please enter the station code for the observing location:\t")
#            modes["location_name"]=location_name
#            modes=get_location(modes)
#            
#        elif "2" == menu_choice:
#            location_name=""
#            modes["location_name"]=location_name
#            modes["location_coords"]=[0]
#            modes=get_location(modes)
#                        
# 
#        else:
#            print("Input: "+str(menu_choice)+" not valid or not implemented.")