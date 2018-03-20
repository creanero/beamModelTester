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

def plot_p_q_values_1f(merge_df):
    '''
    This function takes a merged dataframe as an argument and plots a two part
    graph of the P- and Q-channel values for the model and the scope against 
    time.
    
    This plot is only usable and valid if the data is ordered in time and has 
    only a single frequency
    '''
    #creates a two part plot of the values of model and scope
    #part one: plots the model and scope values for p-channel against time
    plt.figure()
    plt.title("Plot of the values in p- and q-channels over time")
    plt.subplot(211)
    plt.title("p-channel")
    #plots the p-channel in one colour
    plt.plot(merge_df.Time,merge_df.p_ch_model,label='model',
             color=colour_models('p_light'))
    plt.plot(merge_df.Time,merge_df.p_ch_scope,label='scope',
             color=colour_models('p_dark'))
    plt.legend(frameon=False)
    #removes axis labels: the two plots share an x-axis
    plt.xticks([])
    
    #part two: plots the model and scope values for q-channel against time
    plt.subplot(212)
    plt.title("q-channel")
    #plots the q-channel in another colour
    plt.plot(merge_df.Time,merge_df.q_ch_model,label='model',
             color=colour_models('q_light'))
    plt.plot(merge_df.Time,merge_df.q_ch_scope,label='scope',
             color=colour_models('q_dark'))
    
    #plots the axis labels rotated so they're legible
    plt.xticks(rotation=90)
    plt.legend(frameon=False)
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
    plt.plot(merge_df.Time,merge_df.p_ch_diff,label=r'$\Delta p$',
             color=colour_models('p'))
    plt.plot(merge_df.Time,merge_df.q_ch_diff,label=r'$\Delta q$',
             color=colour_models('q'))
    #plots the axis labels rotated so they're legible
    plt.xticks(rotation=90)
    
    #calculates and adds title with frequency in MHz
    plt.title("Plot of the differences in p- and q-channels over time at %.0f MHz"%(merge_df.Freq[0]/1e6))
    plt.legend(frameon=False)
    plt.xlabel('Time')
    plt.show()
    return(0)
    
    
    
    
def merge_dfs(model_df,scope_df):
    '''
    This function takes a dataframe created from the dream_beam model and one
    created from the scope and merges them into a single dataframe using the 
    time and frequency as the joining variables. In the merged dataframe are
    calculated the p- and q-channel intensities & the differences between them.
    Finally, a time difference from the start time is calculated.
    
    The merged dataframe is then returned
    
    NOTE this module currently uses DreamBeam type output for the scope input
    data.  If this changes, then changes may be needed to this module
    '''
    #merges the two datagrames using time and frequency
    merge_df=pd.merge(model_df,scope_df,on=('Time','Freq'),suffixes=('_model','_scope'))
    
    #calculates the p-channel intensity as per DreamBeam for both model and scope
    merge_df['p_ch_model'] = np.abs(merge_df.J11_model)**2+np.abs(merge_df.J12_model)**2
    merge_df['p_ch_scope'] = np.abs(merge_df.J11_scope)**2+np.abs(merge_df.J12_scope)**2
    #calculates the difference between model and scope
    merge_df['p_ch_diff'] = merge_df.p_ch_model - merge_df.p_ch_scope
    
    #calculates the q-channel intensity as per DreamBeam for both model and scope
    merge_df['q_ch_model'] = np.abs(merge_df.J21_model)**2+np.abs(merge_df.J22_model)**2
    merge_df['q_ch_scope'] = np.abs(merge_df.J21_scope)**2+np.abs(merge_df.J22_scope)**2
    #calculates the difference between model and scope
    merge_df['q_ch_diff'] = merge_df.q_ch_model - merge_df.q_ch_scope
    
    #creates a variable to hold the time since the start of the plot
    #this is necessary for plots that are not compatible with Timestamp data
    start_time=min(merge_df.Time)
    merge_df['d_Time']=(merge_df.Time-start_time)/np.timedelta64(1,'s')
    
    return(merge_df)



    
def calc_corr_1d(merge_df):
    '''
    This function takes a merged dataframe as an argument and 
    calculates the pearson correlation coeffiecient between scope 
    and model
    '''
    #using [0] from the pearsonr to return the correlation coefficient, but not
    #the 2-tailed p-value stored in [1]
    p_corr=pearsonr(merge_df.p_ch_model,merge_df.p_ch_scope)[0]
    q_corr=pearsonr(merge_df.q_ch_model,merge_df.q_ch_scope)[0]
    
    return(p_corr,q_corr)
    
    
    
    
def calc_corr_nd(merge_df, var_str):
    '''
    This function calculates the correlation between the scope and model values
    for p- and q-channel as they are distributed against another column of the 
    dataframe merge_df which is identified by var_str
    
    in current versions, useable values for var_str are "Time" and "Freq"
    '''
    
    #creates empty lists for the correlations
    p_corrs=[]
    q_corrs=[]
    
    #identifies allthe unique values of the variable in the column
    unique_vals=merge_df[var_str].unique()
    
    #iterates over all unique values
    for unique_val in unique_vals:
        #creates a dataframe with  only the elements that match the current 
        #unique value
        unique_merge_df=merge_df[merge_df[var_str]==unique_val]
        #uses this unique value for and the 1-dimensional calc_corr_1d function
        #to calculate the correlations for each channel
        p_corr,q_corr=calc_corr_1d(unique_merge_df)
        
        #appends these to the list
        p_corrs.append(p_corr)
        q_corrs.append(q_corr)
    
    #creates an overlaid plot of how the correlation of between model and scope
    #varies for each of the p-and q-channels against var_str
    plt.figure()
    plt.title("Plot of the correlations in p- and q-channels over "+var_str)
    
    #uses colour codes for the correlations
    plt.plot(unique_vals,p_corrs,label='p_correlation',color=colour_models('p'))
    plt.plot(unique_vals,q_corrs,label='q_correlation',color=colour_models('q'))
    
    #rotates the labels.  This is necessary for timestamps
    plt.xticks(rotation=90)
    plt.legend(frameon=False)
    plt.xlabel(var_str)
    
    #prints the plot
    plt.show()
    
    #returns the correlation lists if needed    
    return (p_corrs,q_corrs)    
    



def calc_rmse_1d(merge_df):
    '''
    This function takes a merged dataframe as an argument and 
    calculates and returns the root mean square difference between scope and 
    model
    '''
    p_rmse=np.mean(merge_df.p_ch_diff**2)**0.5
    q_rmse=np.mean(merge_df.q_ch_diff**2)**0.5
    return(p_rmse,q_rmse)
 
    
    
    
def calc_rmse_nd(merge_df, var_str):
    '''
    This function calculates the correlation between the scope and model values
    for p- and q-channel  as they are distributed against another column of the 
    dataframe merge_df which is identified by var_str
    
    in current versions, useable values for var_str are "Time" and "Freq"
    '''
    
    #creates empty lists for the Errors
    p_rmses=[]
    q_rmses=[]
    
    
    #identifies allthe unique values of the variable in the column
    unique_vals=merge_df[var_str].unique()
    
    #iterates over all unique values
    for unique_val in unique_vals:
        #creates a dataframe with  only the elements that match the current 
        #unique value
        unique_merge_df=merge_df[merge_df[var_str]==unique_val]
        #uses this unique value for and the 1-dimensional calc_corr_1d function
        #to calculate the RMSE for each channel
        p_rmse,q_rmse=calc_rmse_1d(unique_merge_df)
        
        #appends these to the list
        p_rmses.append(p_rmse)
        q_rmses.append(q_rmse)
    
    #creates an overlaid plot of how the correlation of between model and scope
    #varies for each of the p-and q-channels against var_str    
    plt.figure()
    plt.title("Plot of the RMSE in p- and q-channels over "+var_str)
    
    #uses colour codes for the correlations
    plt.plot(unique_vals,p_rmses,label='p_RMSE',color=colour_models('p'))
    plt.plot(unique_vals,q_rmses,label='q_RMSE',color=colour_models('q'))
    
    #rotates the labels.  This is necessary for timestamps
    plt.xticks(rotation=90)
    plt.legend(frameon=False)
    plt.xlabel(var_str)
    
    #prints the plot
    plt.show()
    
    #returns the correlation lists if needed    
    return (p_rmses,q_rmses)    




def plot_diff_values_nf(merge_df):
    '''
    This function creates two 3d colour plots using time and frequency from a 
    merged data frame as the independent variables and the difference between
    source and model as the dependent (colour) variable 
    '''
    #create a plot with two subplots
    plt.figure()
    
    #top subplot for P-channel
    plt.subplot(211)
    #display main title and subplot title together
    plt.title("Plot of the differences in p- and q-channel over time and frequency\np-channel")
    #plots p-channel difference
    plt.tripcolor(merge_df.d_Time,merge_df.Freq,merge_df.p_ch_diff,
                  cmap=plt.get_cmap(colour_models('ps')))
    plt.ylabel("Frequency")
    #blanks x labels on p-channel plot as x-axis is shared
    plt.xticks([])
    
    #bottom subplot is q-channel
    plt.subplot(212)
    plt.title("q-channel")
    #plots p-channel differences
    plt.tripcolor(merge_df.d_Time,merge_df.Freq,merge_df.q_ch_diff,
                  cmap=plt.get_cmap(colour_models('qs')))
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
    #plots the p and q values
    plot_p_q_values_1f(merge_df)
    
    #plots the differences in the values
    plot_diff_values_1f(merge_df)
    
    #calculates the pearson correlation coefficient between scope and model
    p_corr,q_corr=calc_corr_1d(merge_df)
    print("\nThe P-channel correlation is %f\nThe Q-channel correlation is %f"
          %(p_corr,q_corr))
    
    #calculates the root mean squared error between scope and model
    p_rmse,q_rmse=calc_rmse_1d(merge_df)
    print("\nThe P-channel RMSE is %f\nThe Q-channel RMSE is %f"
          %(p_rmse,q_rmse))
    
    
def analysis_nd(merge_df):
    #using 1-d versions to provide an overall perspective
    #calculates the pearson correlation coefficient between scope and model
    p_corr,q_corr=calc_corr_1d(merge_df)
    print("\nThe overall P-channel correlation is %f\nThe overall Q-channel correlation is %f"%(p_corr,q_corr))
    
    #calculates the root mean squared error between scope and model
    p_rmse,q_rmse=calc_rmse_1d(merge_df)
    print("\nThe overall P-channel RMSE is %f\nThe overall Q-channel RMSE is %f"%(p_rmse,q_rmse))

    plot_diff_values_nf(merge_df)
    
    p_corrs,q_corrs=calc_corr_nd(merge_df,"Freq")
    p_rmses,q_rmses=calc_rmse_nd(merge_df,"Freq")
    
    p_corrs,q_corrs=calc_corr_nd(merge_df,"Time")
    p_rmses,q_rmses=calc_rmse_nd(merge_df,"Time")    

 
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
    
    #sets Red, Purple and Blue as colour maps for XX, XY and YY values
    if 'xx'==colour_id:
        return('Reds')    
    if 'xy'==colour_id:
        return('Purples')
    if 'yy'==colour_id:
        return('Blues')
    
    #returns black as a default
    else:
        print("Warning: Colour incorrectly specified.  Defaulting to Black")
        return ('black')    
    
if __name__ == "__main__":
    #User input the filenames - probably want to parameterise this.
    in_file_model=raw_input("Please enter the model filename:\n")#"~/outputs/test/dreamBeam/2018-03-05/SE607_1d_160M.csv"
    in_file_scope=raw_input("Please enter the scope filename:\n")#"~/outputs/test/dreamBeam/2018-03-05/IE613_1d_160M.csv"
    
    #read in the csv files from DreamBeam and format them correctly
    #want to modularise this
    model_df=read_dreambeam_csv(in_file_model)
    
    #using dreambeam input initially, will replace this with something suited to real telescope input if possible
    scope_df=read_dreambeam_csv(in_file_scope)
    
    #merges the dataframes
    merge_df=merge_dfs(model_df, scope_df)
    
    #runs different functions if there are one or multiple frequencies
    if merge_df.Freq.nunique()==1:
        #if only one frequency, does one-dimensional analysis
        analysis_1d(merge_df)
    else:
        #otherwise does multi-dimensional analysis
        analysis_nd(merge_df)