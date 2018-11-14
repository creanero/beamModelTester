# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 10:48:33 2018

@author: User
"""

#!/usr/bin/python

import Tkinter  as tk

#def sel():
#    selection = "You selected the option " + str(var.get())
#    label.config(text = selection)

def gui_menu(menu_title="", menu_list=[], menu_status="", menu_prompt="",
             exit_prompt=""):
    
    #Creates an interactive window
    root = tk.Tk()
    
    #sets up a variable that will eventually set the output
    var = tk.StringVar()
    
    #if the title isn't blank
    if menu_title!="":
        #prints the title as a label
        title = tk.Label(root,text=menu_title)
        title.pack()    
    
    #if an overall menu status is provided
    if menu_status != "":
        #if it is provided as a function/method
        if callable(menu_status):
            #call it and record its return value in status
            status=("Current: {0}").format(menu_status())
        else:
            #otherwise, return its value
            status=("Current: {0}").format(menu_status)
        #prints the status as a Label
        status_label = tk.Label(root,text=status)
        status_label.pack()    
    
    
    #prints a warning as a label if there's no menu options
    if 0==len(menu_list):
        warning_label = tk.Label(root,text="Menu_empty")
        warning_label.pack() 
    
    #iterates over the menu list
    for i in range(len(menu_list)):
        #creates a menu number
        menu_number = i + 1
        
        #reads in the menu option
        option=menu_list[i]["option"]
        
        #attempts to read the status corresponding to that menu item
        #if the menu item has a status variable
        if ('status' in menu_list[i].keys()):
            #check if it is a function
            if callable(menu_list[i]["status"]):
                #if so, call it and record its return value in status
                status=("(Current: {0})").format(menu_list[i]["status"]())
            else:
                #otherwise, return its value
                status=("(Current: {0})").format(menu_list[i]["status"])
        #if the menu item does not have a status variable
        else:
            #generate an empty string for the status
            status=""
        
        #Createsa string which contains the option and its status
        button_string=("{0} {1}").format(option,status)
        
        #produces a radiobutton for each option
        R=tk.Radiobutton(root, text=button_string, variable=var, value=menu_number)
        R.pack( anchor = W )
    
    #if the exit/up a level prompt is not provided
    if ""==exit_prompt:
        #produces a default prompt
        exit_prompt="Return to previous menu"
    
    #and creates a corresponding radio button
    exit_button=tk.Radiobutton(root, text=exit_prompt, variable=var, value=0)
    exit_button.pack( anchor = W )
 
    #uses a default instruction if no better prompt is given
    if ""==menu_prompt:
        menu_prompt="Please click your selection from the menu above:\t"

    #and prints the instructions as a label   
    prompt = tk.Label(root,text=menu_prompt)
    prompt.pack() 
    
    #creates a "confirm" button which kills root when it is called
    submit=tk.Button(root, text="Click to confirm", command=root.destroy)
    submit.pack()
    
    #runs the mainloop
    root.mainloop()
    
    #creates an ordinary string from the variable
    out_choice=str(var.get())
    
    #returns the choice string.
    return(out_choice)
    
