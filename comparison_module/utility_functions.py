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
    
def get_source_separator(source):
    if source == "":
        sep = ""
    else:
        sep = "_"
    return (sep)

def get_df_keys(merge_df, modes={"values":"all"}):
    '''
    Calculates the keys from a given dataframe or based on the input modes.
    '''
    if modes['verbose'] >=2:
        print("Identifying channels to analyse")
    m_keys=[]
    
    #if key groups have been supplied, extend the keylist with their components
    if "all" in modes["values"]:
        m_keys.extend(["xx","xy","yy","U","V","I","Q"])
    else:
        if "stokes" in modes["values"]:
            m_keys.extend(["U","V","I","Q"])
        if "linear" in modes["values"]:
            m_keys.extend(["xx","xy","yy"])
       
        #if keys have been supplied individually                
        if "xx" in modes["values"]:
            m_keys.append("xx")
        if "xy" in modes["values"]:
            m_keys.append("xy")
        if "yy" in modes["values"]:
            m_keys.append("yy")
        if "U" in modes["values"]:
            m_keys.append("U")
        if "V" in modes["values"]:
            m_keys.append("V")
        if "I" in modes["values"]:
            m_keys.append("I")
        if "Q" in modes["values"]:
            m_keys.append("Q")
    
    
    #if the keys are still blank
    if m_keys == []:
        if modes['verbose'] >=1:
            print ("Warning, no appropriate keys found!")
    
    
    return(m_keys)