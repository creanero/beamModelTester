#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 10:15:22 2018

@author: creanero
"""

merge_df.d_Time=(merge_df.Time-merge_df.Time[0])/np.timedelta64(1,'s')
plt.tripcolor(merge_df.d_Time,merge_df.Freq,list(merge_df.q_ch_diff))
