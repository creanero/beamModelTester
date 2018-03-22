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
    return out_df

def get_df_keys(merge_df,key_str):
    m_keys=[]
    for m_key in merge_df.keys():
        if key_str in m_key:
            m_keys.append(m_key.split(key_str)[0])
    return(m_keys)

def plot_values_1f(merge_df):
    '''
    This function takes a merged dataframe as an argument and plots a graph of
    each of the various values for the model and the scope against time.
    
    This plot is only usable and valid if the data is ordered in time and has 
    only a single frequency
    '''
    
    m_keys=get_df_keys(merge_df,"_diff")
    
    for key in m_keys:
        #creates a two part plot of the values of model and scope
        #part one: plots the model and scope values for p-channel against time
        plt.figure()
        plt.title("Plot of the values in "+key+"-channel over time")

        #plots the p-channel in one colour
        plt.plot(merge_df.Time,merge_df[key+'_model'],label='model',
                 color=colour_models(key+'_light'))
        plt.plot(merge_df.Time,merge_df[key+'_scope'],label='scope',
                 color=colour_models(key+'_dark'))
        plt.legend(frameon=False)
        #plots the axis labels rotated so they're legible
        plt.xticks(rotation=90)
        plt.xlabel('Time')
        
        #prints the plot
        plt.show()
    return(0)
    
    
    
    
def plot_diff_values_1f(merge_df):
    '''
    This function takes a merged dataframe as an argument and 
    plots the differences in p-channel and q-channel values over time
    
    This plot is only usable and valid if the data is ordered in time and has 
    only a single frequency
    '''
    
    m_keys=get_df_keys(merge_df,"_diff")

    plt.figure()
    
    graph_title = "Plot of the differences in "
    for key in m_keys:
        plt.plot(merge_df.Time,
                 merge_df[key+'_diff'], 
                 label=r'$\Delta $'+key,
                 color=colour_models(key))
        if (m_keys.index(key) < (len(m_keys)-2)) :
            graph_title=graph_title+key+", "
        elif m_keys.index(key)==(len(m_keys)-2):
            graph_title=graph_title+key+" & "
        else:
            graph_title=graph_title+key
    
    #calculates and adds title with frequency in MHz
    
    graph_title=graph_title+"-channels over time at %.0f MHz"%(merge_df.Freq[0]/1e6)    
    
    


    
    #plots the axis labels rotated so they're legible
    plt.xticks(rotation=90)

    plt.title(graph_title)
    plt.legend(frameon=False)
    plt.xlabel('Time')
    plt.show()
    return(0)
    
    
    
#   
#def merge_dfs(model_df,scope_df):
#    '''
#    This function takes a dataframe created from the dream_beam model and one
#    created from the scope and merges them into a single dataframe using the 
#    time and frequency as the joining variables. In the merged dataframe are
#    calculated the p- and q-channel intensities & the differences between them.
#    Finally, a time difference from the start time is calculated.
#    
#    The merged dataframe is then returned
#    
#    NOTE this module currently uses DreamBeam type output for the scope input
#    data.  If this changes, then changes may be needed to this module
#    '''
#    #merges the two datagrames using time and frequency
#    merge_df=pd.merge(model_df,scope_df,on=('Time','Freq'),suffixes=('_model','_scope'))
#    
#    #calculates the p-channel intensity as per DreamBeam for both model and scope
#    merge_df['p_model'] = np.abs(merge_df.J11_model)**2+np.abs(merge_df.J12_model)**2
#    merge_df['p_scope'] = np.abs(merge_df.J11_scope)**2+np.abs(merge_df.J12_scope)**2
#    #calculates the difference between model and scope
#    merge_df['p_diff'] = merge_df.p_model - merge_df.p_scope
#    
#    #calculates the q-channel intensity as per DreamBeam for both model and scope
#    merge_df['q_model'] = np.abs(merge_df.J21_model)**2+np.abs(merge_df.J22_model)**2
#    merge_df['q_scope'] = np.abs(merge_df.J21_scope)**2+np.abs(merge_df.J22_scope)**2
#    #calculates the difference between model and scope
#    merge_df['q_diff'] = merge_df.q_model - merge_df.q_scope
#    
#    #creates a variable to hold the time since the start of the plot
#    #this is necessary for plots that are not compatible with Timestamp data
#    start_time=min(merge_df.Time)
#    merge_df['d_Time']=(merge_df.Time-start_time)/np.timedelta64(1,'s')
#    
#    return(merge_df)
#


    
def calc_corr_1d(merge_df):
    '''
    This function takes a merged dataframe as an argument and 
    calculates the pearson correlation coeffiecients between scope 
    and model
    '''
    
    
    m_keys=get_df_keys(merge_df,"_diff")
    corr_outs=[]
    for key in m_keys:
        #uses absolute values as real values cannot be negative and complex 
        #values cannot be plotted
        corr_outs.append(pearsonr(abs(merge_df[key+'_model']),
                                  abs(merge_df[key+'_scope']))[0])
    #using [0] from the pearsonr to return the correlation coefficient, but not
    #the 2-tailed p-value stored in [1]
    
    return(corr_outs)
    
    
    
    
def calc_corr_nd(merge_df, var_str):
    '''
    This function calculates the correlation between the scope and model values
    for p- and q-channel as they are distributed against another column of the 
    dataframe merge_df which is identified by var_str
    
    in current versions, useable values for var_str are "Time" and "Freq"
    '''
    #identifies the keys with _diff suffix
    m_keys=get_df_keys(merge_df,"_diff")
        
    #creates empty lists for the correlations
    n_corrs=[]
    for i in range(len(m_keys)):
        n_corrs.append([])
    
    

    #identifies allthe unique values of the variable in the column
    unique_vals=merge_df[var_str].unique()
    
    #iterates over all unique values
    for unique_val in unique_vals:
        #creates a dataframe with  only the elements that match the current 
        #unique value
        unique_merge_df=merge_df[merge_df[var_str]==unique_val]
        #uses this unique value for and the 1-dimensional calc_corr_1d function
        #to calculate the correlations for each channel
        n_corr=calc_corr_1d(unique_merge_df)
        
        #appends these to the list
        for i in range(len(m_keys)):
            n_corrs[i].append(n_corr[i])

    #creates an overlaid plot of how the correlation of between model and scope
    #varies for each of the channels against var_str
    plt.figure()

    graph_title = "Plot of the correlation in "
    for key in m_keys:    
        plt.plot(unique_vals,n_corrs[m_keys.index(key)],
                label=key+'_correlation',color=colour_models(key))
        
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
    
    #prints the plot
    plt.show()
    
    #returns the correlation lists if needed    
    return (n_corrs)    
    



def calc_rmse_1d(merge_df):
    '''
    This function takes a merged dataframe as an argument and 
    calculates and returns the root mean square difference between scope and 
    model
    '''
    m_keys=get_df_keys(merge_df,"_diff")
    rmse_outs=[]
    for key in m_keys:
        rmse_outs.append(np.mean(merge_df[key+'_diff']**2)**0.5)
   
    return(rmse_outs)
 
    
    
    
def calc_rmse_nd(merge_df, var_str):
    '''
    This function calculates the correlation between the scope and model values
    for p- and q-channel  as they are distributed against another column of the 
    dataframe merge_df which is identified by var_str
    
    in current versions, useable values for var_str are "Time" and "Freq"
    '''
    
    #identifies the keys with _diff suffix
    m_keys=get_df_keys(merge_df,"_diff")
        
    #creates empty lists for the Errors
    n_rmses=[]
    for i in range(len(m_keys)):
        n_rmses.append([])
    
    
    
    #identifies allthe unique values of the variable in the column
    unique_vals=merge_df[var_str].unique()
    
    #iterates over all unique values
    for unique_val in unique_vals:
        #creates a dataframe with  only the elements that match the current 
        #unique value
        unique_merge_df=merge_df[merge_df[var_str]==unique_val]
        #uses this unique value for and the 1-dimensional calc_corr_1d function
        #to calculate the RMSE for each channel
        n_rmse=calc_rmse_1d(unique_merge_df)
        
        #appends these to the list
        for i in range(len(m_keys)):
            n_rmses[i].append(n_rmse[i])
    
    #creates an overlaid plot of how the correlation of between model and scope
    #varies for each of the p-and q-channels against var_str    
    plt.figure()
    graph_title = "Plot of the RMSE in "
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
    
    #prints the plot
    plt.show()
    
    #returns the correlation lists if needed    
    return (n_rmses)




def plot_diff_values_nf(merge_df):
    '''
    This function creates 3d colour plots using time and frequency from a 
    merged data frame as the independent variables and the difference between
    source and model as the dependent (colour) variable 
    '''
    
    #identifies the keys with _diff suffix
    m_keys=get_df_keys(merge_df,"_diff")    
    
    for key in m_keys:
        #create a plot with two subplots
        plt.figure()
        
        #display main title and subplot title together
        plt.title("Plot of the differences in %s over time and frequency"%key)
        #plots p-channel difference
        plt.tripcolor(merge_df.d_Time,merge_df.Freq,abs(merge_df[key+'_diff']),
                      cmap=plt.get_cmap(colour_models(key+'s')))

        #plots x-label for both using start time 
        plt.xlabel("Time in seconds since start time\n"+str(min(merge_df.Time)))
        plt.ylabel("Frequency")
        plt.show()

def analysis_1d(merge_df):
    '''
    This function carries out all plotting and calculations needed for a 1-d 
    dataset (i.e. one frequency)
    
    Future iterations may include optional arguments to enable selection of the
    plots that are preferred
    '''
    #plots the values for each channel
    plot_values_1f(merge_df)
    
    #plots the differences in the values
    plot_diff_values_1f(merge_df)
    
    #identifies the keys with _diff suffix
    m_keys=get_df_keys(merge_df,"_diff")    
    
    #calculates the pearson correlation coefficient between scope and model
    corrs=calc_corr_1d(merge_df)
    
    for i in range(len(m_keys)):
        print("The %s-channel correlation is %f"%(m_keys[i],corrs[i]))

    print("\n")    
    #calculates the root mean squared error between scope and model
    rmses=calc_rmse_1d(merge_df)
    for i in range(len(m_keys)):
        print("The %s-channel RMSE is %f" %(m_keys[i],rmses[i]))
    
    
def analysis_nd(merge_df):
    '''
    This function carries out all plotting and calculations needed for a n-d 
    dataset (i.e. multiple frequencies)
    
    Future iterations may include optional arguments to enable selection of the
    plots that are preferred
    '''
        
    #identifies the keys with _diff suffix
    m_keys=get_df_keys(merge_df,"_diff")
    
    #calculates the pearson correlation coefficient between scope and model
    corrs=calc_corr_1d(merge_df)
    #prints that coefficient for each key and correlation
    for i in range(len(m_keys)):
        print("The %s-channel correlation is %f"%(m_keys[i],corrs[i]))

    #newline to separate outputs
    print("\n")  
        
    #calculates the root mean squared error between scope and model
    rmses=calc_rmse_1d(merge_df)
    for i in range(len(m_keys)):
        print("The %s-channel RMSE is %f" %(m_keys[i],rmses[i]))

    #plots the differences in values for the various channels
    plot_diff_values_nf(merge_df)
    
    #calculates the correlations and rmse over time at each frequency 
    #return values are stored as possible future outputs
    n_corrs_freq=calc_corr_nd(merge_df,"Freq")
    n_rmses_freq=calc_rmse_nd(merge_df,"Freq")
    n_freq=merge_df.Freq.unique()
    freq_df=pd.DataFrame(data={"Freq":n_freq})
    for key in m_keys:
        freq_df[key+'_corr']=n_corrs_freq[m_keys.index(key)]
        freq_df[key+'_RMSE']=n_rmses_freq[m_keys.index(key)]
    
    #calculates the correlations and rmse over frequency at each time 
    #return values are stored as possible future outputs
    n_corrs_time=calc_corr_nd(merge_df,"Time")
    n_rmses_time=calc_rmse_nd(merge_df,"Time")
    n_time=merge_df.Time.unique()
    time_df=pd.DataFrame(data={"Time":n_time})
    for key in m_keys:
        time_df[key+'_corr']=n_corrs_time[m_keys.index(key)]
        time_df[key+'_RMSE']=n_rmses_time[m_keys.index(key)]
    
    return (freq_df,time_df)
    
    
    

 
def colour_models(colour_id):
    '''
    The colours used are defined in a function that returns the colour strings
    '''
    #sets oranges for various applications for the P channel
    if 'p'==colour_id:
        return('orange')
    if 'p_light'==colour_id:
        return('sandybrown')
    if 'p_dark'==colour_id:
        return('darkorange')
    if 'ps'==colour_id:
        return('Oranges')
        
    #sets greens for various applications of the Q channel    
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
    
    #returns black as a default
    else:
        print("Warning: Colour incorrectly specified.  Defaulting to Black")
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
                             help="The file containing the data from the model (Usually DreamBeam)")
    group_model.add_argument("--model","-m", 
                             help="Alternative way of specifying the file containing the data from the model")
    
    
    #creates a group for the scope filename
    group_scope = parser.add_mutually_exclusive_group()
    
    #gives positional and optional ways of providing the scope data 
    group_scope.add_argument("scope_p",nargs='?', default=None, 
                             help="The file containing the observed data from the telescope")
    group_scope.add_argument("--scope","-s", 
                             help="Alternative way of specifying the file containing the observed data from the telescope")
    
    
    #passes these arguments to a unified variable
    args = parser.parse_args()
    
    #outputs the filename for the model to a returnable variable
    if args.model_p != None:
        in_file_model=args.model_p
    elif args.model != None:
        in_file_model=args.model
    else:
        in_file_model=raw_input("No model filename specified:\n"
                                "Please enter the model filename:\n")
    
    
    #outputs the filename for the scope to a returnable variable
    if args.scope_p != None:
        in_file_scope=args.scope_p
    elif args.scope != None:
        in_file_scope=args.scope
    else:
        in_file_scope=raw_input("No filename specified for observed data from the telescope:\n"
                                "Please enter the telescope filename:\n")
    
    return(in_file_model,in_file_scope)


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
    d_time=[]
    freq_list=[]
    xx_list=[]
    xy_list=[]
    yy_list=[]

    #creates an index for the time stamps
    time_index=0

    #identifies the start time.  Times in HDF5 are stored as floats since the
    #epoch of Jan 01 00:00:00 1970
    min_time=pd.to_datetime(min(list(f["timeaccstart"])),unit='s')
    
    #this shouldn't be needed in the final product, included durind calibration
    #mismatch issues
    min_freq=min(list(f['frequency']))
    
    #Iterates over the time values in the HDF5 file
    for time_val in list(f["timeaccstart"]):
        #(re-)initialises the index for frequencies in the HDF5 file
        freq_index=0
        #Iterates over the frequency values in the HDF5 file
        for freq_val in list(f['frequency']):
            time_stamp_val=pd.to_datetime(time_val,unit='s')
            #appends the values from the iterators for Time and Frequency
            time_list.append(time_stamp_val)
            d_time.append((time_stamp_val-min_time)/np.timedelta64(1,'s')) #useful for calculations



            #TTTTTTT         FFFFFFF iii       
            #  TTT    oooo   FF          xx  xx
            #  TTT   oo  oo  FFFF    iii   xx  
            #  TTT   oo  oo  FF      iii   xx  
            #  TTT    oooo   FF      iii xx  xx            
            #TODO: Fix and replace once HDF5 writer is fixed
            
            freq_list.append(min_freq+(freq_index*(1e8/512.0)))
            
            
            ##This is the correct code to process from the file
            #freq_list.append(freq_val)
            
            #uses the indices to find the correct values for XX, XY and YY
            xx_list.append(f['XX'][time_index][freq_index])
            xy_list.append(f['XY'][time_index][freq_index])
            yy_list.append(f['YY'][time_index][freq_index])
            
            #increments the indices
            freq_index = freq_index+1
        time_index=time_index+1
    
    #creates the data frame by pasting the lists together    
    scope_df=pd.DataFrame(data={'Time':time_list, 'd_Time':d_time, 
                                'Freq':freq_list,
                                'xx':xx_list,'xy':xy_list,'yy':yy_list})
    
    #returns the data frame
    return(scope_df)

def read_var_file(file_name):
    suffix=file_name.rsplit('.',1)[1]
    if 'csv'==suffix:
        out_df=read_dreambeam_csv(file_name)
    if 'hdf5'==suffix:
        out_df=read_OSO_h5(file_name)    
    return(out_df)


def merge_dfs(model_df,scope_df):
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
    if 'J11_scope' in merge_df:
        merge_df=calc_pq(merge_df)
    elif 'xx' in merge_df:
        merge_df=calc_xy(merge_df)
    
    return(merge_df)        

def calc_pq(merge_df):
    '''
    Calculates the P and Q channel intensities as per dreamBeam, and from there
    calculates the differeces in each channel, as well as the time since start
    '''
    
    #calculates the p-channel intensity as per DreamBeam for both model and scope
    merge_df['p_model'] = np.abs(merge_df.J11_model)**2+np.abs(merge_df.J12_model)**2
    merge_df['p_scope'] = np.abs(merge_df.J11_scope)**2+np.abs(merge_df.J12_scope)**2
    #calculates the difference between model and scope
    merge_df['p_diff'] = merge_df.p_model - merge_df.p_scope
    
    #calculates the q-channel intensity as per DreamBeam for both model and scope
    merge_df['q_model'] = np.abs(merge_df.J21_model)**2+np.abs(merge_df.J22_model)**2
    merge_df['q_scope'] = np.abs(merge_df.J21_scope)**2+np.abs(merge_df.J22_scope)**2
    #calculates the difference between model and scope
    merge_df['q_diff'] = merge_df.q_model - merge_df.q_scope
    
    #creates a variable to hold the time since the start of the plot
    #this is necessary for plots that are not compatible with Timestamp data
    start_time=min(merge_df.Time)
    merge_df['d_Time']=(merge_df.Time-start_time)/np.timedelta64(1,'s')
    
    return (merge_df)


def calc_xy(merge_df):
    
    '''
    Calculates the XY parameters for the model from the JNN values and 
    normalises the XY parameters from the scope so they are comparable.  
    
    NOTE: this version makes no allowance for outliers or smoothing in the
    scope data.  This may be added to future versions
    
    calculates the xx, xy, yx and yy parameters for the model from the JNN 
    values Using the formulae below
     B = [[XX, XY] ,[YX, YY]]
     J = [[J11,J12],[J21,J22]]
     B = J * J'
     XX= (J11 *  ̅J̅1̅1 )+ (J12 *  ̅J̅1̅2 )
     XY= (J11 *  ̅J̅2̅1 )+ (J12 *  ̅J̅2̅2 )
     YX= (J21 *  ̅J̅1̅1 )+ (J22 *  ̅J̅1̅2 )
     YY= (J21 *  ̅J̅2̅1 )+ (J22 *  ̅J̅2̅2 )
    '''
    merge_df['xx_model']=merge_df.J11*np.conj(merge_df.J11)+merge_df.J12*np.conj(merge_df.J12)
    merge_df['xy_model']=merge_df.J11*np.conj(merge_df.J21)+merge_df.J12*np.conj(merge_df.J22)
    merge_df['yx_model']=merge_df.J21*np.conj(merge_df.J11)+merge_df.J22*np.conj(merge_df.J12)
    merge_df['yy_model']=merge_df.J21*np.conj(merge_df.J21)+merge_df.J22*np.conj(merge_df.J22)
    
    #normalises by dividing by the maximum
    merge_df['xx_scope']=merge_df.xx/np.max(merge_df.xx)
    merge_df['xy_scope']=merge_df.xy/np.max(merge_df.xy)
    merge_df['yy_scope']=merge_df.yy/np.max(merge_df.yy)
    
    #calculates the differences
    merge_df['xx_diff']=abs(merge_df.xx_model)-abs(merge_df.xx_scope)
    merge_df['xy_diff']=abs(merge_df.xy_model)-abs(merge_df.xy_scope)
    merge_df['yy_diff']=abs(merge_df.yy_model)-abs(merge_df.yy_scope)
    
    #note the d_Time is already calculated
    return (merge_df)
    
if __name__ == "__main__":
    #gets the command line arguments for the scope and model filename
    in_file_model,in_file_scope=beam_arg_parser()
    
    #read in the csv files from DreamBeam and format them correctly
    model_df=read_var_file(in_file_model)
    
    #read in the file from the scope using variable reader
    scope_df=read_var_file(in_file_scope)
    
    #merges the dataframes
    merge_df=merge_dfs(model_df, scope_df)
    
    #runs different functions if there are one or multiple frequencies
    if merge_df.Freq.nunique()==1:
        #if only one frequency, does one-dimensional analysis
        analysis_1d(merge_df)
    else:
        #otherwise does multi-dimensional analysis
        analysis_nd(merge_df)