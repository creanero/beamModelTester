# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 10:03:28 2018

@author: User
"""

###############################################################################
#
#coordinate setting functions
#    
###############################################################################
#TODO see if import warnings can be suppressed without passing arguments
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
try:
    import numpy as np
except ImportError:
    print("WARNING: unable to import numpy.\n"\
      "This may cause subsequent modules to fail")

from interactive_ops import interactive_get_location
from interactive_ops import interactive_get_object

    
def set_object_coords(modes):
    '''
    returns a 2-long list of the coordinates of an object identified by name
    Want to replace this with something better at a later point, but this is 
    designed as a module to be replaced.
    '''
    coords=[0.0,0.0]
    
    name_str=modes['object_name']
    
    if name_str == "CasA":
        coords=[350.85,  58.815]
    elif name_str == "CygA":
        coords=[299.86791667,  40.73388889]
    elif name_str == "VirA":
        coords=[187.70415,  12.39111]
    else:
        if modes['verbose'] >=1:
            print("Warning: Object: "+name_str+" not found.  Setting object "+
              "coordinates to 0,0 which will disable object tracking.\n\n" + 
              "for an object at exactly 0,0 set one coordinate to 1e-308")
    #minimum float increment coordinates will not affect the actual results
    #due to precision limits but will pass a =!0 test later in the program
    
    return(coords)

def get_object(modes):
    
    """
    This function prompts the user to enter the coordinates of the target
    """
    warn_flag = False

    #sets up the object coordinates
    if modes['object_name'] != None:
        modes['object_coords']=set_object_coords(modes)
      
    #checks the coordinates are valid
    
    #if there are 2  coordinates
    if len(modes['object_coords']) == 2:
        
        #checks the validity of those coordinates
        warn_flag = check_coords(modes['object_coords'][1], #Dec (N/S)
                                 modes['object_coords'][0], #RA (E/W)
                                 modes) #supplied separately for compatibility

    else:
        if modes['verbose'] >=1:
            if modes['object_name'] == None:
                print("Warning: Target: "+ str(modes['object_coords'])+
                      " incorrectly specified.  ")
        warn_flag = True    
    if warn_flag == True:
        if modes['interactive']>=1:
            modes = interactive_get_object(modes)
            modes = get_object(modes)
        else:
            if modes['verbose'] >=1:
                print("Interactivity mode: "+str(modes['interactive'])+"\n"
                      "Setting site coordinates to 0,0 which will"+
                      " disable object tracking.")    
                modes['object_coords']=[0.0, 0.0]
        #there is no land at lat/long (0,0), so it should be ok to assume no
        #observations at this object
    
    return(modes)
    

    
def set_location_coords(modes):
    '''
    returns a 3-long list of the coordinates of an observing location 
    identified by name.
    Want to replace this with something better at a later point, but this is 
    designed as a module to be replaced.
    '''
    coords=[]
    
    name_str=modes['location_name']
    
    if name_str == "IE613": 
        coords=[53.095263, -7.922245,150.0] #coords for LBA.  HBA almost identical
    elif name_str == "SE607":
        coords=[57.398743, 11.929636, 20.0]
    else:
        if modes['verbose'] >=1:
            print("Warning: Site: "+name_str+" not found.  " )
            modes['location_name']=None #blanks the name to prevent further use

    return(coords)


def get_location(modes):
    """
    This function prompts the user to enter the coordinates of the observing 
    station
    """
    warn_flag = False

    #sets up the location coordinates
    if modes['location_name'] != None:
        modes['location_coords']=set_location_coords(modes)
      
    #checks the coordinates are valid
    
    #if there are 2 or 3 coordinates
    if len(modes['location_coords']) == 2 or len(modes['location_coords']) == 3:
        
        #checks the validity of those coordinates
        warn_flag = check_coords(modes['location_coords'][0], #latitude
                                 modes['location_coords'][1], #longitude
                                 modes) #supplied separately for compatibility

    
        #if there are only two coordinates (missing height)
        if len(modes['location_coords']) == 2 and not warn_flag:
            
            if modes['verbose'] >=1:
                print("Warning: no height above sea level specified")
        
            if modes['interactive']>=1:
                height_flag=True
                while height_flag:
                    height_test = raw_input("\nDo you want to specify a height (Default 0m)? [y/n]:\t")
                    
                    if height_test in ["N", "n"]: 
                        print("Height above sea level defaulting to 0m")
                        modes['location_coords']=modes['location_coords']+[0.0]
                        height_flag=False#end the while loop
                        
                    elif height_test in ["Y", "y"]:
                        warn_flag = True #reenter the coordinates
                        height_flag=False #end while loop
                    else:
                        print("Input not understood.")
                        height_flag=True #continue while loop
            
            
            else:#in low interactivity modes
                #appends a height of zero (sea level) for the observing site
                if modes['verbose'] >=1:
                    print("Interactivity mode: "+str(modes['interactive'])+"\n"
                          "Height above sea level defaulting to 0m")
                modes['location_coords']=modes['location_coords']+[0.0]
    else:
        if modes['verbose'] >=1:
            if modes['location_name'] == None:
                print("Warning: Site: "+ str(modes['location_coords'])+
                      " incorrectly specified.  ")
        warn_flag = True    
    if warn_flag == True:
        if modes['interactive']>=1:
            modes = interactive_get_location(modes)
            modes = get_location(modes)
        else:
            if modes['verbose'] >=1:
                print("Interactivity mode: "+str(modes['interactive'])+"\n"
                      "Setting site coordinates to 0,0,0 which will"+
                      " disable object tracking.")    
                modes['location_coords']=[0.0, 0.0, 0.0]
        #there is no land at lat/long (0,0), so it should be ok to assume no
        #observations at this location
    
    return(modes)



def check_coords(ns, ew, modes={"verbose":1}): #default value gives responses
    warn_flag = False
    
    if ns>90 or ns<(-90):
        if modes['verbose'] >=1:
            print("Warning: North/South coordinate supplied out of range.  "
                  "North/South coordinates restricted to +/-90 degrees!")
        warn_flag = True
    if ew>360 or ns<(-360):
        if modes['verbose'] >=1:
            print("Warning: East/West coordinate supplied out of range.  "
                  "East/West coordinates restricted to +/-360 degrees!")
        warn_flag = True
    
    return(warn_flag)


def calc_alt_az_all_sky(in_df, modes):
    """
    This function uses astropy to calculate a set of altitude and azimuth coordinates from a set of RA/Dec coordinates
    from an all-sky analysis.

    :param merge_df:
    :param modes:
    :return:
    """
    out_df=in_df.copy()
    return(out_df)


def calc_alt_az(merge_df,modes):
    '''
    This function uses astropy to calculate a set of altitude and azimuth 
    coordinates for the target object at each time in the the dataset
    '''
    if modes['verbose'] >=2:
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
    if modes['verbose'] >=2:
        print("Calculating East/West Horizontal Coordinates")
    (merge_df.loc[merge_df['az']>180,'az_ew'])=(merge_df.loc[merge_df['az']>180,'az'])-360
    return (merge_df)

def calc_alt_az_lofar(merge_df,modes):
    '''
    This function is not currently defined.  This placeholder will be used to 
    define the function to calculate LOFAR specific coordinates
    '''
    if modes['verbose'] >=2:
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
