# -*- coding: utf-8 -*-
"""
Created on Wed Jun 06 15:48:07 2018

@author: User
"""
import numpy as np
import pandas as pd
from horizontalAzEl2stnAzEl import horizon_to_station

#creates user generated dataframe to simplify testing
size = int(raw_input("please enter the size of the dataframe you wish to test: "))

alt=range(size)
az=range(size)
altaz_df=pd.DataFrame(data={"alt":alt,"az":az})

altaz_df.alt=altaz_df.alt*90.0/size
altaz_df.az=altaz_df.az*360.0/size

stnid = raw_input("please enter the station ID ")

stn_alt_az=[horizon_to_station(stnid, altaz_df.az[i], altaz_df.alt[i]) for i in range(len(altaz_df.alt))]

stn_alt_az_t=zip(*stn_alt_az)

#switching back to degrees
stn_alt=np.array(stn_alt_az_t[1])*180/np.pi
stn_az=np.array(stn_alt_az_t[0])*180/np.pi

#adding to the array
altaz_df['stn_alt']=stn_alt
altaz_df['stn_az']=stn_az