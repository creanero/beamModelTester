#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 13:39:28 2018

@author: Oisin Creaner
"""

import pandas as pd
import numpy as np


import argparse


try:
    from astropy.coordinates import EarthLocation,SkyCoord
    from astropy.time import Time
    from astropy import units as u
    from astropy.coordinates import AltAz
except ImportError:
    print("WARNING: Unable to import astropy.\n"\
          "This may cause subsequent modules to fail")
    
try:
    import casacore.measures
    import casacore.quanta.quantity

except ImportError:
    print("WARNING: Unable to import casacore.\n"\
          "This may cause subsequent modules to fail")
    
try:    
    import ilisa.antennameta.antennafieldlib as antennafieldlib

except ImportError:
    print("WARNING: unable to import ilisa.\n"\
          "This may cause subsequent modules to fail")




#modules of this project
from reading_functions import read_var_file
from reading_functions import merge_dfs 
#from utility_functions import plottable

from io_functions import prep_out_dir
from io_functions import prep_out_file

from analysis_functions import analysis_1d
from analysis_functions import analysis_nd




def get_df_keys(merge_df,key_str="", modes={"values":"all"}):
    '''
    Calculates the keys from a given dataframe or based on the input modes.
    '''
    print("Identifying channels to analyse")
    m_keys=[]
    
    #if key groups have been supplied, extend the keylist with their components
    if "stokes" in modes["values"]:
        m_keys.extend(["U","V","I","Q"])
    if "linear" in modes["values"]:
        m_keys.extend(["xx","xy","yy"])
    if "all" in modes["values"]:
        for m_key in merge_df.keys():
            if key_str in m_key:
                m_keys.append(m_key.split(key_str)[0])
                
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
        print ("Warning, no appropriate keys found!")
    
    
    return(m_keys)








#            for i in range(len_dir):
#                four_var_plot(merge_df,modes,directions[i],"Freq",key,
#                              directions[len_dir-i-1],source)
#    
    



###############################################################################
#
#argument setting functions
#    
###############################################################################

def beam_arg_parser():
    '''
    This function parses the arguments from the command line and returns the 
    file names for the model data and the scope data
    
    Several options are provided: Positional arguments, followed by optional
    arguments followed by interactive entry of the argument values.
    
    future expansions to arguments will allow the user to specify modes of 
    operation and the type of output generated
    '''
    
    parser = argparse.ArgumentParser()
    
###############################################################################
#Model filenames
###############################################################################
    
    #creates a group for the model filename
    group_model = parser.add_mutually_exclusive_group()
    
    #gives positional and optional ways of providing the model data 
    group_model.add_argument("model_p",nargs='?', default=None, 
                             help='''
The file containing the data from the model (Usually DreamBeam)
                             ''')
    group_model.add_argument("--model","-m", 
                             help='''
Alternative way of specifying the file containing the data from the model
                             ''')
    
###############################################################################
#Scope filenames
###############################################################################
    
    #creates a group for the scope filename
    group_scope = parser.add_mutually_exclusive_group()
    
    #gives positional and optional ways of providing the scope data 
    group_scope.add_argument("scope_p",nargs='?', default=None, 
                             help='''
The file containing the observed data from the telescope
                             ''')
    group_scope.add_argument("--scope","-s", 
                             help='''
Alternative way of specifying the file containing the observed data from the 
telescope
                             ''')

###############################################################################
#Output filename, file type and plot titles
###############################################################################

    #adds an optional argument for output directory
    parser.add_argument("--out_dir","-o", default=None,
                             help='''
path to a directory in which the output of the program is intended to be stored
.  IF this argument is blank, output is to std.out and plots are to screen.
                             ''')   
    
    
    #adds an optional argument for the title of graphs and out_files
    parser.add_argument("--title","-t", default=[], nargs = '*',
                             help='''
The title for graphs and output files.  Spaces are permitted in title.  Output
files will have spaces replaced with underscores
                             ''')   
    
    
    #adds an optional argument for the file types for image plots
    parser.add_argument("--image_type","-i", default="png",
                        choices=('png', 'gif', 'jpeg', 'tiff', 'sgi', 'bmp', 
                                 'raw', 'rgba', 'html'),
                        help = '''
Sets the file type for image files to be saved as.  If using amimations, some
file types will save animations, and others will save frames.  Default is png.
                        ''')     
                        
###############################################################################
#Normalisation options
###############################################################################    
    
    #adds an optional argument for normalisation method
    parser.add_argument("--norm","-n", default='o',
                        choices=('o',"f","n",'t'), 
                             help='''
Method for normalising the data 
o = overall (divide by maximum for all data)
f = frequency (divide by maximum by frequency/subband)
t = time (divide by maximum by time/observation)
n = no normalisation.
                             ''')
    #adds an optional argument for normalisation target
    parser.add_argument("--norm_data","-N", default="s",
                        choices=("s","m","n","b"), 
                             help='''
Target data for applying the normalisation to
s = scope
m = model
n = no cropping
b = normalise both
                             ''')       
###############################################################################
#Cropping options
###############################################################################    
    
    #adds an optional argument for the cropping type for noise on the scope
    parser.add_argument("--crop_type","-C", default="median",
                        choices=("median","mean","percentile"),
                        help = '''
Sets what style of cropping will be applied to the scope data to remove 
outliers. A value for --crop must also be specified or this argument is ignored.  
    median implies drop all values over a given multiple of the median value.
    mean implies drop all values over a given multiple of the median value.
    percentile implies drop all values over a given percentile value.
    percentiles over 100 are ignored''')     

    #adds an optional argument for the cropping level for noise on the scope
    parser.add_argument("--crop","-c", default = 0.0, type=float,
                        help = '''
Set the numeric value for cropping. Depending on crop mode, this may be a 
multiple of the mean or median, or the percentile level to cut the scope values
 to. Default is not to crop (crop = 0.0). Negative values are converted to 
 positive before use.
                             ''')
    

    #adds an optional argument for cropping method
    parser.add_argument("--crop_basis","-k", default='o',choices=('o',"f","n"), 
                             help='''
Method for cropping the data
o = overall (crop equally for all data)
f = frequency (crop by frequency/subband)
n = no cropping
                             ''')

    #adds an optional argument for cropping method
    parser.add_argument("--crop_data","-K", default="s",
                        choices=("s","m","n","b"), 
                             help='''
Target data for applying the cropping to
s = scope
m = model
n = no cropping
b = crop both
                             ''')    

###############################################################################
#Difference options
###############################################################################    
    
    #adds an optional argument for the mechanism for comparing scope with model
    parser.add_argument("--diff","-d", default = "sub",
                        choices=("sub","div", "idiv"),
                        help = '''
determines whether to use subtractive or divisive differences when calculating 
the difference between the scope and the model.  Default is subtract
  sub = model - scope
  div = model / scope
  idiv = scope/model
                        ''')
###############################################################################
#Plotting options
###############################################################################    
    
    #adds an optional argument for the set of values to analyse and plot
    parser.add_argument("--values","-v", default=["all"], nargs="*",
                        choices=("all","linear","stokes",
                                 "xx","xy","yy","U","V","I","Q",
                                 "each"),
                        help = '''
Sets the parameters that will be plotted on the value and difference graphs.
  linear implies xx, xy and yy-channel values will be plotted. 
  stokes implies that Stokes U- V- I- and Q-channels will be plotted.
  all implies that all seven channels will be plotted.
  An individual channel name means to plot that channel alone. 
  each means that the channels will be plotted separately rather than overlaid.
  
                        ''')     
    
    #adds an optional argument for the plots to show
    parser.add_argument("--plots","-p", nargs="*",
                        default=["rmse", "corr", "spectra",
                                 "model","scope", "diff"],
                        choices=("rmse", "corr", "spectra", 
                                 "file",
                                 "alt","az","ew", "stn", "split",
                                 "values","model","scope", "diff", 
                                 "overlay"
                                 ),
                        help = '''
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
#Three D/Animation options
###############################################################################    
    
    #adds an optional argument for the way to show 3d data
    parser.add_argument("--three_d","-3", default="colour",
                        choices=("colour","color", "anim", "animf"),
                        help = '''
Sets how to show three dimensional plots.  If colour is chosen, then they are 
plotted as colours.  If anim is chosen, plots the data animated over time.  If 
animf is chosen, plots the data animated over frequency 
                        ''')     
    
    #adds an optional argument for the framerate of animations
    parser.add_argument("--frame_rate","-r", default = 60.0, type=float,
                        help = '''
Set the numeric value for the number of frames per second to attempt to plot 
animated graphs at.  If no animated plots are used, or animations are plotted 
to files on a per-frame basis, this variable is ignored.  Default is 60 FPS
                             ''')
     
###############################################################################
#Timing options
###############################################################################
    #adds an optional argument for a time offset between model and scoep
    parser.add_argument("--offset","-O", default = 0, type=int,
                        help = '''
Sets an offset for the scope.  This is the amount of time (in seconds) that the
scope is believed to be ahead of the model.  This will be subtracted from the 
time of the scope data.  Default is no offset.  Offsets may only be given in
whole seconds
                             ''')
       


###############################################################################
#Frequencies
###############################################################################
    #creates a group for the chosen frequency or frequencies
    group_freq = parser.add_mutually_exclusive_group()
    #adds an optional argument for the frequency to filter to
    group_freq.add_argument("--freq","-f", default = [0.0], 
                            type=float, nargs="*",
                        help = '''
set a frequency filter to and display the channels for.   
Must supply a float or collection of floats separated by spaces.
                        ''')
    #adds an optional argument for a file containing a set of frequencies 
    #to filter to
    group_freq.add_argument("--freq_file","-F", default = "", 
                            help = '''
set a file containing multiple frequencies to filter to and display the 
channels for.  The file must contain one float per line in text format.
                            ''')    

###############################################################################
#Target object
###############################################################################
    
    #creates a group for the target object
    group_object = parser.add_mutually_exclusive_group()
    #adds an optional argument for target object
    group_object.add_argument("--object_name","-X", default = None,
                        choices=("","CasA", "CygA"), 
                            help = '''
set a variable for the name of the target object.  This is used to generate sky
coordinates.  At present this is enabled only for CasA and CygA
                            ''')        
    #adds an optional argument for target object
    group_object.add_argument("--object_coords","-x", default = [0.0,0.0], 
                            type=float, nargs=2,
                            help = '''
set a variable for the coordinates of the target object.  Coordinates should 
be 2 floats: RA and Dec (decimal degrees)
                            ''')   
    #TODO: deak with restricted units
    #may later add functionality to parse non-decimal degree values or add a 
    #unit functionality
    
###############################################################################
#Observing Location
###############################################################################
    
    #creates a group for the target object
    group_location = parser.add_mutually_exclusive_group()
    #adds an optional argument for target object
    group_location.add_argument("--location_name","-L", default = None,
                        choices=("","IE613", "SE607"), 
                            help = '''
Set the name of the observing location.  This is used to generate ground 
coordinates for the oberving location.  From this and target coordinates, 
Alt-Az coordinates can be generated.  At present this is only defined for LOFAR
stations IE613 and SE607
                            ''')        
    #adds an optional argument for target object
    group_location.add_argument("--location_coords","-l", 
                                default = [0.0,0.0,0.0], 
                            type=float, nargs='*',
                            help = '''
set a variable for the coordinates of the observing site.  Coordinates should 
be 3 floats: Latitude, longitude (degrees) and height above sea level (metres).
If two coordinates are specified, height will be assumed to be 0 (sea level)
                            ''')   
    
###############################################################################
#Using the arguments
###############################################################################
    #passes these arguments to a unified variable
    args = parser.parse_args()
    

    
    #creates and uses a dictionary to store the mode arguments
    modes={}    
    modes['norm']=args.norm
    modes['norm_data']=args.norm_data
    modes['crop_data']=args.crop_data
    modes['crop_type']=args.crop_type
    modes['crop_basis']=args.crop_basis
    modes['crop']=abs(args.crop)#abs value to prevent use of negative crops
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
    modes['object_name']=args.object_name
    
    #ensures that whichever spelling of colour is input by the user, only one 
    #needs to be used in the rest of the code.
    if modes['three_d'] == "color":
        modes['three_d'] = "colour"
    
    #combines the components of the title with spaces to create titles
    modes['title']= " ".join(args.title)

    #combines the components of the title with underscores to create titles
    modes['title_']= "_".join(args.title)    
    
    #outputs the filename for the model to a returnable variable
    if args.model_p != None:
        modes['in_file_model']=args.model_p
    elif args.model != None:
        modes['in_file_model']=args.model
    else:
        modes['in_file_model']=raw_input("No model filename specified:\n"
                                "Please enter the model filename:\n")
    
    
    #outputs the filename for the scope to a returnable variable
    if args.scope_p != None:
        modes['in_file_scope']=args.scope_p
    elif args.scope != None:
        modes['in_file_scope']=args.scope
    else:
        modes['in_file_scope']=raw_input("No filename specified for observed"+
                                     " data from the telescope:\n"
                                     "Please enter the telescope filename:\n")
    
    #sets up the output directory based on the input
    modes['out_dir']=prep_out_dir(args.out_dir)
    
    
    #sets up the object coordinates
    if args.object_name != None:
        modes['object_coords']=set_object_coords(args.object_name)
    else:
        modes['object_coords']=args.object_coords
    
    #sets up the location coordinates
    if args.location_name != None:
        modes['location_coords']=set_location_coords(args.location_name)
        
    elif len(args.location_coords) == 3:
        modes['location_coords']=args.location_coords
    elif len(args.location_coords) == 2:
        #appends a height of zero (sea level) for the observing site
        print("Warning, no height above sea level specified, defaulting to 0m")
        modes['location_coords']=args.location_coords+[0.0]
    else:
        print("Warning: Site: "+ str(args.location_coords)+" incorrectly "+
              "specified.  Setting site coordinates to 0,0,0 which will"+
              " disable object tracking./n/n")    
        modes['location_coords']=[0.0, 0.0, 0.0]
    
    return(modes)




###############################################################################
#
#coordinate setting functions
#    
###############################################################################


    
def set_object_coords(name_str=""):
    '''
    returns a 2-long list of the coordinates of an object identified by name
    Want to replace this with something better at a later point, but this is 
    designed as a module to be replaced.
    '''
    coords=[0.0,0.0]
    if name_str == "CasA":
        coords=[350.85,  58.815]
    elif name_str == "CygA":
        coords=[299.86791667,  40.73388889]
    else:
        print("Warning: Object: "+name_str+" not found.  Setting object "+
              "coordinates to 0,0 which will disable object tracking./n/n" + 
              "for an object at exactly 0,0 set one coordinate to 1e-308")
    #minimum float increment coordinates will not affect the actual results
    #due to precision limits but will pass a =!0 test later in the program
    
    return(coords)
    
def set_location_coords(name_str=""):
    '''
    returns a 2-long list of the coordinates of an observing location 
    identified by name.
    Want to replace this with something better at a later point, but this is 
    designed as a module to be replaced.
    '''
    coords=[0.0,0.0,0.0]
    if name_str == "IE613": 
        coords=[53.095263, -7.922245,150.0] #coords for LBA.  HBA almost identical
    elif name_str == "SE607":
        coords=[57.398743, 11.929636, 20.0]
    else:
        print("Warning: Site: "+name_str+" not found.  Setting site "+
              "coordinates to 0,0,0 which will disable object tracking./n/n" )    
        #there is no land at lat/long (0,0), so it should be ok to assume no
        #observations at this location
    return(coords)











def calc_alt_az(merge_df,modes):
    '''
    This function uses astropy to calculate a set of altitude and azimuth 
    coordinates for the target object at each time in the the dataset
    '''
    print("Calculating Horizontal Coordinates")
    observing_location = EarthLocation(lat= modes['location_coords'][0],
                                       lon= modes['location_coords'][1],
                                       height =modes['location_coords'][2]*u.m)
    
    coord = SkyCoord(modes['object_coords'][0],
                     modes['object_coords'][1], 
                     unit='deg')
    
    time_set = Time(list(merge_df.Time))
    aa_set= AltAz(location=observing_location, obstime=time_set)
    coord_set=coord.transform_to(aa_set)
    
    merge_df['alt'] = coord_set.alt
    merge_df['az'] = coord_set.az
    
    merge_df['az_ew'] = coord_set.az
    print("Calculating East/West Horizontal Coordinates")
    (merge_df.loc[merge_df['az']>180,'az_ew'])=(merge_df.loc[merge_df['az']>180,'az'])-360
    return (merge_df)

def calc_alt_az_lofar(merge_df,modes):
    '''
    This function is not currently defined.  This placeholder will be used to 
    define the function to calculate LOFAR specific coordinates
    '''
    print("Calculating LOFAR Coordinates")
    stn_id=modes['location_name']
    stn_alt_az=horizon_to_station(stn_id, merge_df.az, merge_df.alt)
    
    merge_df['stn_alt']=np.array(stn_alt_az[1])
    merge_df['stn_az_ew']=np.array(stn_alt_az[0])
    merge_df['stn_az']=merge_df['stn_az_ew']
    (merge_df.loc[merge_df['stn_az_ew']<0,'stn_az'])=(merge_df.loc[merge_df['stn_az_ew']<0,'stn_az_ew'])+360
    return (merge_df)

def horizon_to_station(stnid, refAz, refEl):
    # Algorithm does not depend on time but need it for casacore call.
    obstimestamp = "2000-01-01T12:00:00" 


    obsstate = casacore.measures.measures()
    when = obsstate.epoch("UTC", obstimestamp)
    # Use antennafieldlib to get station position and rotation
    # (using HBA here but it shouldn't matter much if it were LBA)
    stnPos, stnRot, arrcfgpos_ITRF, stnIntilePos = \
                         antennafieldlib.getArrayBandParams(stnid, 'HBA')

    # Convert from ITRF to LOFAR station coordsys
    #arrcfgpos_stncrd = stnRot.T * arrcfgpos_ITRF.T
    pos_ITRF_X = str(stnPos[0,0])+'m'
    pos_ITRF_Y = str(stnPos[1,0])+'m'
    pos_ITRF_Z = str(stnPos[2,0])+'m'
    where = obsstate.position("ITRF", pos_ITRF_X, pos_ITRF_Y, pos_ITRF_Z)
    
    
    
    obsstate.doframe(where)
    obsstate.doframe(when)
    
    # Set Horizontal AZEL (not really necessary since request is already in
    # coordinate system, but acts as a check)
#    whatconv=obsstate.measure(what,'AZEL')
#    az = whatconv['m0']['value']
#    el = whatconv['m1']['value']
#    print "Horizontal coord. AZ, EL: {}deg, {}deg".format(numpy.rad2deg(az),
#                                                          numpy.rad2deg(el))
    az_stn=[]
    el_stn=[]
    for i in range(len(refAz)):
        refAz_i = np.deg2rad(float(refAz[i]))
        refEl_i = np.deg2rad(float(refEl[i]))
        what = obsstate.direction("AZEL", str(refAz_i)+"rad", str(refEl_i)+"rad")
        # Convert to Station Coordinate system.
        # First convert to ITRF
        whatconvITRF=obsstate.measure(what,'ITRF')
        lonITRF = whatconvITRF['m0']['value']
        latITRF = whatconvITRF['m1']['value']
        # then turn it into a vector
        xITRF = np.cos(lonITRF)*np.cos(latITRF)
        yITRF = np.sin(lonITRF)*np.cos(latITRF)
        zITRF = np.sin(latITRF)
        xyzITRF = np.matrix([[xITRF],[yITRF],[zITRF]])
        # then rotate it using station's rotation matrix
        what_stn = stnRot.T * xyzITRF
        l_stn=what_stn[0,0]
        m_stn=what_stn[1,0]
        n_stn=what_stn[2,0]
        # now convert vector in station local coordinate system to az/el
        az_stn.append(np.rad2deg(np.arctan2(l_stn,m_stn)))
        el_stn.append(np.rad2deg(np.arcsin(n_stn)))
    
    return(az_stn, el_stn)

    
if __name__ == "__main__":
    #gets the command line arguments and parses them into the modes dictionary
    modes=beam_arg_parser()
    

    
    #read in the csv files from DreamBeam and format them correctly
    model_df=read_var_file(modes['in_file_model'],modes,"m")
    
    #read in the file from the scope using variable reader
    scope_df=read_var_file(modes['in_file_scope'],modes,"s")
    
    #adjusts for the offset if needed (e.g. comparing two observations)
    offset=np.timedelta64(modes['offset'],'s')
    scope_df.Time=scope_df.Time-offset
  
    
    #merges the dataframes
    merge_df=merge_dfs(model_df, scope_df, modes)
    
    if modes['freq'] !=[0.0]:
        print ("isolating frequencies: "+str(modes['freq']))
        #drops all frequencies which do not match the filter if applicable
        merge_df=merge_df[merge_df['Freq'].isin(modes['freq'])]
        merge_df.reset_index(drop=True, inplace=True)
    
    if modes['freq_file'] != "":
        print ("isolating frequencies from file: "+modes['freq_file'])
        freq_df=pd.read_csv(modes['freq_file'], header=None)
        merge_df=merge_df[merge_df['Freq'].isin(freq_df[0])]
        merge_df.reset_index(drop=True, inplace=True)
    
    #identifies the keys with _diff suffix
    m_keys=get_df_keys(merge_df,"_diff", modes)
    

    
    if  len(merge_df)>0:
        #calculates Alt-Az coordinates if possible
        if (modes['object_coords']!=[0.0,0.0]) and (modes['location_coords']!=[0.0,0.0,0.0]):
            try:
                merge_df = calc_alt_az(merge_df,modes)
            except NameError:
                print("ERROR: Unable to calculate Horizontal coordintates\n"\
                       "\tPossible issue with AstroPy imports.")
                for option in ["alt","az","stn"]:
                    if option in modes["plots"]:
                        #removes plot options that are no longer valid
                        modes["plots"].remove(option)
    
        
        #calculates station Alt-Az if possible and requested
        if modes['location_name']!=None and "stn" in modes["plots"]:
            try:
                merge_df=calc_alt_az_lofar(merge_df,modes)
            except NameError:
                print ("ERROR: Unable to calculate Station coordintates\n"\
                       "\tKnown issue: Casacore is not compatible with Windows\n"\
                       "\tProceeding without station coordinates.")
        
        #runs different functions if there are one or multiple frequencies
        if merge_df.Freq.nunique()==1:
            #if only one frequency, does one-dimensional analysis
            if "each" in modes['values']: #if the plots are to be separate
                for key in m_keys: #analyses them one at a time
                    analysis_1d(merge_df,modes, [key])
            else: #allows plots to be overlaid 
                ind_dfs=analysis_1d(merge_df,modes, m_keys)
        else: #otherwise does multi-dimensional analysis
            if "each" in modes['values']: #if the plots are to be separate
                for key in m_keys: #analyses them one at a time
                    ind_dfs=analysis_nd(merge_df,modes, [key])
            else: #allows plots to be overlaid 
                ind_dfs=analysis_nd(merge_df,modes, m_keys)
    
        #output the dataframe if requested
        if (modes['out_dir'] != None) & ('file' in modes['plots']):
            path_out_df = prep_out_file(modes,out_type=".csv")
            try:
                merge_df.to_csv(path_out_df)
            except IOError:
                print("WARNING: unable to output to file:\n\t"+path_out_df)
        if (modes['out_dir'] == None) & ('file' in modes['plots']):
            print("ERROR: file output requested, but no directory selected.")
                
    else:
        print("ERROR: NO DATA AVAILABLE TO ANALYSE!\nEXITING")
    