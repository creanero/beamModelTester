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

**Outputs**\
*All outputs are optional based on user input contained in the modes dictionary*
1.  A calculation of the correlation coefficient between the model
    and the scope data for each channel
2.  A calculation of the Root Mean Square Error between the model
    and the scope data for each channel
3.  A plot of the values of the model and scope for each channel over time and frequency
4.  A plot of the differences between the model and scope for each channel over time and frequency
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
1.  If the modes dictionary includes "corr" in plots
    1.calculates the pearson correlation coefficient between scope and model using calc_corr_1d
        1.  for each channel prints the correlation 
2.  If the modes dictionary includes "rmse" in plots
    1.  calculates the root mean squared error between scope and model using calc_rmse_1d
        1.  for each channel prints the RMSE 
3.  If the modes dictionary includes "values" in plots
    1.  plots the  the values of model and scope for each channel using plot_diff_values_nf
        1.  for each key in m_keys
            1.  for each source (model, scope)
                1.  creates the graph title from the key
                2.  Plots the values for each channel in a scale of consistient **hue** 
                using colour_models and plt.tripcolor to plot values against time and frequency
                3.  Adds a ylabel and xlabel to the graph 
                4.  If no output directory is specified
                    1.  shows the plot
                5.  otherwise 
                    1.  prepares a systematic file name using prep_out_file
                    2.  prints a progress message as output to the user
                    3.  saves the plot to the file.
4.  If the modes dictionary includes "diff" in plots
    1.  plots the differences in the values of model and scope using plot_diff_values_nf
        1.  For each channel specified with m_keys, plots the differences for the channels on a **different** graph
            1.  creates the graph title from the key
            2.  Plots the differences for each channel in a scale of consistient **hue** 
            using colour_models and plt.tripcolor to plot differences against time and frequency
            3.  Adds a ylabel and xlabel to the graph and  
            4.  If no output directory is specified
                1.  shows the plot
            5.  otherwise 
                1.  prepares a systematic file name using prep_out_file
                2.  prints a progress message as output to the user
                3.  saves the plot to the file.    
5.  Creates a dictionary ind_dfs to hold the dataframes for each independent variable and plot below
6.  For each of the independent variables (Frequency and Time)
    1.  Identifies the unique values of that independent variable
    2.  If the modes dictionary includes "corr" in plots
        1.  Creates a temporary dataframe to hold the outputs for the correlation against that independent variable
        2.  Calculates and plots the correlation between the model and the scope 
            for each value of that independent variable for each channel using 
            [calc_corr_nd](/comparison_module/function_docs/calc_corr_nd.md) 
            (e.g. for each frequency, plot the correlation over time)
        3. For each channel specified by m_keys
            1.  Adds the correlations to the temporary Dataframe
        4.  Adds this dataframe to the output dictionary with the name [time|freq]_corr
    2.  If the modes dictionary includes "rmse" in plots
        1.  Creates a temporary dataframe to hold the outputs for the RMSE against that independent variable
        2.  Calculates and plots the RMSE between the model and the scope 
            for each value of that independent variable for each channel using 
            [calc_rmse_nd](/comparison_module/function_docs/calc_rmse_nd.md) 
            (e.g. for each frequency, plot the correlation over time)
        3. For each channel specified by m_keys
            1.  Adds the RMSEs to the temporary Dataframe
        4.  Adds this dataframe to the output dictionary with the name [time|freq]_RMSE
   
6.  If there is an output directory set, outputs the dataframes from the dictionary to files
7.  returns ind_dfs
 

