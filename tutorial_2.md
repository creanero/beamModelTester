# Tutorial 2: Plotting Options

In this tutorial, you will learn about the plotting options of beamModelTester.  If you have not completed [Tutorial 1](/tutorial_1.md) you should do so now.


## Select the variables<a name="variables"></a>
Now that we have comparable data, it's time to learn how to select the variables for the plots you wish to generate.  From the Main Menu select "plotting options."

![Plotting Options menu](/images/interactive_snips/gicm_5_plot_menu.PNG)

From there, click on "select variables to plot."  This will bring up a menu that allows you to select which channels to plot.  By default, the linear (xx, yy) and cross (xy) plots are generated.  From this menu you can select linear channels or Stokes parameters individually, by group, or all at once.  There are also options for plotting linegraphs overlaid or separate from one another.  We will consider these later.


![Values to plot menu](/images/interactive_snips/gicm_5_2_graph_values_menu.PNG)

Click on the option to toggle plotting of the Stokes Parameters now, then return to the main menu and "Plot with current options"

<img src="/images/tutorial_model_I_5.png" width=400><img src="/images/tutorial_scope_Q_5.png" width=400>\
*Plotting with Stokes and Linear parameters produces a total of 14 plots, one each for the model data and the observation of each of the 4 Stokes and 3 Linear channels.  Two samples of the output are shown above.*

## Plotting Differences<a name="differences"></a>

Side-by-side visual comparisons of data are vulnerable to human error such as saccadic masking.  It's much better to be able to plot differences between the data directly.

Return to the plotting options menu and from there select "set graphs to plot." 

![Graph Selection menu](/images/interactive_snips/gicm_5_1_graph_plot_menu.PNG)

This menu includes a number of options we will use for more advanced plots in a later tutorial.  For now, though, we want to select "Set wheher to plot model, scope or difference values"

![Model/Scope/Diff menu](/images/interactive_snips/gicm_5_1_3_graph_plot_values_menu.PNG)

There, toggle on the option for Difference Plotting.  This means that as well as the model and scope data, the difference between these two values will be plotted as shown below.  Return to the main menu and select plot with current options.  To speed up the tutorial, return to the [variable selection screen](#variables) and disable plotting of all of the channels except xx.  You can explore the differences in the other channels if you want to.

<img src="/images/tutorial_model_xx_6.png" width=280><img src="/images/tutorial_scope_xx_6.png" width=280><img src="/images/tutorial_diff_xx_6.png" width=280>\
*The model,observed and difference values for the xx-channel are shown here.*


## Animation vs 3-D plots<a name="animation"></a>

So far, we have used static 3-D colourplots to represent the data.  beamModelTester includes options for using animated plots or 3-d lineplots instead of the colourplots to represent the data.  Let's take a look at some of these options now.  Return to the Main Menu and select Animation/3-D Options

![Animation/3D menu](/images/interactive_snips/gicm_3_anim_menu.PNG)

Click on "Set 3d plotting Options" to choose how multi-dimensional data is represented in the system.

![Animation/3D Plotting menu](/images/interactive_snips/gicm_3_1_anim_colour_menu.PNG)

Select plot animated against time to show visually how the data from the source and the model evolve over time.  By selecting "animated against time," the time since the start of the observation is mapped to the time on the animation.  Return to the main menu and plot with current options.

<img src="/images/tutorial_model_xx_7.gif" width=280><img src="/images/tutorial_scope_xx_7.gif" width=280><img src="/images/tutorial_diff_xx_7.gif" width=280>\
*The model,observed and difference values for the xx-channel are shown here, now in animated format.*

Mapping time in the source data to time in the animation may be intuitively satisfying, but it may be useful to look at other options.  Return to the "Set 3d plotting Options" menu and select "plot animated against frequency" to show visually how the pattern of variation in the data changes with frequency.  These plots show a progression through the frequencies, and can be used to highlight frequencies with RFI or other issues.

<img src="/images/tutorial_model_xx_8.gif" width=280><img src="/images/tutorial_scope_xx_8.gif" width=280><img src="/images/tutorial_diff_xx_8.gif" width=280>\

## Frequency filtering<a name="frequencies"></a>

### Single Frequency