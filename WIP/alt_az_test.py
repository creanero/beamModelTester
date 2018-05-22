# -*- coding: utf-8 -*-
"""
@author: Derek OKeeffe
from: convert ra dec to alt az with astropy.py
https://gist.github.com/dokeeffe/18857db66dbabc14679c20a8560e2cd6

Used experimentally for alt-az calculations

Modified by: Oisin Creaner
"""


from astropy.coordinates import EarthLocation,SkyCoord
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import AltAz

#from google maps 53.095263, -7.922245 coordinates for IE613 LBA
#from google maps 53.094676, -7.921566 coordinates for IE613 HBA
#from google maps 57.398743, 11.929636 coordinates for SE607 LBA
#from google maps 57.398784, 11.930933 coordinates for SE607 HBA
observing_location = EarthLocation(lat='53.094676', lon='-7.921566', height=150*u.m)  
#observing_time = Time('2018-03-16 11:49:21')  
#aa = AltAz(location=observing_location, obstime=observing_time)

coord = SkyCoord('23h23m26s', '58d48m')
#coord.transform_to(aa)

time_set = Time(list(merge_df.Time))
aa_set= AltAz(location=observing_location, obstime=time_set)
coord_set=coord.transform_to(aa_set)

merge_df['alt'] = coord_set.alt
merge_df['az'] = coord_set.az