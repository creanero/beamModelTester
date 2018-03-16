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

filename = '/home/creanero/outputs/observations/OSO/2018-03-16T11_26_11_acc2bst_rcu5_CasA_dur2587_ct20161220.hdf5'
f = h5py.File(filename, 'r')

# List all groups
print("Keys: %s" % f.keys())
#group_key = list(f.keys())[0]

# NOTE: this is a hack-job.  Really need to find a cleaner way to read HDF5s 
#into data frames.  That being said, this should do the trick
time_list=[]
freq_list=[]
xx_list=[]
xy_list=[]
yy_list=[]
time_index=0
min_time=min(list(f["timeaccstart"]))

# Get the data
for time_val in list(f["timeaccstart"]):
    freq_index=0
    for freq_val in list(f['frequency']):
        time_list.append(time_val-min_time)
        freq_list.append(freq_val)
        xx_list.append(f['XX'][time_index][freq_index])
        xy_list.append(f['XY'][time_index][freq_index])
        yy_list.append(f['YY'][time_index][freq_index])
        freq_index = freq_index+1
    time_index=time_index+1
    
scope_df=pd.DataFrame(data={'time':time_list, 'freq':freq_list,'xx':xx_list,'xy':xy_list,'yy':yy_list})

plt.figure()
plt.tripcolor(scope_df.time,scope_df.freq,scope_df.xx,
              cmap=plt.get_cmap('Oranges'))
plt.title("Plot of XX against time and frequency without cleaning\nNOTE OUTLIERS")
plt.xlabel("Time since start time of\n"+time.ctime(min_time))
plt.ylabel("Frequency")
plt.show()


clean_df_xx=scope_df[scope_df.xx<np.mean(scope_df.xx)*2]
plt.tripcolor(clean_df_xx.time,clean_df_xx.freq,clean_df_xx.xx,
              cmap=plt.get_cmap('Blues'))
plt.title("Plot of XX against time and frequency after\nremoval of values above double the mean")
plt.xlabel("Time since start time of\n"+time.ctime(min_time))
plt.ylabel("Frequency")
plt.show()