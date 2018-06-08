# -*- coding: utf-8 -*-
"""
Created on Wed Jun 06 15:48:07 2018

@author: User
"""
import numpy as np
import pandas as pd
from horizontalAzEl2stnAzEl import horizon_to_station
from astropy.time import Time

#creates user generated dataframe to simplify testing
size_step = int(raw_input("please enter the step size of the dataframe you wish to test: "))
size_range = int(raw_input("please enter the step range of the dataframe you wish to test: "))
stnid = "SE607"#raw_input("please enter the station ID ")

for size in range(size_step,size_range+1,size_step):
    alt=range(size)
    az=range(size)
    altaz_df=pd.DataFrame(data={"alt":alt,"az":az})
    
    altaz_df.alt=altaz_df.alt*90.0/size
    altaz_df.az=altaz_df.az*360.0/size
    
    
    
    start_time=Time.now()
    #stn_alt_az=[horizon_to_station(stnid, altaz_df.az[i], altaz_df.alt[i]) for i in range(len(altaz_df.alt))]
    stn_alt_az=horizon_to_station(stnid, altaz_df.az, altaz_df.alt)
    
    
    
    #adding to the array
    altaz_df['stn_alt']=np.array(stn_alt_az[1])
    altaz_df['stn_az']=np.array(stn_alt_az[0])
    
    end_time=Time.now()
    
    total_time=(end_time-start_time).sec
    
    print(str(size)+" altaz in %.4g seconds." %total_time)