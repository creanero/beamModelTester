**Comparison Module (*Prototype*)\
Version 0.1\
16ᵗʰ March 2018\
Oisin Creaner**

This module takes input from a model of telescope performance and
compares it with calibration data from real telescopes to generate
metrics for the deviation of the model from reality

**Outline**\
This (Python) module reads in input from a modelling system and input 
from a real telescope and compares the two against one another. In its
current status, this module expects inputs in dreamBeam output format as
shown at .  The outputs of this system are a series of text outputs and
plots showing the dependence of the different statistical measures of difference
on time and frequency.  The plots which are shown are dependent on whether 
the inputs are single or multiple frequency.

**Inputs**\
model file [(DreamBeam.csv file)](https://github.com/creaneroDIAS/beamModelTester/blob/master/DreamBeam_Source_data_description.md)\
scope file (DreamBeam.csv file) NOTE: this is to be changed in future versions

**Outputs**\
*Single Frequency Mode*\
A plot of the P- and Q-channel values over time for the model and the scope\
A plot of the differences between model and scope over time for each of P-Channel and Q-Channel\
A print of the Pearson R correlation between model and scope for P- and Q-channels\
A print of the Root Mean Square Error between model and scope for P- and Q-channels

*Multi Frequency Mode*
A print of the Pearson R correlation between model and scope for P- and Q-channels\
A print of the Root Mean Square Error between model and scope for P- and Q-channels\
A plot of the differences between model and scope over Time and Frequency for each of P-Channel and Q-Channel\
A plot of the Pearson R correlation between model and scope for P- and Q-channels against Frequency\
A print of the Root Mean Square Error between model and scope for P- and Q-channels against Frequency\
A plot of the Pearson R correlation between model and scope for P- and Q-channels against Time\
A print of the Root Mean Square Error between model and scope for P- and Q-channels against Time

**NOTE: to add (images/links)**

