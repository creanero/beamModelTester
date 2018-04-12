**OSO HDF5 Source data\
Version 0.0\
23ʳᵈ March 2018\
Oisin Creaner**

This describes the formats for output from OSO's HDF5 files containing 
the processed results of observations of a series of 
[ACC files](/data_descriptions/ACC_Source_data_description_0_0.md) 
from a LOFAR station in its current state.

**Outline**
These files each contain a series of measurements of the power of the
XX, XY and YY channels observed at a LOFAR station targeted on a specific 
bright object.  

The initial measurements are taken in the form of ACC files which 
each contain a table of values pertaining to the observation for each of 
512 subbands representing a different frequency separated by 1e8/512Hz.
Each subband takes one second to process, so each ACC file takes 512 seconds
to generate and produces 1 second's worth of data for each subband.

These are processed by OSO **link to go here when available** into a series of observations 
consisting of five datasets

![File Description Diagram](/images/OSO_HDF5_Source_Fig1_v2.PNG)

**Detailed Contents**
1.  M Times (one per ACC file observed) which are stored as a list of 
    floats of the number of seconds since the epoch of 1970 Jan 01 00:00:00
2.  N Frequencies (typically 512) which are stored as a list of floats
3.  MxN XX values stored as a list (one for each time) of lists 
    (one for each frequency) of values in float number format
4.  MxN XY values stored as a list (one for each time) of lists 
    (one for each frequency) of values in complex number format
5.  MxN YY values stored as a list (one for each time) of lists 
    (one for each frequency) of values in float number format
