#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 08:24:36 2018

@author: creanero
"""

'''
This program reads in a DreamBeam csv file and a OSO HDF5 file and merges them
'''

from prototype_comparison_module_1d_0_1 import beam_arg_parser
from prototype_comparison_module_1d_0_1 import read_dreambeam_csv
from hdf5_opener_0_1 import read_OSO_h5
import pandas as pd
import numpy as np


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
    
    merge_df['xx_scope']=merge_df.xx/np.max(merge_df.xx)
    merge_df['xy_scope']=merge_df.xy/np.max(merge_df.xy)
    merge_df['yy_scope']=merge_df.yy/np.max(merge_df.yy)
    return (merge_df)

if __name__ == "__main__":
    #gets the command line arguments for the scope and model filename
    in_file_model,in_file_scope=beam_arg_parser()
    
    
    #read in the csv files from DreamBeam and format them correctly
    model_df=read_var_file(in_file_model)
    
    #read in the file from the scope using variable reader
    scope_df=read_var_file(in_file_scope)

    merge_df=merge_dfs(model_df,scope_df)