#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 14:47:12 2018

@author: creanero
"""

#!/usr/bin/env python
"""Script to convert horizontal Azimuth Elevation to station Azimuth Elevation.
example usage:
$ horizontalAzEl2stnAzEl.py SE607 0.,80.
(outputs:)
Horizontal coord. AZ, EL: 0.0deg, 80.0000000003deg
Station    coord. AZ, EL: -4.26889012412deg, 80.024138478deg
"""
import sys
import numpy
import casacore.measures
import casacore.quanta.quantity
import ilisa.antennameta.antennafieldlib as antennafieldlib


def horizon_to_station(stnid, refAz, refEl):
    # Algorithm does not depend on time but need it for casacore call.
    obstimestamp = "2000-01-01T12:00:00" 

    refAz = numpy.deg2rad(float(refAz))
    refEl = numpy.deg2rad(float(refEl))
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
    what = obsstate.direction("AZEL", str(refAz)+"rad", str(refEl)+"rad")
    
    obsstate.doframe(where)
    obsstate.doframe(when)
    
    # Set Horizontal AZEL (not really necessary since request is already in
    # coordinate system, but acts as a check)
#    whatconv=obsstate.measure(what,'AZEL')
#    az = whatconv['m0']['value']
#    el = whatconv['m1']['value']
#    print "Horizontal coord. AZ, EL: {}deg, {}deg".format(numpy.rad2deg(az),
#                                                          numpy.rad2deg(el))
    
    # Convert to Station Coordinate system.
    # First convert to ITRF
    whatconvITRF=obsstate.measure(what,'ITRF')
    lonITRF = whatconvITRF['m0']['value']
    latITRF = whatconvITRF['m1']['value']
    # then turn it into a vector
    xITRF = numpy.cos(lonITRF)*numpy.cos(latITRF)
    yITRF = numpy.sin(lonITRF)*numpy.cos(latITRF)
    zITRF = numpy.sin(latITRF)
    xyzITRF = numpy.matrix([[xITRF],[yITRF],[zITRF]])
    # then rotate it using station's rotation matrix
    what_stn = stnRot.T * xyzITRF
    l_stn=what_stn[0,0]
    m_stn=what_stn[1,0]
    n_stn=what_stn[2,0]
    # now convert vector in station local coordinate system to az/el
    az_stn = numpy.arctan2(l_stn,m_stn)
    el_stn = numpy.arcsin(n_stn)
    
    return(az_stn, el_stn)

if  __name__ == "__main__":
    
    stnid = sys.argv[1]
    #(refAz, refEl) = sys.argv[2].split(',') # az,el in units degrees
    
    refAz = range(0,360,4)
    refEl = range(0,90,1)
    
    #az_stn, el_stn=[horizon_to_station(stnid, refAz[i], refEl[i]) for i in range(len(refAz))]
    stn_alt_az=[horizon_to_station(stnid, refAz[i], refEl[i]) for i in range(len(refAz))]
    stn_alt_az=zip(*stn_alt_az)
    stn_alt=np.array(stn_alt_az[1])
    stn_az=np.array(stn_alt_az[0])
    
#    print "Horizontal coord. AZ, EL: {}deg, {}deg".format((refAz),(refEl))
#    print "Station   coord. AZ, EL: {}deg, {}deg".format(numpy.rad2deg(az_stn),
#                                                         numpy.rad2deg(el_stn))    