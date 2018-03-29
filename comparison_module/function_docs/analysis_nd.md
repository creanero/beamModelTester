**Comparison Module \
multi dimensional analysis functions\
Version 0.3\
28ᵗʰ March 2018\
Oisin Creaner**

This set of functions describes the multi-dimensional analysis elements of the 
[comparison module](/comparison_module/Comparison_Module.md).

**Functions**\
plot_diff_values_nf\
calc_corr_1d\
calc_rmse_1d\
calc_corr_nd\
calc_rmse_nd

**Dependencies**\
pandas\
numpy\
matplotlib.pyplot\
scipy.stats.stats.pearsonr

**Inputs**\
A merged data frame containing model and scope data

**Outputs**
1.  A calculation of the correlation coefficient between the model
    and the scope data for each channel
2.  A calculation of the Root Mean Square Error between the model
    and the scope data for each channel
3.  A plot of the differences between the model and scope for each channel over time
4.  A plot and dataframe of the how the correlation coefficient between the model
    and the scope data for each channel varies over each independent variable
5.  A plot and dataframe of the how the Root Mean Square Error between the model
    and the scope data for each channel varies over each independent variable
    
    
**Outline**\
These functions form the multi-dimensional analysis elements of the 
[comparison module](/comparison_module/Comparison_Module.md) of 
[beamModelTester](/README.md)
This element produces outputs for each polarisation for which there is a difference
recorded in the input.  

**Design Diagram**\
![Design diagram](/images/comparison_module_analysis_nf_fig1_v1.PNG)

**Operation**
1.  identifies the keys (polarisation channels) with '_diff' suffix using get_df_keys
2.  calculates the pearson correlation coefficient between scope and model using calc_corr_1d
    1.  for each channel prints the correlation 
3.  calculates the root mean squared error between scope and model using calc_rmse_1d
    1.  for each channel prints the RMSE 
4.  plots the differences in the values of model and scope using plot_diff_values_nf
    1.  identifies the keys (polarisation channels) with '_diff' suffix using get_df_keys
    2.  for each such channel, plots the differences for the channels on a **different** graph
        1.  creates the graph title from the key
        2.  Plots the differences for each channel in a scale of consistient **hue** 
        using colour_models and plt.tripcolor to plot differences against time and frequency
        3.  Adds a ylabel and xlabel to the graph and shows it    
5.  For each of the independent variables (Frequency and Time)
    1.  Calculates and plots the correlation between the model and the scope 
    for each value of that independent variable for each channel using 
    [calc_corr_nd](/comparison_module/function_docs/calc_corr_nd.md) 
    (e.g. for each frequency, plot the correlation over time)
    2.  Calculates and plots the RMSE between the model and the scope 
    for each value of that independent variable using for each channel using 
    [calc_rmse_nd ](/comparison_module/function_docs/calc_rmse_nd.md)
    (e.g. for each frequency, plot the RMSE over time)

6.  returns a data frame for the correlations and RMSEs over frequency and time
 

