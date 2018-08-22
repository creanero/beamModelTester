# Comparison Module 
## Dataframe merging functions
**Version 1.0\
22 August 2018\
Oisin Creaner**

This set of functions describes the Dataframe merging elements of the [comparison module](/comparison_module/Comparison_Module.md).

## Functions
merge_dfs\
calc_diff\
calc_xy

## Dependencies
pandas\
numpy

## Inputs
Two data frames containing model or scope data\
argument *norm_mode* which describes the desired normalisation mode to use

## Outputs
One merged dataframe containing data for model, scope and differences

## Outline
These functions form the Dataframe merging component of the 
[comparison module](/comparison_module/Comparison_Module.md) of 
[beamModelTester](/README.md)
Depending on the dataframe content provided, the system uses one of several (currently two) options
to process the data from two existing dataframes suitable for futher processing.

## Design Diagram
![Design diagram](/images/comparison_module_merge_dfs_fig1_v5.PNG) \
**Figure 1: Schematic representation of merge software.**

## Operations
1.  Crops and normalises the model and scope dataframes using crop_and_norm
    1.  if crop_data is set for the origin (scope or model) then crops the data using crop_vals
        1.  If the crop basis is set to "overall," runs crop_operation on the whole dataframe
        2.  If the crop basis is set to "frequency," creates subset dataframes corresponding to each unique frequency and runs crop_operation on each of these in turn
            1.  crop_operation makes a copy of the input data frame
            2.  For each dependent variable in the dataframe
                1.  Drops all rows with value equal to zero.
                2.  Sets a maximum limit for the value in that column based on
                    1.  if the crop_mode is median, multiplies the median value for that column by the crop value
                    2.  if the crop_mode is mean, multiplies the mean value for that column by the crop value
                    3.  if the crop_mode is percentile, calculates that percentile value for the column
                3.  Drops all rows with value greater than the maximum
            3.  Returns the modified data frame                
    2.  if norm_data is set for the origin (scope or model) then:
        1.  normalises the data for each linear channel (xx, xy and yy) using normalise_data
            1.  If norm is set to overall, then it divides all values for that channel by the maximum for that channel
            2.  If norm is set to frequency or time mode, then it executes norm_operation with that variable as an argument
                1.  For every unique value of the input parameter, 
                    1.  find the maximum value in that channel
                    2.  divide all values for the channel that correspond to the unique value by that maximum
        2.  Recalculates the stokes parameters for the normalised values.
2.  Calls the pandas merge method on the model and scope dataframes with the following arguments
    1.  the columns to join on (Time and Freq)
    2.  the suffixes to add for disambiguation (_model and _scope)
3.  Calls calc_diff for each of the channels (xx, xy, yy, U, V, I, Q)
    1.  Calculates the difference between scope and model for a channel and stores it with an appropriate suffix
    2.  Returns the merged dataframe
4.  if the difference in time is d_time has not been calculated, then it is calculated at this point.
5.  Returns the merged dataframe
