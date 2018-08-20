# Comparison Module 
**Version 1.0\
1ˢᵗ August 2018\
Oisin Creaner**

This module takes input from a model of telescope performance and
compares it with calibration data from real telescopes to generate
metrics for the deviation of the model from reality.

In addition, it can plot the varation in data from either a telescope 
or the model data alone.


## Software design
Software design diagrams and descriptions are available at [this link](/comparison_module/Comparison_Module.md)

## Outline
This (Python) module reads in input from a modelling system and input 
from a real telescope and compares the two against one another. In its
current status, this module expects inputs in 
[dreamBeam .CSV output format](/data_descriptions/DreamBeam_Source_data_description.md) or 
[OSO .HDF5 file format](/data_descriptions/OSO_HDF5.md)
The outputs of this system are a series of text outputs and
plots showing the dependence of the different statistical measures of difference
on time and frequency.  The plots which are shown are dependent on whether 
the inputs are single or multiple frequency, and whether a model is being 
compared with another model or with a real scope input.

## Inputs
model file [(DreamBeam.csv file)](/data_descriptions/DreamBeam_Source_data_description.md)\
scope file (DreamBeam.csv file or [OSO .HDF5 file](/data_descriptions/OSO_HDF5.md))
control parameters

## Usage:

### command line mode:
**./comparison_module_1_0.py \[arguments\]** (see [this file for arguments](/comparison_module/cli_arguments.md))
### Interactive mode:
**./comparison_module_1_0.py** (see [this file for walkthrough](/comparison_module/interactive_mode.md))

                        
## Outputs
A variety of graphs plotted either to the screen or to an output file depending on the chosen options ([see this link](/comparison_module/outputs.md) for more detials
 
