# Tutorial 6: Figures of Merit
beamModelTester is designed to compare models (such as the Hamaker model) with observations to allow for an assessment of the quality of the model.  Therefore, a figure of merit that can be calculated for the relationship between these is needed before a qualitative assessment of multiple models can meaningfully be made.  The two figures of merit used are Root Mean Squared Error and Pearson's Correlation.

Follow the previous tutorials such that you have the [data](/tutorial_1.md#input) loaded into memory, and create [xx channel](/tutorial_2.md#variables) plots for the model, the scope and the [difference](/tutorial_2.md#differences) with [filtered frequencies](/tutorial_3.md#file), [normalisation](/tutorial_1.md#normalisation) but no [cropping](/tutorial_1.md#cropping).  Add the [target](/tutorial_5.md#target) and [location](/tutorial_5.md#location) information to enable horizontal coordinate plotting. Once you have this done, you are ready to start this tutorial.

## Root Mean Squared Error (RMSE)<a name="rmse"></a>
The RMSE is a measure of the average separation between the observed and model values.  This measure is dimension dependent, and should therefore only be used with normalised data.  To show calculate figures of merit, select "Plotting Options" then "Set Graphs to plot" then "set figure of merit for closeness of fit"

![Figure of Merit Menu](/images/interactive_snips/gicm_5_1_1_graph_plot_fom_menu.PNG)

From there, toggle Root Mean Squared Error Plotting to on and plot with current options from the main menu.

![Overall RMSE](/images/tutorial_6_1_1.png)\
*This shows the text output to the terminal with the RMSE for the dataset as a whole.  Since this data is normalised to 1, this represents an average difference of 22.5% between the Hamaker model and the observation.  Note also that this data has been filtered to remove the most obvious RFI spikes.*

To isolate parts of the spectrum with better or worse performance in terms of deviation between model and observation, return to the Figure of Merit menu and toggle frequency plotting on, and again plot with these options

![RMSE by Frequency](/images/tutorial_6_1_2.png)\
*The RMSE shows a very flat distribution with respect to frequency.*

Alternatively, it is possible to toggle the plots such that the RMSE is plotted against time.  To do this, from the figure of merit menu, toggle off frequency plotting and toggle on time plotting.

![RMSE by Time](/images/tutorial_6_1_3.png)\
*the peaks and troughs in RMSE correspond strongly with the peaks and troughs in the data overall.  This suggests perhaps that RMSE is not as suited to this type of analysis*

## Pearson's Correlation<a name="corr"></a>
Correlation is a dimensionless quantity that measures how much changes in one quantity are reflected in another. Return to the figure of merit menu and toggle correlation on and RMSE off.  Also toggle frequency plotting back on.  This will produce two plots and the text output as shown below

![Overall Correlation](/images/tutorial_6_2_1.png)\
*This shows the text output to the terminal with the correlation for the dataset as a whole.  Since this data is normalised to 1, this represents the fact that there is a 62.8% correlation between the model and observation.  This is a fairly strong correlation, but not a perfect one.  Note also that this data has been filtered to remove the most obvious RFI spikes.*

![Correlation by Frequency](/images/tutorial_6_2_2.png)\
*The Correlation shows a very flat distribution with respect to frequency. Note the scale of the graph carefully.  Note also taht the correlation at each frequency is higher than the overall correlation.  This indicates that the prediction of variation over time is consistently good over these frequencies.*

![Correlation by Time](/images/tutorial_6_2_3.png)\
*The correlation with time appears to be negative!  This indicates that the distribution of data across frequencies is poorly predicted by the Hamaker model.*

## Alt-Azimuth plots

This is the end of this tutorial.  In [Tutorial 7](/tutorial_7.md), we will look at making offsets and changes to the scale of the system.
