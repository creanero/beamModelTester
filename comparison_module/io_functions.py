# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 13:43:38 2018

@author: User
"""
import os


    
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


