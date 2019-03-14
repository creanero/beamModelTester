# Tutorial 4

In this tutorial, you will learn how to use beamModelTester to save images and animations to disk instead of displaying them to the screen.  Depending on your implementation, you may be able to save images directly from the matplotlib window that pops up when a graph is plotted, but usually it is not possible to save animated plots in this way.  By following this tutorial, you will be able to create files directly into the filesystem from beamModelTester.  This can help when using beamModelTester to generate many outputs consecutively.

Follow [the](/tutorial_1.md) [previous](/tutorial_2.md) [tutorials](/tutorial_3.md) such that you have the data loaded into memory, and create xx channel plots for the model, the scope and the difference with filtered frequencies, normalisation but no cropping.  Once you have this done, you are ready to start this tutorial.

## Selecting an output location

From the main menu, select "File Input/Output options" as you did when [selecting input data](/tutorial_1.md#select-the-input-data) and then choose "Set output file directory."

![Output menu](/images/interactive_snips/gicm_6_4_FileIO_out_menu.PNG)

From there, click on "Select Directory" and pick a suitable location on your file system using the resulting dialogue box.

![Output dialogue](/images/interactive_snips/gicm_6_4_1_FileIO_out_select_menu.PNG)

If you return to the main menu and click "plot with current options," it may appear as though nothing happens.  However, if you check in the directory you have selected, you will find the files corresponding to the outputs you have chosen there.  These files can take a couple of minutes to generate, depending on the performance specifications of your computer.  These files are systematically named based on the parameters they show.

## Selecting output file type
To select an image type for the output from this program to disk, return to the File Input/Output options menu and from there select "Set Output File type."

![File Type Selection](/images/interactive_snips/gicm_6_3_FileIO_type_menu.PNG)

From there, one can select from a variety of image types to store the outputs in.  For most static image outputs, Portable Netowrk Graphics (.png) is suitable and is used as the default.  .gif format is recommended for animated outputs as it preserves the animated nature of the data.  If animated outputs are selected, but the output data type selected is not suitable for animations, then each frame of the animation will be saved in the file format chosen.  HMTL output produces a HTML web page which links locally to a directory containing one or more PNG files.

For now select .gif and return to the previous menu.  Set the output plots to [animated as shown in a previous Tutorial][/tutorial_2.md#animation-vs-3-d-plots] and then plot with current options. You should see the animated plots appear in your chosen directory.

## Dataframe output
In some cases, it may be useful to export the linked data from the model and obvservation to a portable format to enable analyses not provided for by beamModelTester.  This can be done by enabling dataframe output to CSV.

Return to the File Input/Output options menu and from there toggle the option for "output data file."  Return to the main menu and plot the output.  You'll notice a CSV file appear in the directory you selected earlier.  This can be opened in Excel or many other pieces of software for easy analysis.

## Selecting graph titles
The final part of this tutorial has two effects: adding titles to the plots, and using those titles as part of the procedurally generated file names used for output files.

From the main menu, select "Other Options" to bring up a screen with options which do not easily fit into any of the other categories

![Miscellaneous Menu](/images/interactive_snips/gicm_8_misc_menu.PNG)

From that menu, select "Set graph and title prefix."  

![Miscellaneous Menu](/images/interactive_snips/gicm_8_2_misc_title_menu.PNG)

On this screen, use the text box to enter your preferred graph title.  Since this is an observation by the HBA of LOFAR station SE607 of CasA, then "LOFAR Station SE607 HBA Observation of CasA" is the recommended title.  This will produce a graph and file similar to that shown below.

![Output file](/images/LOFAR_Station_SE607_HBA_Observation_of_Cas_A_vals_nd_xx_scope.gif)

In [Tutorial 5](/tutorial_5.md), we will introduce target and location options, which enable plotting of the data with respect the the Horizontal coordinate system.
