# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 14:44:17 2018

@author: User
"""
from alt_az_functions import get_location
from alt_az_functions import interactive_get_location
from alt_az_functions import get_object
from alt_az_functions import interactive_get_object

def interactive_operation(modes):
    """
    This function controls interactive elements of the software system and 
    enables iterative use of the system
    """
    continue_option='o'
    menu_choice = "X"
    num_options = 9
    menu_options=range(0,num_options)
    
    while continue_option not in ["Y", "y", "N", "n"]:
        continue_option=raw_input("Do you want to continue to analyse the data? (y/n):\t")
        if continue_option not in ["Y", "y", "N", "n"]:
            print("Warning, invalid input!")
        elif continue_option in ["N", "n"]:
            modes['interactive']=1
        elif continue_option in ["y", "Y"]:

            while menu_choice not in menu_options:
                print("""
              INTERACTIVE MODE MENU
                
        1: Cropping Options
        2: Normalisation Options
        3: Animation/3D Options
        4: Location/Target Options
        5: Plotting Options
        6: File Output Options
        7: Frequency Options
        8: Other Options
        
        0: Plot with current options
                      """)
            
                try:#read in the choice as an int
                    menu_choice=int(raw_input("Please enter your selection from the menu above:\t"))
                    
                except ValueError: #can't be converted to an int
                    print("Warning: invalid menu choice.") #print a warning
                    menu_choice="X" #set the option back to default
                    
                if 0 == menu_choice:
                    pass #finish the loop
                
                elif 1 == menu_choice:
                    set_crop_options(modes)
                    menu_choice="X" #resets the menu choice to restart the loop
                elif 2 == menu_choice:
                    set_norm_options(modes)
                    menu_choice="X" #resets the menu choice to restart the loop
                elif 3 == menu_choice:
                    set_3d_options(modes)
                    menu_choice="X" #resets the menu choice to restart the loop
                elif 4 == menu_choice:
                    set_coordinate_options(modes)
                    menu_choice="X" #resets the menu choice to restart the loop
                elif 5 == menu_choice:
                    set_plotting_options(modes)
                    menu_choice="X" #resets the menu choice to restart the loop                    
                else:
                    print("Input: "+str(menu_choice)+" not valid or not implemented.")
                    
def set_crop_options(modes):
    """
    This function modifies the cropping options in the modes
    """
    menu_choice = "X"
    num_options = 5
    menu_options=range(0,num_options)
    
    while menu_choice not in menu_options:

        print("""
              CROPPING MODE MENU
      
      1: Set Crop Level
      2: Set Crop Basis (Frequency/Overall)
      3: Set Crop Data (Model/Scope)
      4: Set Crop Operation Type
      
      0: Return to previous menu
              """)
        try:#read in the choice as an int
            menu_choice=int(raw_input("Please enter your selection from the menu above:\t"))
            
        except ValueError: #can't be converted to an int
            print("Warning: invalid menu choice.") #print a warning
            menu_choice="X" #set the option back to default
            
        if 0 == menu_choice:
            pass #finish the loop
        
        elif 1 == menu_choice:
            set_crop_level(modes)
            menu_choice="X" #resets the menu choice to restart the loop
        elif 2 == menu_choice:
            set_crop_basis(modes)
            menu_choice="X" #resets the menu choice to restart the loop            
        elif 3 == menu_choice:
            set_crop_data(modes)
            menu_choice="X" #resets the menu choice to restart the loop   
        elif 4 == menu_choice:
            set_crop_type(modes)
            menu_choice="X" #resets the menu choice to restart the loop   
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
   
    menu_options=['n', 'N', 'o', 'O', 'f', 'F', '0']
    
    while menu_choice not in menu_options:

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
            pass #finish the loop
        
        elif menu_choice in ['n', 'N']:
            modes["crop_basis"]='n'
            menu_choice="X" #resets the menu choice to restart the loop
        elif menu_choice in ['f', 'F']:
            modes["crop_basis"]='f'
            menu_choice="X" #resets the menu choice to restart the loop           
        elif menu_choice in ['o', 'O']:
            modes["crop_basis"]='o'
            menu_choice="X" #resets the menu choice to restart the loop
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")

def set_crop_data(modes):
    """
    This function modifies the cropping basis options in the modes
    """
    menu_choice = "X"
   
    menu_options=['n', 'N', 's', 'S', 'm', 'M', 'b', 'B', '0']
    
    while menu_choice not in menu_options:

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
            pass #finish the loop
        
        elif menu_choice in ['n', 'N']:
            modes["crop_data"]='n'
            menu_choice="X" #resets the menu choice to restart the loop
        elif menu_choice in ['s', 'S']:
            modes["crop_data"]='s'
            menu_choice="X" #resets the menu choice to restart the loop           
        elif menu_choice in ['m', 'M']:
            modes["crop_data"]='m'
            menu_choice="X" #resets the menu choice to restart the loop
        elif menu_choice in ['b', 'B']:
            modes["crop_data"]='b'
            menu_choice="X" #resets the menu choice to restart the loop
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")

def set_crop_type(modes):
    """
    This function modifies the cropping operation type options in the modes
    """
    menu_choice = "X"
    num_options = 4
    menu_options=range(0,num_options)
    
    while menu_choice not in menu_options:

        print(("""
              CROPPING MODE MENU
              Current: {0}
      
      1: Median
      2: Mean
      3: Percentile
      
      0: Return to previous menu
              """).format(modes["crop_type"]))
        try:#read in the choice as an int
            menu_choice=int(raw_input("Please enter your selection from the menu above:\t"))
            
        except ValueError: #can't be converted to an int
            print("Warning: invalid menu choice.") #print a warning
            menu_choice="X" #set the option back to default
            
        if 0 == menu_choice:
            pass #finish the loop
        
        elif 1 == menu_choice:
            modes["crop_type"]="median"
            menu_choice="X" #resets the menu choice to restart the loop
        elif 2 == menu_choice:
            modes["crop_type"]="mean"
            menu_choice="X" #resets the menu choice to restart the loop            
        elif 3 == menu_choice:
            modes["crop_type"]="percentile"
            menu_choice="X" #resets the menu choice to restart the loop   

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
    num_options = 3
    menu_options=range(0,num_options)
    
    while menu_choice not in menu_options:

        print("""
              NORMALISATION MODE MENU
      
      1: Set Normalisation Basis (Frequency/Overall)
      2: Set Normalisation Data (Model/Scope)
      
      0: Return to previous menu
              """)
        try:#read in the choice as an int
            menu_choice=int(raw_input("Please enter your selection from the menu above:\t"))
            
        except ValueError: #can't be converted to an int
            print("Warning: invalid menu choice.") #print a warning
            menu_choice="X" #set the option back to default
            
        if 0 == menu_choice:
            pass #finish the loop
        
        elif 1 == menu_choice:
            set_norm_basis(modes)
            menu_choice="X" #resets the menu choice to restart the loop
        elif 2 == menu_choice:
            set_norm_data(modes)
            menu_choice="X" #resets the menu choice to restart the loop            
 
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")


def set_norm_basis(modes):
    """
    This function modifies the normalisation basis options in the modes
    """
    menu_choice = "X"
   
    menu_options=['n', 'N', 'o', 'O', 'f', 'F', '0']
    
    while menu_choice not in menu_options:

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
            pass #finish the loop
        
        elif menu_choice in ['n', 'N']:
            modes["norm"]='n'
            menu_choice="X" #resets the menu choice to restart the loop
        elif menu_choice in ['f', 'F']:
            modes["norm"]='f'
            menu_choice="X" #resets the menu choice to restart the loop           
        elif menu_choice in ['o', 'O']:
            modes["norm"]='o'
            menu_choice="X" #resets the menu choice to restart the loop
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")

def set_norm_data(modes):
    """
    This function modifies the normalisation basis options in the modes
    """
    menu_choice = "X"
   
    menu_options=['n', 'N', 's', 'S', 'm', 'M', 'b', 'B', '0']
    
    while menu_choice not in menu_options:

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
            pass #finish the loop
        
        elif menu_choice in ['n', 'N']:
            modes["norm_data"]='n'
            menu_choice="X" #resets the menu choice to restart the loop
        elif menu_choice in ['s', 'S']:
            modes["norm_data"]='s'
            menu_choice="X" #resets the menu choice to restart the loop           
        elif menu_choice in ['m', 'M']:
            modes["norm_data"]='m'
            menu_choice="X" #resets the menu choice to restart the loop
        elif menu_choice in ['b', 'B']:
            modes["norm_data"]='b'
            menu_choice="X" #resets the menu choice to restart the loop
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")

def set_3d_options(modes):
    """
    This function modifies the 3d plotting options in the modes
    """
    menu_choice = "X"
    num_options = 3
    menu_options=range(0,num_options)
    
    while menu_choice not in menu_options:

        print("""
              3D/ANIMATION MODE MENU
      
      1: Set 3d plotting Options
      2: Set frame rate
      
      0: Return to previous menu
              """)
        try:#read in the choice as an int
            menu_choice=int(raw_input("Please enter your selection from the menu above:\t"))
            
        except ValueError: #can't be converted to an int
            print("Warning: invalid menu choice.") #print a warning
            menu_choice="X" #set the option back to default
            
        if 0 == menu_choice:
            pass #finish the loop
        
        elif 1 == menu_choice:
            set_3d_plotting(modes)
            menu_choice="X" #resets the menu choice to restart the loop
        elif 2 == menu_choice:
            set_frame_rate(modes)
            menu_choice="X" #resets the menu choice to restart the loop            
 
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")

def set_3d_plotting(modes):
    """
    This function modifies the 3d plotting options in the modes
    """
    menu_choice = "X"
    num_options = 3
    menu_options=range(0,num_options)
    current_name=""
    
    while menu_choice not in menu_options:
        
        if "colour" == modes["three_d"]:
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
      
      0: Return to previous menu
              """).format(current_name))
        try:#read in the choice as an int
            menu_choice=int(raw_input("Please enter your selection from the menu above:\t"))
            
        except ValueError: #can't be converted to an int
            print("Warning: invalid menu choice.") #print a warning
            menu_choice="X" #set the option back to default
            
        if 0 == menu_choice:
            pass #finish the loop
        
        elif 1 == menu_choice:
            modes["three_d"]='colour'
            menu_choice="X" #resets the menu choice to restart the loop
        elif 2 == menu_choice:
            modes["three_d"]='anim'
            menu_choice="X" #resets the menu choice to restart the loop    
        elif 3 == menu_choice:
            modes["three_d"]='animf'
            menu_choice="X" #resets the menu choice to restart the loop    
 
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
    num_options = 3
    menu_options=range(0,num_options)
    
    while menu_choice not in menu_options:

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
        try:#read in the choice as an int
            menu_choice=int(raw_input("Please enter your selection from the menu above:\t"))
            
        except ValueError: #can't be converted to an int
            print("Warning: invalid menu choice.") #print a warning
            menu_choice="X" #set the option back to default
            
        if 0 == menu_choice:
            pass #finish the loop
        
        elif 1 == menu_choice:
            modes = interactive_get_location(modes)
            modes = get_location(modes)
            menu_choice="X" #resets the menu choice to restart the loop
        elif 2 == menu_choice:
            modes = interactive_get_object(modes)
            modes = get_object(modes)
            menu_choice="X" #resets the menu choice to restart the loop            
 
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")
            

def set_plotting_options(modes):
    """
    This function modifies the plotting options in the modes
    """
    menu_choice = "X"
    num_options = 3
    menu_options=range(0,num_options)
    
    while menu_choice not in menu_options:

        print("""
              PLOTTING MODE MENU
      
      1: Set graphs to plot
      2: Set variables to plot
      
      0: Return to previous menu
              """)
        try:#read in the choice as an int
            menu_choice=int(raw_input("Please enter your selection from the menu above:\t"))
            
        except ValueError: #can't be converted to an int
            print("Warning: invalid menu choice.") #print a warning
            menu_choice="X" #set the option back to default
            
        if 0 == menu_choice:
            pass #finish the loop
        
        elif 1 == menu_choice:
            set_plotting(modes)
            menu_choice="X" #resets the menu choice to restart the loop
        elif 2 == menu_choice:
            set_values(modes)
            menu_choice="X" #resets the menu choice to restart the loop            
 
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")            

def set_plotting(modes):
    print ("Not implemented, returning")
    pass

def set_values(modes):
    """
    This function modifies the values to plot in the modes
    """
    menu_choice = "X"

    menu_options=["all","linear","stokes",
                  "xx","xy","yy","U","V","I","Q",
                  "each",
                  "0"]
    list_linear=["xx","xy","yy"]
    list_stokes=["U","V","I","Q"]
    list_all=["xx","xy","yy","U","V","I","Q"]
    dict_lists={"linear":list_linear,
                "stokes":list_stokes,
                "all":list_all}

    
    
    
    while menu_choice not in menu_options:
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
            pass #finish the loop
        
        #if it's a single value
        elif menu_choice in list_all:
            process_single_values_menu(menu_choice, modes, dict_lists)
            menu_choice="X" #resets the menu choice to restart the loop
            
        #if a group value
        elif menu_choice in dict_lists:
            process_group_values_menu(menu_choice, modes, dict_lists)
            menu_choice="X" #resets the menu choice to restart the loop
            
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
#"rmse", "corr", "spectra", 
#                                 "file",
#                                 "alt","az","ew", "stn", "split",
#                                 "values","model","scope", "diff", 
#                                 "overlay"
#looks like this was already done.  Partial version left for records
#def set_loc_options(modes):
#    """
#    This function modifies the observatory location options
#    """
#    menu_choice = "X"
#    num_options = 3
#    menu_options=range(0,num_options)
#    location_name=""
#    
#    while menu_choice not in menu_options:
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
#        if 0 == menu_choice:
#            pass #finish the loop
#        
#        elif 1 == menu_choice:
#            location_name=raw_input("Please enter the station code for the observing location:\t")
#            modes["location_name"]=location_name
#            modes=get_location(modes)
#            menu_choice="X" #resets the menu choice to restart the loop
#        elif 2 == menu_choice:
#            location_name=""
#            modes["location_name"]=location_name
#            modes["location_coords"]=[0]
#            modes=get_location(modes)
#            menu_choice="X" #resets the menu choice to restart the loop            
# 
#        else:
#            print("Input: "+str(menu_choice)+" not valid or not implemented.")