# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 18:30:07 2018

@author: User
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#from animation_test import update

def animated_plot(merge_df, modes, var_x, var_ys, var_t, source, time_delay=20):
    fig, ax = plt.subplots()
    fig.set_tight_layout(True)
    


    
    min_y=0#min(merge_df[(var_y+"_"+source)].min(),0)
    max_y=merge_df[(var_ys[0]+"_"+source)].mean()
    ax.set_ylim(min_y,max_y)
    
    
    
    # Plot a scatter that persists (isn't redrawn) and the initial line.
    var_t_vals = np.sort(merge_df[var_t].unique())
    var_t_val=var_t_vals[0]
    var_x_vals =merge_df.loc[merge_df[var_t]==var_t_val,var_x].reset_index(drop=True)
    
    lines = []
    
    for i in range(len(var_ys)):
        var_y = var_ys[i]
        
        var_y_vals = plottable(merge_df.loc[merge_df[var_t]==var_t_val,
                                (var_y+"_"+source)].reset_index(drop=True))
    

        line, = ax.plot(var_x_vals, var_y_vals, color=colour_models(var_y))
        lines.append(line)

    ax.set_xlabel(var_x)
    ax.set_ylabel(channel_maker(var_ys,modes," "))    
 
    global anim
    if modes['out_dir']==None:
        repeat_option = False
    else:
        repeat_option = True
        
        
    anim = FuncAnimation(fig, update_a, frames=range(len(var_t_vals)), 
                         interval=time_delay,
                         fargs=(merge_df, modes, var_x, var_ys, var_t, 
                                source,lines,ax),
                         repeat=repeat_option)

    if modes['out_dir']!=None:
        str_channel = channel_maker(var_ys,modes)
        plt_file = prep_out_file(modes,source=source,plot="vals",dims="nd",
                               channel=str_channel,out_type="htm")
        anim.save(plt_file, dpi=80, writer='imagemagick')
    else:
        plt.show()# will just loop the animation forever.

    print("End of function")



def update_a(i,merge_df, modes, var_x, var_ys, var_t, source,lines,ax):
    print("test in update")
    var_t_vals = np.sort(merge_df[var_t].unique())
    var_t_val=var_t_vals[i]
    str_channel = channel_maker(var_ys,modes,", ")
    label = "Plot of "+str_channel+" against "+var_x+ " at\n"+var_t+" of "+str(var_t_val)

    var_x_vals = (merge_df.loc[merge_df[var_t]==var_t_val,var_x]).reset_index(drop=True)
    
    for i in range(len(var_ys)):
        var_y = var_ys[i]
        var_y_vals = (merge_df.loc[merge_df[var_t]==var_t_val,(var_y+"_"+source)]).reset_index(drop=True)

        lines[i].set_data(var_x_vals, var_y_vals)
    

    plt.title(label)

    

def main():
    var_t="d_Time"
    var_x="Freq"
    #var_y="xx"
    #var_y2="yy"
    var_ys=["xx"]
    source="scope"
    animated_plot(merge_df, modes, var_x, var_ys, var_t, source, time_delay=200)
    print("end of main")
main()