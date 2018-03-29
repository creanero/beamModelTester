**Comparison Module \
Dataframe merging functions\
Version 0.3\
23ʳᵈ March 2018\
Oisin Creaner**

This set of functions describes the Dataframe merging elements of the [comparison module](/comparison_module/Comparison_Module.md).

**Functions**\
merge_dfs\
calc_pq\
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
**Figure 1: Schematic representation of merge software. **

**Operations**
1.  This function calls the pandas merge method with the following arguments
    1.  the columns to join on (Time and Freq)
    2.  the suffixes to add for disambiguation (_model and _scope)
2.  If the columname J11_scope is present in the dataframe
    1.  This means both model and scope dataframes had a J11 value
    2.  Therefore we execute *calc_pq* to determine the dreamBeam P and Q channels
    3.  Calculates the p-channel intensity for the scope and model
        1.  Formula used: p = |J11|²+|J12|²
    4.  Calculates the difference in P between scope and model
    5.  Calculates the q-channel intensity for the scope and model
        1.  Formula used: q = |J21|²+|J22|²
    6.  Calculates the difference in Q between scope and model
    7.  Calculates the start (minimum) time and from that the time since the start
    8.  Returns the merged dataframe
3.  If the columname xx is present in the dataframe
    1.  This means only one dataframe had an xx value
    2.  Therefore we execute *calc_xy* to determine the XX, XY and YY channels
    for the model input.\
    NOTE: This will actually work with either input (scope or model), 
    calculating the channels for the input that didn't have it
    3.  Normalises the XX, XY and YY channel values using normalise_scope and 
    based on the normalisation mode provided
    4.  Calculates the XX, XY and YY channel values for the model
        1.  XX = (J11 * conj(J11)) + (J12 * conj(J12))
        2.  XX = (J11 * conj(J21)) + (J12 * conj(J22))
        3.  YY = (J21 * conj(J21)) + (J22 * conj(J22))
        4.  NOTE: not currently using YX = (J21 * conj(J11)) + (J22 * conj(J12))
    5.  Calculates the difference in XX, XY and YY between scope and model
    6.  Returns the merged dataframe
4.  Returns the merged dataframe
