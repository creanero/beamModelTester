# -*- coding: utf-8 -*-
"""
Created on Tue May 15 17:43:16 2018

@author: User
"""

key = 'xx'

source = 'scope'


plt.figure()
plt.subplot(211)
plt.tripcolor(merge_df.alt,merge_df.Freq,plottable(merge_df[key+'_'+source]), cmap=plt.get_cmap(colour_models(key+'s')))
plt.clim(np.percentile(plottable(merge_df[key+'_'+source]),5),np.percentile(plottable(merge_df[key+'_'+source]),95))
plt.subplot(212)
#plt.plot(merge_df.d_Time,merge_df.az,color="magenta", marker=".", linestyle="None")
plt.plot(merge_df.alt,merge_df.az_360,color="magenta", marker=".", linestyle="None")
plt.show()