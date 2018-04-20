**Comparison Module \
Dataframe merging functions\
Version 0.3\
23ʳᵈ March 2018\
Oisin Creaner**

This set of functions describes the Dataframe merging elements of the [comparison module](/comparison_module/Comparison_Module.md).

**Functions**\
merge_dfs\
calc_diff\
calc_xy

**Dependencies**\
pandas\
numpy

**Inputs**\
Two data frames containing model or scope data\
argument *norm_mode* which describes the desired normalisation mode to use

**Outputs**\
One merged dataframe containing data for model, scope and differences

**Outline**\
These functions form the Dataframe merging component of the 
[comparison module](/comparison_module/Comparison_Module.md) of 
[beamModelTester](/README.md)
Depending on the dataframe content provided, the system uses one of several (currently two) options
to process the data from two existing dataframes suitable for futher processing.

**Design Diagram**\
![Design diagram](/images/comparison_module_merge_dfs_fig1_v4.PNG) \
**Figure 1: Schematic representation of merge software.**

**Operations**
1.  Calls the pandas merge method on the model and scope dataframes with the following arguments
    1.  the columns to join on (Time and Freq)
    2.  the suffixes to add for disambiguation (_model and _scope)
2.  calc_xy calls calc_diff for each of the linear channels
    1.  Calculates the difference between scope and model for a channel
    2.  Returns the merged dataframe
3.  calc_stokes calculates the Stokes U, V, I and Q parameters for each source (scope and model)
    1.  Stokes U is the real component of the XY
    2.  Stokes V is the imaginary component of the XY
    3.  Stokes I is the sum of XX and YY
    4.  Stokes Q is the difference between XX and YY
    5.  calls calc_diff which calculates the difference in each of the Stokes Parameters between scope and model
    6.  Returns the merged dataframe
4.  Returns the merged dataframe
