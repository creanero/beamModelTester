# Tutorial 4

In this tutorial, you will learn how to use beamModelTester to save images and animations to disk instead of displaying them to the screen.  Depending on your implementation, you may be able to save images directly from the matplotlib window that pops up when a graph is plotted, but usually it is not possible to save animated plots in this way.  By following this tutorial, you will be able to create files directly into the filesystem from beamModelTester.  This can help when using beamModelTester to generate many outputs consecutively.

Follow [the](/tutorial_1.md) [previous](/tutorial_2.md) [tutorials](/tutorial_3.md) such that you have the data loaded into memory, and create xx channel plots for the model, the scope and the difference with filtered frequencies, normalisation but no cropping.  Once you have this done, you are ready to start this tutorial.

## Selecting an output location

From the main menu, select "File Input/Output options" as you did when [selecting input data](/tutorial_1.md#select-the-input-data) and then choose "Set output file directory."

![Output menu](/images/interactive_snips/gicm_6_4_FileIO_out_menu.PNG)

From there, click on "Select Directory" and pick a suitable location on your file system using the resulting dialogue box.

![Output dialogue](/images/interactive_snips/gicm_6_4_1_FileIO_out_select_menu.PNG)

If you return to the main menu and click "plot with current options," it may appear as though nothing happens.  However, if you check in the directory you have selected, you will find the files corresponding to the outputs you have chosen there.  These files are systematically named based on the parameters they show.
## Selecting output file type
## Dataframe output
## Selecting graph titles

