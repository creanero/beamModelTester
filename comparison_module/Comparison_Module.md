# Comparison Module 
Version 1.0\
1st September 2018\
Oisin Creaner

This module takes input from a model of telescope performance and
compares it with calibration data from real telescopes to generate
metrics for the deviation of the model from reality

## Dependencies
pandas\
numpy\
matplotlib.pyplot\
scipy.stats.stats.pearsonr\
argparse\
h5py\
os

## Assumptions

1.  Model data and telescope data can be made available
2.  The datasets have common independent variables with which to match
    the datasets
3.  The datasets have a comparable dependent variable (either both have the same 
    actual variable, or variables that can be calculated from those stored in the data.)
4.  Inputs will only be provided in the correct format.

## Inputs
Two files each containing one of the following:
1.  model data in [dreamBeam csv format](/data_descriptions/DreamBeam_Source_data_description.md)  
2.  scope data in [OSO HDF5 format](/data_descriptions/OSO_HDF5.md)

[Command line arguments](/comparison_module/cli_arguments.md) to control the program\
**AND\OR**\
[Interactive input via a menu screen](/comparison_module/interactive_mode.md)

## Outputs
Graphs and charts as detailed at [this link](/comparison_module/outputs.md) either plotted to the screen or output to files according to the user input  

## Outline

This Python module reads in input from a modelling system and input from a real
telescope and compares the two against one another. This module assumes
that the inputs have been brought to a suitable format (so far [dreamBeam CSV](/data_descriptions/DreamBeam_Source_data_description.md) 
or [OSO HDF5](/data_descriptions/OSO_HDF5.md) formats are supported), with common
independent variables (e.g. sky position, time, frequency) and at least one
common dependent variable to be compared. Outputs include a plot of the
variation of the dependent variable between the "scope" and the "model" files, 
a calculated value of Root
Mean-Square Error (RMSE), and a calculated value for the correlation of
the variables. (*These outputs can be expanded in Future*)

## Design Diagram

![Design Diagram](/images/comparison_module_fig1_v6.PNG)

**Figure 1: Outline of the Comparison Module**

## Operation

1. Parse the command line arguments or user interactive input using 
[beam_arg_parser](/comparison_module/function_docs/arg_parser.md)
2. Read in the data from the model file using the variable reader function 
[read_var_file](/comparison_module/function_docs/file_reading_functions.md)
and store the contents in a dataframe
3.  Read in the data from the telescope file using the same variable reader function and store the contents in a
    dataframe
4.  If the program is in low-interactivity modes:
    1.  Run the [Operational Loop](/comparison_module/operational_loop.md) of the program once
5.  In fully interactive mode, do the following until the user enters the command to stop
    1.  Run the [Operational Loop](/comparison_module/operational_loop.md).
    2.  Run the [Interactive Operation](/comparison_module/interactive_operation.md) to allow the user to set the parameters for the program

