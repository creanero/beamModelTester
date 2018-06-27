# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 13:51:56 2018

@author: User
"""
import pandas as pd

from graphing_functions import plots_1f
#from graphing_functions import plot_diff_values_1f
from graphing_functions import plot_spectra_nf
from graphing_functions import calc_fom_1d
from graphing_functions import calc_fom_nd
from graphing_functions import plot_altaz_values_nf
#from graphing_functions import identify_plots

from appearance_functions import channel_maker
from appearance_functions import gen_pretty_name

from utility_functions import get_alt_az_var
from utility_functions import split_df


from io_functions import prep_out_file

def analysis_1d(merge_df,modes, m_keys,sources):
    '''
    This function carries out all plotting and calculations needed for a 1-d 
    dataset (i.e. one frequency)
    
    Future iterations may include optional arguments to enable selection of the
    plots that are preferred
    '''
    
    if modes['verbose'] >=2:
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
        plots_1f(merge_df, m_keys, modes,"Time", sources)
        
        
        
    if ((all(coord in merge_df for coord in ["alt","az","az_ew"])) and
        (any (plot in modes["plots"] for plot in ["alt","az","ew"]))):
        alt_var = "alt"
        az_var = "az"
        if "stn" in modes["plots"]:
            if all(coord in merge_df \
                   for coord in ["stn_alt","stn_az","stn_az_ew"]):
                alt_var = "stn_"+alt_var
                az_var = "stn_"+az_var           
            else:
                if modes['verbose'] >=1:
                    print("Warning: Station coordinates selected but unavailable")
        if "ew" in modes["plots"]:
            az_var=az_var+"_ew"
        if "alt" in modes["plots"]:
            plots_1f(merge_df, m_keys, modes,alt_var, sources)
        if "az" in  modes["plots"]:
            plots_1f(merge_df, m_keys, modes,az_var, sources)
    elif any (plot in modes["plots"] for plot in ["alt","az","ew"]):
        if modes['verbose'] >=1:
            print("Warning: Horizontal coordinates selected but unavailable")
    
    #checks to see if there are differences to analyse
    if (any ("diff" in col_name for col_name in merge_df.columns)):        
        foms = []
        if "corr" in modes["plots"]:
            foms.append("corr")
        
        if "rmse" in modes["plots"]:
            foms.append("rmse")
            
        for fom in foms:
            fom_results=calc_fom_1d(merge_df, m_keys,fom)
            
            for i in range(len(m_keys)):
                out_str=("The "+str(m_keys[i])+"-channel "+gen_pretty_name(fom)+
                         " is "+str(fom_results[i]))
                if modes['out_dir'] == None:
                    print(out_str)
                else:
    
                    #creates an output-friendly string for the channel
                    str_channel = channel_maker(m_keys,modes)
            
                            
                    plt_file=prep_out_file(modes,plot=fom, dims="1d",
                                           channel=str_channel,
                                           out_type="txt")
                    out_file=open(plt_file,'a')
                    out_file.write(out_str)
                    out_file.close()
                    
            print("\n")
    else:
        if "corr" in modes["plots"]:
            if modes['verbose'] >=1:
                print("Warning: Correlation selected, but no differences available")
        
        if "rmse" in modes["plots"]:
            if modes['verbose'] >=1:
                print("Warning: RMSE selected, but no differences available")
            
        

#    if "corr" in modes["plots"]:
#        #calculates the pearson correlation coefficient between scope and model
#        corrs=calc_fom_1d(merge_df, m_keys,"corr")
#        
#        for i in range(len(m_keys)):
#            out_str=("The "+str(m_keys[i])+"-channel correlation is "+str(corrs[i]))
#            if modes['out_dir'] == None:
#                print(out_str)
#            else:
#
#                #creates an output-friendly string for the channel
#                str_channel = channel_maker(m_keys,modes)
#        
#                        
#                plt_file=prep_out_file(modes,plot="corr", dims="1d",
#                                       channel=str_channel,
#                                       out_type="txt")
#                out_file=open(plt_file,'a')
#                out_file.write(out_str)
#                out_file.close()
#                
#        print("\n")
#        
#    if "rmse" in modes["plots"]:        
#        #calculates the root mean squared error between scope and model
#        rmses=calc_fom_1d(merge_df, m_keys,"rmse")
#        for i in range(len(m_keys)):
#            out_str=("The "+str(m_keys[i])+"-channel RMSE is "+str(rmses[i]))
#            if modes['out_dir'] == None:
#                print(out_str)
#            else:
#                #creates an output-friendly string for the channel
#                str_channel = channel_maker(m_keys,modes)
#        
#        
#                plt_file=prep_out_file(modes,plot="rmse", dims="1d",
#                                       channel=str_channel,
#                                       out_type="txt")
#                out_file=open(plt_file,'a')
#                out_file.write(out_str)
#                out_file.close()    
    
def analysis_nd(merge_df,modes, m_keys,sources):
    '''
    This function carries out all plotting and calculations needed for a n-d 
    dataset (i.e. multiple frequencies)
    
    Future iterations may include optional arguments to enable selection of the
    plots that are preferred
    '''
    
    if modes['verbose'] >=2:
        print("Carrying out multi-frequency Analysis")
    
  
    if "spectra" in modes["plots"]:
        plot_spectra_nf(merge_df, m_keys, modes, sources)
    
    if any (plot in modes["plots"] for plot in ["alt","az","ew"]):
        if all(coord in merge_df for coord in ["alt","az","az_ew"]) :

            plot_altaz_values_nf(merge_df, m_keys, modes, sources)
            
        else:
            if modes['verbose'] >=1:
                print("Warning: Alt-Azimuth plotting selected, but not available!")
    
    #calculates the figures of merit at each independent variable 
    #return values are stored as possible future outputs

    ind_dfs = {}
    foms=[]
    if "corr" in modes["plots"]:
        foms.append("corr")
    if "rmse" in modes["plots"]:
        foms.append("rmse")

        #checks to see if there are differences to analyse
    if (any ("diff" in col_name for col_name in merge_df.columns)):     
 

        for fom in foms:
            ind_dfs=plot_fom_vs_ind(merge_df, m_keys, modes, fom)
                        
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
    else:
        if "corr" in modes["plots"]:
            if modes['verbose'] >=1:
                print("Warning: Correlation selected, but no differences available")
        
        if "rmse" in modes["plots"]:
            if modes['verbose'] >=1:
                print("Warning: RMSE selected, but no differences available")
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
                    if modes['verbose'] >=1:
                        print("WARNING: Unable to output to file:\n\t"+path_out_df)
    

    
    return (ind_dfs)

def plot_fom_vs_ind(merge_df, m_keys, modes, fom):
    ind_dfs = {}
    
    ind_var = []
    
    alt_var,az_var,az_var_ew = get_alt_az_var(merge_df, modes)
        
        
    if "spectra" in modes["plots"]:
        ind_var.append("Freq")
        ind_var.append("Time")
    if "alt" in modes['plots']:
        ind_var.append(alt_var)
    if "az" in modes['plots']:
        ind_var.append(az_var)
    
    for ind in ind_var:        
        splits, names = split_df(merge_df, modes, ind)
        for i in range(len(splits)):
            n_ind=splits[i][ind].unique()   
            ind_df=pd.DataFrame(data={ind:n_ind})
            n_foms=calc_fom_nd(splits[i],ind, m_keys, modes, fom)
            for key in m_keys:
                ind_df[key+'_'+fom]=n_foms[m_keys.index(key)]
            ind_dfs[ind+names[i]+"_"+fom]=ind_df
    
    return (ind_dfs)

