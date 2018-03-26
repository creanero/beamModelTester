**Comparison Module \
1 dimensional analysis functions\
Version 0.3\
26ᵗʰ March 2018\
Oisin Creaner**

This set of functions describes the 1-dimensional analysis elements of the [comparison module](/comparison_module/Comparison_Module.md).

**Functions**\
plot_values_1f\
plot_diff_values_1f\
calc_corr_1d\
calc_rmse_1d

**Dependencies**\
pandas\
numpy\
matplotlib.pyplot\
scipy.stats.stats.pearsonr

**Inputs**\
A merged data frame containing model and scope data

**Outputs**\
1.  A plot of the values of each of the channels for both model and scope over time
2.  A plot of the differences between the model and scope for each channel over time
3.  A calculation of the correlation coefficient between the model
    and the scope data for each channel
4.  A calculation of the Root Mean Square Error between the model
    and the scope data for each channel

**Outline**\
These functions form the 1-dimensional analysis elements of the 
[comparison module](/comparison_module/Comparison_Module.md) of 
[beamModelTester](/README.md)
This element produces outputs for each polarisation for which there is a difference
recorded in the input.  

**Design Diagram**\
TODO: add design diagram

**Operation**
1.  plots the values for each channel using plot_values_1f
    1.  identifies the keys (polarisation channels) with '_diff' suffix using get_df_keys
    2.  for each such key, plots a **separate** graph for the values for that channel
        1.  Creates the title for the graph from the key
            1.  "Plot of the values in "+key+"-channel over time"
            2.  Calculates and appends the frequency in MHz
        2.  Plots the values for the model in a light **shade** using colour_models
        3.  Plots the values for the scope in a dark **shade** using colour_models
        4.  Adds a legend, xticks and xlabel to the graph and shows it
2.  plots the differences in the values using plot_diff_values_1ff
    1.  identifies the keys (polarisation channels) with '_diff' suffix using get_df_keys
    2.  Begins to create the graph title
    3.  for each such channel, plots the differences for the channels on the **same** graph
        1.  Plots the differences for each channel in a different **hue** using colour_models
        2.  Adds the channel to the title
            1.  If it is before the second last, adds the channel name and a comma
            2.  If it is the second last, adds the channel name and an ampersand
            3.  Otherwise, (if it is the last) adds the channel name       
    3.  Calculates and appends the frequency in MHz
    4.  Adds a legend, xticks and xlabel to the graph and shows it
3.  identifies the keys (polarisation channels) with '_diff' suffix using get_df_keys
4.  for each such key
    1.  calculates and prints the pearson correlation coefficient between scope and model using calc_corr_1d
    2.  calculates and prints  the root mean squared error between scope and model using calc_rmse_1d(merge_df)
