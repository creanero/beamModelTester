# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 13:43:38 2018

@author: User
"""
import os

def prep_out_dir(out_dir=None, modes={"verbose":1}):
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
                    #print a warning and ask the user for new input
                    out_dir = raw_input("WARNING: output directory not suitable, "
                                       "please enter a new output directory:\n"
                                       "Leave blank for output to screen\n\t")
                    #TODO: Check if this still works after interactive mode
                    #if they leave the input blank, return a Null value
                    if out_dir == '':
                        out_dir = None
                
                    #otherwise try this function again
                    else:
                        out_dir=prep_out_dir(out_dir)
                else:
                    out_dir = None
    
    return(out_dir)
    
def prep_out_file(modes,source="",ind_var="",plot="",dims="",channel="",
                  freq=0.0, plot_name = "",
                  out_type=""):
    '''
    Prepares the output path for a variety of options given input parameters 
    
    '''
    
    #starts the file path by joining the out_dir and title
    out_file_path = os.path.join(modes['out_dir'],modes['title_'])
    
    #adds any non-blank parameters to the end with an underscore
    if plot != "":
        out_file_path= out_file_path + "_" + plot

    if dims != "":
        out_file_path= out_file_path + "_" + dims

    if channel != "":
        out_file_path= out_file_path + "_" + channel
        
    if source != "":
        out_file_path= out_file_path + "_" + source

    if ind_var != "":
        out_file_path= out_file_path + "_" + ind_var

    if plot_name != "":
        out_file_path= out_file_path + "_" + plot_name

    if freq != 0.0:
        out_file_path= out_file_path + "_" + str(freq).replace(".","-")+"Hz"
        
    #sets the file extension based on file type
    if out_type != "":
        if "." not in out_type:
            out_file_path= out_file_path + "." + out_type   
        else:
            out_file_path= out_file_path + out_type 
    return (out_file_path)


