# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 13:51:56 2018

@author: User
"""
import pandas as pd

from graphing_functions import plots_1f
from graphing_functions import plot_diff_values_1f
from graphing_functions import plot_spectra_nf
from graphing_functions import calc_fom_1d
from graphing_functions import calc_fom_nd
from graphing_functions import plot_altaz_values_nf

from appearance_functions import channel_maker
from appearance_functions import gen_pretty_name
from io_functions import prep_out_file

def analysis_1d(merge_df,modes, m_keys):
    '''
    This function carries out all plotting and calculations needed for a 1-d 
    dataset (i.e. one frequency)
    
    Future iterations may include optional arguments to enable selection of the
    plots that are preferred
    '''
  
    print("Carrying out 1-frequency Analysis")
#    if "spectra" in modes["plots"]:
#        #plots the values for each channel
#        plot_values_1f(merge_df, m_keys, modes)
#    
#    if "diff" in modes["plots"]:    
#        #plots the differences in the values
#        plot_diff_values_1f(merge_df, m_keys, modes)
    if "spectra" in modes["plots"]:
        #plots the values for each channel
        plots_1f(merge_df, m_keys, modes,"Time")
        
        
        
    if all(coord in merge_df for coord in ["alt","az","az_ew"]) :
        alt_var = "alt"
        az_var = "az"
        if "stn" in modes["plots"]:
            if all(coord in merge_df \
                   for coord in ["stn_alt","stn_az","stn_az_ew"]):
                alt_var = "stn_"+alt_var
                az_var = "stn_"+az_var           
            else:
                print("Warning: Station coordinates selected but unavailable")
        if "ew" in modes["plots"]:
            az_var=az_var+"_ew"
        if "alt" in modes["plots"]:
            plots_1f(merge_df, m_keys, modes,alt_var)
        if "az" in  modes["plots"]:
            plots_1f(merge_df, m_keys, modes,az_var)
    else:
        print("Warning: Horizontal coordinates selected but unavailable")
            
    if "corr" in modes["plots"]:
        #calculates the pearson correlation coefficient between scope and model
        corrs=calc_fom_1d(merge_df, m_keys,"corr")
        
        for i in range(len(m_keys)):
            out_str=("The "+str(m_keys[i])+"-channel correlation is "+str(corrs[i]))
            if modes['out_dir'] == None:
                print(out_str)
            else:

                #creates an output-friendly string for the channel
                str_channel = channel_maker(m_keys,modes)
        
                        
                plt_file=prep_out_file(modes,plot="corr", dims="1d",
                                       channel=str_channel,
                                       out_type="txt")
                out_file=open(plt_file,'a')
                out_file.write(out_str)
                out_file.close()
                
        print("\n")
        
    if "rmse" in modes["plots"]:        
        #calculates the root mean squared error between scope and model
        rmses=calc_fom_1d(merge_df, m_keys,"rmse")
        for i in range(len(m_keys)):
            out_str=("The "+str(m_keys[i])+"-channel RMSE is "+str(rmses[i]))
            if modes['out_dir'] == None:
                print(out_str)
            else:
                #creates an output-friendly string for the channel
                str_channel = channel_maker(m_keys,modes)
        
        
                plt_file=prep_out_file(modes,plot="rmse", dims="1d",
                                       channel=str_channel,
                                       out_type="txt")
                out_file=open(plt_file,'a')
                out_file.write(out_str)
                out_file.close()    
    
def analysis_nd(merge_df,modes, m_keys):
    '''
    This function carries out all plotting and calculations needed for a n-d 
    dataset (i.e. multiple frequencies)
    
    Future iterations may include optional arguments to enable selection of the
    plots that are preferred
    '''
    
    print("Carrying out multi-frequency Analysis")
  
    if "spectra" in modes["plots"]:
        plot_spectra_nf(merge_df, m_keys, modes)
    
    if any (plot in modes["plots"] for plot in ["alt","az","ew"]):
        if all(coord in merge_df for coord in ["alt","az","az_ew"]) :
#            try:
#                plot_altaz_values_nf(merge_df, m_keys, modes)
#            except NameError:
#                print("Error: unable to plot altaz values")
            plot_altaz_values_nf(merge_df, m_keys, modes)
            
        else:
            print("Warning: Alt-Azimuth plotting selected, but not available!")
    
    #calculates the figures of merit at each independent variable 
    #return values are stored as possible future outputs
    ind_var = ["Freq", "Time"]
    ind_dfs = {}
    for ind in ind_var:        
        n_ind=merge_df[ind].unique()
        
        foms=[]
        if "corr" in modes["plots"]:
            foms.append("corr")
        if "rmse" in modes["plots"]:
            foms.append("rmse")

        for fom in foms:
            ind_df=pd.DataFrame(data={ind:n_ind})
            n_foms=calc_fom_nd(merge_df,ind, m_keys, modes, fom)
            for key in m_keys:
                ind_df[key+'_'+fom]=n_foms[m_keys.index(key)]
            ind_dfs[ind+"_"+fom]=ind_df
                    
            #calculates the overall figure of merit between scope and model
            fom_1=calc_fom_1d(merge_df, m_keys,fom)
            #prints that coefficient for each key and correlation
            for i in range(len(m_keys)):
                out_str=("The "+str(m_keys[i])+"-channel "+\
                         gen_pretty_name(fom)+" is "+str(fom_1[i]))
                if modes['out_dir'] == None:
                    print(out_str)
                else:
                    plt_file=prep_out_file(modes,plot=fom, dims="1d",
                                           channel=m_keys[i],
                                           out_type="txt")
                    out_file=open(plt_file,'a')
                    out_file.write(out_str)
                    out_file.close()
        
            #newline to separate outputs
            #print("\n")  

    
    str_channel=channel_maker(m_keys,modes)
    
    if modes['out_dir']!=None:
        for plot_item in ind_dfs:
            #prints the correlations to a file
            path_out_df = prep_out_file(modes,plot=plot_item,
                                   channel=str_channel,out_type=".csv")
            try:
                ind_dfs[plot_item].to_csv(path_out_df)
            except IOError:
                print("WARNING: Unable to output to file:\n\t"+path_out_df)
    

    
    return (ind_dfs)