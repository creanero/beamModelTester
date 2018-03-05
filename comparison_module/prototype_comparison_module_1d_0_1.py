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


if __name__ == "__main__":
    #temporarily hard-coded filenames
    in_file_model="~/outputs/test/dreamBeam/2018-03-05/SE607_1d_160M.csv"
    in_file_scope="~/outputs/test/dreamBeam/2018-03-05/IE613_1d_160M.csv"
    
    #read in the csv files from DreamBeam and format them correctly
    #want to modularise this
    model_df=pd.read_csv(in_file_model,\
                        converters={u' J11':complex,u' J12':complex,\
                                    u' J21':complex,u' J22':complex}, \
                        parse_dates=[u'Time'])
    
    #using dreambeam input initially, will replace this with something suited to real telescope input if possible
    scope_df=pd.read_csv(in_file_scope,\
                        converters={u' J11':complex,u' J12':complex,\
                                    u' J21':complex,u' J22':complex}, \
                        parse_dates=[u'Time'])
    
    #merges the two datagrames using time and frequency
    merge_df=pd.merge(model_df,scope_df,on=(u'Time',u' Freq'),suffixes=('_model','_scope'))
    
    #calculates the p-channel intensity as per DreamBeam for both model and scope
    p_ch_model = np.abs(merge_df[u' J11_model'])**2+np.abs(merge_df[u' J12_model'])**2
    p_ch_scope = np.abs(merge_df[u' J11_scope'])**2+np.abs(merge_df[u' J12_scope'])**2
    #calculates the difference between model and scope
    p_ch_diff = p_ch_model - p_ch_scope
    
    #calculates the q-channel intensity as per DreamBeam for both model and scope
    q_ch_model = np.abs(merge_df[u' J21_model'])**2+np.abs(merge_df[u' J22_model'])**2
    q_ch_scope = np.abs(merge_df[u' J21_scope'])**2+np.abs(merge_df[u' J22_scope'])**2
    #calculates the difference between model and scope
    q_ch_diff = q_ch_model - q_ch_scope
    
    #creates a two part plot of the values of model and scope
    #part one: plots the model and scope values for p-channel against time
    plt.figure()
    plt.title("Plot of the values in p- and q-channels over time")
    plt.subplot(211)
    plt.title("p-channel")
    plt.plot(merge_df[u'Time'],p_ch_model,label='model',color='orangered')
    plt.plot(merge_df[u'Time'],p_ch_scope,label='scope',color='darkred')
    plt.legend(frameon=False)
    plt.xticks([])
    
    #part two: plots the model and scope values for q-channel against time
    plt.subplot(212)
    plt.title("q-channel")
    plt.plot(merge_df[u'Time'],q_ch_model,label='model',color='limegreen')
    plt.plot(merge_df[u'Time'],q_ch_scope,label='scope',color='darkgreen')
    plt.xticks(rotation=90)
    plt.legend(frameon=False)
    plt.xlabel('Time')
    
    #prints the plot
    plt.show()
    
    
    
    
    #plots the differences in p-channel and q-channel values over time
    plt.plot(merge_df[u'Time'],p_ch_diff,label=r'$\Delta p$',color='red')
    plt.plot(merge_df[u'Time'],q_ch_diff,label=r'$\Delta q$',color='green')
    plt.xticks(rotation=90)
    plt.title("Plot of the differences in p- and q-channels over time")
    plt.legend(frameon=False)
    plt.xlabel('Time')
    plt.show()
    
    #calculates the pearson correlation coefficient between scope and model
    p_corr=pearsonr(p_ch_model,p_ch_scope)[0]
    q_corr=pearsonr(q_ch_model,q_ch_scope)[0]
    print("\nThe P-channel correlation is %f\nThe Q-channel correlation is %f"%(p_corr,q_corr))
    
    #calculates the root mean squared error between scope and model
    p_rmse=np.mean(p_ch_diff**2)**0.5
    q_rmse=np.mean(q_ch_diff**2)**0.5
    print("\nThe P-channel RMSE is %f\nThe Q-channel RMSE is %f"%(p_rmse,q_rmse))
