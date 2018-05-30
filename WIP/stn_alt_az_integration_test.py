#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 19:17:51 2018

@author: creanero
"""

stn_alt_az=[horizon_to_station(stnid, merge_df.az[i], merge_df.alt[i]) for i in range(len(merge_df.alt))]


stn_alt_az_t=zip(*stn_alt_az)

stn_alt=np.array(stn_alt_az_t[1])*180/np.pi
stn_az=np.array(stn_alt_az_t[0])*180/np.pi

merge_df['stn_alt']=stn_alt
merge_df['stn_az']=stn_az


time_delay = 1000.0/modes['frame_rate']
source = 'scope'

animated_plot(merge_df, modes, 'az', m_keys, "Freq", source, 
                              time_delay, plot_name = "az")
four_var_plot(merge_df,modes,"stn_az","Freq",'Q',"stn_alt",source)