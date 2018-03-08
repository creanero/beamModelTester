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
from mpl_toolkits.mplot3d import Axes3D

def read_dreambeam_csv(in_file):
    '''
    This function reads in csv files output by dreambeam into a formatted dataframe
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
    time
    '''
    #creates a two part plot of the values of model and scope
    #part one: plots the model and scope values for p-channel against time
    plt.figure()
    plt.title("Plot of the values in p- and q-channels over time")
    plt.subplot(211)
    plt.title("p-channel")
    plt.plot(merge_df.Time,merge_df.p_ch_model,label='model',color='orangered')
    plt.plot(merge_df.Time,merge_df.p_ch_scope,label='scope',color='darkred')
    plt.legend(frameon=False)
    plt.xticks([])
    
    #part two: plots the model and scope values for q-channel against time
    plt.subplot(212)
    plt.title("q-channel")
    plt.plot(merge_df.Time,merge_df.q_ch_model,label='model',color='limegreen')
    plt.plot(merge_df.Time,merge_df.q_ch_scope,label='scope',color='darkgreen')
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
    '''
    plt.plot(merge_df.Time,merge_df.p_ch_diff,label=r'$\Delta p$',color='red')
    plt.plot(merge_df.Time,merge_df.q_ch_diff,label=r'$\Delta q$',color='green')
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
    The merged dataframe is then returned
    
    NOTE this module currently uses DreamBeam type output for the scope input
    data.  If this changes, then changes may be needed to this module
    '''
    #merges the two datagrames using time and frequency
    merge_df=pd.merge(model_df,scope_df,on=('Time','Freq'),suffixes=('_model','_scope'))
    
    #calculates the p-channel intensity as per DreamBeam for both model and scope
    merge_df.p_ch_model = np.abs(merge_df.J11_model)**2+np.abs(merge_df.J12_model)**2
    merge_df.p_ch_scope = np.abs(merge_df.J11_scope)**2+np.abs(merge_df.J12_scope)**2
    #calculates the difference between model and scope
    merge_df.p_ch_diff = merge_df.p_ch_model - merge_df.p_ch_scope
    
    #calculates the q-channel intensity as per DreamBeam for both model and scope
    merge_df.q_ch_model = np.abs(merge_df.J21_model)**2+np.abs(merge_df.J22_model)**2
    merge_df.q_ch_scope = np.abs(merge_df.J21_scope)**2+np.abs(merge_df.J22_scope)**2
    #calculates the difference between model and scope
    merge_df.q_ch_diff = merge_df.q_ch_model - merge_df.q_ch_scope
    
    return(merge_df)

    
def calc_corr_1d(merge_df):
    '''
    This function takes a merged dataframe as an argument and 
    calculates and prints the pearson correlation coeffiecient between scope and model
    '''
    
    p_corr=pearsonr(merge_df.p_ch_model,merge_df.p_ch_scope)[0]
    q_corr=pearsonr(merge_df.q_ch_model,merge_df.q_ch_scope)[0]
    print("\nThe P-channel correlation is %f\nThe Q-channel correlation is %f"%(p_corr,q_corr))
    return(p_corr,q_corr)
    
def calc_rmse_1d(merge_df):
    '''
    This function takes a merged dataframe as an argument and 
    calculates and prints the root mean square difference between scope and model
    '''
    p_rmse=np.mean(merge_df.p_ch_diff**2)**0.5
    q_rmse=np.mean(merge_df.q_ch_diff**2)**0.5
    print("\nThe P-channel RMSE is %f\nThe Q-channel RMSE is %f"%(p_rmse,q_rmse))
    
    
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
    
    #does slightly different things if there are one or multiple frequencies
    if merge_df.Freq.nunique()==1:
        #plots the p and q values
        plot_p_q_values_1f(merge_df)
        
        #plots the differences in the values
        plot_diff_values_1f(merge_df)
        
        #calculates the pearson correlation coefficient between scope and model
        calc_corr_1d(merge_df)
        
        #calculates the root mean squared error between scope and model
        calc_rmse_1d(merge_df)
    else:
        pass
    #implement functionality for multi-frequency use, then replace
        
