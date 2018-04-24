#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 13:39:28 2018

@author: Oisin Creaner
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
import argparse
import h5py
import os
from matplotlib.animation import FuncAnimation

def read_dreambeam_csv(in_file):
    '''
    This function reads in csv files output by dreambeam into a formatted 
    dataframe
    
    DreamBeam format described at 
    https://github.com/creaneroDIAS/beamModelTester/blob/multi-frequency-upgrade/DreamBeam_Source_data_description.md
    '''
    out_df=pd.read_csv(in_file,\
                        converters={'J11':complex,'J12':complex,\
                                    'J21':complex,'J22':complex}, \
                        parse_dates=['Time'], skipinitialspace=True)   
    
    
    '''
    calculates the xx, xy, yx and yy parameters for the model from the JNN 
    values Using the formulae below
     B = [[XX, XY] ,[YX, YY]]
     J = [[J11,J12],[J21,J22]]
     B = J * J'
     XX= (J11 *  ̅J̅1̅1 )+ (J12 *  ̅J̅1̅2 )
     XY= (J11 *  ̅J̅2̅1 )+ (J12 *  ̅J̅2̅2 )
     YX= (J21 *  ̅J̅1̅1 )+ (J22 *  ̅J̅1̅2 )
     YY= (J21 *  ̅J̅2̅1 )+ (J22 *  ̅J̅2̅2 )
        
    #yx_model not calculated for two reasons
    # 1. xy equal to within floating point errors
    # 2. yx not included in scope data (presumably because of 1.)
    #merge_df['yx_model']=merge_df.J21*np.conj(merge_df.J11)+merge_df.J22*np.conj(merge_df.J12)
    '''
    out_df['xx']=np.real(out_df.J11*np.conj(out_df.J11)+out_df.J12*np.conj(out_df.J12))
    out_df['xy']=out_df.J11*np.conj(out_df.J21)+out_df.J12*np.conj(out_df.J22)
    out_df['yy']=np.real(out_df.J21*np.conj(out_df.J21)+out_df.J22*np.conj(out_df.J22))
    return out_df

def get_df_keys(merge_df,key_str="", modes={"values":"all"}):
    '''
    Calculates the keys from a given dataframe or based on the input modes.
    '''
    m_keys=[]
    
    #if key groups have been supplied, extend the keylist with their components
    if "stokes" in modes["values"]:
        m_keys.extend(["U","V","I","Q"])
    if "linear" in modes["values"]:
        m_keys.extend(["xx","xy","yy"])
    if "all" in modes["values"]:
        for m_key in merge_df.keys():
            if key_str in m_key:
                m_keys.append(m_key.split(key_str)[0])
                
    #if keys have been supplied individually                
    if "xx" in modes["values"]:
        m_keys.append("xx")
    if "xy" in modes["values"]:
        m_keys.append("xy")
    if "yy" in modes["values"]:
        m_keys.append("yy")
    if "U" in modes["values"]:
        m_keys.append("U")
    if "V" in modes["values"]:
        m_keys.append("V")
    if "I" in modes["values"]:
        m_keys.append("I")
    if "Q" in modes["values"]:
        m_keys.append("Q")
    
    
    #if the keys are still blank
    if m_keys == []:
        print ("Warning, no appropriate keys found!")
    
    
    return(m_keys)

def plot_values_1f(merge_df, m_keys, modes):
    '''
    This function takes a merged dataframe as an argument and plots a graph of
    each of the various values for the model and the scope against time.
    
    This plot is only usable and valid if the data is ordered in time and has 
    only a single frequency
    '''
    
    
    for key in m_keys:
        #creates a two part plot of the values of model and scope
        #part one: plots the model and scope values per channel against time
        plt.figure()
        graph_title="\n".join([modes['title'],
                        ("Plot of the values in "+key+"-channel over time"+
                         "\nat %.2f MHz"%(min(merge_df.Freq)/1e6))])
        
        plt.title(graph_title)

        #plots the model in one colour
        plt.plot(merge_df.Time,plottable(merge_df[key+'_model']),label='model',
                 color=colour_models(key+'_light'))
        #plots the scope in another colour
        plt.plot(merge_df.Time,plottable(merge_df[key+'_scope']),label='scope',
                 color=colour_models(key+'_dark'))
        plt.legend(frameon=False)
        #plots the axis labels rotated so they're legible
        plt.xticks(rotation=90)
        plt.xlabel('Time')
        
        #prints or saves the plot
        if modes['out_dir'] == None:
            plt.show()
        else:
            plt_file=prep_out_file(modes,plot="vals",dims="1d",channel=key,
                                   freq=min(merge_df.Freq),
                                   out_type="png")
            print("plotting: "+plt_file)
            plt.savefig(plt_file,bbox_inches='tight')
        plt.close()
    return(0)
    
def plottable(in_series):
    '''
    turns a complex number into a series of absolute values, but just returns a
    real number
    '''
    out_series=in_series.reset_index(drop=True)
    if len(out_series)>0:
        if 'complex' in str(type(out_series[0])):
            return abs(in_series)
        else:
            return in_series
    else:
        return abs(in_series)
    
def plot_values_nf(merge_df, m_keys, modes):
    '''
    This function takes a merged dataframe as an argument and plots a graph of
    each of the various values for the model and the scope against time and 
    frequency.
    

    '''
    time_delay = 1000.0/modes['frame_rate']
    
    if modes['threed']=="colour":
        for key in m_keys:
            #creates a plot each of the values of model and scope
            
            for source in ["model","scope"]:
                plot_against_freq_time(merge_df, key, modes, source)

    elif modes['threed']=="anim":
        for source in ["model","scope"]:
            
            animated_plot(merge_df, modes, 'Freq', m_keys, "Time", source, time_delay)
#        if "each" in modes['values']:
##            print("WARNING: Each mode not supported by animations at this time")
#            for key in m_keys: #analyses them one at a time
#                for source in ["model","scope"]:
#                    animated_plot(merge_df, modes, 'Freq', [key], "Time", source, time_delay=20)
#        else: #allows plots to be overlaid 
#            for source in ["model","scope"]:
#                animated_plot(merge_df, modes, 'Freq', m_keys, "Time", source, time_delay=20)
                
    elif modes['threed']=="animf":
        for source in ["model","scope"]:
            animated_plot(merge_df, modes, "d_Time", m_keys, 'Freq', source, time_delay)
#        if "each" in modes['values']:
##            print("WARNING: Each mode not supported by animations at this time")
#            for key in m_keys: #analyses them one at a time
#                for source in ["model","scope"]:
#                    animated_plot(merge_df, modes, "d_Time", [key], 'Freq', source, time_delay=20)
#        else: #allows plots to be overlaid 
#            for source in ["model","scope"]:
#                animated_plot(merge_df, modes, "d_Time", m_keys, 'Freq', source, time_delay=20)
                
    else:
        print("WARNING: No valid value for 3d plots")
#            plt.figure()
#            graph_title="\n".join([modes['title'],("Plot of the values in "+key+"-channel \nover time "+
#                      "and frequency for "+source)])
#            plt.title(graph_title)
#    
#            #plots the channel in a colour based on its name
#            plt.tripcolor(merge_df.d_Time,merge_df.Freq,plottable(merge_df[key+'_'+source]),
#                          cmap=plt.get_cmap(colour_models(key+'s')))
#            plt.legend(frameon=False)
#            #plots x-label for both using start time 
#            plt.xlabel("Time in seconds since start time\n"+str(min(merge_df.Time)))
#            plt.ylabel("Frequency")
#            plt.colorbar()
#            #prints or saves the plot
#            if modes['out_dir'] == None:
#                plt.show()
#            else:
#                plt_file=prep_out_file(modes,source=source,plot="vals",dims="nd",
#                                       channel=key,
#                                       out_type="png")
#                print("plotting: "+plt_file)
#                plt.savefig(plt_file,bbox_inches='tight')
#            plt.close()
    return(0)    


def plot_against_freq_time(merge_df, key, modes, source):
    '''
    This function generates 3d colour plots against frequency and time for the 
    given value for a given channel
    '''
    plt.figure()
    if source == "diff":
        graph_title="\n".join([modes['title'],("Plot of the differences in %s\n over time and frequency"%key)])
    else:
        graph_title="\n".join([modes['title'],("Plot of the values in "+key+"-channel \nover time "+
                  "and frequency for "+source)])
    plt.title(graph_title)

    #plots the channel in a colour based on its name
    plt.tripcolor(merge_df.d_Time,merge_df.Freq,plottable(merge_df[key+'_'+source]),
                  cmap=plt.get_cmap(colour_models(key+'s')))
    plt.legend(frameon=False)
    #plots x-label for both using start time 
    plt.xlabel("Time in seconds since start time\n"+str(min(merge_df.Time)))
    plt.ylabel("Frequency")
    plt.colorbar()
    #prints or saves the plot
    if modes['out_dir'] == None:
        plt.show()
    else:
        plt_file=prep_out_file(modes,source=source,plot="vals",dims="nd",
                               channel=key,
                               out_type=modes['image_type'])
        print("plotting: "+plt_file)
        plt.savefig(plt_file,bbox_inches='tight')
        plt.close()

def animated_plot(merge_df, modes, var_x, var_ys, var_t, source, time_delay=20):
    '''
    Produces an animated linegraph(s) with the X, Y and T variables specified
    '''
    
    fig, ax = plt.subplots()
    fig.set_tight_layout(True)
    
    #hard coded for now, need to parameterise
    percentile_gap = 5
    multiplier = 1.5
    
    
    #sets default values for max_ and min_y
    max_y= 0
    min_y = 0
    

    
    
    # Plot a scatter that persists (isn't redrawn) and the initial line.
    var_t_vals = np.sort(merge_df[var_t].unique())
    var_t_val=var_t_vals[0]
    
    str_channel = list_to_string(var_ys,", ")
    var_t_string = str(var_t_val).rstrip('0').rstrip('.')
    anim_title="Plot of "+source+" for "+str_channel+" against "+var_x+ " at\n"+var_t+" of "+var_t_string
    label = "\n".join([modes["title"],anim_title])
    plt.title(label)
    
    var_x_vals =merge_df.loc[merge_df[var_t]==var_t_val,var_x].reset_index(drop=True)
    
    lines = []
    
    for i in range(len(var_ys)):
        var_y = var_ys[i]
        
        var_y_vals = plottable(merge_df.loc[merge_df[var_t]==var_t_val,
                                (var_y+"_"+source)].reset_index(drop=True))
    

        line, = ax.plot(var_x_vals, var_y_vals, color=colour_models(var_y))
        lines.append(line)
            #code to set x and y limits.  
        #Really want to get a sensible way of doing this
        if plottable(merge_df[(var_ys[i]+"_"+source)]).min() < 0:
            local_min_y=np.percentile(plottable(merge_df[(var_ys[i]+"_"+source)]),percentile_gap)*multiplier
        else:
            local_min_y = 0
        min_y=min(min_y,local_min_y)
        #min_y=0#min(merge_df[(var_y+"_"+source)].min(),0)
        local_max_y=np.percentile(plottable(merge_df[(var_ys[i]+"_"+source)]),100-percentile_gap)*multiplier
        max_y=max(max_y,local_max_y)
    
    ax.set_ylim(min_y,max_y)
    

    ax.set_xlabel(var_x)
    ax.set_ylabel(channel_maker(var_ys,modes,", ")+" flux\n(arbitrary units)")    
 
    ax.legend(frameon=False)
    
    if modes['out_dir']==None:
        repeat_option = True
    else:
        repeat_option = False
        
    global anim
    anim = FuncAnimation(fig, update_a, frames=range(len(var_t_vals)), 
                                 interval=time_delay,
                                 fargs=(merge_df, modes, var_x, var_ys, var_t, 
                                        source,lines,ax),
                                 repeat=repeat_option)

    if modes['out_dir']!=None:
        str_channel = channel_maker(var_ys,modes)
        #str_channel = list_to_string(var_ys,", ")
        plt_file = prep_out_file(modes,source=source,plot="vals",dims="nd",
                               channel=str_channel,out_type=modes['image_type'])
        anim.save(plt_file, dpi=80, writer='imagemagick')
    else:
        plt.show()# will just loop the animation forever.

    



def update_a(i,merge_df, modes, var_x, var_ys, var_t, source,lines,ax):
    
    var_t_vals = np.sort(merge_df[var_t].unique())
    var_t_val=var_t_vals[i]
    str_channel = list_to_string(var_ys,", ")
    var_t_string = str(var_t_val).rstrip('0').rstrip('.')
    anim_title="Plot of "+source+" for "+str_channel+" against "+var_x+ " at\n"+var_t+" of "+var_t_string
    label = "\n".join([modes["title"],anim_title])
    plt.title(label)
    
    var_x_vals = (merge_df.loc[merge_df[var_t]==var_t_val,var_x]).reset_index(drop=True)
    
    for y_index in range(len(var_ys)):
        var_y = var_ys[y_index]
        var_y_vals = plottable((merge_df.loc[merge_df[var_t]==var_t_val,(var_y+"_"+source)]).reset_index(drop=True))

        lines[y_index].set_data(var_x_vals, var_y_vals)
    

    

    
def plot_diff_values_1f(merge_df, m_keys, modes):
    '''
    This function takes a merged dataframe as an argument and 
    plots the differences in various channel values over time
    
    This plot is only usable and valid if the data is ordered in time and has 
    only a single frequency
    '''

    plt.figure()
    
    graph_title = "\n".join([modes['title'],"Plot of the differences in "])
    for key in m_keys:
        plt.plot(merge_df.Time,
                 plottable(merge_df[key+'_diff']), 
                 label=r'$\Delta $'+key,
                 color=colour_models(key))
        if (m_keys.index(key) < (len(m_keys)-2)) :
            graph_title=graph_title+key+", "
        elif m_keys.index(key)==(len(m_keys)-2):
            graph_title=graph_title+key+" & "
        else:
            graph_title=graph_title+key
    
    #calculates and adds title with frequency in MHz
    
    graph_title=graph_title+"-channels over time at %.2f MHz"%(min(merge_df.Freq)/1e6)    
    
    


    
    #plots the axis labels rotated so they're legible
    plt.xticks(rotation=90)

    plt.title(graph_title)
    plt.legend(frameon=False)
    plt.xlabel('Time')
    
    #prints or saves the plot
    if modes['out_dir'] == None:
        plt.show()
    else:
        plt_file=prep_out_file(modes,plot="diff",dims="1d",
                               out_type=modes['image_type'])
        print("plotting: "+plt_file)
        plt.savefig(plt_file,bbox_inches='tight')
    plt.close()
    return(0)
    
    
    
   
def calc_corr_1d(merge_df, m_keys):
    '''
    This function takes a merged dataframe as an argument and 
    calculates the pearson correlation coeffiecients between scope 
    and model
    '''
    
    
    corr_outs=[]
    for key in m_keys:
        #uses absolute values as real values cannot be negative and complex 
        #values cannot be correlated
        model_vals=list(plottable(merge_df[key+'_model']))
        scope_vals=list(plottable(merge_df[key+'_scope']))
        corr=pearsonr(model_vals,scope_vals)[0]
        corr_outs.append(corr)
    #using [0] from the pearsonr to return the correlation coefficient, but not
    #the 2-tailed p-value stored in [1]
    
    return(corr_outs)
    
    
    
    
def calc_corr_nd(merge_df, var_str, m_keys, modes):
    '''
    This function calculates the correlation between the scope and model values
    for p- and q-channel as they are distributed against another column of the 
    dataframe merge_df which is identified by var_str
    
    in current versions, useable values for var_str are "Time" and "Freq"
    '''
        
    #creates empty lists for the correlations
    n_corrs=[]
    for i in range(len(m_keys)):
        n_corrs.append([])
    
    

    #identifies allthe unique values of the variable in the column
    unique_vals=merge_df[var_str].unique()
    
    unique_vals=np.sort(unique_vals)
    
    #iterates over all unique values
    for unique_val in unique_vals:
        #creates a dataframe with  only the elements that match the current 
        #unique value
        unique_merge_df=merge_df[merge_df[var_str]==unique_val]
        #uses this unique value for and the 1-dimensional calc_corr_1d function
        #to calculate the correlations for each channel
        n_corr=calc_corr_1d(unique_merge_df, m_keys)
        
        #appends these to the list
        for i in range(len(m_keys)):
            n_corrs[i].append(n_corr[i])

    #creates an overlaid plot of how the correlation of between model and scope
    #varies for each of the channels against var_str
    plt.figure()

    graph_title = "\n".join([modes['title'],"Plot of the correlation in "])
    for key in m_keys:    
        plt.plot(unique_vals,n_corrs[m_keys.index(key)],
                label=key+'_correlation',color=colour_models(key))
        
        if (m_keys.index(key) < (len(m_keys)-2)) :
            graph_title=graph_title+key+", "
        elif m_keys.index(key)==(len(m_keys)-2):
            graph_title=graph_title+key+" & "
        else:
            graph_title=graph_title+key
    
    #completes the title using the independent variable plotted over
    
    graph_title=graph_title+"-channels over "+var_str    
            
    

    plt.title(graph_title)
    
    #rotates the labels.  This is necessary for timestamps
    plt.xticks(rotation=90)
    plt.legend(frameon=False)
    plt.xlabel(var_str)
    
    #prints or saves the plot
    if modes['out_dir'] == None:
        plt.show()
    else:
        #creates an output-friendly string for the channel
        str_channel = channel_maker(m_keys,modes)
        
        
        plt_file=prep_out_file(modes,plot="corr",ind_var=var_str,
                               channel=str_channel,
                               out_type=modes['image_type'])
        print("plotting: "+plt_file)
        plt.savefig(plt_file,bbox_inches='tight')
    plt.close()
        
    #returns the correlation lists if needed    
    return (n_corrs)    
    



def calc_rmse_1d(merge_df, m_keys):
    '''
    This function takes a merged dataframe as an argument and 
    calculates and returns the root mean square difference between scope and 
    model
    '''
    rmse_outs=[]
    for key in m_keys:
        rmse_outs.append(np.mean(plottable(merge_df[key+'_diff'])**2)**0.5)
   
    return(rmse_outs)
 
    
    
    
def calc_rmse_nd(merge_df, var_str, m_keys, modes):
    '''
    This function calculates the correlation between the scope and model values
    for p- and q-channel  as they are distributed against another column of the 
    dataframe merge_df which is identified by var_str
    
    in current versions, useable values for var_str are "Time" and "Freq"
    '''

        
    #creates empty lists for the Errors
    n_rmses=[]
    for i in range(len(m_keys)):
        n_rmses.append([])
    
    
    
    #identifies allthe unique values of the variable in the column
    unique_vals=merge_df[var_str].unique()
    
    unique_vals=np.sort(unique_vals)
    
    #iterates over all unique values
    for unique_val in unique_vals:
        #creates a dataframe with  only the elements that match the current 
        #unique value
        unique_merge_df=merge_df[merge_df[var_str]==unique_val]
        #uses this unique value for and the 1-dimensional calc_rmse_1d function
        #to calculate the RMSE for each channel
        n_rmse=calc_rmse_1d(unique_merge_df, m_keys)
        
        #appends these to the list
        for i in range(len(m_keys)):
            n_rmses[i].append(n_rmse[i])
    
    #creates an overlaid plot of how the RMSE  between model and scope
    #varies for each of the channels against var_str    
    plt.figure()
    graph_title = "\n".join([modes['title'],"Plot of the RMSE in "])
    for key in m_keys:    
        plt.plot(unique_vals,n_rmses[m_keys.index(key)],
                label=key+'_RMSE',color=colour_models(key))
        
        if (m_keys.index(key) < (len(m_keys)-2)) :
            graph_title=graph_title+key+", "
        elif m_keys.index(key)==(len(m_keys)-2):
            graph_title=graph_title+key+" & "
        else:
            graph_title=graph_title+key
    
    #calculates and adds title with frequency in MHz
    
    graph_title=graph_title+"-channels over "+var_str    
            
    plt.title(graph_title)


    #rotates the labels.  This is necessary for timestamps
    plt.xticks(rotation=90)
    plt.legend(frameon=False)
    plt.xlabel(var_str)
    
    #prints or saves the plot
    if modes['out_dir'] == None:
        plt.show()
    else:
        #creates an output-friendly string for the channel
        str_channel = channel_maker(m_keys,modes)
        
        
        plt_file=prep_out_file(modes,plot="rmse",ind_var=var_str,
                               channel=str_channel,
                               out_type=modes['image_type'])
        print("plotting: "+plt_file)
        plt.savefig(plt_file,bbox_inches='tight')
    plt.close()
    
    #returns the correlation lists if needed    
    return (n_rmses)

def channel_maker(channels,modes,sep_str="_"):
    str_channel = ""
    if "each" not in modes ['values']:
        if "all" in modes ['values']:
            str_channel = "all"
        
        elif "stokes" in modes['values']:
            str_channel = "stokes"
        
        elif "linear" in modes['values']:
            str_channel = "linear"
        else:
            str_channel=list_to_string (channels, sep_str)
        return(str_channel)
    else:
        str_channel=list_to_string (channels, sep_str)
                
    return (str_channel)

def list_to_string (m_keys, sep_str="_"):
    
    #creates an output-friendly string for the channel
    str_channel = str(m_keys)
    for char in (["[","]","'"]):
        str_channel = str_channel.replace(char,'',)
    str_channel.replace(", ",sep_str)    
    
    return (str_channel)

def plot_diff_values_nf(merge_df, m_keys, modes):
    '''
    This function creates 3d colour plots using time and frequency from a 
    merged data frame as the independent variables and the difference between
    source and model as the dependent (colour) variable 
    '''
    source = "diff"
    
    time_delay = 1000.0/modes['frame_rate']
    
    if modes['threed']=="colour":
        for key in m_keys:
            #create a plot 
            plot_against_freq_time(merge_df, key, modes, source)
    elif modes['threed']=="anim":

        animated_plot(merge_df, modes, 'Freq', m_keys, "Time", source, time_delay)
                
    elif modes['threed']=="animf":

        animated_plot(merge_df, modes, "d_Time", m_keys, 'Freq', source, time_delay)

    else:
        print("WARNING: No valid value for 3d plots")
#        plt.figure()
#        
#        #display main title and subplot title together
#        graph_title="\n".join([modes['title'],("Plot of the differences in %s\n over time and frequency"%key)])
#        plt.title(graph_title)
#        
#        #plots p-channel difference
#        plt.tripcolor(merge_df.d_Time,merge_df.Freq,plottable(merge_df[key+'_diff']),
#                      cmap=plt.get_cmap(colour_models(key+'s')))
#        plt.colorbar()
#        #plots x-label for both using start time 
#        plt.xlabel("Time in seconds since start time\n"+str(min(merge_df.Time)))
#        plt.ylabel("Frequency")
#        #prints or saves the plot
#        if modes['out_dir'] == None:
#            plt.show()
#        else:
#            plt_file=prep_out_file(modes,plot="diff", dims="nd",
#                                   channel=key,
#                                   out_type="png")
#            print("plotting: "+plt_file)
#            plt.savefig(plt_file,bbox_inches='tight')
#        plt.close()

def analysis_1d(merge_df,modes, m_keys):
    '''
    This function carries out all plotting and calculations needed for a 1-d 
    dataset (i.e. one frequency)
    
    Future iterations may include optional arguments to enable selection of the
    plots that are preferred
    '''
  
    if "value" in modes["plots"]:
        #plots the values for each channel
        plot_values_1f(merge_df, m_keys, modes)
    
    if "diff" in modes["plots"]:    
        #plots the differences in the values
        plot_diff_values_1f(merge_df, m_keys, modes)
    

    if "corr" in modes["plots"]:
        #calculates the pearson correlation coefficient between scope and model
        corrs=calc_corr_1d(merge_df, m_keys)
        
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
        rmses=calc_rmse_1d(merge_df, m_keys)
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
        
  
    if "corr" in modes["plots"]:
        #calculates the pearson correlation coefficient between scope and model
        corrs=calc_corr_1d(merge_df, m_keys)
        #prints that coefficient for each key and correlation
        for i in range(len(m_keys)):
            out_str=("The "+str(m_keys[i])+"-channel correlation is "+str(corrs[i]))
            if modes['out_dir'] == None:
                print(out_str)
            else:
                plt_file=prep_out_file(modes,plot="corr", dims="1d",
                                       channel=m_keys[i],
                                       out_type="txt")
                out_file=open(plt_file,'a')
                out_file.write(out_str)
                out_file.close()
    
        #newline to separate outputs
        print("\n")  
    
    if "rmse" in modes["plots"]:        
        #calculates the root mean squared error between scope and model
        rmses=calc_rmse_1d(merge_df, m_keys)
        for i in range(len(m_keys)):
            out_str=("The "+str(m_keys[i])+"-channel RMSE is "+str(rmses[i]))
            if modes['out_dir'] == None:
                print(out_str)
            else:
                plt_file=prep_out_file(modes,plot="rmse", dims="1d",
                                       channel=m_keys[i],
                                       out_type="txt")
                out_file=open(plt_file,'a')
                out_file.write(out_str)
                out_file.close() 
                
    if "value" in modes["plots"]:
        #plots the values of scope and model 
        plot_values_nf(merge_df, m_keys, modes)
    
    if "diff" in modes["plots"]:
        #plots the differences in values for the various channels
        plot_diff_values_nf(merge_df, m_keys, modes)
    
    #calculates the correlations and rmse over time at each independent variable 
    #return values are stored as possible future outputs
    ind_var = ["Freq", "Time"]
    ind_dfs = {}
    for ind in ind_var:        
        n_ind=merge_df[ind].unique()
        
        
        

        if "corr" in modes["plots"]:
            ind_df=pd.DataFrame(data={ind:n_ind})
            n_corrs=calc_corr_nd(merge_df,ind, m_keys, modes)
            for key in m_keys:
                ind_df[key+'_corr']=n_corrs[m_keys.index(key)]
            ind_dfs[ind+"_corr"]=ind_df
        
        ind_df=pd.DataFrame(data={ind:n_ind})
        if "rmse" in modes["plots"]: 
            ind_df=pd.DataFrame(data={ind:n_ind})
            n_rmses=calc_rmse_nd(merge_df,ind, m_keys, modes)
            for key in m_keys:
                ind_df[key+'_RMSE']=n_rmses[m_keys.index(key)]
            ind_dfs[ind+"_RMSE"]=ind_df
    
    str_channel=channel_maker(m_keys,modes)
    
    if modes['out_dir']!=None:
        for plot_item in ind_dfs:
            #prints the correlations to a file
            path_out_df = prep_out_file(modes,plot=plot_item,
                                   channel=str_channel,out_type=".csv")
            try:
                ind_dfs[plot_item].to_csv(path_out_df)
            except IOError:
                print("WARNING: unable to output to file:\n\t"+path_out_df)
    

    
    return (ind_dfs)
    
    
    

 
def colour_models(colour_id):
    '''
    The colours used are defined in a function that returns the colour strings
    '''
    #sets oranges for various applications for the p channel
    if 'p'==colour_id:
        return('orange')
    if 'p_light'==colour_id:
        return('sandybrown')
    if 'p_dark'==colour_id:
        return('darkorange')
    if 'ps'==colour_id:
        return('Oranges')
        
    #sets greens for various applications of the q channel    
    if 'q'==colour_id:
        return('green')
    if 'q_light'==colour_id:
        return('limegreen')
    if 'q_dark'==colour_id:
        return('darkgreen')
    if 'qs'==colour_id:
        return('Greens')
    
    #sets reds for various applications of the XX channel 
    if 'xx'==colour_id:
        return('red')   
    if 'xx_light'==colour_id:
        return('orangered')
    if 'xx_dark'==colour_id:
        return('darkred')
    if 'xxs'==colour_id:
        return('Reds')
    
    
    #sets purples for various applications of the XY channel 
    if 'xy'==colour_id:
        return('darkviolet')
    if 'xy_light'==colour_id:
        return('mediumorchid')
    if 'xy_dark'==colour_id:
        return('purple')
    if 'xys'==colour_id:
        return('Purples')
    
    
    #sets greens for various applications of the YY channel 
    if 'yy'==colour_id:
        return('blue')
    if 'yy_light'==colour_id:
        return('deepskyblue')
    if 'yy_dark'==colour_id:
        return('darkblue')
    if 'yys'==colour_id:
        return('Blues')
        
    #sets golds/yellows for various applications of stokes U
    if 'U'==colour_id:
        return('yellow')
    if 'U_light'==colour_id:
        return('goldenrod')
    if 'U_dark'==colour_id:
        return('darkgoldenrod')
    if 'Us'==colour_id:
        return('YlOrBr')
        
    #sets oranges for various applications for the Stokes V
    if 'V'==colour_id:
        return('darkorange')
    if 'V_light'==colour_id:
        return('sandybrown')
    if 'V_dark'==colour_id:
        return('chocolate')
    if 'Vs'==colour_id:
        return('Oranges')        

    #sets cyans for various applications for the Stokes I
    if 'I'==colour_id:
        return('cyan')
    if 'I_light'==colour_id:
        return('aquamarine')
    if 'I_dark'==colour_id:
        return('teal')
    if 'Is'==colour_id:
        return('winter')   

    #sets greens for various applications for the Stokes Q
    #note the distinction from the generic q-channel
    if 'Q'==colour_id:
        return('green')
    if 'Q_light'==colour_id:
        return('limegreen')
    if 'Q_dark'==colour_id:
        return('darkgreen')
    if 'Qs'==colour_id:
        return('Greens')           
    
    #sets grey values for other plots, where there are partial matches.
    if '_light' in colour_id:
        print("Warning: Colour incompletely specified as:\n\n\t"+colour_id+              
              "\n\n'light' found in colourstring.\n"
              "Defaulting to grey\n")
        return ('grey')    
    if '_dark' in colour_id:
        print("Warning: Colour incompletely specified as:\n\n\t"+colour_id+              
              "\n\n'dark' found in colourstring.\n"
              "Defaulting to darkeslategrey\n")
        return ('darkslategrey')  
    if 's' in colour_id:    
        print("Warning: Colour incompletely or inaccurately specified as:\n\n\t"+colour_id+              
              "\n\n's' found in colourstring.\n"
              "Defaulting to Greys\n")
        return ('Greys')      
    
    #returns black as a final default
    else:
        print("Warning: Colour incorrectly specified as:\n\n\t"+colour_id+              
              "\n\nDefaulting to black\n")
        return ('black')    

def beam_arg_parser():
    '''
    This function parses the arguments from the command line and returns the 
    file names for the model data and the scope data
    
    Several options are provided: Positional arguments, followed by optional
    arguments followed by interactive entry of the argument values.
    
    future expansions to arguments will allow the user to specify modes of 
    operation and the type of output generated
    '''
    
    parser = argparse.ArgumentParser()
    
    #creates a group for the model filename
    group_model = parser.add_mutually_exclusive_group()
    
    #gives positional and optional ways of providing the model data 
    group_model.add_argument("model_p",nargs='?', default=None, 
                             help='''
The file containing the data from the model (Usually DreamBeam)
                             ''')
    group_model.add_argument("--model","-m", 
                             help='''
Alternative way of specifying the file containing the data from the model
                             ''')
    
    
    #creates a group for the scope filename
    group_scope = parser.add_mutually_exclusive_group()
    
    #gives positional and optional ways of providing the scope data 
    group_scope.add_argument("scope_p",nargs='?', default=None, 
                             help='''
The file containing the observed data from the telescope
                             ''')
    group_scope.add_argument("--scope","-s", 
                             help='''
Alternative way of specifying the file containing the observed data from the 
telescope
                             ''')

    #adds an optional argument for output directory
    parser.add_argument("--out_dir","-o", default=None,
                             help='''
path to a directory in which the output of the program is intended to be stored
.  IF this argument is blank, output is to std.out and plots are to screen.
                             ''')   
    
    #adds an optional argument for the title of graphs and out_files
    parser.add_argument("--title","-t", default=[""], nargs = '*',
                             help='''
The title for graphs and output files.  Spaces are permitted in title.  Output
files will have spaces replaced with underscores
                             ''')   
    
    #adds an optional argument for normalisation method
    parser.add_argument("--norm","-n", default='o',
                        choices=('o',"f","n",'t'), 
                             help='''
Method for normalising the data 
o = overall (divide by maximum for all data)
f = frequency (divide by maximum by frequency/subband)
t = time (divide by maximum by time/observation)
n = no normalisation.
                             ''')
    #adds an optional argument for normalisation target
    parser.add_argument("--norm_data","-N", default="s",
                        choices=("s","m","n","b"), 
                             help='''
Target data for applying the normalisation to
s = scope
m = model
n = no cropping
b = normalise both
                             ''')       
    #adds an optional argument for the cropping type for noise on the scope
    parser.add_argument("--crop_type","-C", default="median",
                        choices=("median","mean","percentile"),
                        help = '''
Sets what style of cropping will be applied to the scope data to remove 
outliers. A value for --crop must also be specified or this argument is ignored.  
        median implies drop all values over a given multiple of the median value.
        mean implies drop all values over a given multiple of the median value.
        percentile implies drop all values over a given percentile value.
        percentiles over 100 are ignored''')     

    #adds an optional argument for the cropping level for noise on the scope
    parser.add_argument("--crop","-c", default = 0.0, type=float,
                        help = '''
Set the numeric value for cropping. Depending on crop mode, this may be a 
multiple of the mean or median, or the percentile level to cut the scope values
 to. Default is not to crop (crop = 0.0). Negative values are converted to 
 positive before use.
                             ''')
    

    #adds an optional argument for cropping method
    parser.add_argument("--crop_basis","-k", default='o',choices=('o',"f","n"), 
                             help='''
Method for cropping the data
o = overall (crop equally for all data)
f = frequency (crop by frequency/subband)
n = no cropping
                             ''')

    #adds an optional argument for cropping method
    parser.add_argument("--crop_data","-K", default="s",
                        choices=("s","m","n","b"), 
                             help='''
Target data for applying the cropping to
s = scope
m = model
n = no cropping
b = crop both
                             ''')    
    #adds an optional argument for the cropping level for noise on the scope
    parser.add_argument("--diff","-d", default = "sub",
                        choices=("sub","div", "idiv"),
                        help = '''
determines whether to use subtractive or divisive differences when calculating 
the difference between the scope and the model.  Default is subtract
  sub = model - scope
  div = model / scope
  idiv = scope/model
                        ''')
    
    #adds an optional argument for the set of values to analyse and plot
    parser.add_argument("--values","-v", default=["all"], nargs="*",
                        choices=("all","linear","stokes",
                                 "xx","xy","yy","U","V","I","Q",
                                 "each"),
                        help = '''
Sets the parameters that will be plotted on the value and difference graphs.
  linear implies xx, xy and yy-channel values will be plotted. 
  stokes implies that Stokes U- V- I- and Q-channels will be plotted.
  all implies that all seven channels will be plotted.
  An individual channel name means to plot that channel alone. 
  each means that the channels will be plotted separately rather than overlaid.
                        ''')     
    
    #adds an optional argument for the plots to show
    parser.add_argument("--plots","-p", nargs="*",
                        default=["rmse", "corr", "value", "diff"],
                        choices=("rmse", "corr", "value", "diff"),
                        help = '''
Sets which plots will be shown.  Default is to show all plots and calculations
rmse shows plots of RMSE (overall, per time and per freq as appropriate)
corr shows plots of corrlation (overall, per time and per freq as appropriate)
value shows plots of the values of the channels (per time and per freq as appropriate)
diff shows plots of the differences in values of the channels (per time and per freq as appropriate)
 
                        ''') 
    #adds an optional argument for the way to show 3d data
    parser.add_argument("--threed","-3", default="colour",
                        choices=("colour","color", "anim", "animf"),
                        help = '''
Sets how to show three dimensional plots.  If colour is chosen, then they are 
plotted as colours.  If anim is chosen, plots the data animated over time.  If 
animf is chosen, plots the data animated over frequency 
                        ''')     
    
    #adds an optional argument for the framerate of animations
    parser.add_argument("--frame_rate","-r", default = 60.0, type=float,
                        help = '''
Set the numeric value for the number of frames per second to attempt to plot 
animated graphs at.  If no animated plots are used, or animations are plotted 
to files on a per-frame basis, this variable is ignored.  Default is 60 FPS
                             ''')
     
    #adds an optional argument for a time offset between model and scoep
    parser.add_argument("--offset","-O", default = 0, type=int,
                        help = '''
Sets an offset for the scope.  This is the amount of time (in seconds) that the
scope is believed to be ahead of the model.  This will be subtracted from the 
time of the scope data.  Default is no offset.  Offsets may only be given in
whole seconds
                             ''')
       
    #adds an optional argument for the file types for image plots
    parser.add_argument("--image_type","-i", default="png",
                        choices=('png', 'gif', 'jpeg', 'tiff', 'sgi', 'bmp', 'raw', 'rgba'),
                        help = '''
Sets the file type for image files to be saved as.  If using amimations, some
file types will save animations, and others will save frames.  Default is png.
                        ''')     
    #creates a group for the scope filename
    group_freq = parser.add_mutually_exclusive_group()
    #adds an optional argument for the frequency to filter to
    group_freq.add_argument("--freq","-f", default = [0.0], 
                            type=float, nargs="*",
                        help = '''
set a frequency filter to and display the channels for.   
Must supply a float or collection of floats separated by spaces.
                        ''')
    #adds an optional argument for a file containing a set of frequenciesy 
    #to filter to
    group_freq.add_argument("--freq_file","-F", default = "", 
                            help = '''
set a file containing multiple frequencies to filter to and display the 
channels for.  The file must contain one float per line in text format.
                            ''')    
    
    
    
    #passes these arguments to a unified variable
    args = parser.parse_args()
    

    
    #creates and uses a dictionary to store the mode arguments
    modes={}    
    modes['norm']=args.norm
    modes['norm_data']=args.norm_data
    modes['crop_data']=args.crop_data
    modes['crop_type']=args.crop_type
    modes['crop_basis']=args.crop_basis
    modes['crop']=abs(args.crop)#abs value to prevent use of negative crops
    modes['diff']=args.diff
    modes['values']=args.values
    modes['plots']=args.plots
    modes['freq']=args.freq
    modes['freq_file']=args.freq_file
    modes['threed']=args.threed
    modes['image_type']=args.image_type
    modes['frame_rate']=args.frame_rate
    modes['offset']=args.offset
    
    #fixes issues with spelling of colour
    if modes['threed'] == "color":
        modes['threed'] = "colour"
    
    #combines the components of the title with spaces to create titles
    modes['title']= " ".join(args.title)

    #combines the components of the title with spaces to create titles
    modes['title_']= "_".join(args.title)    
    
    #outputs the filename for the model to a returnable variable
    if args.model_p != None:
        modes['in_file_model']=args.model_p
    elif args.model != None:
        modes['in_file_model']=args.model
    else:
        modes['in_file_model']=raw_input("No model filename specified:\n"
                                "Please enter the model filename:\n")
    
    
    #outputs the filename for the scope to a returnable variable
    if args.scope_p != None:
        modes['in_file_scope']=args.scope_p
    elif args.scope != None:
        modes['in_file_scope']=args.scope
    else:
        modes['in_file_scope']=raw_input("No filename specified for observed data from the telescope:\n"
                                "Please enter the telescope filename:\n")
    
    #sets up the output directory based on the input
    modes['out_dir']=prep_out_dir(args.out_dir)
    
    return(modes)

def prep_out_dir(out_dir=None):
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
                #print a warning and ask the user for new input
                os_dir = raw_input("WARNING: output directory not suitable, "
                                   "please enter a new output directory:\n"
                                   "Leave blank for output to screen\n\t")
                
                #if they leave the input blank, return a Null value
                if os_dir == '':
                    os_dir = None
                
                #otherwise try this function again
                else:
                    prep_out_dir(out_dir)
    
    return(out_dir)
    
def prep_out_file(modes,source="",ind_var="",plot="",dims="",channel="",
                  freq=0.0,
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

    if freq != 0.0:
        out_file_path= out_file_path + "_" + str(freq).replace(".","-")+"Hz"
        
    #sets the file extension based on file type
    if out_type != "":
        if "." not in out_type:
            out_file_path= out_file_path + "." + out_type   
        else:
            out_file_path= out_file_path + out_type 
    return (out_file_path)

def read_OSO_h5 (filename):
    '''
    This function reads in the data from an OSO-supplied HDF5 file and converts
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
    d_time=[]
    freq_list=[]
    xx_list=[]
    xy_list=[]
    yy_list=[]

    #creates an index for the time stamps
    time_index=0
    
    #creates lists from the file
    f_start_list = list(f["timeaccstart"])
    f_freq_list = list(f['frequency'])
    f_xx=list(f['XX'])
    f_xy=list(f['XY'])
    f_yy=list(f['YY'])

    #identifies the start time.  Times in HDF5 are stored as floats since the
    #epoch of Jan 01 00:00:00 1970
    min_time=pd.to_datetime(min(f_start_list),unit='s')
    
    #this shouldn't be needed in the final product, included durind calibration
    #mismatch issues
    #min_freq=min(list(f['frequency']))
    
    #Iterates over the time values in the HDF5 file
    for time_val in f_start_list:
        #(re-)initialises the index for frequencies in the HDF5 file
        freq_index=0
        #Iterates over the frequency values in the HDF5 file
        for freq_val in f_freq_list:
            time_stamp_val=pd.to_datetime(time_val,unit='s')
            #appends the values from the iterators for Time and Frequency
            time_list.append(time_stamp_val)
            d_time.append((time_stamp_val-min_time)/np.timedelta64(1,'s')) #useful for calculations


            '''
            #Code removed after corrections to lightcurve generation software
            
            #leave this here for possible tests in case there are issues later
           
            freq_list.append(min_freq+(freq_index*(1e8/512.0)))
            
            
            ##This is the correct code to process from the file
            #
            '''            
            freq_list.append(freq_val)
            
            #uses the indices to find the correct values for XX, XY and YY
            xx_list.append(f_xx[time_index][freq_index])
            xy_list.append(f_xy[time_index][freq_index])
            yy_list.append(f_yy[time_index][freq_index])
            
            #increments the indices
            freq_index = freq_index+1
        time_index=time_index+1
    
    #creates the data frame by pasting the lists together    
    out_df=pd.DataFrame(data={'Time':time_list, 'd_Time':d_time, 
                                'Freq':freq_list,
                                'xx':xx_list,'xy':xy_list,'yy':yy_list})


        
    #returns the data frame
    return(out_df)

def read_var_file(file_name,modes,source):
    '''
    This function reads in the filename and checks the suffix.  Depending on
    the suffix chosen, it calls different file reader functions
    '''
    suffix=file_name.rsplit('.',1)[1]
    if 'csv'==suffix:
        out_df=read_dreambeam_csv(file_name)
    elif 'hdf5'==suffix:
        out_df=read_OSO_h5(file_name)    
    else:
        print (file_name+" is not an appropriate file")
        out_df=pd.DataFrame(data={"none":[]})
    
    source_options = ['b']
    source_options.append(source)
    
    if any (c in modes['crop_data'] for c in source_options):
        #always crops zero values, may crop high values depending on user input
        out_df=crop_vals(out_df,modes)
    if any (c in modes['norm_data'] for c in source_options):    
        for channel in ['xx','xy','yy']:
            #normalises the dataframe
            out_df=normalise_data(out_df,modes,channel)    
    
    return(out_df)


def merge_dfs(model_df,scope_df,modes):
    '''
    This function takes a dataframe created from the dream_beam model and one
    created from the scope and merges them into a single dataframe using the 
    time and frequency as the joining variables. In the merged dataframe are
    calculated the p- and q-channel intensities & the differences between them.
    Finally, a time difference from the start time is calculated.
    
    The merged dataframe is then returned
    
    '''
    #merges the two datagrames using time and frequency
    merge_df=pd.merge(model_df,scope_df,on=('Time','Freq'),suffixes=('_model','_scope'))
    if len(merge_df) > 0:
        merge_df=calc_xy(merge_df,modes)
        merge_df=calc_stokes(merge_df,modes)
        
        if 'd_Time' not in merge_df:
            #creates a variable to hold the time since the start of the plot
            #this is necessary for plots that are not compatible with Timestamp data
            start_time=min(merge_df['Time'])
            merge_df['d_Time']=(merge_df.Time-start_time)/np.timedelta64(1,'s')
    else:
        print("ERROR: NO MATCHING DATA: CLOSING")
    return(merge_df)        



def calc_xy(merge_df,modes):
    
    '''
    Calculates the XY parameters for the model from the JNN values and 
    normalises the XY parameters from the scope so they are comparable.  
    
    NOTE: this version makes no allowance for outliers or smoothing in the
    scope data.  This may be added to future versions
    
    '''


    #calculates the differences
    for channel in ["xx","xy","yy"]:
        calc_diff(merge_df, modes, channel)
    #note the d_Time is already calculated
    return (merge_df)

def calc_stokes(merge_df,modes):
    '''
    this function calculates the Stokes UVIQ parameters for each time and 
    frequency in a merged dataframe
    '''

    for source in ["model","scope"]:
        #Stokes U is the real component of the XY
        merge_df['U_'+source]=np.real(merge_df['xy_'+source])
        #Stokes V is the imaginary component of the XY
        merge_df['V_'+source]=np.imag(merge_df['xy_'+source])
        
        #Stokes I is the sum of XX and YY
        merge_df['I_'+source]=merge_df['xx_'+source]+merge_df['yy_'+source]
        #Stokes Q is the difference between XX and YY
        merge_df['Q_'+source]=merge_df['xx_'+source]-merge_df['yy_'+source]

    for channel in ["U","V","I","Q"]:
        calc_diff(merge_df, modes, channel)    
    return (merge_df)

def normalise_data(merge_df,modes,channel,out_str=""):
    '''
    This function normalises the data for the scope according to the 
    normalisation mode specified.  These options are detailed belwo
    '''
    if 'o' in modes['norm'] :
        #normalises by dividing by the maximum
        merge_df[channel+out_str]=merge_df[channel]/np.max((plottable(merge_df[channel])))
    elif 'f' in modes['norm']:
        #normalises by dividing by the maximum for each frequency
        var_str='Freq'
        norm_operation(merge_df, var_str,channel,out_str)
    elif 't' in modes['norm']:
        #normalises by dividing by the maximum for each frequency
        var_str='Time'
        norm_operation(merge_df, var_str,channel,out_str)
    elif 'n' in modes ['norm']:
        pass     #nothing to be done       
    else:
        print("WARNING: Normalisation mode not specified correctly!")
 
    return (merge_df)

def norm_operation(in_df, var_str,channel,out_str=""):
    '''
    This function carries out the normalisation operation based on the input 
    which specifies which variable to normalise over.  
    '''

    #identifies allthe unique values of the variable in the column
    unique_vals=in_df[var_str].unique()
    

    #iterates over all unique values
    for unique_val in unique_vals:

        unique_max = np.max(plottable(in_df.loc[(in_df[var_str]==unique_val),channel]))

        if unique_max !=0:
            in_df.loc[(in_df[var_str]==unique_val),(channel+out_str)]=in_df.loc[(in_df[var_str]==unique_val),channel]/unique_max
        else:
            in_df.loc[(in_df[var_str]==unique_val),(channel+out_str)]=0

def crop_vals(in_df,modes):
    '''
    This function drops all rows where the value for the channel is greater 
    than the MEDIAN for that channel by thenumber of times specified by the 
    cropping argument
    
    This function also removes all 0.0 values for the various channels.
    '''
    if 'o' in modes["crop_basis"]:
        out_df=crop_operation (in_df,modes)
    elif 'f' in modes["crop_basis"]:
        var_str='Freq'
        unique_vals=in_df[var_str].unique()
        out_df= pd.DataFrame(columns=in_df.columns)
        for col in in_df:
            out_df[col]=out_df[col].astype(in_df[col].dtypes.name)
        for unique_val in unique_vals:
            unique_df=in_df.loc[(in_df.Freq==unique_val),:].copy()
            out_df=out_df.append(crop_operation (unique_df,modes))
        out_df.reset_index(drop=True, inplace=True) 
    else:
        out_df=crop_operation (in_df,modes)
    
    return(out_df)

def crop_operation (in_df,modes):
    out_df=in_df.copy()
    #goes through all the columns of the data
    for col in out_df:
        #targets the dependent variables
        if col not in ['Time','Freq','d_Time']:
            #drops all zero values from the data
            out_df.drop(out_df[out_df[col] == 0.0].index, inplace=True)
            #if the cropping mode isn't set to 0, crop the scope data
            if 0.0 != modes['crop']:
                if modes['crop_type']=="median":
                    col_limit = np.median(out_df[col])*modes['crop']
                elif modes['crop_type']=="mean":
                    col_limit = np.mean(out_df[col])*modes['crop']
                elif modes['crop_type']=="percentile":
                    if modes['crop'] <100:
                        col_limit = np.percentile(out_df[col],modes['crop'])
                    else:
                        print("WARNING: Percentile must be less than 100")
                        col_limit = np.max(plottable(out_df[col]))
                else:
                    print("WARNING: crop_type incorrectly specified.")
                    col_limit = np.median(out_df[col])*modes['crop']
                out_df.drop(out_df[out_df[col] > col_limit].index, inplace=True)
            
    return(out_df)

    
def calc_diff(merge_df, modes, channel):
    '''
    Calculates the difference between the model and scope values for the 
    '''
    
    if modes['diff']=='sub':
        merge_df[channel+'_diff']=(merge_df[channel+"_model"])-(merge_df[channel+"_scope"])
    elif modes['diff']=='div':
        merge_df[channel+'_diff']=(merge_df[channel+"_model"])/((merge_df[channel+"_scope"])+0.0)
    elif modes['diff']=='idiv':
        merge_df[channel+'_diff']=(merge_df[channel+"_scope"])/((merge_df[channel+"_model"])+0.0)
    else:
        print("Difference mode "+str(modes['diff'])+" incorrectly specified.  "
              "Defaulting to subtraction mode.")
        merge_df[channel+'_diff']=(merge_df[channel+"_model"])-(merge_df[channel+"_scope"])
    
if __name__ == "__main__":
    #gets the command line arguments for the scope and model filename
    modes=beam_arg_parser()
    

    
    #read in the csv files from DreamBeam and format them correctly
    model_df=read_var_file(modes['in_file_model'],modes,"m")
    



    #read in the file from the scope using variable reader
    scope_df=read_var_file(modes['in_file_scope'],modes,"s")
    
    #adjusts for the offset if needed (e.g. comparing two observations)
    offset=np.timedelta64(modes['offset'],'s')
    scope_df.Time=scope_df.Time-offset
  
    
    #merges the dataframes
    merge_df=merge_dfs(model_df, scope_df, modes)
    
    if modes['freq'] !=[0.0]:
        #drops all frequencies which do not match the filter if applicable
        merge_df=merge_df[merge_df['Freq'].isin(modes['freq'])]
        merge_df.reset_index(drop=True, inplace=True)
    
    if modes['freq_file'] != "":
        freq_df=pd.read_csv(modes['freq_file'], header=None)
        merge_df=merge_df[merge_df['Freq'].isin(freq_df[0])]
        merge_df.reset_index(drop=True, inplace=True)
    
    #identifies the keys with _diff suffix
    m_keys=get_df_keys(merge_df,"_diff", modes)
    
    
    if  len(merge_df)>0:
        #runs different functions if there are one or multiple frequencies
        if merge_df.Freq.nunique()==1:
            #if only one frequency, does one-dimensional analysis
            analysis_1d(merge_df,modes, m_keys)
        else: #otherwise does multi-dimensional analysis
            if "each" in modes['values']: #if the plots are to be separate
                for key in m_keys: #analyses them one at a time
                    ind_dfs=analysis_nd(merge_df,modes, [key])
            else: #allows plots to be overlaid 
                ind_dfs=analysis_nd(merge_df,modes, m_keys)
    
        #output the dataframe if requested
        if modes['out_dir']!=None:
            path_out_df = prep_out_file(modes,out_type=".csv")
            try:
                merge_df.to_csv(path_out_df)
            except IOError:
                print("WARNING: unable to output to file:\n\t"+path_out_df)
                
    else:
        print("ERROR: NO DATA AVAILABLE TO ANALYSE!\nEXITING")
    