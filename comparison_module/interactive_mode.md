# Interactive mode operations of comparison_module

In interactive mode, the comparison module presents the user with a series of screens requesting information from them to enable 
plotting of suitable graphs.

![flowchart](/images/interactive_menu.png)

## Main Menu <a name="MainMenu"></a>
From the main menu, the user can access all the futher menus to select plotting options, proceed to plot, or exit the program

![main menu](/images/interactive_snips/icm_main_menu.png)


Type 0 to exit

## Cropping Menu <a name="1_crop_menu"></a>
From this menu, the user can select what data to crop to remove outliers.
![Cropping menu](/images/interactive_snips/icm_1_crop_menu.PNG)

Type 1 to set the [numerical value for cropping](1_1_crop_level_menu)\
Type 2 to set the [Crop Basis](1_2_crop_basis_menu)\
Type 3 to set the [Crop Data](1_3_crop_data_menu)\
Type 4 to set the [Crop Mode](1_4_crop_mode_menu)\
Type 0 to return to the [Main menu](#MainMenu)

### Crop Level Menu <a name="1_1_crop_level_menu"></a>
![Crop Level menu](/images/interactive_snips/icm_1_1_crop_level_menu.PNG)

Type 0 to return to the [Cropping Menu](#1_crop_menu)

### Crop Basis Menu <a name="1_2_crop_basis_menu"></a> 
![Crop Basis menu](/images/interactive_snips/icm_1_2_crop_basis_menu.PNG)

Type 0 to return to the [Cropping Menu](#1_crop_menu)

### Crop Data Menu <a name="1_3_crop_data_menu"></a>
![Crop Data menu](/images/interactive_snips/icm_1_3_crop_data_menu.PNG)

Type 0 to return to the [Cropping Menu](#1_crop_menu)

### Crop Mode Menu <a name="1_4_crop_mode_menu"></a>
![Crop Mode menu](/images/interactive_snips/icm_1_4_crop_mode_menu.PNG)

Type 0 to return to the [Cropping Menu](#1_crop_menu)


## Normalisation Menu <a name="2_norm_menu"></a>
From this menu, the user can select how to normalise the data from the sources
![Normalisation menu](/images/interactive_snips/icm_2_norm_menu.PNG)

Type 0 to return to the [Main menu](#MainMenu)

### Normalisation Basis Menu <a name="2_1_norm_basis_menu"></a>
![Normalisation Basis menu](/images/interactive_snips/icm_2_1_norm_basis_menu.PNG)

### Normalisation Data Menu <a name="2_2_norm_data_menu"></a>
![Normalisation Data menu](/images/interactive_snips/icm_2_2_norm_data_menu.PNG)


## Animation/3D Effects Menu <a name="icm_3_anim_menu"></a>
From this menu, the user can select options for animating the data or plotting it as a 3-d graph
![Animation/3D Effects menu](/images/interactive_snips/icm_3_anim_menu.PNG)

Type 0 to return to the [Main menu](#MainMenu)

### Animation/3D Selection Menu <a name="3_1_anim_colour_menu"></a>
![Animation/3D Selection menu](/images/interactive_snips/icm_3_1_anim_colour_menu.PNG)

### Frame Rate Menu <a name="3_2_anim_frame_rate_menu"></a>
![Frame Rate menu](/images/interactive_snips/icm_3_2_anim_frame_rate_menu.PNG)



## Target/Location Menu <a name="4_coords_menu"></a>
From this menu, the user can select what a Target or Observing Site
![Target/Location menu](/images/interactive_snips/icm_4_coords_menu.PNG)

Type 0 to return to the [Main menu](#MainMenu)

### Location Menu <a name="4_1_coords_loc_menu"></a>
![Location menu](/images/interactive_snips/icm_4_1_coords_loc_menu.PNG)

#### Enter Location by Name <a name="4_1_coords_loc_menu"></a>
![Enter Location by Name](/images/interactive_snips/icm_4_1_1_coords_loc_name_menu.PNG)
#### Enter Location by Coordinates <a name="4_1_2_coords_loc_coords_menu"></a>
![Enter Location by Coordinates](/images/interactive_snips/icm_4_1_2_coords_loc_coords_menu.PNG)

### Target Menu <a name="4_2_coords_tar_menu"></a>
![Target menu](/images/interactive_snips/icm_4_2_coords_tar_menu.PNG)

#### Enter Target by Name <a name="4_2_1_coords_tar_name_menu"></a>
![Enter Target by Name menu](/images/interactive_snips/icm_4_2_1_coords_tar_name_menu.PNG)
#### Enter Target by Coordinates <a name="4_2_2_coords_tar_coords_menu"></a>
![Enter Target by Name menu](/images/interactive_snips/icm_4_2_2_coords_tar_coords_menu.PNG)

## Plots and Graphs Menu <a name="5_plot_menu"></a>
From this menu, the user can select what graphs to plot
![Plots and Graphs menu](/images/interactive_snips/icm_5_plot_menu.PNG)

Type 0 to return to the [Main menu](#MainMenu)

### Graphs Menu <a name="5_1_graph_plot_menu"></a>
![Graphs menu](/images/interactive_snips/icm_5_1_graph_plot_menu.PNG)

#### Figure of Merit Menu <a name="5_1_1_graph_plot_fom_menu"></a>
![Figure of Merit menu](/images/interactive_snips/icm_5_1_1_graph_plot_fom_menu.PNG)
#### Alt-Azimuth Menu <a name="5_1_2_graph_plot_alt_az_menu"></a>
![Alt-Azimuth menu](/images/interactive_snips/icm_5_1_2_graph_plot_alt_az_menu.PNG)
#### Plot values Menu <a name="5_1_3_graph_plot_values_menu"></a>
![Plot values menu](/images/interactive_snips/icm_5_1_3_graph_plot_values_menu.PNG)

### Graph Values Menu <a name="5_2_graph_values_menu"></a>
![Graph Values menu](/images/interactive_snips/icm_5_2_graph_values_menu.PNG)

## File I/O Menu
From this menu, the user can select File I/O options <a name="6_FileIO_menu"></a>
![File I/O menu](/images/interactive_snips/icm_6_FileIO_menu.PNG)

Type 0 to return to the [Main menu](#MainMenu)

### Model File Entry <a name="6_1_FileIO_model"></a>
![Model File Entry](/images/interactive_snips/icm_6_1_FileIO_model.PNG)

### Scope File Entry <a name="6_2_FileIO_scope"></a>
![Scope File Entry](/images/interactive_snips/icm_6_2_FileIO_scope.PNG)

### Output File Type Menu <a name="6_3_FileIO_type_menu"></a>
![Output File Type menu](/images/interactive_snips/icm_6_3_FileIO_type_menu.PNG)

### Output Directory Menu <a name="6_4_FileIO_out_menu"></a>
![Output Directory menu](/images/interactive_snips/icm_6_4_FileIO_out_menu.PNG)

## Frequency Menu
From this menu, the user can select Frequency filtering options <a name="7_Freq_menu"></a>
![Frequency menu](/images/interactive_snips/icm_7_Freq_menu.PNG)

![Frequency menu with selection](/images/interactive_snips/icm_7_Freq_menu_2.PNG)

Type 0 to return to the [Main menu](#MainMenu)

### Manual Frequency Entry Screen <a name="7_1_Freq_manual_menu"></a>
![Manual Frequency Entry menu](/images/interactive_snips/icm_7_1_Freq_manual_menu.PNG)

#### Manual Frequency Entries <a name="7_1_2_Freq_manual_entries_menu."></a>
![Manual Frequency Entries](/images/interactive_snips/icm_7_1_2_Freq_manual_entries_menu.PNG)

### Frequency File Menu <a name="7_2_Freq_file_menu"></a>
![Frequency File Menu](/images/interactive_snips/icm_7_2_Freq_file_menu.PNG)

## Miscellaneous Menu<a name="8_misc_menu"></a>
From this menu, the user can the offset in time between model and scope, the Title for plots and the calculation used for differences.

![Miscellaneous menu](/images/interactive_snips/icm_8_misc_menu.PNG)

Type 0 to return to the [Main menu](#MainMenu)

### Offset Entry <a name="8_1_misc_offset_menu"></a>
![Offset Entry](/images/interactive_snips/icm_8_1_misc_offset_menu.PNG)

### Title Entry <a name="8_2_misc_title_menu"></a>
![Title Entry](/images/interactive_snips/icm_8_2_misc_title_menu.PNG)

### Difference Type Menu <a name="8_3_misc_diff_menu"></a>
![Difference Type menu](/images/interactive_snips/icm_8_3_misc_diff_menu.PNG)
