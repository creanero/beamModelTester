# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 14:44:17 2018

@author: User
"""
from alt_az_functions import get_location
from alt_az_functions import interactive_get_location

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
              CROPPING DATA MENU
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

        print("""
              COORDINATE MODE MENU
      
      1: Set Observing Location Options
      2: Set Target Coordinate Options
      
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
            modes = interactive_get_location(modes)
            modes = get_location(modes)
            menu_choice="X" #resets the menu choice to restart the loop
        elif 2 == menu_choice:
            set_target_options(modes)
            menu_choice="X" #resets the menu choice to restart the loop            
 
        else:
            print("Input: "+str(menu_choice)+" not valid or not implemented.")
            
            
def set_target_options(modes):
    print("Functionality not implmented")

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