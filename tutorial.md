# Tutorial
This tutorial will explain the basic steps to running beamModelTester by demonstrating a Sample Analysis of existing data.

## Acquire Data
Save the [two files at this link](https://zenodo.org/record/1744987#.XAEbpdv7SUk) to your local file system.  
You should find a CSV file containing the model of an observation from LOFAR station SE607 and
a HDF5 file containing data extracted from an actual observation which took place on 16th March 2018.

## Run the Script
Run the **rungui.sh** script to start the software in interactive GUI mode

## Select the input data
Go to "File Input/Output Options"
From there, use "Set input model file" to select the CSV file downloaded above as the model input
and use "Set input scope file" to select the HDF5 file downloaded above as the observed input

## Plot with default options
The default options are to plot the linear parameters (xx, xy and yy) for each of the model and observed data.  
A total of six such images are shown, similar to the plots below

<img src="/images/tutorial_model_xx_1.png" width=400><img src="/images/tutorial_scope_yy_1.png" width=400>\
*The model image (left) shows the Hamaker-Arts model of the variation of CasA over a 24 hour observation period.  The actual observation (right) looks almost flat due to the presence of RFI orders of magnitude more intense than the astronomical sources*

## Cropping
In order to remove RFI peaks, 

## Select the plots
Select the plots you wish to generate.  



