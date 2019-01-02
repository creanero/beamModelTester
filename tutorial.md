# Tutorial
This tutorial will explain the basic steps to running beamModelTester by demonstrating a Sample Analysis of existing data.

## Acquire Data
Save the [two files at this link](https://zenodo.org/record/1744987#.XAEbpdv7SUk) to your local file system.  
You should find a CSV file containing the model of an observation from LOFAR station SE607 and
a HDF5 file containing data extracted from an actual observation which took place on 16th March 2018.

## Run the Script
Run the **rungui.sh** script to start the software in interactive GUI mode

![Main Menu](/images/interactive_snips/gicm_main_menu.PNG)

## Select the input data
Go to "File Input/Output Options"

![File I/O Menu](/images/interactive_snips/gicm_6_FileIO_menu.PNG)

From there, use "Set input model file" to select the CSV file downloaded above as the model input
and use "Set input scope file" to select the HDF5 file downloaded above as the observed input

![Select Model Menu](/images/interactive_snips/gicm_6_1_FileIO_model.PNG)![Select Scope File](/images/interactive_snips/gicm_6_2_1_FileIO_scope_select.PNG)

## Plot with default options
The default options are to plot the linear parameters (xx, xy and yy) for each of the model and observed data.  
A total of six such images are shown, similar to the plots below

<img src="/images/tutorial_model_xx_1.png" width=400><img src="/images/tutorial_scope_yy_1.png" width=400>\
*The model image (left) shows the Hamaker-Arts model of the variation of CasA over a 24 hour observation period.  The actual observation (right) looks almost flat due to the presence of RFI orders of magnitude more intense than the target astronomical source*

## Cropping
In order to remove RFI peaks, several approaches can be taken.  One simple approach is to crop the data to remove all data above a certain level.  In doing so, it becomes possible to see the features of the observed data.  

![Cropping menu](/images/interactive_snips/gicm_1_crop_menu.PNG)

To Enable cropping, go to the cropping menu.  There you are presented with a series of options to define the level
above which to crop, the basis on which to perform the cropping, which of the input files to crop and what type of 
crop operation to perform.  

For now, we'll select "set crop level" and enter "99" to crop the data at the 99th percentile.  

![Crop Level menu](/images/interactive_snips/gicm_1_1_crop_level_menu.PNG)

Next, return to the Cropping Menu, then select the Crop Data menu and click to crop the scope data.  (Only the observed data has the RFI spikes we want to remove.)

![Crop Data menu](/images/interactive_snips/gicm_1_3_crop_data_menu.PNG)

Return to the main menu and select "plot with current options."  Plots similar to the ones below should emerge. (As before, you should expect 6 images, not just the two shown here.

<img src="/images/tutorial_model_xx_2.png" width=400><img src="/images/tutorial_scope_yy_2.png" width=400>\
*The model image (left) remains much the same, but there is now definite structure to the observed data (right).  
Notice the distribution in Frequency and the scale of the observation.  The Hamaker-Arts model is a normalised scale and, by design, does not incorporate the instrumental frequency dependence.  As a result, some normalisation must be applied to the observation to make comparison meaningful.*

## Normalisation

## Select the plots
Select the plots you wish to generate.  



