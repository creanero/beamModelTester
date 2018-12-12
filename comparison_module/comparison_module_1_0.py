#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 13:39:28 2018

@author: Oisin Creaner
"""

import pandas as pd

import argparse

import sys

# modules of this project
from reading_functions import read_var_file
from reading_functions import merge_crop_test

from utility_functions import get_df_keys

from interactive_ops import prep_out_dir
from io_functions import prep_out_file

from analysis_functions import analysis_1d
from analysis_functions import analysis_nd

from interactive_ops import interactive_operation
from interactive_ops import get_object
from interactive_ops import get_location

from alt_az_functions import calc_alt_az
from alt_az_functions import calc_alt_az_lofar


###############################################################################
#
# argument setting functions
#    
###############################################################################

def beam_arg_parser():
    """
    This function parses the arguments from the command line and returns the 
    file names for the model data and the scope data
    
    Several options are provided: Positional arguments, followed by optional
    arguments followed by interactive entry of the argument values.
    
    future expansions to arguments will allow the user to specify modes of 
    operation and the type of output generated
    """
    
    parser = argparse.ArgumentParser()

###############################################################################
# Verbosity
###############################################################################

    # adds an optional argument for verbosity
    parser.add_argument("--verbose", "-V", default=2, type=int,
                        choices = (0,1,2),
                             help='''
sets the level of verbosity for the program outputs.  
0 indicates silent mode
1 indicates to show warnings or errors only
2 gives verbose progress indicators
                             ''')   
   

###############################################################################
# Interactivity
###############################################################################

    # adds an optional argument for interactivity
    parser.add_argument("--interactive", "-I", default=3, type=int,
                        choices = (0,1,2,3),
                             help='''
sets the level of interactivity for the program inputs.  
0 indicates non-interactive mode
1 indicates to allow interactions when crucial elements are missing
2 indicates command line interactive mode
3 indicates graphical interface interactive mode 
                             ''')   
    
    
###############################################################################
# Model filenames
###############################################################################
    
    # creates a group for the model filename
    group_model = parser.add_mutually_exclusive_group()
    
    # gives positional and optional ways of providing the model data
    group_model.add_argument("model_p",nargs='?', default=None, 
                             help='''
The file containing the data from the model (Usually DreamBeam)
                             ''')
    group_model.add_argument("--model", "-m",
                             help='''
Alternative way of specifying the file containing the data from the model
                             ''')
    
###############################################################################
# Scope filenames
###############################################################################
    
    # creates a group for the scope filename
    group_scope = parser.add_mutually_exclusive_group()
    
    # gives positional and optional ways of providing the scope data
    group_scope.add_argument("scope_p",nargs='?', default=None, 
                             help='''
The file containing the observed data from the telescope
                             ''')
    group_scope.add_argument("--scope", "-s",
                             help='''
Alternative way of specifying the file containing the observed data from the 
telescope
                             ''')

###############################################################################
# Output filename, file type and plot titles
###############################################################################

    # adds an optional argument for output directory
    parser.add_argument("--out_dir", "-o", default=None,
                             help='''
path to a directory in which the output of the program is intended to be stored
.  IF this argument is blank, output is to std.out and plots are to screen.
                             ''')   

    # adds an optional argument for the title of graphs and out_files
    parser.add_argument("--title", "-t", default=[], nargs = '*',
                             help='''
The title for graphs and output files.  Spaces are permitted in title.  Output
files will have spaces replaced with underscores
                             ''')
    
    # adds an optional argument for the file types for image plots
    parser.add_argument("--image_type", "-i", default="png",
                        choices=('png', 'gif', 'jpeg', 'tiff', 'sgi', 'bmp', 
                                 'raw', 'rgba', 'html'),
                        help='''
Sets the file type for image files to be saved as.  If using amimations, some
file types will save animations, and others will save frames.  Default is png.
                        ''')     
                        
###############################################################################
# Normalisation options
###############################################################################
    
    # adds an optional argument for normalisation method
    parser.add_argument("--norm", "-n", default='n',
                        choices=('o', "f", "n",'t'),
                             help='''
Method for normalising the data 
o = overall (divide by maximum for all data)
f = frequency (divide by maximum by frequency/subband)
t = time (divide by maximum by time/observation)
n = no normalisation.
                             ''')
    # adds an optional argument for normalisation target
    parser.add_argument("--norm_data", "-N", default="n",
                        choices=("s", "m", "n", "b"),
                             help='''
Target data for applying the normalisation to
s = scope
m = model
n = no cropping
b = normalise both
                             ''')       
###############################################################################
# Cropping options
###############################################################################
    
    # adds an optional argument for the cropping type for noise on the scope
    parser.add_argument("--crop_type", "-C", default="median",
                        choices=("median", "mean", "percentile"),
                        help='''
Sets what style of cropping will be applied to the scope data to remove 
outliers. A value for --crop must also be specified or this argument is ignored.  
    median implies drop all values over a given multiple of the median value.
    mean implies drop all values over a given multiple of the median value.
    percentile implies drop all values over a given percentile value.
    percentiles over 100 are ignored''')     

    # adds an optional argument for the cropping level for noise on the scope
    parser.add_argument("--crop", "-c", default = 0.0, type=float,
                        help='''
Set the numeric value for cropping. Depending on crop mode, this may be a 
multiple of the mean or median, or the percentile level to cut the scope values
 to. Default is not to crop (crop = 0.0). Negative values are converted to 
 positive before use.
                             ''')

    # adds an optional argument for cropping method
    parser.add_argument("--crop_basis", "-k", default='n',
                        choices=('o', "f", "n",'t'),
                             help='''
Method for cropping the data
o = overall (crop equally for all data)
f = frequency (crop by frequency/subband)
t = time
n = no cropping
                             ''')

    # adds an optional argument for cropping method
    parser.add_argument("--crop_data", "-K", default="n",
                        choices=("s", "m", "n", "b"),
                             help='''
Target data for applying the cropping to
s = scope
m = model
n = no cropping
b = crop both
                             ''')    

###############################################################################
# Difference options
###############################################################################
    
    # adds an optional argument for the mechanism for comparing scope with model
    parser.add_argument("--diff", "-d", default = "sub",
                        choices=("sub", "div", "idiv"),
                        help='''
determines whether to use subtractive or divisive differences when calculating 
the difference between the scope and the model.  Default is subtract
  sub = model - scope
  div = model / scope
  idiv = scope/model
                        ''')
###############################################################################
# Plotting options
###############################################################################
    
    # adds an optional argument for the set of values to analyse and plot
    parser.add_argument("--values", "-v", default=["linear"], nargs="*",
                        choices=("all", "linear", "stokes",
                                 "xx", "xy", "yy", "U", "V", "I", "Q",
                                 "each"),
                        help='''
Sets the parameters that will be plotted on the value and difference graphs.
  linear implies xx, xy and yy-channel values will be plotted. 
  stokes implies that Stokes U- V- I- and Q-channels will be plotted.
  all implies that all seven channels will be plotted.
  An individual channel name means to plot that channel alone. 
  each means that the channels will be plotted separately rather than overlaid.
  
                        ''')     
    
    # adds an optional argument for the plots to show
    parser.add_argument("--plots", "-p", nargs="*",
                        default=["spectra", "values"],
                        choices=("rmse", "corr", "spectra", 
                                 "file",
                                 "alt", "az", "ew", "stn", "split",
                                 "values", "model", "scope", "diff",
                                 "overlay"
                                 ),
                        help='''
Sets which plots will be shown.  Default is to show rmse, corr and spectra plots
rmse shows plots of RMSE (overall, per time and per freq as appropriate)
corr shows plots of corrlation (overall, per time and per freq as appropriate)
spectra shows plots of the spectrum of the channels (by frequency over time as 
appropriate) 
file determines whether to output the dataframe to a file for later analyses
alt shows plots of value against altitude
az shows plots of value against azimuth
ew means azimuth is plotted East/West (-180/+180) instead of absolute (0/360)
stn means alt/az coordinates are calculated in the station reference frame
split means dynamic plots of Alt-Az coordinates are split to avoid aliasing
values means to plot both model and scope values
model means to plot model values
scope means to plot scope values
diff shows plots of the differences in values of the channels 
overlay means that for a given channel, the plots will be overlaid
                        ''') 

###############################################################################
# Three D/Animation options
###############################################################################
    
    # adds an optional argument for the way to show 3d data
    parser.add_argument("--three_d", "-3", default="colour",
                        choices=("colour", "color", "anim", "animf", "contour"),
                        help='''
Sets how to show three dimensional plots.  If colour is chosen, then they are 
plotted as colours.  If anim is chosen, plots the data animated over time.  If 
animf is chosen, plots the data animated over frequency 
 If contour is chosen, plots the data as a 3-D Contour plot
                        ''')     
    
    # adds an optional argument for the framerate of animations
    parser.add_argument("--frame_rate", "-r", default = 60.0, type=float,
                        help='''
Set the numeric value for the number of frames per second to attempt to plot 
animated graphs at.  If no animated plots are used, or animations are plotted 
to files on a per-frame basis, this variable is ignored.  Default is 60 FPS
                             ''')
     
###############################################################################
# Timing options
###############################################################################
    # adds an optional argument for a time offset between model and scope
    parser.add_argument("--offset", "-O", default = 0, type=int,
                        help='''
Sets an offset for the scope.  This is the amount of time (in seconds) that the
scope is believed to be ahead of the model.  This will be subtracted from the 
time of the scope data.  Default is no offset.  Offsets may only be given in
whole seconds
                             ''')

                 
###############################################################################
# Scale options
###############################################################################
    # adds an optional argument for a time offset between model and scope
    parser.add_argument("--scale", "-S", default = 'linear',
                        choices=("linear", "log"),
                        help='''
Sets whether to plot on logarithmic or linear scales
                             ''')

###############################################################################
# Frequencies
###############################################################################
    # creates a group for the chosen frequency or frequencies
    group_freq = parser.add_mutually_exclusive_group()
    # adds an optional argument for the frequency to filter to
    group_freq.add_argument("--freq", "-f", default = [0.0],
                            type=float, nargs="*",
                        help='''
set a frequency filter to and display the channels for.   
Must supply a float or collection of floats separated by spaces.
                        ''')
    # adds an optional argument for a file containing a set of frequencies
    # to filter to
    group_freq.add_argument("--freq_file", "-F", default = "",
                            help='''
set a file containing multiple frequencies to filter to and display the 
channels for.  The file must contain one float per line in text format.
                            ''')    

###############################################################################
#Target object
###############################################################################
    
    # creates a group for the target object
    group_object = parser.add_mutually_exclusive_group()
    # adds an optional argument for target object
    group_object.add_argument("--object_name", "-X", default = None,
                        choices=("", "CasA", "CygA", "VirA"),
                            help='''
set a variable for the name of the target object.  This is used to generate sky
coordinates.  At present this is enabled only for CasA, CygA and VirA
                            ''')        
    # adds an optional argument for target object
    group_object.add_argument("--object_coords", "-x", default = None,
                            type=float, nargs=2,
                            help='''
set a variable for the coordinates of the target object.  Coordinates should 
be 2 floats: RA and Dec (decimal degrees)
                            ''')   
    # TODO: deal with restricted units
    # may later add functionality to parse non-decimal degree values or add a
    # unit functionality
    
###############################################################################
#Observing Location
###############################################################################
    
    # creates a group for the target object
    group_location = parser.add_mutually_exclusive_group()
    # adds an optional argument for target object
    group_location.add_argument("--location_name", "-L", default = None,
                        choices=("", "IE613", "SE607"),
                            help='''
Set the name of the observing location.  This is used to generate ground 
coordinates for the oberving location.  From this and target coordinates, 
Alt-Az coordinates can be generated.  At present this is only defined for LOFAR
stations IE613 and SE607
                            ''')        
    # adds an optional argument for target object
    group_location.add_argument("--location_coords", "-l",
                                default = None, 
                            type=float, nargs='*',
                            help='''
set a variable for the coordinates of the observing site.  Coordinates should 
be 3 floats: Latitude, longitude (degrees) and height above sea level (metres).
If two coordinates are specified, height will be assumed to be 0 (sea level)
                            ''')   
    
###############################################################################
# Using the arguments
###############################################################################
    # passes these arguments to a unified variable
    args = parser.parse_args()

    # creates and uses a dictionary to store the mode arguments
    modes={}
    modes['verbose']=args.verbose    
    modes['interactive']=args.interactive    
    modes['norm']=args.norm
    modes['norm_data']=args.norm_data
    modes['crop_data']=args.crop_data
    modes['crop_type']=args.crop_type
    modes['crop_basis']=args.crop_basis
    modes['crop']=abs(args.crop)  # abs value to prevent use of negative crops
    modes['diff']=args.diff
    modes['values']=args.values
    modes['plots']=args.plots
    modes['freq']=args.freq
    modes['freq_file']=args.freq_file
    modes['three_d']=args.three_d
    modes['image_type']=args.image_type
    modes['frame_rate']=args.frame_rate
    modes['offset']=args.offset
    modes['location_name']=args.location_name
    modes['location_coords']=args.location_coords
    modes['object_name']=args.object_name
    modes['object_coords']=args.object_coords
    modes['scale']=args.scale
    
    # ensures that whichever spelling of colour is input by the user, only one
    # needs to be used in the rest of the code.
    if modes['three_d'] == "color":
        modes['three_d'] = "colour"
    
    # combines the components of the title with spaces to create titles
    modes['title']= " ".join(args.title)

    # combines the components of the title with underscores to create titles
    modes['title_']= "_".join(args.title)    
    
    # outputs the filename for the model to a returnable variable
    if args.model_p != None:
        modes['in_file_model']=args.model_p
    elif args.model != None:
        modes['in_file_model']=args.model
    else:
        if modes['interactive']==1: # should only occur in interactive mode 1
            modes['in_file_model']=raw_input("No model filename specified:\n"
                                    "Please enter the model filename:\n")
        else:
            modes['in_file_model']=""
    
    # outputs the filename for the scope to a returnable variable
    if args.scope_p != None:
        modes['in_file_scope']=args.scope_p
    elif args.scope != None:
        modes['in_file_scope']=args.scope
    else:
        if modes['interactive']==1:#should only occur in interactive mode 1
            modes['in_file_scope']=raw_input("No filename specified for observed"+
                                     " data from the telescope:\n"
                                     "Please enter the telescope filename:\n")
        else:
            modes['in_file_scope']=""
    
    # sets up the output directory based on the input
    modes['out_dir']=prep_out_dir(args.out_dir, modes)

    # finalises the location coordinates
    modes=get_location(modes)
    
    # sets up the object coordinates
    modes=get_object(modes)

    # sets up non-interactive plotting
    if modes['interactive'] == 0:  # non-interactive mode
        import matplotlib
        matplotlib.use('agg')
    else:
        pass  # use whatever the default is, usually tk

    return(modes)


def filter_frequencies(merge_df, modes):
    """
    This function takes a dataframe and (through modes) either a file or a list
    of frequencies, and drops any rows which do not correspond to that 
    frequency.
    """
    if modes['freq_file'] != "":
        if modes['verbose'] >=2:
            print ("isolating frequencies from file: "+modes['freq_file'])
        try:
            freq_df=pd.read_csv(modes['freq_file'], header=None)
            modes['freq']=list(freq_df[0])
        except IOError:
            if modes['verbose'] >=1:
                print("ERROR: File: "+modes['freq_file']+" inaccessible!")
                print("\tproceeding without frequency filter.")
    if modes['freq'] !=[0.0]:
        if modes['verbose'] >=2:
            print ("isolating frequencies: "+str(modes['freq'])+"Hz")
        # drops all frequencies which do not match the filter if applicable
        merge_df=merge_df[merge_df['Freq'].isin(modes['freq'])]
        merge_df.reset_index(drop=True, inplace=True)

    return (merge_df)
    

def alt_az_ops(merge_df, modes):
    """
    This function calculates the Alt-Az coordinates and Station Alt-Az coords 
    if possible.
    """
    # calculates Alt-Az coordinates if possible
    if (modes['object_coords']!=None) and (modes['location_coords']!=None):
        try:
            merge_df = calc_alt_az(merge_df,modes)
        except NameError:
            if modes['verbose'] >=1:
                print("ERROR: Unable to calculate Horizontal coordintates\n"\
                   "\tPossible issue with AstroPy imports.")
            for option in ["alt", "az", "stn"]:
                if option in modes["plots"]:
                    # removes plot options that are no longer valid
                    modes["plots"].remove(option)
    
        
    # calculates station Alt-Az if possible and requested
    if modes['location_name']!=None and "stn" in modes["plots"]:
        try:
            merge_df=calc_alt_az_lofar(merge_df,modes)
        except ValueError:#except NameError:
            if modes['verbose'] >=1:
                print ("ERROR: Unable to calculate Station coordintates\n"\
                   "\tKnown issue: Casacore is not compatible with Windows\n"\
                   "\tProceeding without station coordinates.")    
    return(merge_df)


def analysis(merge_df, modes, m_keys, sources):
    """
    based on options, chooses the analysis to perform and returns the 
    dataframes of the independent variables
    """
    # runs different functions if there are one or multiple frequencies
    if merge_df.Freq.nunique()==1:
        # if only one frequency, does one-dimensional analysis
        if "each" in modes['values']: # if the plots are to be separate
            for key in m_keys: # analyses them one at a time
                ind_dfs=analysis_1d(merge_df,modes, [key],sources)
        else: # allows plots to be overlaid
            ind_dfs=analysis_1d(merge_df,modes, m_keys,sources)
    else: # otherwise does multi-dimensional analysis
        if "each" in modes['values']: # if the plots are to be separate
            for key in m_keys: # analyses them one at a time
                ind_dfs=analysis_nd(merge_df,modes, [key],sources)
        else: # allows plots to be overlaid
            ind_dfs=analysis_nd(merge_df,modes, m_keys,sources)  
    
    return(ind_dfs)


def output_df(merge_df, modes):
    """
    This function saves the merged dataframe to a CSV file
    """
    # output the dataframe if requested
    if (modes['out_dir'] != None) & ('file' in modes['plots']):
        path_out_df = prep_out_file(modes,out_type=".csv")
        try:
            merge_df.to_csv(path_out_df)
        except IOError:
            if modes['verbose'] >=1:
                print("WARNING: unable to output to file:\n\t"+path_out_df)
    if (modes['out_dir'] == None) & ('file' in modes['plots']):
        if modes['verbose'] >=1:
            print("ERROR: file output requested, but no directory selected.")


def operational_loop(model_df, scope_df, modes):       
    """
    This function contains the main operational loop of the program.  This can
    be iterated many times as part of an interactive system.
    """
    # creates the dataframe to be used in plotting.  This dataframe may be
    # cropped or normalised based on parameters from the user.
    merge_df,sources=merge_crop_test(model_df, scope_df, modes)

    # identifies the channels
    m_keys=get_df_keys(merge_df, modes)
    
    # filters the frequencies if requested
    merge_df = filter_frequencies(merge_df, modes)

    # if there is some data in the merged dataframe
    if len(merge_df)>0:
        # performs the various operations to create the alt-az components
        merge_df= alt_az_ops(merge_df, modes)

        # chooses between various analysis options and then carries them out
        ind_dfs=analysis(merge_df, modes, m_keys, sources)

        # outputs the dataframe to disc if required.
        output_df(merge_df, modes)

    # otherwise gives an error
    else:
        if modes['verbose'] >=1:
            print("ERROR: NO DATA AVAILABLE TO ANALYSE!")
        if modes['interactive']<2:
            if modes['verbose'] >=1:
                print("EXITING!")
            sys.exit(1)


def main():
    # gets the command line arguments and parses them into the modes dictionary
    modes = beam_arg_parser()

    # read in the csv files from DreamBeam and format them correctly
    model_df = read_var_file(modes['in_file_model'], modes)

    # read in the file from the scope using variable reader
    scope_df = read_var_file(modes['in_file_scope'], modes)

    if modes['interactive'] < 2:
        operational_loop(model_df, scope_df, modes)
    else:
        while modes['interactive'] >= 2:
            operational_loop(model_df, scope_df, modes)
            (modes, model_df, scope_df) = interactive_operation(modes, model_df, scope_df)


if __name__ == "__main__":
    main()

