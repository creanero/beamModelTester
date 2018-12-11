# beamModelTester

beamModelTester is a general-purpose tool that enables evaluation of models 
of the variation in sensitivity and apparent polarisation of fixed antenna phased array 
radio telescopes.  

The sensitivity of such instruments varies with respect to the orientation
of the source to the antenna.  This creates a variation in sensitivity over altitude and azimuth.
Further geometric effects mean that this variation is not conisistent with respect to frequency.
In addition, the different relative orientation of orthogonal pairs of linear antennae produces 
a difference in sensitivity between the antennae, leading to an artificial apparent polarisation

By comparing the model with observations made using the given telescope, it is possible to
evaluate the model's performance.  The results of this evaluation can be used to provide a 
figure of merit for the model, and also to guide improvements to the model.  

As an additional feature, this system enables plotting of results from a single station observation on a variety of parameters.

## System Requirements

### Language and Libraries
This software runs in **Python 2.7**.  Ensure the following Libraries are installed and up-to-date
in your python environment.  

To install, run pip install \<package\>\
To update, run pip update \<package\>

 * Required: pandas, numpy, sys, argparse, os, h5py, matplotlib, scipy
 * Recommended: astropy (Horizontal coordinate plotting will not work without this package)

### Depenent packages
The following 3rd-party packages (not available as pip packages) are required for full functionality of this system. 
Some functionality may work without these packages, but installation is recommended.  
Follow the links below to install these packges
  * [dreamBeam](https://github.com/2baOrNot2ba/dreamBeam)
  * [iLiSA](https://github.com/2baOrNot2ba/iLiSA)
  * [python-casacore](https://github.com/casacore/python-casacore)

### Operating System
* Recommended OS: Ubuntu 18.04
* Partial functionality available in Windows 8, 10
* Other operating systems not tested, but may work with appropriate Python interpreter.

## How to use

### Analysis of existing Data

Save the [two files at this link](https://zenodo.org/record/1744987#.XAEbpdv7SUk) to your computer and 
Run the [comparison module](/comparison_module/comparison_module_1_0.py) 
and input the HDF5 file as the "scope" parameter and the CSV file as the "model."
[Follow the instructions at this link. ](/comparison_module/interactive_mode.md)
Select the plots you wish to generate.  This may be carried out interactively using the menu system or by passing command line arguments
[More complete Documentation on the comparison module may be found here.](/comparison_module/readme.md)

*Non-interactive version*
e.g. ***./comparison_module/comparison_module_1_0.py --model ~/SE607_24h_sim.csv
 --scope ~/SE607_2018-03-16T15_58_25_rcu5_CasA_dur86146_ct20161220_acc2bst.hdf5
 --values xx yy --plots spectra model scope diff -I 0***

*Interactive version*
e.g. ***./comparison_module/comparison_module_1_0.py***

*Command Line Interactive version*
e.g. ***./comparison_module/comparison_module_1_0.py -I 2***

### Full Pipeline Data Processing
Acquire ACC Data from LOFAR and store it in a directory with the following name structure

*{STN_ID}_YYYYMMDD_HHMMSS_rcu{RCU_MODE}_dur{DURATION}_{SOURCE}_acc*\
e.g. *IE613_20180406_091321_rcu3_dur91863_CasA_acc*

A sample of suitable data is available at https://zenodo.org/record/1326532#.W3L8FNVKiUk

Run the [data extraction script](https://github.com/creaneroDIAS/beamWrapper/blob/master/data_wrapper.sh) 
with that directory as an argument.\
e.g ***./beamWrapper/data_wrapper.sh ~/IE613_20180406_091321_rcu3_dur85628_CasA_acc***

This will produce a [HDF5 file](/data_descriptions/OSO_HDF5.md)
and a [CSV file](/data_descriptions/DreamBeam_Source_data_description.md) which can be used in the next step
or otherwise as needed.

## Design Components

There are three major components to this system:
  * Data from the Telescope (Currently LOFAR ACC files converted to HDF5 by [iLiSA](https://github.com/2baOrNot2ba/iLiSA))
  * Data from the Model (Currently Hamaker as output from [dreamBeam](https://github.com/2baOrNot2ba/dreamBeam))
  * Comparison/Analysis
  
Software Design Documents are available at [This Link](/overall_design.md)

![Design Diagram](images/testHarness_Fig1v3.PNG)
  
Extraction of data, especially observed data, can be time-consuming.  As a result, separate scripts are provided to 
[extract the data](https://github.com/creaneroDIAS/beamWrapper/blob/master/data_wrapper.sh) 
and to [analyse it](/comparison_module/comparison_module_1_0.py).
An [overall script](https://github.com/creaneroDIAS/beamWrapper/blob/master/complete_wrapper.sh) 
which calls all three components of the software is provided, but usually the data extraction routines are carried out once, 
but the analysis and visualisations are repeated, so the use of this script is deprecated. *Currently a minor bug in this to be worked out*






