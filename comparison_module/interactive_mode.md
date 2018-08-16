# Interactive mode operations of comparison_module

In interactive mode, the comparison module presents the user with a series of screens requesting information from them to enable 
plotting of suitable graphs.

![flowchart](/images/interactive_menu.png)


## Main Menu <a name="MainMenu"></a>
From the main menu, the user can access all the futher menus to select plotting options, proceed to plot, or exit the program

![main menu](/images/interactive_snips/icm_main_menu.png)

Type 1 to set [Cropping options](#1_crop_menu)\
Type 2 to set [Normalisation options](#2_norm_menu)\
Type 3 to set [3d Plotting or Animation options](#3_anim_menu)\
Type 4 to set [Target or Station Location options](#4_coords_menu)\
Type 5 to set [Graphing and Plotting options](#5_plot_menu)\
Type 6 to set [File I/O options](#6_FileIO_menu)\
Type 7 to set [Select frequencies to plit](#7_Freq_menu)\
Type 8 to set [Miscellaneous options](#8_misc_menu)

Type 9 to plot the outputs as [shown here](/comparison_module/outputs.md)\
Type 0 to exit the program without plotting further

## Cropping Menu <a name="1_crop_menu"></a>
From this menu, the user can select what data to crop to remove outliers.
![Cropping menu](/images/interactive_snips/icm_1_crop_menu.PNG)

Type 1 to set the [Numerical value for cropping](#1_1_crop_level_menu)\
Type 2 to set the [Crop Basis](#1_2_crop_basis_menu)\
Type 3 to set the [Crop Data](#1_3_crop_data_menu)\
Type 4 to set the [Crop Mode](#1_4_crop_mode_menu)

Type 0 to return to the [Main menu](#MainMenu)

### Crop Level Menu <a name="1_1_crop_level_menu"></a>
At this menu, the user may select the level of crop to apply to discard outliers from the data commonly caused by RFI

![Crop Level menu](/images/interactive_snips/icm_1_1_crop_level_menu.PNG)

Type in a number and hit enter.  This number will inform the level at which to apply cropping.  If crop mode is set to mean or median, this becomes a multiplier for the mean or median, above which all values are excluded.  If crop mode is set to percentile, then this is the percentile above which values are excluded.  If percentile mode is selected and a value over 100% is entered, no cropping will take place.

### Crop Basis Menu <a name="1_2_crop_basis_menu"></a> 
At this menu the user may select whether to crop based on the level over each frequency individually (to attempt to exclude transient noise) or to exclude based on the overall level (which will typically exclude frequencies with loud RFI)

![Crop Basis menu](/images/interactive_snips/icm_1_2_crop_basis_menu.PNG)

Type n to choose not to crop any data\
Type o to choose to crop data based on overall level\
Type f to choose to crop data based on each frequency separately

Type 0 to return to the [Cropping Menu](#1_crop_menu)

### Crop Data Menu <a name="1_3_crop_data_menu"></a>
At this menu, the user may select whether to crop scope or model data, or both or neither.

![Crop Data menu](/images/interactive_snips/icm_1_3_crop_data_menu.PNG)

Type n to choose not to crop any data\
Type s to choose to crop scope data only\
Type m to choose to crop model data only\
Type b to choose to crop both scope and model data

Type 0 to return to the [Cropping Menu](#1_crop_menu)

### Crop Mode Menu <a name="1_4_crop_mode_menu"></a>
At this menu, the user can select the variable upon which the crop level is calculated

This mode is used with crop level to determine what values are excluded from plotting.  If crop mode is set to mean or median, crop level becomes a multiplier for the mean or median, above which all values are excluded.  If crop mode is set to percentile, then crop level sets is the percentile above which values are excluded.  If percentile mode is selected and a value over 100% is entered, no cropping will take place.

![Crop Mode menu](/images/interactive_snips/icm_1_4_crop_mode_menu.PNG)

Type 1 to choose to crop data based on median\
Type 2 to choose to crop data based on mean\
Type 3 to choose to crop data based on percentile

Type 0 to return to the [Cropping Menu](#1_crop_menu)


## Normalisation Menu <a name="2_norm_menu"></a>
From this menu, the user can select how to normalise the data from the sources
![Normalisation menu](/images/interactive_snips/icm_2_norm_menu.PNG)

Type 1 to set the [Normalisation Basis](#2_1_norm_basis_menu)\
Type 2 to set the [Normalisation Data](#2_2_norm_data_menu)

Type 0 to return to the [Main menu](#MainMenu)

### Normalisation Basis Menu <a name="2_1_norm_basis_menu"></a>
At this menu the user may select whether to normalise based on the maximum (post cropping) level for each frequency individually (to attempt to exclude flatten out effects due to instrument sensitivity by frequency) or to normalise based on the overall maximum level after any cropping (if no cropping is present and there is loud RFI on one or more subbands, many other values will be close to zero in this case.)

![Normalisation Basis menu](/images/interactive_snips/icm_2_1_norm_basis_menu.PNG)

Type n to choose not to normalise any data\
Type o to choose to normalise data based on overall level\
Type f to choose to normalise data based on each frequency separately

Type 0 to return to the [Normalisation Menu](#2_norm_menu)

### Normalisation Data Menu <a name="2_2_norm_data_menu"></a>
At this menu, the user may select whether to crop scope or model data, or both or neither.

![Normalisation Data menu](/images/interactive_snips/icm_2_2_norm_data_menu.PNG)

Type n to choose not to normalise any data\
Type s to choose to normalise scope data only\
Type m to choose to normalise model data only\
Type b to choose to normalise both scope and model data

Type 0 to return to the [Normalisation Menu](#2_norm_menu)

## Animation/3D Effects Menu <a name="3_anim_menu"></a>
From this menu, the user can select options for animating the data or plotting it as a 3-d graph

![Animation/3D Effects menu](/images/interactive_snips/icm_3_anim_menu.PNG)

Type 1 to set how 3-variable graphs are plotted [(animated or 3d colour/contour plots)](#3_1_anim_colour_menu)\
Type 2 to set the [Frame Rate](#3_2_anim_frame_rate_menu) for animated plots

Type 0 to return to the [Main menu](#MainMenu)

### Animation/3D Selection Menu <a name="3_1_anim_colour_menu"></a>
From this menu, the user can select how 3-variable graphs are plotted.  They may be plotted as 3-d colour plots, with colour schemes selected based on the data to be plotted, as animated 2-d graphs where time is used to represent the third variable or as 3-d contour plots.

![Animation/3D Selection menu](/images/interactive_snips/icm_3_1_anim_colour_menu.PNG)

Type 1 to plot 3-d colour graphs\
Type 2 to plot animated graphs where time represents itself (or orientation when time is not plotted)\
Type 3 to plot animated graphs where time represents frequency\
Type 4 to plot 3-d contour graphs

Type 0 to return to the [Cropping Menu](#1_crop_menu)

### Frame Rate Menu <a name="3_2_anim_frame_rate_menu"></a>
From this menu, the user can enter the frame rate per second for any animated plots generated.  If there are no animated plots, this value will be ignored.  By default, the frame rate is 60FPS.  If the frame rate exceeds the capability of the device used to generate it, the frame rate will be maximised.

![Frame Rate menu](/images/interactive_snips/icm_3_2_anim_frame_rate_menu.PNG)

The user enters their preferred frame rate and then presses enter

## Target/Location Menu <a name="4_coords_menu"></a>
From this menu, the user can select a Target or Observing Site
![Target/Location menu](/images/interactive_snips/icm_4_coords_menu.PNG)

Type 1 to set the [Observing Location](#4_1_coords_loc_menu)\
Type 2 to set the [Target Object](#4_2_coords_tar_menu) for animated plots

Type 0 to return to the [Main menu](#MainMenu)

### Location Menu <a name="4_1_coords_loc_menu"></a>
From this menu, the user can set the observing location, either by entering the station name or by manually entering the Latitude/Longitude/Altitude coordinates of the station.

![Location menu](/images/interactive_snips/icm_4_1_coords_loc_menu.PNG)

Type N to enter the location by [station name](#4_1_1_coords_loc_name_menu)\
Type C to enter the location by [coordinates](#4_1_2_coords_loc_coords_menu)

Type 0 to return to the [Target/Location Menu](#4_coords_menu)

#### Enter Location by Name <a name="4_1_1_coords_loc_name_menu"></a>
![Enter Location by Name](/images/interactive_snips/icm_4_1_1_coords_loc_name_menu.PNG)

On this menu, the user may enter a LOFAR station ID (e.g. IE613) and the coordinates will be automatically set.  Note that station IDs are case sensitive and letters must be UPPERCASE.  Note also that not all station IDs are currently available for use and it may be necessary to submit coordinates manually in that case.

#### Enter Location by Coordinates <a name="4_1_2_coords_loc_coords_menu"></a>
![Enter Location by Coordinates](/images/interactive_snips/icm_4_1_2_coords_loc_coords_menu.PNG)

On this menu, the user is prompted to enter first the Latitude coordinate (in decimal degrees), then the Longitude coordinate (in decimal degrees), then the Altitude above sea level in metres.  If the user enters a blank value for any coordinate, then that coordinate and any subsequent coordinates are set to 0, and the screen returns to the previous menu.  If the user submits an invalid coordinate (e.g. non-numeric characters) they are prompted to reenter the coordinate.  The coordinates (Lat: 0, Long: 0) are reserved to indicate no geographical plots are needed. Since there is no land (and no radio telescope) at this location, this is not considered a limitation, but should such a location be needed, an arbitrarily small value (e.g. 1e-308) should be used for one or both of the coordinates.

### Target Menu <a name="4_2_coords_tar_menu"></a>
From this menu, the user can set the target object, either by entering the object's name or by manually entering the RA/Dec coordinates of the object.

![Target menu](/images/interactive_snips/icm_4_2_coords_tar_menu.PNG)

Type N to enter the target by [name](#4_2_1_coords_tar_name_menu)\
Type C to enter the target by [coordinates](#4_2_2_coords_tar_coords_menu)

Type 0 to return to the [Target/Location Menu](#4_coords_menu)

#### Enter Target by Name <a name="4_2_1_coords_tar_name_menu"></a>
![Enter Target by Name menu](/images/interactive_snips/icm_4_2_1_coords_tar_name_menu.PNG)

On this menu, the user may enter a target object name (e.g. CasA) and the coordinates will be automatically set.  Note that object names are case sensitive and letters must be in PascalCase.  Note also that relatively few object IDs are currently available for use and it may be necessary to submit coordinates manually in that case.

#### Enter Target by Coordinates <a name="4_2_2_coords_tar_coords_menu"></a>
![Enter Target by Name menu](/images/interactive_snips/icm_4_2_2_coords_tar_coords_menu.PNG)

On this menu, the user is prompted to enter first the Right Ascension coordinate (in decimal degrees), then the Declination coordinate (in decimal degrees).  If the user enters a blank value for any coordinate, then that coordinate and any subsequent coordinates are set to 0, and the screen returns to the previous menu.  If the user submits an invalid coordinate (e.g. non-numeric characters) they are prompted to reenter the coordinate.  The coordinates (RA: 0, Dec: 0) are reserved to indicate no Astrometric plots are needed. Should a target at the point of the Vernal Equinox be needed, an arbitrarily small value (e.g. 1e-308) should be used for one or both of the coordinates.

## Plots and Graphs Menu <a name="5_plot_menu"></a>
From this menu, the user can select between choosing which graphs to plot or which channels to plot them for

![Plots and Graphs menu](/images/interactive_snips/icm_5_plot_menu.PNG)

Type 1 to set the [graphs to plot](#5_1_graph_plot_menu)\
Type 2 to select the [Channels to plot](#5_2_graph_values_menu)

Type 0 to return to the [Main menu](#MainMenu)


### Graphs Menu <a name="5_1_graph_plot_menu"></a>
From this menu, the user may select which graphs to plot.

![Graphs menu](/images/interactive_snips/icm_5_1_graph_plot_menu.PNG)

Type 1 to select [figures of merit](#5_1_1_graph_plot_fom_menu) of the difference between model and scope\
Type 2 to select [Alt-Azimuth plotting options](#5_1_2_graph_plot_alt_az_menu)\
Type 3 to which of the [model, scope or difference](#5_1_3_graph_plot_values_menu) values to plot\
Type 4 to toggle whether or not to overlay 2-d plots from a single channel\
Type 5 to toggle whether or not to plot time series plots

Type 0 to return to the [Plots and Graphs Menu](#5_plot_menu)

#### Figure of Merit Menu <a name="5_1_1_graph_plot_fom_menu"></a>
From this menu, the user may toggle which figures of merit to plot

![Figure of Merit menu](/images/interactive_snips/icm_5_1_1_graph_plot_fom_menu.PNG)

Type 1 to toggle whether or not to plot Root Mean Square Error (RMSE)\
Type 2 to toggle whether or not to plot Pearson's Correlation

Type 0 to return to the [Graphs Menu](#5_1_graph_plot_menu)

#### Alt-Azimuth Menu <a name="5_1_2_graph_plot_alt_az_menu"></a>
From this menu, the user may toggle which variables to plot for Alt/Azimuth plots

![Alt-Azimuth menu](/images/interactive_snips/icm_5_1_2_graph_plot_alt_az_menu.PNG)

Type 1 to toggle whether or not to plot against Altitude\
Type 2 to toggle whether or not to plot against Azimuth\
Type 3 to toggle whether or not to plot Azimuth from -180 to +180 (as opposed to 0 to 360)\
Type 4 to toggle whether or not to plot using the LOFAR Station coordinate system (instead of the standard horizon)\
Type 5 to toggle whether or not to split plots which loop in half to avoid aliasing of data

Type 0 to return to the [Graphs Menu](#5_1_graph_plot_menu)

#### Plot values Menu <a name="5_1_3_graph_plot_values_menu"></a>
From this menu, the user may toggle which variables to plot from model, scope and difference values

![Plot values menu](/images/interactive_snips/icm_5_1_3_graph_plot_values_menu.PNG)

Type 1 to toggle whether or not to plot Model Data\
Type 2 to toggle whether or not to plot Scope Data\
Type 3 to toggle whether or not to plot the Difference between Model and Scope Data

Type 0 to return to the [Graphs Menu](#5_1_graph_plot_menu)

### Graph Values Menu <a name="5_2_graph_values_menu"></a>
From this menu, the user may toggle which channels to plot.

![Graph Values menu](/images/interactive_snips/icm_5_2_graph_values_menu.PNG)

Type the case-sensitive name of the channel to toggle plotting that channel from the list (xx, xy, yy, U, V, I, Q)

Type the name of a group to toggle all channels in that group.  If some but not all members of the group are on, then toggling a group will turn on all members of the group.\
Group composition:\
linear (xx, xy, yy)\
stokes (U, V, I, Q)\
all (xx, xy, yy, U, V, I, Q)

## File I/O Menu<a name="6_FileIO_menu"></a>
From this menu, the user can select File I/O options 

![File I/O menu](/images/interactive_snips/icm_6_FileIO_menu.PNG)


Type 1 to set the [input file for Model Data](#6_1_FileIO_model)\
Type 2 to set the [input file for Scope Data](#6_2_FileIO_scope)\
Type 3 to set the [output file type](#6_3_FileIO_type_menu)\
Type 4 to set the [output data directory](#6_4_FileIO_out_menu)\
Type 5 to toggle whether or not to output the calculated data to a file

Type 0 to return to the [Main menu](#MainMenu)

### Model File Entry <a name="6_1_FileIO_model"></a>
From this screen, the user can enter the path to the input file containing model data.

![Model File Entry](/images/interactive_snips/icm_6_1_FileIO_model.PNG)

### Scope File Entry <a name="6_2_FileIO_scope"></a>
From this screen, the user can enter the path to the input file containing scope data.

![Scope File Entry](/images/interactive_snips/icm_6_2_FileIO_scope.PNG)

### Output File Type Menu <a name="6_3_FileIO_type_menu"></a>
From this screen, the user may select the file type for output image files

![Output File Type menu](/images/interactive_snips/icm_6_3_FileIO_type_menu.PNG)

Type 1 to switch the file type to Portable Network Graphics (png) \[Default\]\
Type 2 to switch the file type to Graphics Interchange Format (gif)\
Type 3 to switch the file type to Joint Photographic Experts Group format (jpeg)\
Type 4 to switch the file type to Tagged Image File Format (tiff)\
Type 5 to switch the file type to Silicon Graphics Image (sgi)\
Type 6 to switch the file type to Bitmap (bmp)\
Type 7 to switch the file type to Raw Image Format (raw)\
Type 8 to switch the file type to Red Green Blue Alpha (rgba)\
Type 9 to switch the file type to HyperText Markup Language (html) \[images stored as png, html controls animation\]

Type 0 to return to the [File I/O menu](#6_1_FileIO_model)

### Output Directory Menu <a name="6_4_FileIO_out_menu"></a>
From this screen, the user can enter the path to a directory which will be used to store output data.  If the user leaves this entry blank, output will instead be sent to the screen if possible.

![Output Directory menu](/images/interactive_snips/icm_6_4_FileIO_out_menu.PNG)

## Frequency Menu<a name="7_Freq_menu"></a>
From this menu, the user can select Frequency filtering options 

![Frequency menu](/images/interactive_snips/icm_7_Freq_menu.PNG)

Type 1 to enter [Frequencies Manually](#7_1_Freq_manual_menu) one at a time\
Type 2 to set the [input file for Frequencies to select](#7_2_Freq_file_menu)

Type 0 to return to the [Main menu](#MainMenu)

![Frequency menu with selection](/images/interactive_snips/icm_7_Freq_menu_2.PNG)\
This menu also shows the frequencies that have been selected.

Type 0 to return to the [Main menu](#MainMenu)

### Manual Frequency Entry Screen <a name="7_1_Freq_manual_menu"></a>
This menu is used to add or clear frequencies from the selected list.

![Manual Frequency Entry menu](/images/interactive_snips/icm_7_1_Freq_manual_menu.PNG)

Type 1 to clear any selected frequencies and go back to plotting all frequencies\
Type 2 to [start entering frequencies](#7_1_2_Freq_manual_entries_menu)

Type 0 to return to the [Main menu](#MainMenu)

#### Manual Frequency Entries <a name="7_1_2_Freq_manual_entries_menu"></a>
On this screen, the user is prompted to enter a frequency to be plotted.  Once they do, they are prompted for another.  This repeats until they enter "0" instead of the frequency to plot.  If they enter an invalid value (e.g. non-numeric value, or a value that includes units) then an error will be generated and they will be prompted for a new value.

![Manual Frequency Entries](/images/interactive_snips/icm_7_1_2_Freq_manual_entries_menu.PNG)

### Frequency File Menu <a name="7_2_Freq_file_menu"></a>
From this screen, the user can enter the path to the input file containing a list of frequencies.  Frequencies entered in this way must be stored as one frequency in Hertz per line with no header or separators other than the newlines.

![Frequency File Menu](/images/interactive_snips/icm_7_2_Freq_file_menu.PNG)

## Miscellaneous Menu<a name="8_misc_menu"></a>
From this menu, the user can the offset in time between model and scope, the Title for plots and the calculation used for differences.

![Miscellaneous menu](/images/interactive_snips/icm_8_misc_menu.PNG)


Type 1 to set the [offset between model and scope](#8_1_misc_offset_menu)\
Type 2 to set the [titles for plots and files](#8_2_misc_title_menu)\
Type 3 to set the [operation used for the difference between model and scope](#8_3_misc_diff_menu)

Type 0 to return to the [Main menu](#MainMenu)

### Offset Entry <a name="8_1_misc_offset_menu"></a>
At this menu, the user can enter the time in seconds between the model and scope data, where observations do not line up exactly on the same times as one another.  Ideally, this should be the closest possible separation between model and scope

![Offset Entry](/images/interactive_snips/icm_8_1_misc_offset_menu.PNG)

Instead of entering a time, if the user leaves the time blank, then this will take them back to the [previous menu](#8_misc_menu).

### Title Entry <a name="8_2_misc_title_menu"></a>
At this scree the user can enter a title for the graphs.  This title will be edited to replace spaces with underscores and used as the prefix for file names.  

![Title Entry](/images/interactive_snips/icm_8_2_misc_title_menu.PNG)

Instead of entering a title, if the user enters 0, then this will take them back to the [previous menu](#8_misc_menu).\
If the user enters "X" then the current title will be cleared.\
It is not possible to begin a title with "0" or "X"

### Difference Type Menu <a name="8_3_misc_diff_menu"></a>
At this menu, the user may choose the operation used to determine the difference between scope and model data

![Difference Type menu](/images/interactive_snips/icm_8_3_misc_diff_menu.PNG)

Type 1 to use subtraction (model - scope)\
Type 2 to use division (model / scope)\
Type 3 to use inverse division (scope / model)

Type 0 to return to the [previous menu](#8_misc_menu)
