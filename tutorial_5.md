# Tutorial 5: Location and Target features

In this tutorial, you will add information about the target of the observation and the location from which it was observed to enable calculation of the horizontal sky coordinates (Alt/Az) of the target at each time in the observation, and thus allow for the variation of the target against Alt or Az to be plotted.

[Follow](/tutorial_1.md) [the](/tutorial_2.md) [previous](/tutorial_3.md) [tutorials](/tutorial_4.md) such that you have the data loaded into memory, and create xx channel plots for the model, the scope and the difference with filtered frequencies, normalisation but no cropping.  Once you have this done, you are ready to start this tutorial.

## Set Observing Location

From the main menu, select "Location/Target Options." 

![Coordinates Menu](/images/interactive_snips/gicm_4_coords_menu.PNG)

From there, select "Set Observing Location Options."

![Location Menu](/images/interactive_snips/gicm_4_1_coords_loc_menu.PNG)

Next, click "By Name" to enter a LOFAR Station ID

![Station Menu](/images/interactive_snips/gicm_4_1_1_coords_loc_name_menu.PNG)

The data used in this observation is from LOFAR Station SE607, so enter SE607 in the dialogue box, then click to confirm.

If you wish to experiment, you can enter the coordinates manually using the "By Coordinates" option.  This is not recommended in use with LOFAR.

![Location Coordinates Menu](/images/interactive_snips/gicm_4_1_2_coords_loc_coords_menu.PNG)

## Set Target Coordinates

Return to the "Location/Target Options" menu.  From there, select "Set Target Coordinate Options."

![Target Menu](/images/interactive_snips/gicm_4_2_coords_tar_menu.PNG)


Next, click "By Name" to enter the name of a celestial source

![Station Menu](/images/interactive_snips/gicm_4_2_1_coords_tar_name_menu.PNG)

The data used in this observation is from Cassiopeia A, so enter CasA in the dialogue box, then click to confirm.

If you wish to experiment, you can enter the coordinates manually using the "By Coordinates" option.  This is not recommended in use with LOFAR.

## Plotting against Altitude
Return to the main menu and select "Plotting Options" then "Set Graphs to Plot" as in [Tutorial 2](/tutorial_2.md).  From there, select "Set alt-azimuth plotting options"

![Alt/Az Menu](/images/interactive_snips/gicm_5_1_2_graph_plot_alt_az_menu.PNG)

Toggle Altitude plotting, then hit plot with current options.  Depending on whether you have contour plotting on or animated plots, you should see a plot like the ones below.

<img src="/images/tutorial_5_1.png" width=400><img src="/images/tutorial_5_2.gif" width=400>\
*The colourplot shows a distinctive vertical banding, the cause of which is revealed in the animated plot.  As the source (CasA) rotates about the sky, it will pass through altitude values twice, once in the East, and once in the West.  These must be separated to allow for clearer interpretation of the trends.  For shorter observations, this type of plot may be suitable*

## Splitting circular plots

Return to the Alt-azimuth plotting options and then toggle splitting of looping plots.  Again, return to the main menu and plot with current options

<img src="/images/tutorial_5_3_3.png" width=400><img src="/images/tutorial_5_3_1.gif" width=400>\
<img src="/images/tutorial_5_3_4.png" width=400><img src="/images/tutorial_5_3_2.gif" width=400>\
*The splitting of the plots separates out the trends between the eastern and western segments of the source's path about the celestial pole.*

## Plotting against Azimuth
Return to the Alt-azimuth plotting options and then toggle Altitude and Azimuth plotting.  Return to the [channel selection menu](/tutorial_2.md#variables) and select to plot only Stokes Q.  Again, return to the main menu and plot with current options.


<img src="/images/tutorial_5_4_1.png" width=400><img src="/images/tutorial_5_4_2.gif" width=400>\
*Plots of linear polarisation (Stokes Q) against Azimuth.  Note the large flat areas in the middle of these plots where no corresponding observations are made.  This is because matplotlib naively plots azimuth as a non-wrapping variable between 0 and 360 degres.*

Return to the Alt-azimuth plotting options and then toggle Azimuth to E/W plotting.  Again, plot with current options.

<img src="/images/tutorial_5_5_1.png" width=400><img src="/images/tutorial_5_5_2.gif" width=400>\
*Now the continuity between the Eastern and Western halves of the data on a given plot are clearly plotted.  Note, however, that the Northern half of the plot (left) still has far fewer datapoints than the Southern half.*

## Station Coordinates
LOFAR Stations are not set up on a North/South axis, but rather each station is offset by a number of degrees.  This creates a "station coordinate" system which is offset from the horizontal coordinates by an equal amount.  To plot in this system, return to the Alt-azimuth plotting options and then toggle LOFAR Station Coordinates.  Plot the outputs as usual.

<img src="/images/tutorial_5_6_1.png" width=400><img src="/images/tutorial_5_6_2.gif" width=400>

This is the end of this tutorial.  In Tutorial 6, we will look at making offsets and changes to the scale of the system.
