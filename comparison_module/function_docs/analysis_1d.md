# Comparison Module
**1 dimensional analysis functions\
Version 1.0\
25ᵗʰ September 2018\
Oisin Creaner**

This set of functions describes the 1-dimensional analysis elements of the [comparison module](/comparison_module/Comparison_Module.md).

## Functions
plots_1f\
plot_1f\
calc_foms_1d\
gen_alt_az_var

## Dependencies
pandas\
numpy\
matplotlib\
scipy.stats.stats.pearsonr

## Inputs
A merged data frame containing model and scope data\
List of channels (m_keys)\
List of sources\
modes dictionary

## Outputs
All of these outputs are optional as controlled by the modes dictionary
[Link to non-exhaustive sample outputs](/comparison_module/outputs.md#SingleFreq)
1.  A plot of the values of each of the channels for model and scope and the difference between them over time
2.  A plot of the values of each of the channels for model and scope and the difference between them over Altitude and/or Azimuth
3.  A calculation of a set of figures of merit for each channel (currently: Correlation and RMSE)

## Outline
These functions form the 1-dimensional analysis elements of the 
[comparison module](/comparison_module/Comparison_Module.md) of 
[beamModelTester](/README.md)
This element produces outputs for each polarisation for which there is a difference
recorded in the input.  

## Design Diagram
![Design diagram](/images/comparison_module_analysis_1f_fig1_v2.PNG)

## Operation
1.  If "spectra" plots are set in modes
    1.  Plots the variation of the values for the sources over time using plots_1f
        1.  if "overlay" plots are set in modes
            1.  plots all sources together against time using plot_1f (see below)
        2.  otherwise, for each source in sources
            1.  plots each source separately using plot_1f
                1.  Creates a plot
                2.  creates the title out of a series of components beginning with "plot of"
                    1.  For each source, adds the source name using add_key
                    2.  Adds " for "
                    3.  For each channel, adds the channel name using add_key
                    4.  Adds "-channels over "
                    5.  Adds the independent variable using gen_pretty_name
                    6.  Adds " at a frequency of" and the frequency in MHz (i.e. freq/1e6)
                3.  if in verbose mode, prints the title
                4.  For each channel input (can be one channel if channels are not split in [the previous operation](/comparison_module/operational_loop.md))
                    1.  for each source (will be one source if overlay is not set above)
                        1.  plots a line of the value for that source in that channel in a colour determined by [colour_models](/comparison_module/colour_models.md)
                5.  Adds title, legend and axis labels
                6.  if output file generation is set by inputting an out_dir
                    1.  Creates a file name using [prep_out_file](comparison_module/prep_out_file.md)
                    2.  Saves the graph to an output file
2.  if alt/az calculations have been carried out and alt or az plotting has been requested
    1.  identifies the altitude and azimuth variables to use with get_alt_az_var
    2.  for each of alt and az, uses plot_1f with that parameter instead of time as above to plot the data
3.  If a difference has been calculated (i.e. there are two inputs to compare)
    1.  if "corr" is to be plotted, adds it to the list of figures of merit
    2.  if "rmse" is to be plotted, adds it to the list of figures of merit
    3.  for each figure of merit to be plotted
        1.  Calculates the list of values for that figure of merit
        2.  for each channel
            1.  prints the value for the figure of merit
            2.    if output file generation is set by inputting an out_dir
                1.  Creates a file name using [prep_out_file](comparison_module/prep_out_file.md)
                2.  Saves the value for the figure of merit to an output file
