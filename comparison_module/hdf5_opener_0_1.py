#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 14:11:42 2018

@author: creanero
"""

import h5py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from prototype_comparison_module_1d_0_1 import colour_models

def read_OSO_h5 (filename):
    '''
    This function reads in the data from an OSO-supplied HDF5 file and converts#
    it into a data frame. This data is then returned to the calling function
    
    Inputs: file name containing the path to a HDF5 file
    Outputs: Data Frame containing time, frequency, xx, xy and yy values
    
    This function uses slightly crude methods, and probably needs to be 
    updated with a more straightforward conversion from HDF5 to a dataframe
    '''
    #'/home/creanero/outputs/observations/OSO/2018-03-16T11_26_11_acc2bst_rcu5_CasA_dur2587_ct20161220.hdf5'
    #Reads in the designated HDF5 file
    f = h5py.File(filename, 'r')
    
    #Creates lists to hold the contents of the various HDF5 datasets within the
    #file.  These are then merged to form the data frame.
    time_list=[]
    time_diff=[]
    freq_list=[]
    xx_list=[]
    xy_list=[]
    yy_list=[]

    #creates an index for the time stamps
    time_index=0

    #identifies the start time.  Times in HDF5 are stored as floats since the
    #epoch of Jan 01 00:00:00 1970
    min_time=min(list(f["timeaccstart"]))
    
    #Iterates over the time values in the HDF5 file
    for time_val in list(f["timeaccstart"]):
        #(re-)initialises the index for frequencies in the HDF5 file
        freq_index=0
        #Iterates over the frequency values in the HDF5 file
        for freq_val in list(f['frequency']):
            #appends the values from the iterators for Time and Frequency
            time_list.append(time_val)
            time_diff.append(time_val-min_time) #useful for calculations
            freq_list.append(freq_val)
            
            #uses the indices to find the correct values for XX, XY and YY
            xx_list.append(f['XX'][time_index][freq_index])
            xy_list.append(f['XY'][time_index][freq_index])
            yy_list.append(f['YY'][time_index][freq_index])
            
            #increments the indices
            freq_index = freq_index+1
        time_index=time_index+1
    
    #creates the data frame by pasting the lists together    
    scope_df=pd.DataFrame(data={'time':time_list, 'time_diff':time_diff, 
                                'freq':freq_list,
                                'xx':xx_list,'xy':xy_list,'yy':yy_list})
    
    #returns the data frame
    return(scope_df)

def plot_OSO_h5(scope_df,pol_str,plot_type=""):
    '''
    This function plots the contents of an OSO HDF5 file with different titles 
    depending on the plot type argument
    '''
    
    plt.figure()
    plt.tripcolor(scope_df.time_diff,scope_df.freq,abs(scope_df[pol_str]),
                  cmap=plt.get_cmap(colour_models(pol_str)))
    
    if "dirty" == plot_type:
        plot_title = "Plot of "+pol_str+" against time and frequency without cleaning\nDominated by OUTLIERS"
    elif "clean" == plot_type:
        plot_title = "Plot of "+pol_str+" against time and frequency after cleaning"
    else: 
        plot_title = "Plot of "+pol_str+" against time and frequency"
        if "" != plot_type:
            print("WARN: plot type unknown, default used")
        
    plt.title(plot_title)
    plt.xlabel("Time (s) since start time of\n"+time.ctime(min_time))
    plt.ylabel("Frequency (Hz)")
    plt.show()    
    


    
if __name__ == "__main__":
    #prompts the user for the filename
    filename = raw_input("Please enter the filename:\n")
    
    #reads in the 
    scope_df=read_OSO_h5(filename)
    
    #identifies the start time.  Times in HDF5 are stored as floats of seconds 
    #since the epoch of Jan 01 00:00:00 1970
    min_time=min(scope_df.time)    
    
    #plots the xx, xy and yy values 
    plot_OSO_h5(scope_df,'xx','dirty')
    plot_OSO_h5(scope_df,'xy','dirty')
    plot_OSO_h5(scope_df,'yy','dirty')
    
    #identifies and excluedes significant outliers in the dataframe and plots 
    #the remaining values for each of the channels
    clean_df_xx=scope_df[scope_df.xx<np.mean(scope_df.xx)*2]
    plot_OSO_h5(clean_df_xx,'xx','clean')
    
    #xy is complex, so a plot of absolute values is needed
    clean_df_xy=scope_df[abs(scope_df.xy)<np.mean(abs(scope_df.xy))*2]
    plot_OSO_h5(clean_df_xy,'xy','clean')
    
    clean_df_yy=scope_df[scope_df.yy<np.mean(scope_df.yy)*2]
    plot_OSO_h5(clean_df_yy,'yy','clean')
