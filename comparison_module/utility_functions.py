# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 13:08:14 2018

@author: User
"""

def plottable(in_series, col_name=""):
    '''
    produces plot and print friendly versions of variables
    '''
    if col_name == "":
        #if it is a single series, tides up the complex components
        out_series = clean_complex(in_series)
    elif col_name == "Freq":
        if str(type(in_series))=="<class 'pandas.core.frame.DataFrame'>":
            out_series = in_series[col_name]/1e6
        else:
            out_series = in_series/1e6
    else:
        if str(type(in_series))=="<class 'pandas.core.frame.DataFrame'>":
            out_series = clean_complex(in_series[col_name])
        else:
            out_series = clean_complex(in_series)
    return(out_series)

def clean_complex(in_series):
    '''
    turns a complex series into a series of absolute values, but just returns a
    real number
    '''    
    try:
        out_series=in_series.reset_index(drop=True)
    except AttributeError: #if reset index doesn't work
        out_series=in_series
    if len(out_series)>0:
        if 'complex' in str(type(out_series[0])):
            out_series =  abs(in_series)
        else:
            out_series =  in_series
    else:
        out_series = abs(in_series)
    return (out_series)
    