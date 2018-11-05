# Colour Module 
**Version 1.0\
9th October 2018\
Oisin Creaner**

This function takes in a standard format input  and returns a colour code 
suitable for use with the graphing functions used elsewhere in this project.
These colour codes are coordinated such that a given channel is shown in 
the same colour whenever it is presented, and shades of that colour are used
for different sources of the same channel: light for model, dark for scope

## Inputs
colour_id (a string representing the channel and source to be plotted)

## Outputs
a string representing the colour for the graph

## Outline
The function consists of a series of statements of the form

if colour_id in [list of channel names]:
        return(colour)

When used as part of the color argument of a graphing function, they produce outputs as below
        
## Operation
Below are shown the outputs from the matplotlib.colors API given various input parameters

### p-channel linegraphs:
![p channels](/images/colour_models/p_3.PNG)\
p, p_diff -> orange\
p_model -> sandybrown\
p_scope -> darkorange

### p-channel 3d plots
![p channels](/images/colour_models/p_s.png)\
p_s -> Oranges


### q-channel linegraqhs:
![q channels](/images/colour_models/q_3.PNG)\
q, q_diff -> green\
q_model -> limegreen\
q_scope -> darkgreen

### q-channel 3d qlots
![q channels](/images/colour_models/q_s.png)\
q_s -> Greens


### xx-channel linegraphs:
![xx channels](/images/colour_models/xx_3.PNG)\
xx, xx_diff -> red\
xx_model -> orangered\
xx_scope -> darkred

### xx-channel 3d plots
![xx channels](/images/colour_models/xx_s.png)\
xx_s -> Reds


### xy-channel linegraphs:
![xy channels](/images/colour_models/xy_3.PNG)\
xy, xy_diff -> darkviolet\
xy_model -> mediumorchid\
xy_scope -> purple

### xy-channel 3d plots
![xy channels](/images/colour_models/xy_s.png)\
xy_s -> Oranges


### yy-channel linegraphs:
![yy channels](/images/colour_models/yy_3.PNG)\
yy, yy_diff -> blue\
yy_model -> deepskyblue\
yy_scope -> darkblue

### yy-channel 3d plots
![yy channels](/images/colour_models/yy_s.png)\
yy_s -> Blues


### U-channel linegraphs:
![U channels](/images/colour_models/U_3.PNG)\
U, U_diff -> gold\
U_model -> goldenrod\
U_scope -> darkgoldenrod

### U-channel 3d plots
![U channels](/images/colour_models/U_s.png)\
U_s -> YlOrBr


### V-channel linegraphs:
![V channels](/images/colour_models/V_3.PNG)\
V, V_diff -> orange\
V_model -> sandybrown\
V_scope -> darkorange

### V-channel 3d plots
![V channels](/images/colour_models/V_s.png)\
V_s -> Oranges


### I-channel linegraphs:
![I channels](/images/colour_models/I_3.PNG)\
I, I_diff -> c (cyan)\
I_model -> aquamarine\
I_scope -> teal

### I-channel 3d plots
![I channels](/images/colour_models/I_s.png)\
I_s -> winter


### alt-axis linegraphs:
![alt channels](/images/colour_models/alt_3.PNG)\
'alt','stn_alt' -> black\
'alt_light','stn_alt_light','alt_model','stn_alt_model' -> grey\
'alt_dark','stn_alt_dark'-> darkslategrey

### alt-channel 3d plots
![alt channels](/images/colour_models/alt_s.PNG)\
'alt_s','stn_alt_s'-> Greys


### az-axis linegraphs:
![az channels](/images/colour_models/az_3.PNG)\
'az','stn_az' -> brown\
'az_light','az_ew_light','stn_az_light','stn_az_ew_light','az_model','stn_az_model','az_ew_model','stn_az_ew_model' -> chocolate\
'az_dark','stn_az_dark'-> saddlebrown

### az-channel 3d plots
![az channels](/images/colour_models/az_s.PNG)\
'az_s','stn_az_s'-> copper

### OTHER
Used as a default if the user has entered an unrecognised channel.  A Warning message is also displayed.

![other channels](/images/colour_models/other_3.PNG)\* -> black\
'\*_light','\*_model' -> grey\
'\*_dark','\*_scope'-> darkslategrey

### other-channel 3d plots
![other channels](/images/colour_models/other_s.PNG)\
'\*_s'-> Greys
