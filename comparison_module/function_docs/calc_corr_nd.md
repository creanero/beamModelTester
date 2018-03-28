**Comparison Module \
multi dimensional correlation function\
Version 0.3\
28ᵗʰ March 2018\
Oisin Creaner**

**Outline**\
This function Calculates and plots the correlation between the model and the scope 
for each value of a given independent variable (e.g. for each frequency, plot the correlation over time)
**Functions**\
calc_corr_1d\
calc_corr_nd

**Dependencies**\
pandas\
numpy\
matplotlib.pyplot\
scipy.stats.stats.pearsonr

**Inputs**\
A merged data frame containing model and scope data
A string indicating which independent variable to analyse

**Outputs**
1.  A plot and list of the how the correlation coefficient between the model
    and the scope data for each channel varies over each independent variable

**Design Diagram**\
![Design diagram](/images/comparison_module_calc_corr_nd_fig1_v1.PNG)
    
**Operations**
1.  identifies the keys (polarisation channels) with '_diff' suffix using get_df_keys
2.  creates a list of lists to hold the correlations for each channel
3.  identifies the unique values of the independent variable
4.  for each such unique value
    1.  creates a temporary dataframe which holds the values from merge_df 
    corresponding to the unique value
    2.  calculates the correlation for that dataframe using [calc_corr_1d](/comparison_module/function_docs/analysis_1d.md)
    3.  for each channel
        1.  Appends the correlation for the given unique value to the list of correlations
5.  creates a plot
6.  Begins to create the graph title
7.  For each channel
    1.  Plots the correlations for each channel in a different hue using colour_models
    2.  Adds the channel to the title
        1.  If it is before the second last, adds the channel name and a comma
        2.  If it is the second last, adds the channel name and an ampersand
        3.  Otherwise, (if it is the last) adds the channel name   
8.  Completes the title using the independent variable
9.  Adds a legend, xticks and xlabel to the graph and shows it
10. Returns the lists of correlations
