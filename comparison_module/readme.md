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
prototype_comparison_module_1d_0_1.py [-h] [--model MODEL]
                                             [--scope SCOPE]
                                             [--norm_mode {t,f}]
                                             [model_p] [scope_p]

**positional arguments:**\
  model_p               *The file containing the data from the model (Usually
                        DreamBeam)*\
  scope_p               *The file containing the observed data from the
                        telescope*\

**optional arguments:**\
  -h, --help            *show this help message and exit*\
  --model MODEL, -m MODEL\
                        *Alternative way of specifying the file containing the
                        data from the model*\
  --scope SCOPE, -s SCOPE\
                        *Alternative way of specifying the file containing the
                        observed data from the telescope*\
  --norm_mode {t,f}, -n {t,f}\
                        *Method for normalising the scope data*\
                        t = trivial
                        *(divide by maximum for all scope data)*\
                        f = frequency
                        *(divide by maximum by frequency/subband)*
                        
**Outputs**\
*Single Frequency Mode*\
A plot of the P- and Q-channel values over time for the model and the scope\
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
Software design diagrams and descriptions are avaulable at [this link](/data_descriptions/DreamBeam_Source_data_description.md)
    

