# Comparison Module 
## Dataframe merging functions
**Version 1.0\
22nd August 2018\
Oisin Creaner**

*modifications in progress*
This set of functions describes the Dataframe merging elements of the [comparison module](/comparison_module/Comparison_Module.md).

## Functions
merge_crop_test\
merge_dfs\
calc_diff\
calc_xy

## Dependencies
pandas\
numpy

## Inputs
Two data frames containing model or scope data\
modes argument which explains the arguments required

## Outputs
One merged dataframe containing appropriate data for the required plots

## Outline
These functions form the Dataframe merging component of the 
[comparison module](/comparison_module/Comparison_Module.md) of 
[beamModelTester](/README.md)


## Design Diagram
![Design diagram](/images/comparison_module_merge_crop_test_fig1_v1.PNG) \
**Figure 1: Schematic representation of merge software.**

## Operations
1.  If there is data in scope_df
    1.  Apply the offset specified in modes if any
2.  If there is data in both scope_df and model_df
    1.  Call [merge_dfs](/comparison_module/function_docs/merge_dfs.md) to combine the data from both into merge_df
    2.  Identify the sources to be shown using identify_plots
3.  If there is only data in the scope_df
    1.  Sets merge_df to be equal to scope_df
    2.  Sets the sources to be the empty string to ensure that the system doesn't attempt to plot the 
    difference between scope and non-existent model data
4.  If there is only data in the model_df
    1.  Sets merge_df to be equal to model_df
    2.  Sets the sources to be the empty string to ensure that the system doesn't attempt to plot the 
    difference between model and non-existent scope data
5.  If there is no data in either dataframe
    1.  If in low-interactivity modes, exits the program
    2.  If in high-intereactivity modes, returns a blank dataframe
6.  Returns the merge_df dataframe and the list of sources to plot
