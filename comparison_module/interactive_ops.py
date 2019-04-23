# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 14:44:17 2018

@author: User
"""

from alt_az_functions import set_coords
from alt_az_functions import check_coords

from reading_functions import read_var_file

from appearance_functions import gen_pretty_name

import os.path

import Tkinter as tk
import tkFileDialog
import tkFont

def cli_menu(menu_title="", menu_list=[], menu_status="", menu_prompt="",
             exit_prompt="", status_prompt="", desc_text="", warning=""):
    """
    This function produces a text menu on the screen for use with command line
    execution of the program
    """
    # creates a menu option for the user to input
    menu_choice = "X"

    # if the warning isn't blank
    if warning != "":
        # prints the warning
        print(warning + '\n')

    # if the title isn't blank
    if menu_title!="":
        # prints the title
        print(menu_title+"\n")
    
        
    # if a detailed description is provided
    if desc_text != "":
        # if it is provided as a function/method
        if callable(desc_text):
            # call it and record its return value in desc
            desc=desc_text()
        else:
            # otherwise, return its value
            desc=desc_text
        # prints the desc as a Label
        print(desc)        
    
    if status_prompt=="":
        status_prompt = "Current:"
    
    # if an overall menu status is provided
    if menu_status != "":
        # if it is provided as a function/method
        if callable(menu_status):
            # call it and record its return value in status and the default value
            status = menu_status()
        else:
            # otherwise, return its value in status and the default value
            status = menu_status
        status=status_prompt+" "+status
        # prints the status as a Label
        print(status)
    
    # prints a warning if there's no menu options
    if 0==len(menu_list):
        print("Menu Empty")
    
    for i in range(len(menu_list)):
        # creates a menu number
        menu_number = i + 1
        
        # reads in the menu prompt
        option=menu_list[i]["option"]
        
        # attempts to read the status corresponding to that menu item
        # if the menu item has a status variable
        if ('status' in menu_list[i].keys()):
            # check if it is a function
            if callable(menu_list[i]["status"]):
                # if so, call it and record its return value in status
                status=("Current: {0}").format(menu_list[i]["status"]())
            else:
                # otherwise, return its value
                status=("Current: {0}").format(menu_list[i]["status"])
        # if the menu item does not have a status variable
        else:
            # generate an empty string for the status
            status=""
        
        # prints the menu number
        print(("\t{0}: {1} {2}").format(menu_number, option,status))
        
    if ""==exit_prompt:
        exit_prompt="Return to previous menu"
    print(("\n\t0: {}").format(exit_prompt))
    
    # uses a default prompt if no better prompt is given
    if ""==menu_prompt:
        menu_choice=raw_input("Please enter your selection from the menu above:\t")
    else:
        menu_choice=raw_input(menu_prompt)
   
    return(menu_choice)


def cli_entry(menu_title="", menu_status="", menu_prompt="", desc_text="", 
              exit_prompt="", out_type="str", warning="", literal_zero=False,
              status_prompt=""):
    out_var = ""
    
    # uses '0' string as an exit value if true zero isn't a possible value
    if literal_zero:
        exit_value='X'
    else:
        exit_value='0'
    
    # if the warning isn't blank
    if warning != "":
        # prints the warning 
        print(warning +'\n') 
        
    # if the title isn't blank
    if menu_title!="":
        # prints the title as a label
        print(menu_title+'\n')
    
    
    if status_prompt=="":
        status_prompt = "Current:"
    
    # if an overall menu status is provided
    if menu_status != "":
        # if it is provided as a function/method
        if callable(menu_status):
            # call it and record its return value in status and the default value
            status = menu_status()
        else:
            # otherwise, return its value in status and the default value
            status = menu_status
        status=status_prompt+" "+status
        # prints the status as a Label
        print(status)
    
    
    
    
    
    # if a detailed description is provided
    if desc_text != "":
        # if it is provided as a function/method
        if callable(desc_text):
            # call it and record its return value in desc
            desc=desc_text()
        else:
            # otherwise, return its value
            desc=desc_text
        # prints the desc as a Label
        print(desc)          
    
    # sets up exit prompt
    if "" ==  exit_prompt:
        exit_prompt="return to previous menu"
    
    print("Type " + exit_value + " to "+ exit_prompt)
    
    
    # uses a default prompt if no better prompt is given
    if ""==menu_prompt:
        out_var=raw_input("Please enter the value required:\t")
    else:
        out_var=raw_input(menu_prompt+'\t')


    # if the output variable isn't the exit value
    if out_var.strip() != exit_value:        
        if out_type=='float':
            try:
                out_var = float(out_var)
            except ValueError:
                warning = "Warning: '{}' is not valid data.  Decimal number required.".format(out_var)
                out_var = cli_entry(menu_title, menu_status, menu_prompt,
                                    desc_text, exit_prompt, out_type, warning, 
                                    literal_zero)
        elif out_type=='int':
            try:
                out_var = int(out_var)
            except ValueError:
                warning = "Warning: '{}' is not valid data.  Integer required.".format(out_var)
                out_var = cli_entry(menu_title, menu_status, menu_prompt,
                                    desc_text, exit_prompt, out_type, warning, 
                                    literal_zero)
        elif out_type=='file_in':
            exists = os.path.isfile(out_var)
            if exists:
                pass  # out_var is good to go as it is
            else:
                warning = "Warning: '{}' is not a valid file path.  Please Try Again.".format(out_var)
                out_var = cli_entry(menu_title, menu_status, menu_prompt,
                                    desc_text, exit_prompt, out_type, warning, 
                                    literal_zero)
        elif out_type == 'dir':
            check_out_var = prep_out_dir(out_var)
            if check_out_var is None:
                warning = "Warning: '{}' is not a valid directory path.  Please Try Again.".format(out_var)
                out_var = cli_entry(menu_title, menu_status, menu_prompt,
                                    desc_text, exit_prompt, out_type, warning, 
                                    literal_zero)
            else:
                out_var = check_out_var
        else:
            pass # out_var=out_var
    else:
        pass # out_var="0" # leave it as '0' and allow that to return

    return(out_var)

def cli_coords(menu_title = "", menu_status="", status_prompt="", coords=[]):
    l_coords = []

    # if the title isn't blank
    if menu_title != "":
        # prints the title as a label
        print(menu_title + '\n')

    if status_prompt == "":
        status_prompt = "Current:"

    # if an overall menu status is provided
    if menu_status != "":
        # if it is provided as a function/method
        if callable(menu_status):
            # call it and record its return value in status and the default value
            status = menu_status()
        else:
            # otherwise, return its value in status and the default value
            status = menu_status
        status = status_prompt + " " + status
        # prints the status as a Label
        print(status)

    for coord in coords:
        f_coord = 0
        coord_continue = True


        while coord_continue:
            input_coord = raw_input("Please enter the " + coord + " leave blank to stop entering coordinates:\n\t\t")

            if input_coord == "":
                coord_continue = False
            else:
                try:
                    f_coord = (float(input_coord))
                    coord_continue = False
                except ValueError:
                    print("Warning: Coordinates must be specified as decimal numbers:\n\t")
                    coord_continue = True

        if type(f_coord) is int: # because it hasn't been changed from 0
            break  # stops going through the for loop over coordinates
        else:
            l_coords.append(f_coord)

    return (l_coords)

def gui_menu(menu_title="", menu_list=[], menu_status="", menu_prompt="",
             exit_prompt="", status_prompt="", desc_text="", warning=""):
    #TODO: Temp label
    
    # Creates an interactive window
    root = tk.Tk()
    
    # sets up a variable that will eventually set the output
    var = tk.StringVar()
    
    # if the title isn't blank
    if menu_title!="":
        # prints the title as a label
        root.title(menu_title)
        title = tk.Label(root,text=menu_title)
        title.pack()    
    
    
    # if a detailed description is provided
    if desc_text != "":
        # if it is provided as a function/method
        if callable(desc_text):
            # call it and record its return value in desc
            desc=desc_text()
        else:
            # otherwise, return its value
            desc=desc_text
        # prints the desc as a Label
        desc_label = tk.Label(root,text=desc)
        desc_label.pack()        
    
    if status_prompt=="":
        status_prompt = "Current:"
        
    
    # if an overall menu status is provided
    if menu_status != "":
        # if it is provided as a function/method
        if callable(menu_status):
            # call it and record its return value in status and the default value
            var.set(menu_status())
        else:
            # otherwise, return its value in status and the default value
            var.set(menu_status)
        status=status_prompt+" "+var.get()
        # prints the status as a Label
        status_label = tk.Label(root,text=status)
        status_label.pack()     
    else:
        var.set("")
    
    # prints a warning as a label if there's no menu options
    if 0==len(menu_list):
        warning_label = tk.Label(root,text="Menu_empty")
        warning_label.pack() 

    opt_buttons = dict()
    # iterates over the menu list
    for i in range(len(menu_list)):
        # creates a menu number
        menu_number = i + 1
        
        # reads in the menu option
        option=menu_list[i]["option"]
        
        # attempts to read the status corresponding to that menu item
        # if the menu item has a status variable
        if ('status' in menu_list[i].keys()):
            # check if it is a function
            if callable(menu_list[i]["status"]):
                # if so, call it and record its return value in status
                status=("(Current: {0})").format(menu_list[i]["status"]())
            else:
                # otherwise, return its value
                status=("(Current: {0})").format(menu_list[i]["status"])
        # if the menu item does not have a status variable
        else:
            # generate an empty string for the status
            status=""
        
        # Creates a string which contains the option and its status
        button_string=("{0} {1}").format(option,status)
        
        # produces a button for each option
        # R=tk.Radiobutton(root, text=button_string, variable=var, value=menu_number)
        # R.pack( anchor = tk.W )

        button_action = lambda x = menu_number: close_and_value(root, var, x)

        opt_buttons[i] = tk.Button(root, text=button_string, command=button_action)
        opt_buttons[i].pack()
    
    # if the exit/up a level prompt is not provided
    if ""==exit_prompt:
        # produces a default prompt
        exit_prompt="Return to previous menu"
    
    # # and creates a corresponding radio button
    # exit_button=tk.Radiobutton(root, text=exit_prompt, variable=var, value=0)
    # exit_button.pack( anchor = tk.W )

    exit_value = '0'
    # if the exit/up a level prompt is not provided
    if "" == exit_prompt:
        # produces a default prompt
        exit_prompt = "Return to previous menu"

    # and creates a corresponding button
    exit_button = tk.Button(root, text=exit_prompt,
                            command=lambda: close_and_value(root, var, exit_value))
    exit_button.pack()



    # if the title isn't blank
    if warning !="":
        # prints the warning as a label
        warning_label = tk.Label(root,text=warning,fg="red")
        warning_label.pack()
 
    # uses a default instruction if no better prompt is given
    if ""==menu_prompt:
        menu_prompt="Please click your selection from the menu above:\t"

    # and prints the instructions as a label   
    prompt = tk.Label(root,text=menu_prompt)
    prompt.pack() 
    
    # # creates a "confirm" button which kills root when it is called
    # submit=tk.Button(root, text="Click to confirm", command=root.destroy)
    # submit.pack()
    
    # runs the mainloop
    root.mainloop()
    
    # creates an ordinary string from the variable
    out_choice=str(var.get())
    
    # returns the choice string.
    return(out_choice)


def gui_entry(menu_title="", menu_status="", menu_prompt="", desc_text="",
              exit_prompt="", out_type="str", warning="", literal_zero=False,
              status_prompt=""):
    # creates an output variable
    out_var = ""
    
    # Creates an interactive window
    root = tk.Tk()
    
    # sets up a variable that will eventually set the output
    var = tk.StringVar()

    
    # uses '0' string as an exit value if true zero isn't a possible value
    if literal_zero:
        exit_value='X'
    else:
        exit_value='0'    

    # if the title isn't blank
    if menu_title!="":
        # prints the title as a label
        root.title(menu_title)
        title = tk.Label(root,text=menu_title)
        title.pack()    
    
    if status_prompt=="":
        status_prompt = "Current:"
    
    # if an overall menu status is provided
    if menu_status != "":
        # if it is provided as a function/method
        if callable(menu_status):
            # call it and record its return value in status and the default value
            var.set(menu_status())
        else:
            # otherwise, return its value in status and the default value
            var.set(menu_status)
        status=status_prompt+" "+var.get()
        # prints the status as a Label
        status_label = tk.Label(root,text=status)
        status_label.pack()     
    else:
        var.set("")
    
    # if a detailed description is provided
    if desc_text != "":
        # if it is provided as a function/method
        if callable(desc_text):
            # call it and record its return value in desc
            desc=desc_text()
        else:
            # otherwise, return its value
            desc=desc_text
        # prints the desc as a Label
        desc_label = tk.Label(root,text=desc)
        desc_label.pack()           
    


    # if the title isn't blank
    if warning !="":
        # prints the warning as a label
        warning_label = tk.Label(root,text=warning,fg="red")
        warning_label.pack()    



    # uses a default instruction if no better prompt is given
    if ""==menu_prompt:
        menu_prompt="Please type your selection in the box below:"
        
    # and prints the instructions as a label   
    prompt = tk.Label(root,text=menu_prompt)
    prompt.pack()   
    
    if out_type in ['file_in','dir']:
        # creates a variable to hold the name of the data type
        type_name = ""

        if out_type == 'dir':
            type_name = "Directory"
        elif out_type == 'file_in':
            type_name = "File"
        # creates a change file button which opens a select file button
        file_button=tk.Button(root, text="Select "+type_name,
                          command=lambda:pick_in_file(root,var,menu_prompt,type_name))
        file_button.pack()
            # and creates a corresponding button
        clear_button=tk.Button(root, text="Clear "+type_name,
                              command=lambda:close_and_value(root,var,""))
        clear_button.pack()
    else:
        # creates the main data entry box
        entry_box = tk.Entry(root, textvariable=var)
        entry_box.pack()

    # creates a "confirm" button which kills root when it is called
    submit=tk.Button(root, text="Click to confirm", command=root.destroy)
    submit.pack()
    
    # if the exit/up a level prompt is not provided
    if ""==exit_prompt:
        # produces a default prompt
        exit_prompt="Return to previous menu"
    
    # and creates a corresponding button
    exit_button=tk.Button(root, text=exit_prompt, 
                          command=lambda:close_and_value(root,var,exit_value))
    exit_button.pack()
    
    # runs the mainloop
    root.mainloop()
    
    out_var=var.get()
    
    # if the output variable isn't the exit value
    if out_var.strip() != exit_value:  

        if out_type=='float':
            try:
                out_var = float(str(var.get()))
            except ValueError:
                warning = "Warning: {} is not valid data.  Decimal number required.".format(str(var.get()))
                menu_status = out_var
                out_var = gui_entry(menu_title, menu_status, menu_prompt,
                                    desc_text, exit_prompt, out_type, warning)
        elif out_type=='int':
            try:
                out_var = int(float(var.get()))
            except ValueError:
                warning = "Warning: {} is not valid data.  Integer required.".format(str(var.get()))
                menu_status = out_var
                out_var = gui_entry(menu_title, menu_status, menu_prompt,
                                    desc_text, exit_prompt, out_type, warning)
        elif out_type=='file_in':
            if out_var == "":
                pass # OK to leave clear
            else:
                exists = os.path.isfile(out_var)
                if exists:
                    menu_status = out_var
                    pass # out_var is good to go as it is
                else:
                    menu_status = out_var
                    warning = "Warning: {} is not a valid file path.  Please Try Again.".format(out_var)
                    out_var = gui_entry(menu_title, menu_status, menu_prompt,
                                        desc_text, exit_prompt, out_type, warning, 
                                        literal_zero)

        elif out_type == 'dir':
            check_out_var = prep_out_dir(out_var)
            if check_out_var is None:
                warning = "Warning: '{}' is not a valid directory path.  Please Try Again.".format(out_var)
                out_var = gui_entry(menu_title, menu_status, menu_prompt,
                                    desc_text, exit_prompt, out_type, warning,
                                    literal_zero)
            else:
                out_var = check_out_var
        else:
            pass # out_var=var.get() # leave it as it is
    else:
        pass # out_var="0" # leave it as '0' and allow that to return

    return(out_var)


def gui_coords(menu_title="", menu_status=[], menu_prompt="", desc_text="",
              exit_prompt="", warning="", status_prompt="", coord_names=[]):
    # creates an output variable
    vars = []


    # Creates an interactive window
    root = tk.Tk()

    button_var = tk.StringVar()
    exit_value = 'exit'
    clear_value = 'clear'

    # if the title isn't blank
    if menu_title != "":
        # prints the title as a label
        root.title(menu_title)
        title = tk.Label(root, text=menu_title)
        title.pack()

    if status_prompt == "":
        status_prompt = "Current:"

    # if an overall menu status is provided
    if menu_status != "":
        # if it is provided as a function/method
        if callable(menu_status):
            # call it and record its return value in status and the default value
            menu_status = menu_status()
        else:
            # otherwise, return its value in status and the default value
            menu_status = menu_status
        status = status_prompt + " " + menu_status
        # prints the status as a Label
        status_label = tk.Label(root, text=status)
        status_label.pack()


    # if a detailed description is provided
    if desc_text != "":
        # if it is provided as a function/method
        if callable(desc_text):
            # call it and record its return value in desc
            desc = desc_text()
        else:
            # otherwise, return its value
            desc = desc_text
        # prints the desc as a Label
        desc_label = tk.Label(root, text=desc)
        desc_label.pack()

        # if the title isn't blank
    if warning != "":
        # prints the warning as a label
        warning_label = tk.Label(root, text=warning, fg="red")
        warning_label.pack()

    # and prints the instructions as a label
    prompt = tk.Label(root, text=menu_prompt)
    prompt.pack()


    # and creates a corresponding button
    clear_button = tk.Button(root, text="Clear Coordinates" ,
                             command=lambda: close_and_value(root, button_var, clear_value))
    clear_button.pack()
    for i in range(len(coord_names)):
        var = tk.StringVar()
        vars.append(var)
        # creates the main data entry box
        entry_box = tk.Entry(root, textvariable=vars[i])
        entry_box.pack()
        coord_label = tk.Label(root, text=coord_names[i])
        coord_label.pack()

    # creates a "confirm" button which kills root when it is called
    submit = tk.Button(root, text="Click to confirm", command=root.destroy)
    submit.pack()

    # if the exit/up a level prompt is not provided
    if "" == exit_prompt:
        # produces a default prompt
        exit_prompt = "Return to previous menu"

    # and creates a corresponding button
    exit_button = tk.Button(root, text=exit_prompt,
                            command=lambda: close_and_value(root, button_var, exit_value))
    exit_button.pack()

    # runs the mainloop
    root.mainloop()

    out_vars=[]

    warning=""

    check_var = button_var.get()


    # if the output variable isn't the exit value
    if check_var == exit_value:
        out_vars = exit_value
    elif check_var == clear_value:
        out_vars = clear_value
    else:
        for i in range(len(vars)):
            out_var = vars[i].get()


            try:
                out_var = float(out_var)
            except ValueError:
                warning = warning + "Warning: '{}' is not valid for {}.\n".format(out_var, coord_names[i])
            # out_vars = gui_entry(menu_title, menu_status, menu_prompt,
            #                     desc_text, exit_prompt, out_type, warning)
            out_vars.append(out_var)

    if warning != "":
        out_vars = gui_coords(menu_title, menu_status, menu_prompt, desc_text,
                              exit_prompt, warning, status_prompt, coord_names)

    return out_vars


def close_and_value(root,var,value):
    root.destroy()
    var.set(value)


def pick_in_file(root,var,menu_prompt,type_name):# ,file_options=("all files","*.*")):
    root.destroy()
    root = tk.Tk()
    if type_name == "File":
        root.filename = tkFileDialog.askopenfilename(initialdir = os.getcwd(),
                        title = menu_prompt)# ,
    #                    filetypes = file_options)
    elif type_name == "Directory":
        root.filename = tkFileDialog.askdirectory(initialdir=os.getcwd(),
                                                     title=menu_prompt)  # ,
    #                    filetypes = file_options)

    var.set(root.filename)
    root.destroy()

def interactive_operation(modes, model_df, scope_df):
    """
    This function controls interactive elements of the software system and 
    enables iterative use of the system
    """
    continue_option = True
    menu_choice = "X"
    
    warning = ""


    while continue_option:
        # sets up the menu options for cli or gui use
        menu_title = "INTERACTIVE MODE MENU"
        
        # creates a list of menu items
        menu_list = []
                
        # each menu item has an option title.
        # status can be blank, a function or constant
        opt_name = {"option":"Cropping Options"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Normalisation Options"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Animation/3D Options"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Location/Target Options"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Plotting Options"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"File Input/Output Options"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Frequency Options"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Other Options"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Plot with current options"}
        menu_list.append(opt_name)
        

        exit_prompt="Exit"
    
        # Runs with GUI or CLI depending on mode.
        if modes['interactive']==3:
            menu_choice = gui_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   exit_prompt=exit_prompt,
                                   warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   exit_prompt=exit_prompt,
                                   warning = warning)




        # this setion handles the responses
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
            model_df,scope_df = set_file_io_options(modes, model_df, scope_df)
        elif "7" == menu_choice:
            set_frequency_options(modes)
        elif "8" == menu_choice:
            set_other_options(modes)

            
        elif "9" == menu_choice:
            continue_option=False # finish the loop
            pass
                                
        elif "0" == menu_choice:
            modes['interactive']=0 # terminates the interactions which will exit
            continue_option=False # finish the loop

        else:
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."
            continue_option = True

    return (modes, model_df, scope_df)
            
def set_crop_options(modes):
    """
    This function modifies the cropping options in the modes
    """
    menu_choice = "X"
    continue_option=True
    # menu_options=range(0,num_options)
    warning = ""
    
    while continue_option:

        # sets up the menu options for cli or gui use
        menu_title ="CROPPING MODE MENU"
         
        # creates a list of menu items
        menu_list = []
                
        # each menu item has an option title.
        # status can be blank, a function or constant     
        opt_name = {"option":"Set Crop Level"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Set Crop Basis (Frequency/Overall)"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Set Crop Data (Model/Scope)"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Set Crop Operation Type"}
        menu_list.append(opt_name)
        
      
        # Runs with GUI or CLI depending on mode.
        if modes['interactive']==3:
            menu_choice = gui_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning = warning)
            
        if "0" == menu_choice:
            continue_option=False # finish the loop
        
        elif "1" == menu_choice:
            set_crop_level(modes)
            
        elif "2" == menu_choice:
            set_crop_basis(modes)
                        
        elif "3" == menu_choice:
            set_crop_data(modes)
               
        elif "4" == menu_choice:
            set_crop_type(modes)
               
        else:
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."
    
def set_crop_level(modes):
    """
    This function modifies the cropping level options in the modes variable
    """

    continue_option=True
    # menu_options=range(0,num_options)
    
    warning = ""
    
    while continue_option:
        # sets up the menu options for cli or gui use
        menu_title ="CROPPING LEVEL MENU"
        desc_text = """Crop level indicates the numerical factor for cropping. Depending on the crop operation, the crop level is implemented differently.
  
In "median" or "mean" crop operation, the crop level is the multiplier by which those values are multiplied to generate the maximum permitted value
  
In "percentile" crop operation, the crop level is the pecentile level to crop to.  Percentiles higher than 100 are ignored
          """
        menu_prompt = "Please enter the crop level desired:"
        menu_status = str(modes['crop'])
        if modes['interactive']==3:
            crop_level=gui_entry(menu_title, menu_status, menu_prompt, 
                                 desc_text, exit_prompt="", out_type="float", 
                                 warning=warning, literal_zero=False)
        else:
            crop_level=cli_entry(menu_title, menu_status, menu_prompt, 
                                 desc_text, exit_prompt="", out_type="float", 
                                 warning=warning, literal_zero=False)
        if crop_level == '0':
            continue_option=False
        else:
            modes["crop"]=crop_level


def set_crop_basis(modes):
    """
    This function modifies the cropping basis options in the modes
    """
    menu_choice = "X"
    continue_option=True
    # menu_options=['n', 'N', 'o', 'O', 'f', 'F', '0']
    warning = ""
    
    while continue_option:

        # sets up the menu options for cli or gui use
        menu_title ="CROPPING BASIS MENU"
         
        # creates a list of menu items
        menu_list = []
                
        # each menu item has an option title.
        # status can be blank, a function or constant 

              
        opt_name = {"option":"No Cropping"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Crop Overall"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Crop by Frequency"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Crop by Time"}
        menu_list.append(opt_name)        
      

        menu_status=gen_basis_name(modes["crop_basis"])
        
      
        # Runs with GUI or CLI depending on mode.
        if modes['interactive']==3:
            menu_choice = gui_menu(menu_title=menu_title,
                                 menu_list=menu_list,
                                 menu_status=menu_status,
                                 warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                 menu_list=menu_list,
                                 menu_status=menu_status,
                                 warning = warning)  
        
        
        if '0' == menu_choice:
            continue_option=False # finish the loop
        
        elif menu_choice in ['1']:
            modes["crop_basis"]='n'
                       
        elif menu_choice in ['2']:
            modes["crop_basis"]='o'
            
        elif menu_choice in ['3']:
            modes["crop_basis"]='f'
            
        elif menu_choice in ['4']:
            modes["crop_basis"]='t'
            
        else:
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."

def set_crop_data(modes):
    """
    This function modifies the cropping basis options in the modes
    """
    menu_choice = "X"
    
    warning = ""
   
    # menu_options=['n', 'N', 's', 'S', 'm', 'M', 'b', 'B', '0']
    continue_option=True
    while continue_option:

        # sets up the menu options for cli or gui use
        menu_title ="CROPPING DATA MENU"
         
        # creates a list of menu items
        menu_list = []
                
        # each menu item has an option title.
        # status can be blank, a function or constant 
        opt_name = {"option":"Crop Neither"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Crop Scope"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Crop Model"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Crop Both"}
        menu_list.append(opt_name)
        
      

        menu_status=gen_source_name(modes["crop_data"])
        
        # Runs with GUI or CLI depending on mode.
        if modes['interactive']==3:
            menu_choice = gui_menu(menu_title=menu_title,
                                 menu_list=menu_list,
                                 menu_status=menu_status,
                                 warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                 menu_list=menu_list,
                                 menu_status=menu_status,
                                 warning = warning)  
        
        
        if '0' == menu_choice:
            continue_option=False # finish the loop
        
        elif menu_choice in ['1']:
            modes["crop_data"]='n'
            
        elif menu_choice in ['2']:
            modes["crop_data"]='s'
                       
        elif menu_choice in ['3']:
            modes["crop_data"]='m'
            
        elif menu_choice in ['4']:
            modes["crop_data"]='b'
            
        else:
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."

def set_crop_type(modes):
    """
    This function modifies the cropping operation type options in the modes
    """
    menu_choice = "X"
    continue_option=True
    # menu_options=range(0,num_options)
    
    warning = ""
    
    while continue_option:

        # sets up the menu options for cli or gui use
        menu_title ="CROPPING MODE MENU"
         
        # creates a list of menu items
        menu_list = []
                
        # each menu item has an option title.
        # status can be blank, a function or constant 
        opt_name = {"option":"Median"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Mean"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Percentile"}
        menu_list.append(opt_name)
        
      

        menu_status=modes["crop_type"]
        
        # Runs with GUI or CLI depending on mode.
        if modes['interactive']==3:
            menu_choice = gui_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   menu_status=menu_status,
                                   warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   menu_status=menu_status,
                                   warning = warning)  
        
            
        if "0" == menu_choice:
            continue_option=False # finish the loop
        
        elif "1" == menu_choice:
            modes["crop_type"]="median"
            
        elif "2" == menu_choice:
            modes["crop_type"]="mean"
                        
        elif "3" == menu_choice:
            modes["crop_type"]="percentile"
               

        else:
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."

#this function isn't used any more, but is being retained for archival purposes
#def validate_options(user_input, valid_options, permit_partial=True):
#    """
#    This function is used to validate options input by the user to interactive 
#    operations.  User input is compared with a list of valid options and the
#    valid options in the user input are returned.  
#    
#    The "permit partial" option allows for valid options to be retained if the 
#    user submits a mix of valid and invalid options
#    """
#    output_options = []
#    
#    # if all are valid
#    if all (opt in valid_options for opt in user_input):
#        # pass them all to output
#        output_options = user_input
#        
#    else : # not all options are valid
#        # check if partial matches are permitted
#        if True==permit_partial:
#            
#            # Setup the output variable by making a copy of the input
#            output_options=list(user_input)
#            
#            # if so, go through the input
#            for opt in user_input:
#                # and reove invalid inputs from the output
#                if opt not in valid_options:
#                    output_options.remove(opt)
#                    print("Option: "+str(opt)+
#                          " is invalid, continuing with remainder")
#            
#
#        else:
#            output_options=[]
#            print("Some options are invalid.  Stopping.")
#    return(output_options)
                
    
def set_norm_options(modes):
    """
    This function modifies the cropping options in the modes
    """
    menu_choice = "X"
    continue_option=True
    # menu_options=range(0,num_options)
    
    warning = ""
    
    
    while continue_option:

        # sets up the menu options for cli or gui use
        menu_title ="NORMALISATION MODE MENU"
         
        # creates a list of menu items
        menu_list = []
                
        # each menu item has an option title.
        # status can be blank, a function or constant 
        opt_name = {"option":"Set Normalisation Basis (Frequency/Overall)"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Set Normalisation Data (Model/Scope)"}
        menu_list.append(opt_name)
        

      
        # Runs with GUI or CLI depending on mode.
        if modes['interactive']==3:
            menu_choice = gui_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning = warning)  
        
            
        if "0" == menu_choice:
            continue_option=False # finish the loop
        
        elif "1" == menu_choice:
            set_norm_basis(modes)
            
        elif "2" == menu_choice:
            set_norm_data(modes)
                        
 
        else:
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."


def set_norm_basis(modes):
    """
    This function modifies the normalisation basis options in the modes
    """
    menu_choice = "X"
    
    warning = ""
   
    continue_option=True
    while continue_option:

        # sets up the menu options for cli or gui use
        menu_title ="NORMALISATION BASIS MENU"
         
        # creates a list of menu items
        menu_list = []
                
        # each menu item has an option title.
        # status can be blank, a function or constant 
        opt_name = {"option":"No Normalisation"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Normalisation Overall"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Normalisation by Frequency"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Normalisation by Time"}
        menu_list.append(opt_name)
      

        menu_status=gen_basis_name(modes["norm"])
        
        # Runs with GUI or CLI depending on mode.
        if modes['interactive']==3:
            menu_choice = gui_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   menu_status=menu_status,
                                   warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   menu_status=menu_status,
                                   warning = warning)  
        
        if '0' == menu_choice:
            continue_option=False # finish the loop
        
        elif menu_choice in ['1']:
            modes["norm"]='n'
        elif menu_choice in ['2']:
            modes["norm"]='o'            
        elif menu_choice in ['3']:
            modes["norm"]='f'
        elif menu_choice in ['4']:
            modes["norm"]='t'                       

            
        else:
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."

def set_norm_data(modes):
    """
    This function modifies the normalisation data options in the modes
    """
    menu_choice = "X"
    continue_option=True
    
    warning = ""
    
    while continue_option:

        # sets up the menu options for cli or gui use
        menu_title ="NORMALISATION DATA MENU"
         
        # creates a list of menu items
        menu_list = []
                
        # each menu item has an option title.
        # status can be blank, a function or constant 
        opt_name = {"option":"Normalise Neither"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Normalise Scope"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Normalise Model"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Normalise Both"}
        menu_list.append(opt_name)
        
        menu_status=gen_source_name(modes["norm_data"])
        
        # Runs with GUI or CLI depending on mode.
        if modes['interactive']==3:
            menu_choice = gui_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   menu_status=menu_status,
                                   warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   menu_status=menu_status,
                                   warning = warning)  
        
        if '0' == menu_choice:
            continue_option=False # finish the loop
        
        elif menu_choice in ['1']:
            modes["norm_data"]='n'
            
        elif menu_choice in ['2']:
            modes["norm_data"]='s'
                       
        elif menu_choice in ['3']:
            modes["norm_data"]='m'
            
        elif menu_choice in ['4']:
            modes["norm_data"]='b'
            
        else:
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."

def set_3d_options(modes):
    """
    This function modifies the 3d plotting options in the modes
    """
    menu_choice = "X"
    continue_option=True
    # menu_options=range(0,num_options)
    
    warning = ""
    
    while continue_option:

        # sets up the menu options for cli or gui use
        menu_title ="3D/ANIMATION MODE MENU"
         
        # creates a list of menu items
        menu_list = []
                
        # each menu item has an option title.
        # status can be blank, a function or constant 
        opt_name = {"option":"Set 3d plotting Options"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Set frame rate"}
        menu_list.append(opt_name)
        
        # Runs with GUI or CLI depending on mode.
        if modes['interactive']==3:
            menu_choice = gui_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning = warning)  
            
        if "0" == menu_choice:
            continue_option=False # finish the loop
        
        elif "1" == menu_choice:
            set_3d_plotting(modes)
            
        elif "2" == menu_choice:
            set_frame_rate(modes)
                        
 
        else:
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."

def set_3d_plotting(modes):
    """
    This function modifies the 3d plotting options in the modes
    """
    menu_choice = "X"
    continue_option=True
    # menu_options=range(0,num_options)
    
    warning = ""

    
    while continue_option:
        
        
        
        # sets up the menu options for cli or gui use
        menu_title ="3D/ANIMATION PLOTTING MENU"
         
        # creates a list of menu items
        menu_list = []
                
        # each menu item has an option title.
        # status can be blank, a function or constant 
        opt_name = {"option":"Plot 3-d colour plots"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Plot animated against time"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Plot animated against frequency"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Plot 3-d contour plots"}
        menu_list.append(opt_name)
        
        menu_status=gen_three_d_name(modes['three_d'])
        
        # Runs with GUI or CLI depending on mode.
        if modes['interactive']==3:
            menu_choice = gui_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   menu_status=menu_status,
                                   warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   menu_status=menu_status,
                                   warning = warning)  
            
        if "0" == menu_choice:
            continue_option=False # finish the loop
        
        elif "1" == menu_choice:
            modes["three_d"]='colour'
            
        elif "2" == menu_choice:
            modes["three_d"]='anim'
                
        elif "3" == menu_choice:
            modes["three_d"]='animf'
                
        elif "4" == menu_choice:
            modes["three_d"]='contour'
               
        else:
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."
                    
def set_frame_rate(modes):
    """
    This function modifies the cropping level options in the modes variable
    """
    frame_rate = 0.0

    continue_option=True
    # menu_options=range(0,num_options)
    
    warning = ""
    
    while continue_option:
        # sets up the menu options for cli or gui use
        menu_title ="FRAME RATE MENU"
        desc_text = """Sets the frame rate for animated operations in frames per second"""
        menu_prompt = "Please enter the frame rate desired:"
        menu_status = str(modes["frame_rate"])
        if modes['interactive']==3:
            frame_rate = gui_entry(menu_title, menu_status, menu_prompt,
                                 desc_text, exit_prompt="", out_type="float", 
                                 warning=warning, literal_zero=False)
        else:
            frame_rate = cli_entry(menu_title, menu_status, menu_prompt, 
                                 desc_text, exit_prompt="", out_type="float", 
                                 warning=warning, literal_zero=False)
        if frame_rate == '0':
            continue_option=False
        else:
            modes["frame_rate"]=frame_rate

        
def set_coordinate_options(modes):
    """
    This function modifies the observatory location and target options
    """
    menu_choice = "X"
    continue_option=True
    # menu_options=range(0,num_options)
    
    warning = ""
    
    while continue_option:        
        # sets up the menu options for cli or gui use
        menu_title ="TARGET AND LOCATION MENU"
         
        # creates a list of menu items
        menu_list = []
                
        # each menu item has an option title.
        # status can be blank, a function or constant 
        opt_name = {"option":"Set Observing Location Options"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Set Target Coordinate Options"}
        menu_list.append(opt_name)
        
        # constructs the menu status
        menu_status = ""
        
        # starts with location name
        menu_status = menu_status + "Current Location Name:"
        if modes['location_name'] is None:
            menu_status = menu_status + " None Specified\n"
        else:
            menu_status = menu_status + " " + modes['location_name']+'\n'
        
        # then location coordinates if specified
        menu_status = menu_status + "Current Location Coordinates:"
        if modes['location_coords'] is None:
            menu_status = menu_status + " None Specified\n"
        else:
            str_location_coords="\nLat: {0}deg Long: {1}deg Elev: {2}m\n".format(
                    modes['location_coords'][0], # latitude
                    modes['location_coords'][1], # longitude
                    modes['location_coords'][2],) # height,)
            menu_status = menu_status + str_location_coords
        
        # moves on to object
        menu_status = menu_status + "\nCurrent Object Name:"
        if modes['object_name'] is None:
            menu_status = menu_status + " None Specified\n"
        else:
            menu_status = menu_status + " " + modes['object_name']+"\n"
        
        # then object coordinates if specified
        menu_status = menu_status + "Current Object Coordinates:"
        if modes['object_coords'] is None:
            menu_status = menu_status + " None Specified\n"
        else:
            str_object_coords="\nRA: {0}deg DEC: {1}deg\n".format(
                    modes['object_coords'][0], # RA
                    modes['object_coords'][1],) # Dec
            menu_status = menu_status + str_object_coords            
            

        
        
        # Runs with GUI or CLI depending on mode.
        if modes['interactive']==3:
            menu_choice = gui_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   menu_status=menu_status,
                                   warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   menu_status=menu_status,
                                   warning = warning)  
            
        if "0" == menu_choice:
            continue_option=False # finish the loop
        
        elif "1" == menu_choice:
            modes = interactive_get_location(modes) 
            modes = get_location(modes)
            
        elif "2" == menu_choice:
            modes = interactive_get_object(modes)
            modes = get_object(modes)
                        
 
        else:
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."
            

def set_plotting_options(modes):
    """
    This function modifies the plotting options in the modes
    """
    menu_choice = "X"
    continue_option=True
    # menu_options=range(0,num_options)
    
    warning = ""
    
    while continue_option:        
        # sets up the menu options for cli or gui use
        menu_title ="PLOTTING MODE MENU"
         
        # creates a list of menu items
        menu_list = []
                
        # each menu item has an option title.
        # status can be blank, a function or constant 
        opt_name = {"option":"Set graphs to plot"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Set variables to plot"}
        menu_list.append(opt_name)


        # Runs with GUI or CLI depending on mode.
        if modes['interactive']==3:
            menu_choice = gui_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning = warning)  
            
        if "0" == menu_choice:
            continue_option=False # finish the loop
        
        elif "1" == menu_choice:
            set_plotting(modes)
            
        elif "2" == menu_choice:
            set_values(modes)
                        
 
        else:
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."

def set_plotting(modes):
    """
    This functionsets the graphs to be plotted.
    """
    menu_choice = "X"
    continue_option=True
    # menu_options=range(0,num_options)
    
#    ["rmse", "corr", "spectra", 
#                                 "file",
#                                 "alt","az","ew", "stn", "split",
#                                 "values","model","scope", "diff", 
#                                 "overlay"]
    
    warning = ""
    
    
    while continue_option:
        # checks the current status of overlaid plots
        overlay_status="overlay" in modes['plots']
        # checks the current status of time series plots
        spectra_status="spectra" in modes['plots']   
        
        # sets up the menu options for cli or gui use
        menu_title ="GRAPH SELECTION MENU"
         
        # creates a list of menu items
        menu_list = []
                
        # each menu item has an option title.
        # status can be blank, a function or constant 
      
        opt_name = {"option":"Set figure of merit for closeness of fit"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Set alt-azimuth plotting options"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Set whether to plot model, scope or difference values"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Toggle single-channel overlay options",
                  "status":(gen_overlay_boolean(not(overlay_status)))}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Toggle time series plots.",
                  "status":(gen_plotting_boolean(spectra_status))}
        menu_list.append(opt_name)
        
        
        # Runs with GUI or CLI depending on mode.
        if modes['interactive']==3:
            menu_choice = gui_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning = warning)  
            
        if "0" == menu_choice:
            continue_option=False # finish the loop
        
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
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."

def set_fom(modes):
    """
    This function sets the figures of merit to be plotted.
    """
    menu_choice = "X"
    continue_option=True
    # menu_options=range(0,num_options)
    
    warning = ""
    
    while continue_option:
        # checks whether RMSE is currently being used
        rmse_status="rmse" in modes['plots']
        
        # checks whether correlation plots are currently requested
        corr_status="corr" in modes['plots']
  
        # checks whether time plots are currently requested
        time_status="time" in modes['plots']

        # checks whether frequency plots are currently requested
        spectra_status = "spectra" in modes['plots']

        # sets up the menu options for cli or gui use
        menu_title ="FIGURE OF MERIT SELECTION MENU"
         
        # creates a list of menu items
        menu_list = []
                
        # each menu item has an option title.
        # status can be blank, a function or constant 
      
        opt_name = {"option":"Toggle Root Mean Squared Error Plotting.",
                  "status":(gen_plotting_boolean(rmse_status))}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Toggle Pearson's Correlation Plotting.",
                  "status":(gen_plotting_boolean(corr_status))}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Toggle Time Plotting.",
                  "status":(gen_plotting_boolean(time_status))}
        menu_list.append(opt_name)

        opt_name = {"option": "Toggle Frequency Plotting.",
                    "status": (gen_plotting_boolean(spectra_status))}
        menu_list.append(opt_name)

        # Runs with GUI or CLI depending on mode.
        if modes['interactive']==3:
            menu_choice = gui_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning = warning)  
            
        if "0" == menu_choice:
            continue_option=False # finish the loop
        
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
                
            
        elif "3" == menu_choice:
            if time_status:
                modes['plots'].remove("time")
            else:
                modes['plots'].append("time")

        elif "4" == menu_choice:
            if spectra_status:
                modes['plots'].remove("spectra")
            else:
                modes['plots'].append("spectra")


        else:
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."

def set_alt_az(modes):
    """
    This function sets the plotting options for Alt/Az plots.
    """
    menu_choice = "X"
    continue_option=True

    warning = ""
    
    while continue_option:
        # checks whether plots against altitude have been specified
        alt_status="alt" in modes['plots']
        # checks whether plots against azimuth have been specified
        az_status="az" in modes['plots']
        # checks whether azimuth is specified east/west or 0-360
        ew_status="ew" in modes['plots']
        # checks whether geo or station coordinates are used
        stn_status="stn" in modes['plots']        
        # checks whether looping plots are split
        split_status="split" in modes['plots'] 
        
        
        # sets up the menu options for cli or gui use
        menu_title ="ALT-AZIMUTH OPTION SELECTION MENU"
         
        # creates a list of menu items
        menu_list = []
                
        # each menu item has an option title.
        # status can be blank, a function or constant 
        opt_name = {"option":"Toggle Altitude Plotting.",
                  "status":(gen_plotting_boolean(alt_status))}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Toggle Azimuth Plotting.",
                  "status":(gen_plotting_boolean(az_status))}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Toggle how Azimuth is displayed (E/W or 0-360).",
                  "status":(gen_ew_boolean(ew_status))}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Toggle use of LOFAR Station Coordinates.",
                  "status":(gen_use_boolean(stn_status))}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Toggle splitting of looping plots.",
                  "status":(gen_split_boolean(split_status))}
        menu_list.append(opt_name)
        

          
        # Runs with GUI or CLI depending on mode.
        if modes['interactive']==3:
            menu_choice = gui_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning = warning)  
            
            
        if "0" == menu_choice:
            continue_option=False # finish the loop
        
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
                        
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."

def set_msd_vals(modes):
    """
    This function sets Whether to plot Model, scope or difference data.
    """
    menu_choice = "X"
    continue_option=True
    # menu_options=range(0,num_options)
    
    warning = ""
    
    while continue_option:
        # checks if model plotting is requested
        model_status="model" in modes['plots']
        # checks if scope plotting is requested
        scope_status="scope" in modes['plots']
        # checks if difference plotting is requested
        diff_status="diff" in modes['plots']
      

        # sets up the menu options for cli or gui use
        menu_title ="PLOTTING DATA SELECTION MENU"
         
        # creates a list of menu items
        menu_list = []
                
        # each menu item has an option title.
        # status can be blank, a function or constant 
      
        opt_name = {"option":"Toggle Model Data Plotting.",
                  "status":(gen_plotting_boolean(model_status))}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Toggle Scope Data Plotting",
                  "status":(gen_plotting_boolean(scope_status))}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Toggle Difference Plotting.",
                  "status":(gen_plotting_boolean(diff_status))}
        menu_list.append(opt_name)
        

        # Runs with GUI or CLI depending on mode.
        if modes['interactive']==3:
            menu_choice = gui_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning = warning)  
            
            
        if "0" == menu_choice:
            continue_option=False # finish the loop
        
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
                        
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."


def get_location(modes):
    """
    This function prompts the user to enter the coordinates of the observing
    station
    """
    #TODO: get the rest of the prints out of here
    
    warn_flag = False

    # sets up the location coordinates
    if modes['location_name'] is not None:
        modes['location_coords'] = set_coords(modes['location_name'],
                                              modes['verbose'])
    # checks the coordinates are valid

    # if there are 2 or 3 coordinates
    if modes['location_coords'] is None:
        pass  # no coords specified, let it go as is
    elif len(modes['location_coords']) == 2 or len(modes['location_coords']) == 3:

        # checks the validity of those coordinates
        warn_flag = check_coords(modes['location_coords'][0],  # latitude
                                 modes['location_coords'][1],  # longitude
                                 modes)  # supplied separately for compatibility

        # if there are only two coordinates (missing height)
        if len(modes['location_coords']) == 2 and not warn_flag:

            if modes['verbose'] >= 1:
                print("Warning: no height above sea level specified")

            if modes['interactive'] >= 1:
                height_flag = True
                while height_flag:
                    height_test = raw_input("\nDo you want to specify a height (Default 0m)? [y/n]:\t")

                    if height_test in ["N", "n"]:
                        print("Height above sea level defaulting to 0m")
                        modes['location_coords'] = modes['location_coords'] + [0.0]
                        height_flag = False  # end the while loop

                    elif height_test in ["Y", "y"]:
                        warn_flag = True  # reenter the coordinates
                        height_flag = False  # end while loop
                    else:
                        print("Input not understood.")
                        height_flag = True  # continue while loop


            else:  # in low interactivity modes
                # appends a height of zero (sea level) for the observing site
                if modes['verbose'] >= 1:
                    print("Interactivity mode: " + str(modes['interactive']) + "\n"
                                                                               "Height above sea level defaulting to 0m")
                modes['location_coords'] = modes['location_coords'] + [0.0]
    else:
        if modes['verbose'] >= 1:
            if modes['location_name'] is None:
                print("Warning: Site: " + str(modes['location_coords']) +
                      " incorrectly specified.  ")
        warn_flag = True
    if warn_flag == True:
        if modes['interactive'] >= 1:
            modes = interactive_get_location(modes)
            modes = get_location(modes)
        else:
            if modes['verbose'] >= 1:
                print("Interactivity mode: " + str(modes['interactive']))
                modes['location_coords'] = None

    return (modes)


def get_object(modes):
    """
    This function prompts the user to enter the coordinates of the target
    """
    #TODO: get the rest of the prints out of here

    
    warn_flag = False

    # sets up the object coordinates
    if modes['object_name'] is not None:
        modes['object_coords'] = set_coords(modes['object_name'],
                                            modes['verbose'])

    # checks the coordinates are valid

    # if there are 2  coordinates
    if modes['object_coords'] is None:
        pass  # no coords specified, let it go as is
    elif len(modes['object_coords']) == 2:

        # checks the validity of those coordinates
        warn_flag = check_coords(modes['object_coords'][1],  # Dec (N/S)
                                 modes['object_coords'][0],  # RA (E/W)
                                 modes)  # supplied separately for compatibility

    else:
        if modes['verbose'] >= 1:
            if modes['object_name'] is None:
                print("Warning: Target: " + str(modes['object_coords']) +
                      " incorrectly specified.  ")
        warn_flag = True
    if warn_flag == True:
        if modes['interactive'] >= 1:
            modes = interactive_get_object(modes)
            modes = get_object(modes)
        else:
            if modes['verbose'] >= 1:
                print("Interactivity mode: " + str(modes['interactive'])+", disabling object tracking.")
                modes['object_coords'] = None
        # there is no land at lat/long (0,0), so it should be ok to assume no
        # observations at this object

    return (modes)


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
    
    warning = ""
    
    while continue_option:
        if "each" in modes["values"]:
            each_status = True
        else:
            each_status = False
        
        dict_set=gen_channels_dict(modes,dict_lists)
        
        if modes['interactive'] == 3:
            menu_choice = gui_set_values(modes, dict_set, each_status, warning)
        else:
            menu_choice = cli_set_values(modes, dict_set, each_status, warning)
            
            
        if "0" == menu_choice:
            continue_option=False # finish the loop
        
        # if it's a single value
        elif menu_choice in list_all:
            process_single_values_menu(menu_choice, modes, dict_lists)
            
            
        # if a group value
        elif menu_choice in dict_lists:
            process_group_values_menu(menu_choice, modes, dict_lists)
            
            
        # to toggle the overlay/separate plots
        elif menu_choice == "each":
            
            if each_status:
                modes["values"].remove("each")
            else:
                modes["values"].append("each")
     
        # if nonse
        else:
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."

def cli_set_values(modes, dict_set, each_status, warning = ""):

    menu_choice = ''
    
    print(("""CHANNEL SELECTION MENU
  
Linear Polarisations (to Toggle all enter "linear")
  xx - Linear response. Currently: {0}
  xy - Cross-channel. Currently: {1}
  yy - Linear response. Currently: {2}
  
Stokes Parameters (to Toggle all enter "stokes")
  U - Polarisation angle. Currently: {3}
  V - Circular polarisation. Currently: {4}
  I - Intensity: Currently. {5}
  Q - Linear polarisation. Currently: {6}
  
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
    
    # if the warning isn't blank
    if warning != "":
        # prints the warning
        print(warning + '\n')

    menu_choice=raw_input("Please enter your (case sensitive) selection to toggle the option on the menu above:\t")
    
    return(menu_choice)


def gui_set_values(modes, dict_set, each_status, warning = ""):
    #TODO: Work out a way to stop this being so hard-coded
    menu_choice = ''
        
    # Creates an interactive window
    root = tk.Tk()
    
    # sets up a variable that will eventually set the output
    var = tk.StringVar()
    
        # if the title isn't blank
    menu_title = "CHANNEL SELECTION MENU"
    # prints the title as a label
    root.title(menu_title)
    title = tk.Label(root,text=menu_title)
    title.pack()    
    
    boldFont = tkFont.Font (weight = "bold")
    
    # creates a button to toggle all linear polarisations
    linear_button=tk.Button(root, text="Linear Polarisations (click to Toggle all)", 
                          command=lambda:close_and_value(root,var,'linear'),
                          font=boldFont)
    linear_button.pack()
    
    
        # if the title isn't blank
    if warning !="":
        # prints the warning as a label
        warning_label = tk.Label(root,text=warning,fg="red")
        warning_label.pack()
    
    # creates a button to toggle xx linear polarisations
    xx_text=("xx - Linear response. Currently: {0}").format(gen_plotting_boolean(dict_set['xx']))
    xx_button=tk.Button(root, text=xx_text, 
                          command=lambda:close_and_value(root,var,'xx'))
    xx_button.pack()
    
    # creates a button to toggle xy linear polarisations
    xy_text=("xy - cross-channel. Currently: {0}").format(gen_plotting_boolean(dict_set['xy']))
    xy_button=tk.Button(root, text=xy_text, 
                          command=lambda:close_and_value(root,var,'xy'))
    xy_button.pack()  
    
    # creates a button to toggle yy linear polarisations
    yy_text=("yy - Linear response. Currently: {0}").format(gen_plotting_boolean(dict_set['yy']))
    yy_button=tk.Button(root, text=yy_text, 
                          command=lambda:close_and_value(root,var,'yy'))
    yy_button.pack()    
    
    # creates a button to toggle all Stokes Parameters
    stokes_button=tk.Button(root, text="Stokes Parameters (click to Toggle all)", 
                          command=lambda:close_and_value(root,var,'stokes'),
                          font=boldFont)
    stokes_button.pack()
    
    # creates a button to toggle Stokes U Parameter
    U_text=("U - Polarisation angle. Currently: {0}").format(gen_plotting_boolean(dict_set['U']))
    U_button=tk.Button(root, text=U_text, 
                          command=lambda:close_and_value(root,var,'U'))
    U_button.pack()    
    
    # creates a button to toggle Stokes V Parameter
    V_text=("V - Circular polarisation. Currently: {0}").format(gen_plotting_boolean(dict_set['V']))
    V_button=tk.Button(root, text=V_text, 
                          command=lambda:close_and_value(root,var,'V'))
    V_button.pack()    
    
    # creates a button to toggle Stokes I Parameter
    I_text=("I - Intensity: Currently. Currently: {0}").format(gen_plotting_boolean(dict_set['I']))
    I_button=tk.Button(root, text=I_text, 
                          command=lambda:close_and_value(root,var,'I'))
    I_button.pack()    
    
    # creates a button to toggle Stokes Q Parameter
    Q_text=("Q - Linear polarisation. Currently: {0}").format(gen_plotting_boolean(dict_set['Q']))
    Q_button=tk.Button(root, text=Q_text, 
                          command=lambda:close_and_value(root,var,'Q'))
    Q_button.pack()    
    
    # creates a button to toggle all Parameters
    all_button=tk.Button(root, text="Click to toggle all channels simultaneously", 
                          command=lambda:close_and_value(root,var,'all'),
                          font=boldFont)
    all_button.pack()
    
    overlay_text="Channels are currently plotted {0} one another".format(gen_overlay_boolean(each_status))
    overlay_label = tk.Label(root,text=overlay_text)
    overlay_label.pack()    
    
    # creates a button to toggle all Overlay
    overlay_button_text="Click to toggle to plotting {0} one another".format(gen_overlay_boolean(not each_status))
    overlay_button=tk.Button(root, text=overlay_button_text, 
                          command=lambda:close_and_value(root,var,'each'),
                          font=boldFont)
    overlay_button.pack()
    
    
    exit_prompt="Return to previous menu"
    exit_value='0'
     
    # and creates a corresponding button
    exit_button=tk.Button(root, text=exit_prompt, 
                          command=lambda:close_and_value(root,var,exit_value))
    exit_button.pack()
    
    # runs the mainloop
    root.mainloop()
    
    # creates the output variable
    menu_choice=var.get()
    
    return(menu_choice)
    
    
def process_single_values_menu(menu_choice, modes, dict_lists):
    """
    this function responds when a single channel value is set in the interactive
    mode.  It toggles the channel on or off, and if the channel is part of a 
    group that is set, the group is toggled off and the remaining channels in 
    the group are toggled on.
    """
    relevant_group=False
    
    # if the chosen option is currently on, then turn it off
    if menu_choice in modes["values"]:
        modes["values"].remove(menu_choice)
    
    
    # if any of the groups are set
    elif any(group_list in modes["values"] for group_list in dict_lists):
        
        # go through the groups
        for group_list in dict_lists:
            # if a group is set and applies to the menu choice
            if group_list in modes["values"] and menu_choice in dict_lists[group_list]:
                # set the flag indicating that the group was relevant
                relevant_group=True

                # remove the group
                modes["values"].remove(group_list)
                

                
                # create a list of the remaining elements of that collective
                new_list=list(dict_lists[group_list])# makes a copy
                new_list.remove(menu_choice)
                
                # and set them to on
                for channel in new_list:
                    if channel not in modes["values"]:
                        modes["values"].append(channel)
    elif False== relevant_group: # was not in a group or single setting
        modes["values"].append(menu_choice) # toggle it on


def process_group_values_menu(menu_choice, modes, dict_lists):
    """
    this function responds when a group channel value is set in the interactive
    mode.  If all of the channels in the group are on, it toggles them off,
    otherwise it toggles the channels on.
    """
    # if the menu choice is all, toggle on if any are off
  
    dict_set=gen_channels_dict(modes,dict_lists)
    
    # always drop the groups and to be replaced with individual flags
    for group in dict_lists:
        if group in modes["values"]:
            modes["values"].remove(group)
    
    # always clear out the channels to simplify later logic
    for channel in dict_lists["all"]:
        if channel in modes["values"]:
            modes["values"].remove(channel)


    small_dict=dict((k, dict_set[k]) for k in (dict_lists[menu_choice]))
    # if they're all on
    if all(set_value for set_value in small_dict.values()):
        # go through the list
        for channel in dict_lists[menu_choice]:
            # and turn them off
            dict_set[channel] = False
    else:# at least some are off
        # go through the list
         for channel in dict_lists[menu_choice]:
            # and turn them on
            dict_set[channel] = True
       

    # goes through the modified dictionary
    for channel in dict_set:
        # checks if the flag is set in the dictionary
        if dict_set[channel]:
            # adds it to the modes variable
            modes["values"].append(channel)
            
        

    
    
    
def set_file_io_options(modes, model_df, scope_df):
    """
    This function modifies the File I/O options in the modes
    """
    menu_choice = "X"
    continue_option=True
    
    warning = ""
    # menu_options=range(0,num_options)
    while continue_option:
        # checks if data file output is requested
        file_status = "file" in modes["plots"]
        
        # sets up the menu options for cli or gui use
        menu_title ="FILE I/O MENU"
         
        # creates a list of menu items
        menu_list = []
                
        # each menu item has an option title.
        # status can be blank, a function or constant 
      
        opt_name = {"option":"Set Input Model File"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Set Input Scope File"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Set Output File Type"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Set Output File Directory"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Toggle Output data file.",
                  "status":(gen_use_boolean(file_status))}
        menu_list.append(opt_name)
      
          
        # Runs with GUI or CLI depending on mode.
        if modes['interactive']==3:
            menu_choice = gui_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning = warning)  
            
        if "0" == menu_choice:
            continue_option=False # finish the loop
        
        elif "1" == menu_choice:
            model_df = set_in_file(modes, "model", model_df)
            
        elif "2" == menu_choice:
            scope_df = set_in_file(modes, "scope", scope_df)
                        
        elif "3" == menu_choice:
            set_out_file_type(modes)
               
        elif "4" == menu_choice:
            # sets up the output directory based on the input
            set_out_dir(modes)
               
        elif "5" == menu_choice:
            if file_status:
                modes['plots'].remove("file")
            else:
                modes['plots'].append("file")
            
        else:
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."
    
    return (model_df, scope_df)
            
def set_in_file(modes, name, in_df):
    """
    This function reads in a new file specified by the user
    """
    out_df = in_df
    dir_file_name="in_file_"+name
    
    
    continue_option=True
    # menu_options=range(0,num_options)
    warning = ""
    
    while continue_option:
        # sets up the menu options for cli or gui use
        menu_title ="SELECT " + name.upper() + "FILE NAME"
        desc_text = "Use this menu to select a file for "+name
        menu_prompt = "Please enter the file name you want to use for "+name
        menu_status = str(modes[dir_file_name])
        if modes['interactive']==3:
            chosen_file_name = gui_entry(menu_title, menu_status, menu_prompt,
                                 desc_text, exit_prompt="", out_type="file_in", 
                                 warning=warning, literal_zero=False)
        else:
            chosen_file_name = cli_entry(menu_title, menu_status, menu_prompt, 
                                 desc_text, exit_prompt="", out_type="file_in", 
                                 warning=warning, literal_zero=False)
        if chosen_file_name == '0':
            continue_option=False

        elif chosen_file_name != modes[dir_file_name]: # if the user has selected anew
            try:
                out_df = read_var_file(chosen_file_name, modes)
                modes[dir_file_name] = chosen_file_name

            except IOError:
                warning = "Warning, unable to read file " + chosen_file_name + ", returning original data"
        else:
            pass # file remains the same
            # modes[dir_file_name]=chosen_file_name

 
    return(out_df)
    

def set_out_file_type(modes):
    """
    This function allows the user to choose the file type for output data
    """

    menu_choice = "X"
    continue_option=True
    # menu_options=range(0,num_options)
    
    warning = ""
    
    while continue_option:

        # sets up the menu options for cli or gui use
        menu_title ="OUTPUT FILE TYPE MENU"
         
        # creates a list of menu items
        menu_list = []
                
        # each menu item has an option title.
        # status can be blank, a function or constant 
        opt_name = {"option":".png"}
        menu_list.append(opt_name)
        
        opt_name = {"option":".gif"}
        menu_list.append(opt_name)
        
        opt_name = {"option":".jpeg"}
        menu_list.append(opt_name)
        
        opt_name = {"option":".tiff"}
        menu_list.append(opt_name)
        
        opt_name = {"option":".sgi"}
        menu_list.append(opt_name)
        
        opt_name = {"option":".bmp"}
        menu_list.append(opt_name)
        
        opt_name = {"option":".raw"}
        menu_list.append(opt_name)
        
        opt_name = {"option":".rgba"}
        menu_list.append(opt_name)
        
        opt_name = {"option":".html"}
        menu_list.append(opt_name)
        
        # determines the currently selected graphics format
        menu_status=modes['image_type']
        
        # Runs with GUI or CLI depending on mode.
        if modes['interactive']==3:
            menu_choice = gui_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   menu_status=menu_status,
                                   warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   menu_status=menu_status,
                                   warning = warning)  
            
            
        if "0" == menu_choice:
            continue_option=False # finish the loop
        
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
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."

def set_frequency_options(modes):
    """
    This function allows the user to select frequencies to plot
    """
    menu_choice = "X"
    continue_option=True
    # menu_options=range(0,num_options)
    
    warning = ""
    
    while continue_option:
        # sets up the menu options for cli or gui use
        menu_title ="FREQUENCY SETTINGS MENU"
         
        # creates a list of menu items
        menu_list = []
                
        # each menu item has an option title.
        # status can be blank, a function or constant 
      
        opt_name = {"option":"Set frequencies individually"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Set frequency by file"}
        menu_list.append(opt_name)
        

        # Runs with GUI or CLI depending on mode.
        if modes['interactive']==3:
            menu_choice = gui_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning = warning)  
            
            
        if "0" == menu_choice:
            continue_option=False # finish the loop
        
        elif "1" == menu_choice:
            set_freq(modes)
            
        elif "2" == menu_choice:
            set_freq_file(modes)
                        

        else:
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."

def set_freq(modes):
    """
    This function allows the user to manually add frequencies to the list of
    frequencies to be plotted
    """


    menu_choice = "X"
    continue_option=True
    # menu_options=range(0,num_options)
    
    warning = ""
    
    while continue_option:
        
        # sets up the menu options for cli or gui use
        menu_list=[]
        menu_title = "FREQUENCY ENTRY MENU"
        menu_status = " "
        
        # if the specified frequency list only includes the default
        freq_status = (len(modes["freq"])==1) and (0.0 in modes["freq"])
            
        if freq_status:
            status_prompt = "No frequencies specified, plotting all."
        else:
            status_prompt = "Selected frequencies (Hz):\n"
            # iterates over the specified frequencies
            for freq in modes["freq"]:
                # Adds them to the "current status" input
                menu_status = menu_status+str(freq)
                # if it's not the last item in the list
                if modes['freq'].index(freq) < (len(modes['freq'])-1):
                    # appends a comma and a space
                    menu_status = menu_status+", "
                    
        # adds options to the menu
        opt_name = {"option":"Clear frequency selection (all frequencies plotted)"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Add new frequencies to plotting list"}
        menu_list.append(opt_name)
        
        #adds a prompt
        menu_prompt = "Please enter your selection from the menu above:\t"        

        # Runs with GUI or CLI depending on mode.
        if modes['interactive']==3:
            menu_choice = gui_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   menu_prompt=menu_prompt, 
                                   status_prompt=status_prompt,
                                   warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   menu_prompt=menu_prompt, 
                                   status_prompt=status_prompt,
                                   warning = warning)  

            
        if "0" == menu_choice:
            continue_option=False # finish the loop
        
        elif "1" == menu_choice:
            # resets to default
            modes["freq"]=[0.0]
            
        elif "2" == menu_choice:
            # calls the frequency entering function
            enter_freq(modes)       

        else:
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."

def enter_freq(modes):

    continue_option = True
        
    while continue_option:
        # sets up the menu options for cli or gui use
        menu_title ="FREQUENCY SELECTION MENU"
        desc_text = "At this screen you may Enter a file name in which frequencies may be found"
        menu_prompt = "Please enter the next frequency in Hz."
        menu_status = " "
        
        # if the specified frequency list only includes the default
        freq_status = (len(modes["freq"])==1) and (0.0 in modes["freq"])
            
        if freq_status:
            status_prompt = "No frequencies specified, plotting all."
        else:
            status_prompt = "Selected frequencies (Hz):\n"
            # iterates over the specified frequencies
            for freq in modes["freq"]:
                # Adds them to the "current status" input
                menu_status = menu_status+str(freq)
                # if it's not the last item in the list
                if modes['freq'].index(freq) < (len(modes['freq'])-1):
                    # appends a comma and a space
                    menu_status = menu_status+", "
        
        if modes['interactive']==3:
            exit_prompt = "Click to stop entering frequencies."
            input_freq = gui_entry(menu_title, menu_status, menu_prompt,
                                 desc_text, exit_prompt, out_type="float", 
                                 warning="", literal_zero=False, 
                                 status_prompt=status_prompt)
        else:
            exit_prompt = "Enter \"0\" to stop entering frequencies."
            input_freq = cli_entry(menu_title, menu_status, menu_prompt, 
                                 desc_text, exit_prompt, out_type="float", 
                                 warning="", literal_zero=False, 
                                 status_prompt=status_prompt)
        if input_freq == '0':
            continue_option=False

        else:
            modes["freq"].append(input_freq)

        if (len(modes["freq"])>1) and (0.0 in modes["freq"]):
            modes["freq"].remove(0.0)    


def set_freq_file(modes):
    """
    This function allows the user to input the name of a csv file containing 
    the frequencies to be filtered
    """
    

    
    continue_option=True
    # menu_options=range(0,num_options)
    
    while continue_option:
        # sets up the menu options for cli or gui use
        menu_title ="FREQUENCY FILE SELECTION MENU"
        desc_text = "At this screen you may Enter a file name in which frequencies may be found"
        menu_prompt = "Please enter the file name you want to use for frequencies to plot"
        menu_status = str(modes["freq_file"])
        if modes['interactive']==3:
            chosen_file_name = gui_entry(menu_title, menu_status, menu_prompt,
                                 desc_text, exit_prompt="", out_type="file_in", 
                                 warning="", literal_zero=False)
        else:
            chosen_file_name = cli_entry(menu_title, menu_status, menu_prompt, 
                                 desc_text, exit_prompt="", out_type="file_in", 
                                 warning="", literal_zero=False)
        if chosen_file_name == '0':
            continue_option=False

        else:
            modes["freq_file"] = chosen_file_name    
            if chosen_file_name != "":
                # clears the manual entry of frequencies if a file has been selected
                modes["freq"]=[0.0]

        

def set_other_options(modes):
    """
    This function allows the user to set a number of miscellaneous options
    """
    menu_choice = "X"
    continue_option=True
    # menu_options=range(0,num_options)
    
    warning = ""
    
    while continue_option:
        # sets up the menu options for cli or gui use
        menu_title = "MISCELLANEOUS SETTINGS MENU"
         
        # creates a list of menu items
        menu_list = []
                
        # each menu item has an option title.
        # status can be blank, a function or constant 
      
        opt_name = {"option": "Set time offset between scope and frequency"}
        menu_list.append(opt_name)
        
        opt_name = {"option": "Set graph and file title prefix"}
        menu_list.append(opt_name)
        
        opt_name = {"option": "Set difference mode"}
        menu_list.append(opt_name)
        
        opt_name = {"option": "Toggle log/linear plotting.",
                    "status": gen_scale_name(modes['scale'])}
        menu_list.append(opt_name)

        opt_name = {"option": "Toggle percentage plotting.",
                    "status": gen_scale_percent(modes['scale'])}
        menu_list.append(opt_name)

        opt_name = {"option": "Set Image Size"}
        menu_list.append(opt_name)

        opt_name = {"option": "Set Image Resolution"}
        menu_list.append(opt_name)
        
        opt_name = {"option": "Set Colourschemes"}
        menu_list.append(opt_name)
        
        # Runs with GUI or CLI depending on mode.
        if modes['interactive'] == 3:
            menu_choice = gui_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   warning=warning)
            
        if "0" == menu_choice:
            continue_option=False # finish the loop
        
        elif "1" == menu_choice:
            set_offset(modes)
            
        elif "2" == menu_choice:
            set_title(modes)
                        
        elif "3" == menu_choice:
            set_diff(modes)
        elif "4" == menu_choice:
            if "linear" in modes['scale']:
                try:
                    modes['scale'].remove("linear")
                except ValueError:
                    pass  # if it's not there, no worries!

                modes['scale'].append("log")
            else:
                try:
                    modes['scale'].remove("log")
                except ValueError:
                    pass  # if it's not there, no worries!

                modes['scale'].append("linear")
        elif "5" == menu_choice:
            if "percent" in modes['scale']:
                try:
                    modes['scale'].remove("percent")
                except ValueError:
                    pass  # if it's not there, no worries!

            else:
                modes['scale'].append("percent")
                        
        elif "6" == menu_choice:
            set_in_coords(modes,"size")
                        
        elif "7" == menu_choice:
            set_dpi(modes)
                
        elif "8" == menu_choice:
            set_colourscheme(modes)
               
        else:
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."


def set_offset(modes):
    """
    This function allows the user to set the number of seconds of offset that 
    exists between the start time of the scope and model observations
    """
    continue_option=True
    # menu_options=range(0,num_options)
    
    while continue_option:
        # sets up the menu options for cli or gui use
        menu_title ="OFFSET MENU"
        desc_text = """Offset is the number of seconds between the start time of the scope and 
      model observations.  Offset is subtracted from the scope timestamps to
      allow the scope and model observations to match.
      
      Offsets MUST be an integer number of seconds."""
        menu_prompt = "Please Enter the offset time in seconds"
        menu_status = str(modes['offset'])
        if modes['interactive']==3:
            str_offset = gui_entry(menu_title, menu_status, menu_prompt,
                                     desc_text, exit_prompt="", out_type="int",
                                     warning="", literal_zero=True)
        else:
            str_offset = cli_entry(menu_title, menu_status, menu_prompt,
                                     desc_text, exit_prompt="", out_type="int",
                                     warning="", literal_zero=True)
        if str_offset == 'X':
            continue_option=False
        else:
            modes["offset"]=str_offset

def set_dpi(modes):
    """
    This function allows the user to set the number of seconds of offset that 
    exists between the start time of the scope and model observations
    """
    continue_option=True
    # menu_options=range(0,num_options)
    
    while continue_option:
        # sets up the menu options for cli or gui use
        menu_title ="RESOLUTION MENU"
        desc_text = """Resolution is the pixel scaling on the output image. It is measured in Dots Per Inch (DPI).
        Not all devices will respect the assigned pixel scaling, but it allows a user to create an image optimised
        for a particular resolution and size."""
        menu_prompt = "Please Enter the resolution in DPI"
        menu_status = str(modes['dpi'])
        if modes['interactive']==3:
            str_dpi = gui_entry(menu_title, menu_status, menu_prompt,
                                     desc_text, exit_prompt="", out_type="float",
                                     warning="", literal_zero=True)
        else:
            str_dpi = cli_entry(menu_title, menu_status, menu_prompt,
                                     desc_text, exit_prompt="", out_type="float",
                                     warning="", literal_zero=True)
        if str_dpi == 'X':
            continue_option=False
        else:
            modes["dpi"]=str_dpi
        


def set_title(modes):
    """
    This function allows the user to set the titles for graphs and files
    """
    continue_option=True
    # menu_options=range(0,num_options)
    
    while continue_option:
        # sets up the menu options for cli or gui use
        menu_title = "GRAPH AND FILE TITLE PREFIX MENU"
        desc_text = """The prefix is used on graph titles and with underscores for file names."""
        menu_prompt = "Enter a title prefix for the graphs"
        menu_status = str(modes['title'])
        if modes['interactive']==3:
            in_title = gui_entry(menu_title, menu_status, menu_prompt,
                                 desc_text, exit_prompt="", out_type="str", 
                                 warning="", literal_zero=False)
        else:
            in_title = cli_entry(menu_title, menu_status, menu_prompt, 
                                 desc_text, exit_prompt="", out_type="str", 
                                 warning="", literal_zero=False)
        if in_title == '0':
            continue_option=False
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
    # menu_options=range(0,num_options)
    
    warning = ""
    
    while continue_option:

        # sets up the menu options for cli or gui use
        menu_title ="DIFFERENCE MODE MENU"
         
        # creates a list of menu items
        menu_list = []
                
        # each menu item has an option title.
        # status can be blank, a function or constant 
        opt_name = {"option":"Subtraction (model-scope)"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Division (model/scope)"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"Inverse Division (scope/model)"}
        menu_list.append(opt_name)
        
              
        menu_status=gen_diff_name(modes["diff"])
        
        # Runs with GUI or CLI depending on mode.
        if modes['interactive']==3:
            menu_choice = gui_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   menu_status=menu_status,
                                   warning = warning)

        else:    
            menu_choice = cli_menu(menu_title=menu_title,
                                   menu_list=menu_list,
                                   menu_status=menu_status,
                                   warning = warning)  
            
        if "0" == menu_choice:
            continue_option=False # finish the loop
        
        elif "1" == menu_choice:
            modes["diff"]="sub"
            
        elif "2" == menu_choice:
            modes["diff"]="div"
                        
        elif "3" == menu_choice:
            modes["diff"]="idiv"
               

        else:
            warning = "Input: '"+str(menu_choice)+"' not valid or not implemented."


    
def interactive_get_object(modes):
    '''
    This function prompts the user to specify the coordinates of the Target to 
    be used and modifies the modes dictionary to correspond to the new setting.
    '''

    warning = ""


    choice_continue = True
    while choice_continue:

        # sets up the menu options for cli or gui use
        menu_title ="SELECT TARGET MENU"
         
        # creates a list of menu items
        menu_list = []
        menu_prompt = "Please select how you want to specify the object"
        
        opt_name = {"option":"By Name"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"By Coordinates"}
        menu_list.append(opt_name)        
        
        opt_name = {"option":"Clear target"}
        menu_list.append(opt_name)

        # constructs the menu status
        menu_status = ""

        # moves on to object
        menu_status = menu_status + "\nCurrent Object Name:"
        if modes['object_name'] is None:
            menu_status = menu_status + " None Specified\n"
        else:
            menu_status = menu_status + " " + modes['object_name'] + "\n"

        # then object coordinates if specified
        menu_status = menu_status + "Current Object Coordinates:"
        if modes['object_coords'] is None:
            menu_status = menu_status + " None Specified\n"
        else:
            str_object_coords = "\nRA: {0}deg DEC: {1}deg\n".format(
                modes['object_coords'][0],  # RA
                modes['object_coords'][1], )  # Dec
            menu_status = menu_status + str_object_coords

        if modes['interactive'] == 3:
            choice=gui_menu(menu_title = menu_title, menu_list=menu_list, 
                            menu_status=menu_status, menu_prompt=menu_prompt,
                            warning=warning)
        else:
            choice=cli_menu(menu_title = menu_title, menu_list=menu_list, 
                            menu_status=menu_status, menu_prompt=menu_prompt,
                            warning=warning)
        
        if choice == '1':
            name=set_name(modes,"object_name")
            coord=set_coords(name)
            if coord is None:
                name = None
            modes['object_name'] = name
            modes['object_coords'] = coord
                            
        elif choice == '2':

            coord = set_in_coords(modes,"object")
            if coord != modes['object_coords']:
                # if the coordinates have been changed
                modes['object_coords'] = coord
                modes['object_name'] = None  # wipes the name clean
        
        elif choice == '3':
            modes['object_coords'] = None
        
        elif choice == '0':
            choice_continue = False  # ends the loop
        
        else:
            warning = "Warning: Incorrect option '{}' specified!".format(choice)
            
    return(modes)


def interactive_get_location(modes):
    '''
    This function prompts the user to specify the location of the station to be
    used and modifies the modes dictionary to correspond to the new setting.
    '''

    warning = ""
    
    choice_continue = True
    while choice_continue:

        # sets up the menu options for cli or gui use
        menu_title ="SELECT STATION MENU"
         
        # creates a list of menu items
        menu_list = []
        menu_prompt = "Please select how you want to specify the station"
        
        opt_name = {"option":"By Name"}
        menu_list.append(opt_name)
        
        opt_name = {"option":"By Coordinates"}
        menu_list.append(opt_name)        
        
        opt_name = {"option":"Clear station"}
        menu_list.append(opt_name)

        # constructs the menu status
        menu_status = ""

        # starts with location name
        menu_status = menu_status + "Current Location Name:"
        if modes['location_name'] is None:
            menu_status = menu_status + " None Specified\n"
        else:
            menu_status = menu_status + " " + modes['location_name'] + '\n'

        # then location coordinates if specified
        menu_status = menu_status + "Current Location Coordinates:"
        if modes['location_coords'] is None:
            menu_status = menu_status + " None Specified\n"
        else:
            str_location_coords = "\nLat: {0}deg Long: {1}deg Elev: {2}m\n".format(
                modes['location_coords'][0],  # latitude
                modes['location_coords'][1],  # longitude
                modes['location_coords'][2], )  # height,)
            menu_status = menu_status + str_location_coords


        menu_desc="Please specify the location of the station manually"

        
        if modes['interactive'] == 3:
            choice=gui_menu(menu_title = menu_title, menu_list=menu_list,
                            menu_status=menu_status, warning = warning,
                            menu_prompt=menu_prompt, desc_text=menu_desc)
        else:
            choice=cli_menu(menu_title = menu_title, menu_list=menu_list,
                            menu_status=menu_status, warning = warning,
                            menu_prompt=menu_prompt, desc_text=menu_desc)
        
        if choice == '1':
            name=set_name(modes,"location_name")
            coord=set_coords(name)
            if coord is None:
                name = None
            modes['location_name']=name
            modes['location_coords']=coord
                
            
            
        elif choice == '2':

            coord = set_in_coords(modes,"location")
            if coord != modes['location_coords']:
                # if the coordinates have been changed
                modes['location_coords'] = coord
                modes['location_name'] = None  # wipes the name clean


        elif choice == '3':
            if modes['verbose'] >=1:
                #clear the station
                modes['location_coords']=None
        
        elif choice == '0':
            choice_continue = False
        else:
            warning = "Warning: Incorrect option '{}' specified!".format(choice)
            choice_continue = True
            
    return(modes)




def set_name(modes, to_name):
    """
    This function allows the user to set the target or station name
    """
    continue_option=True
    # menu_options=range(0,num_options)
    pretty_name=gen_pretty_name(to_name)
    
    out_name=modes[to_name]
    
    example = ""
    if to_name == "location_name":
        example = " e.g. IE613"
    if to_name == "object_name":
        example = " e.g. CasA"
    
    warning = ""
    
    while continue_option:
        # sets up the menu options for cli or gui use
        menu_title = pretty_name.upper()+" MENU"
        desc_text = "Use this menu to enter the "+pretty_name+" to enable automatic calculation of coordinates."
        menu_prompt = "Please Enter the "+pretty_name+example+" below."
        menu_status = out_name
        if modes['interactive']==3:
            in_name = gui_entry(menu_title, menu_status, menu_prompt,
                                 desc_text, exit_prompt="", out_type="str", 
                                 warning=warning, literal_zero=False)
        else:
            in_name = cli_entry(menu_title, menu_status, menu_prompt, 
                                 desc_text, exit_prompt="", out_type="str", 
                                 warning=warning, literal_zero=False)
        if in_name == '0':
            continue_option=False
        elif in_name in ['',None]:
            out_name = None
        else:
            if set_coords(in_name) is None:
                warning="Name: '{}' is not known.  Please try again.".format(in_name)
            else:
                out_name=in_name
            
    return(out_name)


def set_in_coords(modes,coord_type=""):
    # creates a blank list.
    if coord_type == 'object':
        out_coords = modes['object_coords']
    elif coord_type == "location":
        out_coords=modes['location_coords']
    elif coord_type == 'size':
        out_coords = modes['image_size']
    else:
        out_coords = None

    warning=""
    menu_title = ""
    menu_prompt = ""
    menu_status = ""
    coords = []
    status_prompt = ""

    # out_coords = None  # in case the conditions are missed

    continue_option = True



    while continue_option:
        # sets the menu variables that will operate the numerical entry system
        
        # sets them for the target object
        if coord_type == "object":
            menu_title = "Target Object Coordinate Entry Menu"
            # then location coordinates if specified
            status_prompt = "Current Target Coordinates:"
            menu_prompt = "Please enter the coordinates of the target."
            if out_coords is None:
                menu_status = "None Specified"
            else:
                menu_status = "\nRA: {0}deg DEC: {1}deg\n".format(
                    out_coords[0],  # RA
                    out_coords[1])  # Dec
            coords = ["Right Ascension", "Declination"]

            ns = 1
            ew = 0
        
        # sets them for the oberving location
        elif coord_type == "location":
            menu_title = "Observing Station Coordinate Entry Menu"
            # then location coordinates if specified
            status_prompt = "Current Location Coordinates:"
            menu_prompt = "Please enter the coordinates of the station below."
            if out_coords is None:
                menu_status = "None Specified"
            else:
                menu_status = "Lat: {0}deg Long: {1}deg Elev: {2}m\n".format(
                    out_coords[0],  # latitude
                    out_coords[1],  # longitude
                    out_coords[2])  # height,)

            coords = ["Latitude", "Longitude", "Height"]
            ns = 0
            ew = 1
        
        # sets them for image size
        elif coord_type == "size":
            menu_title = "Output Image Size Selection Menu"
            # then location coordinates if specified
            status_prompt = "Current Image Size:"
            menu_prompt = "Please enter the Image Size in inches"
            if out_coords is None:
                menu_status = "None Specified"
            else:
                menu_status = "\nHeight: {0}in Width: {1}in\n".format(
                    out_coords[0],  # Height
                    out_coords[1])  # Width
            coords = ["Height", "Width"]

        else: # this shouldn't arise, but for safety
            warning = "Unknown menu"

        # runs the entry system for lists of numbers with the variables that have been set
        
        # if the GUI mode is active, uses the GUI coordinates entry menu
        if modes['interactive'] == 3:
            l_coords = gui_coords(menu_title=menu_title, menu_status=menu_status, menu_prompt=menu_prompt,
                                  desc_text="", exit_prompt="", warning=warning, status_prompt=status_prompt,
                                  coord_names=coords)
        # otherwise uses the text entry system
        else:
            l_coords = cli_coords(coords)
            
        # if the user has given the exit option
        if l_coords == 'exit':
            continue_option = False  # end the loop
        
        # if the user has ordered the coordinates to be cleared
        elif l_coords == 'clear':
            out_coords = None  # clears the output

        # if the coordinates are in degrees, checks that they're valid
        elif coord_type in ["object", "location"]:
            coords_warning = check_coords(l_coords[ns],l_coords[ew],modes)
            if coords_warning:
                out_coords = None
            else:
                out_coords = l_coords
        # otherwise just returns the value        
        else:
            out_coords = l_coords

    return (out_coords)

def prep_out_dir(out_dir=None, modes={"verbose":1,"interactive":1, "out_dir":""}):
    '''
    Sets up the output directory based on the inputs.  If there are issues with
    the output directory specified, warns the user and continues by printing 
    the output instead
    '''
    
    #if no directory was specified
    if out_dir == None:
        pass #do nothing - will return None as designed
    
    #if something has been passed in
    else: 
        #if the directory doesn't already exist
        if not os.path.isdir(out_dir):
            #try to make it and any parents needed
            try:
                os.makedirs(out_dir)
            
            #if it's not possible to make that directory
            except OSError:
                if modes['verbose'] >=1:
                    print("WARNING: output directory specified not suitable!")
                if modes['interactive']>=1:
                    set_out_dir(modes)
                else:
                    out_dir = None
    
    return(out_dir)

def set_out_dir(modes):
    """
    This is a function that enables interactive input of the output directory
    """
    out_dir = str(modes['out_dir'])
    
    continue_option=True
    # menu_options=range(0,num_options)
    warning = ""
    
    while continue_option:
        # sets up the menu options for cli or gui use
        menu_title ="SELECT OUTPUT DIRECTORY"
        desc_text = "Use this menu to select directory to place outputs in"
        menu_prompt = "Please enter the directory name you want to use"
        menu_status = out_dir
        if modes['interactive']==3:
            out_dir = gui_entry(menu_title, menu_status, menu_prompt,
                                 desc_text, exit_prompt="", out_type="dir", 
                                 warning=warning, literal_zero=False)
        else:
            out_dir = cli_entry(menu_title, menu_status, menu_prompt, 
                                 desc_text, exit_prompt="", out_type="dir", 
                                 warning=warning, literal_zero=False)
        if out_dir == '0':
            continue_option=False

        else:
            modes['out_dir']=out_dir    

 
   # return(out_dir)



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
    
def gen_ew_boolean(bool_in):
    """
    generates a string which looks better for the status of East/West plots
    """
    out_str = ""
    if bool_in:
        out_str="East/West"
    else:
        out_str="0-360"
    return(out_str)
  
    
def gen_use_boolean(bool_in):
    """
    generates a string which looks better for the status of use
    """
    out_str = ""
    if bool_in:
        out_str="Using"
    else:
        out_str="Not Using"
    return(out_str)

    
def gen_split_boolean(bool_in):
    """
    generates a string which looks better for the status of East/West plots
    """
    out_str = ""
    if bool_in:
        out_str="Splitting"
    else:
        out_str="Not Splitting"
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

def gen_basis_name(abbreviation):
    basis_name = ""
    if "o"==abbreviation:
        basis_name="Overall"
    elif "f"==abbreviation:
        basis_name="Frequency"
    elif "t"==abbreviation:
        basis_name="Time" 
    elif abbreviation in ["","n"]:
        basis_name="None"
    else:
        print("Warning: Unknown basis name used!")
    return (basis_name)

def gen_source_name(abbreviation):
    source_name = ""
    if "b"==abbreviation:
        source_name="Both"
    elif "m"==abbreviation:
        source_name="Model"
    elif "s"==abbreviation:
        source_name="Scope" 
    elif abbreviation in ["","n"]:
        source_name="None"
    else:
        print("Warning: Unknown source name used!")
    return (source_name)

def gen_three_d_name(abbreviation):
    three_d_name=""
    if abbreviation in ["colour","color"]:
        three_d_name="3-D Colour Plots"
    elif "anim" == abbreviation:
        three_d_name="Animated Plots against Time"
    elif "animf" == abbreviation:
        three_d_name="Animated Plots against Frequency"
    elif "contour" == abbreviation:
        three_d_name="3-D Contour Plots"
    else:
        print("Warning: Unknown 3-D name used!")
    return(three_d_name)


def gen_scale_name(scale):
    scale_name=""
    if "log" in scale:
        scale_name="log"
    elif "linear" in scale:
        scale_name="linear"
    else:
        scale_name = "linear"
        print("Warning: Unknown scale name used!")
    return(scale_name)


def gen_scale_percent(scale):
    scale_percent=""
    if "percent" in scale:
        scale_percent="Percentage"

    else:
        scale_percent = "Raw Data"
    return(scale_percent)
            
def gen_channels_dict(modes, dict_lists):
    
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

# looks like this was already done.  Partial version left for records
# def set_loc_options(modes):
#    """
#    This function modifies the observatory location options
#    """
#    menu_choice = "X"
#    continue_option=True
#    # menu_options=range(0,num_options)
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
#        try:# read in the choice as an int
#            menu_choice=int(raw_input("Please enter your selection from the menu above:\t"))
#            
#        except ValueError: # can't be converted to an int
#            print("Warning: invalid menu choice.") # print a warning
#            menu_choice="X" # set the option back to default
#            
#        if "0" == menu_choice:
#            continue_option=False # finish the loop
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
#            print("Input: '"+str(menu_choice)+"' not valid or not implemented.")
