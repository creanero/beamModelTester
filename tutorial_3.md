# Frequency filtering<a name="frequencies"></a>
When using beamModelTester, it is often necessary to focus in on one or a small number of frequencies, or to remove certain frequencies whcih are known to have RFI noise sources.  To achieve this, one can use the frequency filtering options outlined below.  

Follow the previous tutorials such that you have the [data](/tutorial_1.md#input) loaded into memory, and create [xx and yy channel](/tutorial_2.md#variables) plots for the model, the scope and the [difference](/tutorial_2.md#differences), and apply [normalisation](/tutorial_1.md#normalisation) and [cropping](/tutorial_1.md#cropping).  Once you have this done, you are ready to start this tutorial.

## Select Frequencies Manually<a name="manual"></a>
Firstly, let's choose which frequencies to plot manually.  From the main menu, select Frequency Options to bring up the Frequency Settings Menu

![Frequency Menu](/images/interactive_snips/gicm_7_Freq_menu.PNG)

From that menu, select the "Set frequencies individually" option to bring up the manual frequency entry menu.

![Manual Frequency Menu](/images/interactive_snips/gicm_7_1_Freq_manual_menu.PNG)

From this screen, select "add new frequencies to plotting list"

![Manual Frequency Entry Menu](/images/interactive_snips/gicm_7_1_2_Freq_manual_entries_menu.PNG)

Type 125e6 into the text box.  This will select a frequency of 125MHz.  (Note that frequencies are always specified in Hz.)  Hit "click to confirm" to add 125MHz to the list.  Then click "stop entering frequencies" to return to the previous menu.

Return to the main menu and plot the graph as shown below.  

<img src="/images/tutorial_3_1_1.png" width=280><img src="/images/tutorial_3_1_3.png" width=280><img src="/images/tutorial_3_1_3.png" width=280>\
*A static lineplot for the variation of the target at 125MHz is produced.*

Go back to the Manual Frequency menu and select "Clear Frequency Selection" to proceed to the next section.

## Select Frequencies by File<a name="file"></a>
Follow this [link to Zenodo](https://zenodo.org/record/2592487#.XIkyiIXLcUE) and download the file [SE607_HBA_trimmed_freqs.csv](https://zenodo.org/record/2592487/files/SE607_HBA_trimmed_freqs.csv?download=1).  This file will be used to select only clean frequencies.  The file consists of a number on each line corresponding to the a frequency to be plotted.  Now go to the Frequency Settings Menu again and this time select "Set Frequency by File" to bring up the "Frequency File Menu."

![Frequency File Menu](/images/interactive_snips/gicm_7_2_Freq_file_menu.PNG)

From there, go to "Select File" to bring up a dialogue box from which you can pick the file with the list of frequencies that you just downloaded.

![Frequency File Select Menu](/images/interactive_snips/gicm_7_2_1_Freq_file_select_menu.PNG)

Then return to the main menu again and plot the graphs.  

![Filtered Frequency plot](/images/tutorial_3_2_1.png)\
*A plot of the xx channel from the scope using the filtered frequencies list.  Note the area in the bottom right corner of the plot circled in green.  This is where the [cropping system](/tutorial_1.md#cropping) has removed the peak of the true distribution as well as RFI peaks.*

Return to the [cropping system](/tutorial_1.md#cropping) and go to the select drop data option and switch it to "Crop Neither."  Plot the data again.

![Filtered Frequency plot No Crop](/images/tutorial_3_3_1.png)\
*Now, you can see the results of filtering frequencies without cropping the data.  If the frequencies with RFI peaks can be reliably identified, this is a more reliable method for producing a good representation of the observed data than cropping.*

With the frequencies filtered, it becomes much more practically possible to compare the observed data with the model and produce a difference between the two which is not dominated by RFI.  Return to the [Plotting Data Select Menu](/tutorial_2.md#plotting-differences) and plot the differences.

![Filtered Difference plot No Crop](/images/tutorial_3_4_1.png)\
*This plot shows the difference between the real observation and the prediction.  Sidelobe contamination from other sources can be observed in this plot in the form of the parabola-shaped structures towards the top of the plot.*

[Tutorial 4](/tutorial_4.md) will show the options for file output for beamModelTester.
