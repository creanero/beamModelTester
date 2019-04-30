# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 12:47:37 2018

@author: Oisin Creaner
"""

import h5py
import pandas as pd
import numpy as np

from utility_functions import plottable
from utility_functions import get_source_separator

from graphing_functions import identify_plots

import sys


def read_dreambeam_csv(in_file,modes):
    '''
    This function reads in csv files output by dreambeam into a formatted 
    dataframe
    
    DreamBeam format described at 
    https://github.com/creaneroDIAS/beamModelTester/blob/multi-frequency-upgrade/DreamBeam_Source_data_description.md
    '''
    if modes['verbose'] >=2:
        print("Reading in CSV file: "+in_file)
    out_df=pd.read_csv(in_file,\
                        converters={'J11':complex,'J12':complex,\
                                    'J21':complex,'J22':complex}, \
                        parse_dates=['Time'], skipinitialspace=True)   
    
    
    '''
    calculates the xx, xy, yx and yy parameters for the model from the JNN 
    values Using the formulae below
     B = [[XX, XY] ,[YX, YY]]
     J = [[J11,J12],[J21,J22]]
     B = J * J'
     XX= (J11 *  ̅J̅1̅1 )+ (J12 *  ̅J̅1̅2 )
     XY= (J11 *  ̅J̅2̅1 )+ (J12 *  ̅J̅2̅2 )
     YX= (J21 *  ̅J̅1̅1 )+ (J22 *  ̅J̅1̅2 )
     YY= (J21 *  ̅J̅2̅1 )+ (J22 *  ̅J̅2̅2 )
        
    #yx_model not calculated for two reasons
    # 1. xy equal to within floating point errors
    # 2. yx not included in scope data (presumably because of 1.)
    #merge_df['yx_model']=merge_df.J21*np.conj(merge_df.J11)+merge_df.J22*np.conj(merge_df.J12)
    '''
    out_df=calc_xy(out_df)
    
    if 'd_Time' not in out_df:
        #creates a variable to hold the time since the start of the plot
        #this is necessary for plots that are not compatible with Timestamp data
        start_time=min(out_df['Time'])
        out_df['d_Time']=(out_df.Time-start_time)/np.timedelta64(1,'s')
        
    return out_df

def read_OSO_h5 (file_name, modes):
    '''
    This function reads in the data from an OSO-supplied HDF5 file and converts
    it into a data frame. This data is then returned to the calling function
    
    Inputs: file name containing the path to a HDF5 file
    Outputs: Data Frame containing time, frequency, xx, xy and yy values
    
    This function uses slightly crude methods, and probably needs to be 
    updated with a more straightforward conversion from HDF5 to a dataframe
    '''
    if modes['verbose'] >=2:
        print("Reading in HDF5 file: "+file_name)
    #'/home/creanero/outputs/observations/OSO/2018-03-16T11_26_11_acc2bst_rcu5_CasA_dur2587_ct20161220.hdf5'
    #Reads in the designated HDF5 file
    f = h5py.File(file_name, 'r')
    
    #Creates lists to hold the contents of the various HDF5 datasets within the
    #file.  These are then merged to form the data frame.
    time_list=[]
    d_time=[]
    freq_list=[]
    xx_list=[]
    xy_list=[]
    yy_list=[]

    #creates an index for the time stamps
    time_index=0
    
    #creates lists from the file
    f_start_list = list(f["timeaccstart"])
    f_freq_list = list(f['frequency'])
    f_xx=list(f['XX'])
    f_xy=list(f['XY'])
    f_yy=list(f['YY'])

    #identifies the start time.  Times in HDF5 are stored as floats since the
    #epoch of Jan 01 00:00:00 1970
    min_time=pd.to_datetime(min(f_start_list),unit='s')
    
    #this shouldn't be needed in the final product, included durind calibration
    #mismatch issues
    #min_freq=min(list(f['frequency']))
    
    #Iterates over the time values in the HDF5 file
    for time_val in f_start_list:
        #(re-)initialises the index for frequencies in the HDF5 file
        freq_index=0
        #Iterates over the frequency values in the HDF5 file
        for freq_val in f_freq_list:
            time_stamp_val=pd.to_datetime(time_val,unit='s')
            #appends the values from the iterators for Time and Frequency
            time_list.append(time_stamp_val)
            d_time.append((time_stamp_val-min_time)/np.timedelta64(1,'s')) #useful for calculations


            '''
            #Code removed after corrections to lightcurve generation software
            
            #leave this here for possible tests in case there are issues later
           
            freq_list.append(min_freq+(freq_index*(1e8/512.0)))
            
            
            ##This is the correct code to process from the file
            #
            '''            
            freq_list.append(freq_val)
            
            #uses the indices to find the correct values for XX, XY and YY
            xx_list.append(f_xx[time_index][freq_index])
            xy_list.append(f_xy[time_index][freq_index])
            yy_list.append(f_yy[time_index][freq_index])
            
            #increments the indices
            freq_index = freq_index+1
        time_index=time_index+1
    
    #creates the data frame by pasting the lists together    
    out_df=pd.DataFrame(data={'Time':time_list, 'd_Time':d_time, 
                                'Freq':freq_list,
                                'xx':xx_list,'xy':xy_list,'yy':yy_list})


        
    #returns the data frame
    return(out_df)

def read_var_file(file_name,modes):
    '''
    This function reads in the filename and checks the suffix.  Depending on
    the suffix chosen, it calls different file reader functions
    '''
    if modes['verbose'] >=2:
        print("Determining file type for: "+file_name)
    
    #creates a blank dataframe for use in several non-readable cases    
    blank_df=pd.DataFrame(data={"none":[]})

    #Tries to get the file extension    
    try:
        suffix=file_name.rsplit('.',1)[1]
    #if there's no extension, returns the empty string
    except IndexError:
        suffix=""
    
    #sets the blank dataframe 
    out_df=blank_df    
    if '' == file_name:
        pass # return the blank data frame
    elif 'csv'==suffix:
        try:
            out_df=read_dreambeam_csv(file_name, modes)
        except IOError:
            print("Error: file "+file_name+" unable to load as DreamBeam CSV")
    elif 'hdf5'==suffix:
        try:
            out_df=read_OSO_h5(file_name, modes)    
        except IOError:
            print("Error: file "+file_name+" unable to load as OSO HDF5 format")
            
    else:
        if modes['verbose'] >=1:
            print ("Warning: \""+file_name+"\" is not an appropriate file")
        #out_df=blank_df #no longer needed
    
    if "none" in out_df:
        pass
    else:
       
        #calculates the stokes parameters for the dataframe
        out_df=calc_stokes(out_df,modes)
    
    return(out_df)

def crop_and_norm(in_df,modes,origin):
    '''
    this funtion returns a data frame that has been normalised based on the 
    options in modes
    '''
    origin_options = ['b']
    origin_options.append(origin)
    
    out_df=in_df.copy()
    
    if any (c in modes['crop_data'] for c in origin_options):
        #always crops zero values, may crop high values depending on user input
        out_df = crop_vals(out_df,modes)
    if any (c in modes['norm_data'] for c in origin_options):    
        for channel in ["xx","xy","yy"]:
            # normalises the dataframe
            out_df = normalise_data(out_df,modes,channel)
        # recalculates the Stokes Parameters for the normalised values
        out_df = calc_stokes(out_df,modes)
    return(out_df)

def merge_crop_test(model_df, scope_df, modes):
    """
    This function takes in the model and scope data frames, and based on 
    whether they have contents, returns a merge_df which is either the 
    result of merging the two dataframes or the contents of the only DF if only
    one has been supplied.
    
    It also returns sources, which defines whether the model, the scope or the
    difference is to be plotted.  When only one file is provided, sources is 
    a list containing the empty string, which means values are plotted from the
    only dataframe that was loaded with no suffix
    """
    if "none" not in scope_df:        
        # adjusts for the offset if needed (e.g. comparing two observations)
        # creates a backup of the time
        if "original_Time" not in scope_df.columns.values:
            scope_df["original_Time"]=scope_df.Time.copy()
            # then changes the time value based on the offset
            offset=np.timedelta64(modes['offset'],'s')
            scope_df.Time=scope_df.original_Time-offset
        else:
            # then changes the time value based on the offset
            offset=np.timedelta64(modes['offset'],'s')
            scope_df.Time=scope_df.original_Time-offset
    if "none" not in model_df and "none" not in scope_df:
        # merges the dataframes
        merge_df=merge_dfs(model_df, scope_df, modes)
        
        # identifies the sources required
        sources = identify_plots(modes)
        
    # if only scope is valid
    elif "none" in model_df and "none" not in scope_df:
        merge_df=crop_and_norm(scope_df,modes,"s")
        sources = [""]  # sets the source to blank as there are no differentiators
    elif "none" not in model_df and "none" in scope_df:
        merge_df=crop_and_norm(model_df,modes,"m")
        sources = [""]
    else: #Both blank
        if modes['verbose'] >=1:
            print("ERROR: No data available in either file")
        if modes['interactive']<=1: #in low interactivity modes
            sys.exit(1)
        else:
            merge_df=pd.DataFrame(data={"none":[]})
            sources=[""]
            #in high interactivity modes, will be able to create new data later
    return(merge_df, sources)
    
    
def merge_dfs(model_df,scope_df,modes):
    '''
    This function takes a dataframe created from the dream_beam model and one
    created from the scope and merges them into a single dataframe using the 
    time and frequency as the joining variables. In the merged dataframe are
    calculated the p- and q-channel intensities & the differences between them.
    Finally, a time difference from the start time is calculated.
    
    The merged dataframe is then returned
    
    '''
    if modes['verbose'] >=2:
        print("Merging data from scope and source")
        
        
    #crops and normalises the scope and model data if needed
    scope_df_clean=crop_and_norm(scope_df,modes,"s")
    model_df_clean=crop_and_norm(model_df,modes,"m")
    
    
    #merges the two datagrames using time and frequency
    merge_df=pd.merge(model_df_clean,scope_df_clean,on=('Time','Freq'),
                      suffixes=('_model','_scope'))
    if len(merge_df) > 0:
        #calculates differences between model and scope values for each channel
        for channel in ["xx","xy","yy","U","V","I","Q"]:
            calc_diff(merge_df, modes, channel)
        if 'd_Time' not in merge_df:
            #creates a variable to hold the time since the start of the plot
            #this is necessary for plots that are not compatible with Timestamp data
            start_time=min(merge_df['Time'])
            merge_df['d_Time']=(merge_df.Time-start_time)/np.timedelta64(1,'s')
    else:
        if modes['verbose'] >=1:
            print("ERROR: NO MATCHING DATA")
    return(merge_df)        


def crop_vals(in_df,modes):
    '''
    This function drops all rows where the value for the channel is greater 
    than the MEDIAN for that channel by thenumber of times specified by the 
    cropping argument
    
    This function also removes all 0.0 values for the various channels.
    '''
    if modes['verbose'] >=2:
        print("Cropping values")
    if 'o' in modes["crop_basis"]:
        if modes['verbose'] >=2:
            print("Crop basis: Overall")
        out_df=crop_operation (in_df,modes)
    elif 'f' in modes["crop_basis"]:
        if modes['verbose'] >=2:
            print("Crop basis: Frequency")
        var_str='Freq'
        unique_vals=in_df[var_str].unique()
        out_df= pd.DataFrame(columns=in_df.columns)
        for col in in_df:
            out_df[col]=out_df[col].astype(in_df[col].dtypes.name)
        for unique_val in unique_vals:
            unique_df=in_df.loc[(in_df[var_str]==unique_val),:].copy()
            out_df=out_df.append(crop_operation (unique_df,modes))
    elif 't' in modes["crop_basis"]:
        if modes['verbose'] >=2:
            print("Crop basis: Time")
        var_str='Time'
        unique_vals=in_df[var_str].unique()
        out_df= pd.DataFrame(columns=in_df.columns)
        for col in in_df:
            out_df[col]=out_df[col].astype(in_df[col].dtypes.name)
        for unique_val in unique_vals:
            unique_df=in_df.loc[(in_df[var_str]==unique_val),:].copy()
            out_df=out_df.append(crop_operation (unique_df,modes))        
    else:
        out_df=crop_operation (in_df,modes)
        
        
    out_df.reset_index(drop=True, inplace=True) 
    return(out_df)

def crop_operation (in_df,modes):
    if modes['verbose'] >=2:
        print("Carrying out Crop Operation")
    out_df=in_df.copy()
    #goes through all the columns of the data
    for col in out_df:
        #targets the dependent variables
        if col not in ['Time', 'Freq', 'd_Time', 'original_Time']:
            #drops all zero values from the data
            out_df.drop(out_df[out_df[col] == 0.0].index, inplace=True)
            #if the cropping mode isn't set to 0, crop the scope data
            if 0.0 != modes['crop']:
                if modes['crop_type'] == "median":
                    col_limit = np.median(out_df[col])*modes['crop']
                elif modes['crop_type'] == "mean":
                    col_limit = np.mean(out_df[col])*modes['crop']
                elif modes['crop_type'] == "percentile":
                    if modes['crop'] < 100:
                        col_limit = np.percentile(out_df[col], modes['crop'])
                    else:
                        if modes['verbose'] >=1:
                            print("WARNING: Percentile must be less than 100")
                        col_limit = np.max(plottable(out_df[col]))
                else:
                    if modes['verbose'] >=1:
                        print("WARNING: crop_type incorrectly specified.")
                    col_limit = np.median(out_df[col])*modes['crop']
                out_df.drop(out_df[out_df[col] > col_limit].index, inplace=True)
                # out_df.drop(out_df[out_df[col] < 0].index, inplace=True)
            
    return(out_df)

    
def calc_xy(in_df):
    out_df = in_df.copy()
    out_df['xx'] = np.real(out_df.J11*np.conj(out_df.J11)+out_df.J12*np.conj(out_df.J12))
    out_df['xy'] = out_df.J11*np.conj(out_df.J21)+out_df.J12*np.conj(out_df.J22)
    out_df['yy'] = np.real(out_df.J21*np.conj(out_df.J21)+out_df.J22*np.conj(out_df.J22))
    return(out_df)


def calc_stokes(in_df,modes={'verbose':2},sources=[""]):
    '''
    this function calculates the Stokes UVIQ parameters for each time and 
    frequency in a merged dataframe
    '''
    out_df = in_df.copy()
    if modes['verbose'] >=2:
        print("Calculating Stokes Parameters")

    for source in sources:
        sep=get_source_separator(source)
        # Stokes U is the real component of the XY
        out_df['U'+sep+source] = np.real(in_df['xy'+sep+source])
        # Stokes V is the imaginary component of the XY
        out_df['V'+sep+source] = np.imag(in_df['xy'+sep+source])
        
        # Stokes I is the sum of XX and YY
        out_df['I'+sep+source] = in_df['xx'+sep+source]+in_df['yy'+sep+source]
        # Stokes Q is the difference between XX and YY
        out_df['Q'+sep+source] = in_df['xx'+sep+source]-in_df['yy'+sep+source]

    return (out_df)


def normalise_data(merge_df,modes,channel,out_str=""):
    '''
    This function normalises the data for the scope according to the 
    normalisation mode specified.  These options are detailed belwo
    '''
    if modes['verbose'] >=2:
        print("Normalising data")
    if 'o' in modes['norm'] :
        if modes['verbose'] >=2:
            print("Normalisation basis: Overall")
        #normalises by dividing by the maximum
        merge_df[channel+out_str]=merge_df[channel]/np.max((plottable(merge_df[channel])))
    elif 'f' in modes['norm']:
        if modes['verbose'] >=2:
            print("Normalisation basis: Frequency")
        #normalises by dividing by the maximum for each frequency
        var_str='Freq'
        norm_operation(merge_df, var_str,channel,modes,out_str)
    elif 't' in modes['norm']:
        if modes['verbose'] >=2:
            print("Normalisation basis: time")
        #normalises by dividing by the maximum for each frequency
        var_str='Time'
        norm_operation(merge_df, var_str,channel,modes,out_str)
    elif 'n' in modes ['norm']:
        if modes['verbose'] >=2:
            print("Normalisation basis: None")
        pass     #nothing to be done       
    else:
        if modes['verbose'] >=1:
            print("WARNING: Normalisation mode not specified correctly!")
 
    return (merge_df)

def norm_operation(in_df, var_str,channel,modes,out_str=""):
    '''
    This function carries out the normalisation operation based on the input 
    which specifies which variable to normalise over.  
    '''

    if modes['verbose'] >=2:
        print("Carrying out normalisation")
    #identifies allthe unique values of the variable in the column
    unique_vals=in_df[var_str].unique()
    

    #iterates over all unique values
    for unique_val in unique_vals:

        unique_max = np.max(plottable(in_df.loc[(in_df[var_str]==unique_val),channel]))

        if unique_max !=0:
            in_df.loc[(in_df[var_str]==unique_val),(channel+out_str)]=in_df.loc[(in_df[var_str]==unique_val),channel]/unique_max
        else:
            in_df.loc[(in_df[var_str]==unique_val),(channel+out_str)]=0

def calc_diff(merge_df, modes, channel):
    '''
    Calculates the difference between the model and scope values for the given 
    channel
    '''
    
    if modes['verbose'] >=2:
        print("Calculating differences between scope and model for "+channel)
    if modes['diff']=='sub':
        merge_df[channel+'_diff']=(merge_df[channel+"_model"])-(merge_df[channel+"_scope"])
    elif modes['diff']=='div':
        merge_df[channel+'_diff']=(merge_df[channel+"_model"])/((merge_df[channel+"_scope"])+0.0)
    elif modes['diff']=='idiv':
        merge_df[channel+'_diff']=(merge_df[channel+"_scope"])/((merge_df[channel+"_model"])+0.0)
    else:
        if modes['verbose'] >=1:
            print("Warning: Difference mode "+str(modes['diff'])+
                  " incorrectly specified.  Defaulting to subtraction mode.")
        merge_df[channel+'_diff']=(merge_df[channel+"_model"])-(merge_df[channel+"_scope"])
        
        
if __name__ == "__main__":
    print("Warning: this script only defines functions.")        
