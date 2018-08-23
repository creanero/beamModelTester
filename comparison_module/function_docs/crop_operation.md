# Comparison Module 
## crop operation functions
**Version 1.0\
23 August 2018\
Oisin Creaner**

## Functions
crop_operation

## Dependencies
pandas\
numpy

## Inputs
one data frame containing model or scope data\
dictionary modes containing cropping instructions

## Outputs
corresponding dataframe containing data for model or scope

## Outline
This function form the Dataframe cropping component of the as part of [merging operations](/comparison_module/function_docs/merge_crop_test.md)
[comparison module](/comparison_module/Comparison_Module.md) of 
[beamModelTester](/README.md)

## Design Diagram
![crop_operation](/images/comparison_module_crop_operation_fig1_v1.PNG) \
**Figure 1: Schematic representation of crop_operation.**

## Operations
1.  crop_operation makes a copy of the input data frame
2.  For each dependent variable in the dataframe
    1.  Drops all rows with value equal to zero.
    2.  Sets a maximum limit for the value in that column based on
        1.  if the crop_mode is median, multiplies the median value for that column by the crop value
        2.  if the crop_mode is mean, multiplies the mean value for that column by the crop value
        3.  if the crop_mode is percentile, calculates that percentile value for the column
    3.  Drops all rows with value greater than the maximum
3.  Returns the modified data frame
