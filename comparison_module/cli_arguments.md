# Command Line Arguments to comparison_module

# positional arguments:<a name="Positional"></a>

### Model Filename (Positional)<a name="model_p"></a>
  model_p               *The file containing the data from the model (Usually
                        DreamBeam)* 
                        Mutually exclusive with [--model](#model)
### Scope Filename (Positional)<a name="scope_p"></a>                        
  scope_p               *The file containing the observed data from the
                        telescope* 
                        Mutually exclusive with [--scope](#scope)

# Optional Arguments:<a name="Optional"></a>

### Help<a name="help"></a>
  -h, --help            *show this help message and exit*
  
## User Interface Options <a name="interface"></a> 

### Verbosity<a name="verbose"></a>  
  --verbose {0,1,2}, -V {0,1,2}
                        sets the level of verbosity for the program outputs. 0
                        indicates silent mode 1 indicates to show warnings or
                        errors only 2 gives verbose progress indicators
### Interactivity<a name="interactive"></a>                          
  --interactive {0,1,2}, -I {0,1,2}
                        sets the level of interactivity for the program
                        inputs. 0 indicates non-interactive mode 1 indicates
                        to allow interactions when crucial elements are
                        missing 2 indicates fully interactive mode #not fully
                        enabled

## File I/O Options <a name="File_IO"></a> 
### Model Filename (Optional)<a name="model"></a>  
  --model MODEL, -m MODEL\
  *Alternative way of specifying the file containing the data from the model*
  Mutually exclusive with [positional model](#model_p)

### Scope Filename (Optional)<a name="scope"></a>    
  --scope SCOPE, -s SCOPE\
  *Alternative way of specifying the file containing the observed data from the telescope*
  Mutually exclusive with [positional scope](#scope_p)

### Output Directory<a name="out_dir"></a>  
  --out_dir OUT_DIR, -o OUT_DIR\
path to a directory in which the output of the program 
is intended to be stored . IF this argument is blank,
output is to std.out and plots are to screen.

### Title<a name="title"></a>  
  --title [TITLE [TITLE ...]], -t [TITLE [TITLE ...]]\
The title for graphs and output files. Spaces are
permitted in title. Output files will have spaces
replaced with underscores

### Output Image File Type<a name="image_type"></a> 
  --image_type {png,gif,jpeg,tiff,sgi,bmp,raw,rgba,html}, -i {png,gif,jpeg,tiff,sgi,bmp,raw,rgba,html}
      Sets the file type for image files to be saved as. If
      using amimations, some file types will save
      animations, and others will save frames. Default is
      png.


## Normalisation and Cropping Options <a name="corp_and_norm"></a> 

### Normalisation Basis <a name="norm"></a> 
  --norm {o,f,n,t}, -n {o,f,n,t}\
  *Method for normalising the scope data\
    **o** = overall (divide by maximum for all data)\
    **f** = frequency (divide by maximum by frequency/subband)\
    **t** = time (divide by maximum by time/observation)\
    **n** = no normalisation.


### Normalisation Data <a name="norm_data"></a> 
  --norm_data {s,m,n,b}, -N {s,m,n,b}\
*Target data for applying the normalisation to \
**s** = scope \
**m** = model \
**n** = no cropping \
**b** = crop both*


### Crop Type <a name="crop_type"></a> 
  --crop_type {median,mean,percentile}, -C {median,mean,percentile}\
  *Sets what style of cropping will be applied to the scope data to remove 
outliers. A value for [--crop](#crop) must also be specified or this argument is ignored. \
        **median** implies drop all values over a given multiple of the median value.\
        **mean** implies drop all values over a given multiple of the median value.\
        **percentile** implies drop all values over a given percentile value.\
          percentiles over 100 are ignored*

### Crop Level <a name="crop"></a>           
  --crop CROP, -c CROP  \
*Set the numeric value for cropping. Depending on [crop mode](#crop_type), this may be a 
multiple of the mean or median, or the percentile level to cut the scope values
 to. Default is not to crop (crop = 0.0). Negative values are converted to 
 positive before use.*
 
 
### Cropping Basis <a name="crop_basis"></a> 
  --crop_basis {t,f}, -k {t,f}\
 *Method for normalising the scope data\
**o** = overall (crop equally for all data)\
**f** = frequency (crop by frequency/subband)\
**n** = no cropping

### Cropping Data <a name="crop_data"></a> 
  --crop_data {s,m,n,b}, -K {s,m,n,b}\
*Target data for applying the cropping to \
**s** = scope \
**m** = model \
**n** = no cropping \
**b** = crop both *

## Difference Options <a name="difference"></a> 
### Difference Type <a name="diff"></a> 
  --diff {sub,div,idiv}, -d {sub,div,idiv}\
  *determines whether to use subtractive or divisive differences when 
  calculating the difference between the scope and the model. Default 
  is subtract.\
  **sub** = model - scope\
  **div** = model / scope\
  **idiv** = scope/model*


## Plotting Options <a name="plotting"></a> 
### Channels to plot <a name="values"></a> 
  --values {all,linear,stokes,xx,xy,yy,U,V,I,Q}, -v {all,linear,stokes,xx,xy,yy,U,V,I,Q}\
  *Sets the parameters that will be plotted on the value and difference graphs.\
  **linear** implies xx, xy and yy-channel values will be plotted.\
  **stokes** implies that Stokes U- V- I- and Q-channels will be plotted.\
  **all** implies that all seven channels will be plotted.\
  An individual channel name means to plot that channel alone.\
  **each** is a modifier that requires that appropriate plots are plotted separately instead of overlaid*
  
### Plots <a name="plots"></a>   
  --plots  {rmse,corr,spectra,file,alt,az,ew,stn,split,values,model,scope,diff,overlay}, \
  -p {rmse,corr,spectra,file,alt,az,ew,stn,split,values,model,scope,diff,overlay}]\
      Sets which plots will be shown. Default is to show rmse, corr and spectra plots
      
      **rmse** shows plots of RMSE (overall, per time and per freq as appropriate)\
      **corr** shows plots of corrlation (overall, per time and per freq as appropriate)\
      **spectra** shows plots of the spectrum of the channels (by frequency over time as appropriate)\
      
      **file** determines whether to output the dataframe to a file for later analyses\
      
      **alt** shows plots of value against altitude\
      **az** shows plots of value against azimuth\
      **ew** means azimuth is plotted East/West (-180/+180) instead of absolute (0/360)\
      **stn** means alt/az coordinates are calculated in the station reference frame\
      **split** means dynamic plots of Alt-Az coordinates are split to avoid aliasing
      
      **values** means to plot both model and scope values\
      **model** means to plot model values\
      **scope** means to plot scope values\
      **diff** shows plots of the differences in values of the channels
      
      **overlay** means that for a given channel, the plots will be overlaid


## Animation and 3-D Plot Options <a name="anim_3d_plots"></a> 
### 3-d Plot options <a name="three_d"></a> 
  --three_d {colour,color,anim,animf,contour},\
  -3 {colour,color,anim,animf,contour}\
      Sets how to show three dimensional plots.\
      If **colour** is chosen, then they are plotted as colours.\
      If **anim** is chosen, plots the data animated over time.\
      If **animf** is chosen, plots the data animated over frequency.\
      If **contour** is chosen, plots the data as a 3-D Contour plot
 
### Frame Rate <a name="frame_rate"></a>      
  --frame_rate FRAME_RATE, -r FRAME_RATE
      Set the numeric value for the number of frames per
      second to attempt to plot animated graphs at. If no
      animated plots are used, or animations are plotted to
      files on a per-frame basis, this variable is ignored.
      Default is 60 FPS

## Time Settings <a name="time_opts"></a> 
### Offset <a name="offset"></a>
  --offset OFFSET, -O OFFSET
      Sets an offset for the scope. This is the amount of
      time (in seconds) that the scope is believed to be
      ahead of the model. This will be subtracted from the
      time of the scope data. Default is no offset. Offsets
      may only be given in whole seconds


## Frequency Settings <a name="frequency"></a> 
### Direct Frequency Selection <a name="freq"></a>
  --freq [FREQ [FREQ ...]], -f [FREQ [FREQ ...]]\
*set a frequency filter to and display the channels for.   Must supply a float or collection of floats separated by spaces.*


### Frequency Selection from File <a name="freq_file"></a>
  --freq_file FREQ_FILE, -F FREQ_FILE\
*set a file containing multiple frequencies to filter to and display the channels for.\
The file must contain one float per line in text format.*


## Target Object Settings <a name="target"></a> 
### Object Name Selection <a name="object_name"></a>
  --object_name {,CasA,CygA,VirA}, -X {,CasA,CygA,VirA}
      set a variable for the name of the target object. This
      is used to generate sky coordinates. At present this
      is enabled only for CasA, CygA and VirA
      
 ### Object Coordinate Entry <a name="object_coords"></a>     
  --object_coords OBJECT_COORDS OBJECT_COORDS, -x OBJECT_COORDS OBJECT_COORDS
      set a variable for the coordinates of the target
      object. Coordinates should be 2 floats: RA and Dec
      (decimal degrees)
      
 ## Location Settings <a name="location"></a> 
### Location Name Selection <a name="location_name"></a>     
  --location_name {,IE613,SE607}, -L {,IE613,SE607}
                        Set the name of the observing location. This is used
                        to generate ground coordinates for the oberving
                        location. From this and target coordinates, Alt-Az
                        coordinates can be generated. At present this is only
                        defined for LOFAR stations IE613 and SE607
                        
 ### Location Coordinate Entry <a name="location_coords"></a>   
  --location_coords [LOCATION_COORDS [LOCATION_COORDS ...]], -l [LOCATION_COORDS [LOCATION_COORDS ...]]
                        set a variable for the coordinates of the observing
                        site. Coordinates should be 3 floats: Latitude,
                        longitude (degrees) and height above sea level
                        (metres). If two coordinates are specified, height
