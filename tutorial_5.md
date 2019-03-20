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
