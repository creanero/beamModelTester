**Comparison Module (*Prototype*)\
Version 0.1\
16ᵗʰ March 2018\
Oisin Creaner**

This module takes input from a model of telescope performance and
compares it with calibration data from real telescopes to generate
metrics for the deviation of the model from reality.

**Outline**\
This (Python) module reads in input from a modelling system and input 
from a real telescope and compares the two against one another. In its
current status, this module expects inputs in 
[dreamBeam output format](/data_descriptions/DreamBeam_Source_data_description.md) and 
[OSO .HDF5 file format](/data_descriptions/OSO_HDF5.md)
The outputs of this system are a series of text outputs and
plots showing the dependence of the different statistical measures of difference
on time and frequency.  The plots which are shown are dependent on whether 
the inputs are single or multiple frequency, and whether a model is being 
compared with another model or with a real scope input.

**Inputs**\
model file [(DreamBeam.csv file)](/data_descriptions/DreamBeam_Source_data_description.md)\
scope file (DreamBeam.csv file or [OSO .HDF5 file](/data_descriptions/OSO_HDF5.md))
control parameters

**usage:**
prototype_comparison_module_1d_0_1.py \[arguments\] (see below)

**positional arguments:**\
  model_p               *The file containing the data from the model (Usually
                        DreamBeam)*\
  scope_p               *The file containing the observed data from the
                        telescope*\

**optional arguments:**\
  -h, --help            *show this help message and exit*
  
  --model MODEL, -m MODEL\
  *Alternative way of specifying the file containing the data from the model*
  
  --scope SCOPE, -s SCOPE\
  *Alternative way of specifying the file containing the observed data from the telescope*
  
  --norm {t,f}, -n {t,f}\
  *Method for normalising the scope data\
  t = trivial (divide by maximum for all scope data)\
  f = frequency (divide by maximum by frequency/subband)*
  
  --crop_type {median,mean,percentile}, -C {median,mean,percentile}\
  *Sets what style of cropping will be applied to the scope data to remove 
outliers. A value for --crop must also be specified or this argument is ignored. \
        median implies drop all values over a given multiple of the median value.\
        mean implies drop all values over a given multiple of the median value.\
        percentile implies drop all values over a given percentile value.\
          percentiles over 100 are ignored*
          
  --crop CROP, -c CROP  \
*Set the numeric value for cropping. Depending on crop mode, this may be a 
multiple of the mean or median, or the percentile level to cut the scope values
 to. Default is not to crop (crop = 0.0). Negative values are converted to 
 positive before use.*
 
  --crop_basis {t,f}, -k {t,f}\
 *Method for normalising the scope data \
t = trivial (crop equally for all data) \
f = frequency (crop by frequency/subband)*

  --diff {sub,div,idiv}, -d {sub,div,idiv}\
  *determines whether to use subtractive or divisive differences when 
  calculating the difference between the scope and the model. Default 
  is subtract.\
  sub = model - scope\
  div = model / scope\
  idiv = scope/model*
  
  --values {all,linear,stokes,xx,xy,yy,U,V,I,Q}, -v {all,linear,stokes,xx,xy,yy,U,V,I,Q}\
  *Sets the parameters that will be plotted on the value and difference graphs.\
  linear implies xx, xy and yy-channel values will be plotted.\ 
  stokes implies that Stokes U- V- I- and Q-channels will be plotted.\
  all implies that all seven channels will be plotted.\
  An individual channel name means to plot that channel alone.*
  
  --plots [{rmse,corr,value,diff} [{rmse,corr,value,diff} ...]], \
  -p [{rmse,corr,value,diff} [{rmse,corr,value,diff} ...]]\
*Sets which plots will be shown.  Default is to show all plots and calculations\
rmse shows plots of RMSE (overall, per time and per freq as appropriate)\
corr shows plots of corrlation (overall, per time and per freq as appropriate)\
value shows plots of the values of the channels (per time and per freq as appropriate)\
diff shows plots of the differences in values of the channels (per time and per freq as appropriate)*

  --freq [FREQ [FREQ ...]], -f [FREQ [FREQ ...]]\
*set a single frequency filter to and display the channels for.   Must supply a float.*

  --freq_file FREQ_FILE, -F FREQ_FILE\
*set a file containing multiple frequencies to filter to and display the channels for.\
The file must contain one float per line in text format.*
                        
**Outputs**\
*Single Frequency Mode*\
A plot of the Channel values over time for the model and the scope\
A plot of the differences between model and scope over time for each of the Channels\
A print of the Pearson R correlation between model and scope for each of the Channels\
A print of the Root Mean Square Error between model and scope for each of the Channels

*Multi Frequency Mode*\
A print of the Pearson R correlation between model and scope for each of the Channels\
A print of the Root Mean Square Error between model and scope for each of the Channels\
A plot of the differences between model and scope over Time and Frequency for each of the Channels\
A plot of the Pearson R correlation between model and scope for each of the Channels against Frequency\
A print of the Root Mean Square Error between model and scope for each of the Channels against Frequency\
A plot of the Pearson R correlation between model and scope each of the Channels against Time\
A print of the Root Mean Square Error between model and scope each of the Channels against Time

**NOTE: to add (images/links)**

**Software design**
Software design diagrams and descriptions are avaulable at [this link](/comparison_module/Comparison_Module.md)
    

