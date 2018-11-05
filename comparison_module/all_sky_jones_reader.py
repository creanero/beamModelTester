#!/usr/bin/env python2


"""
Tool to visualise data from dreamBeam all sky mode
"""

import pandas as pd
import numpy as np
from reading_functions import calc_xy
from reading_functions import calc_stokes
from graphing_functions import plot_3d_graph

np.seterr(divide='ignore', invalid='ignore')

def read_odd(in_line):
    split_line=in_line.split(" ")
    jones_strs=split_line[1:5]
    jones_outs=[]
    for jones in jones_strs:
        jones_outs.append(complex(jones))
    return(jones_outs)


def read_even(in_line):
    split_line=in_line.split(" ")
    alt_az_strs=split_line[2:4]
    alt_az_outs=[]
    for alt_az in alt_az_strs:
        alt_az_outs.append(np.degrees(float(alt_az)))
    return(alt_az_outs)


#in_file_name=raw_input("Please enter the file name for reading:\t")
in_file_name="/home/creanero/outputs/test/dreamBeam/2018-10-15/FoV_jones/test.out" #for quick testing
in_file=open(in_file_name, "r")
out_dir_name="/home/creanero/outputs/test/dreamBeam/2018-10-15/FoV_jones/" #for quick testing

in_lines=in_file.readlines()

in_file.close()

jones_line = [0,0,0,0]
alt_az_line=[0,0]

out_list=[]

modes={'verbose':2,'three_d':'colour','title':'','title_':'','out_dir':out_dir_name,'image_type':'png'}
source=""

for line_index in range(len(in_lines)):
    if line_index % 2: #line_index % 2 = 1 i.e. odd
        jones_line=read_odd(in_lines[line_index])
        out_line = alt_az_line + jones_line
        out_list.append(out_line)
    else: #line_index % 2 = 0 i.e. even
        alt_az_line=read_even(in_lines[line_index])
headers=["az","alt","J11","J12","J21","J22"]

out_df=pd.DataFrame(out_list, columns=headers)

out_df=calc_xy(out_df)
out_df=calc_stokes(out_df,modes)

keys=["xx","xy","yy","U","V","I","Q"]


var_x='az'
var_y='alt'
for key in keys:
    plot_3d_graph(out_df, key, modes, source, var_x, var_y)
#print(out_df)
