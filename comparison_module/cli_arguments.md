# Command Line Arguments to comparison_module

**positional arguments:**\
  model_p               *The file containing the data from the model (Usually
                        DreamBeam)*\
  scope_p               *The file containing the observed data from the
                        telescope*

**optional arguments:**\
  -h, --help            *show this help message and exit*
  
  --model MODEL, -m MODEL\
  *Alternative way of specifying the file containing the data from the model*
  
  --scope SCOPE, -s SCOPE\
  *Alternative way of specifying the file containing the observed data from the telescope*
  
  --out_dir OUT_DIR, -o OUT_DIR\
path to a directory in which the output of the program 
is intended to be stored . IF this argument is blank,
output is to std.out and plots are to screen.

  --title [TITLE [TITLE ...]], -t [TITLE [TITLE ...]]\
The title for graphs and output files. Spaces are
permitted in title. Output files will have spaces
replaced with underscores

  --norm {t,f,n}, -n {t,f,n}\
  *Method for normalising the scope data\
  t = trivial (divide by maximum for all scope data)\
  f = frequency (divide by maximum by frequency/subband)\
  n = no normalisation.*
  
  --norm_data {s,m,n,b}, -N {s,m,n,b}\
*Target data for applying the normalisation to \
**s** = scope \
**m** = model \
**n** = no cropping \
**b** = crop both*
                        
  --crop_type {median,mean,percentile}, -C {median,mean,percentile}\
  *Sets what style of cropping will be applied to the scope data to remove 
outliers. A value for --crop must also be specified or this argument is ignored. \
        **median** implies drop all values over a given multiple of the median value.\
        **mean** implies drop all values over a given multiple of the median value.\
        **percentile** implies drop all values over a given percentile value.\
          percentiles over 100 are ignored*
          
  --crop CROP, -c CROP  \
*Set the numeric value for cropping. Depending on crop mode, this may be a 
multiple of the mean or median, or the percentile level to cut the scope values
 to. Default is not to crop (crop = 0.0). Negative values are converted to 
 positive before use.*
 
  --crop_basis {t,f}, -k {t,f}\
 *Method for normalising the scope data \
**t** = trivial (crop equally for all data) \
**f** = frequency (crop by frequency/subband)*

  --crop_data {s,m,n,b}, -K {s,m,n,b}\
*Target data for applying the cropping to \
**s** = scope \
**m** = model \
**n** = no cropping \
**b** = crop both *

  --diff {sub,div,idiv}, -d {sub,div,idiv}\
  *determines whether to use subtractive or divisive differences when 
  calculating the difference between the scope and the model. Default 
  is subtract.\
  **sub** = model - scope\
  **div** = model / scope\
  **idiv** = scope/model*
  
  --values {all,linear,stokes,xx,xy,yy,U,V,I,Q}, -v {all,linear,stokes,xx,xy,yy,U,V,I,Q}\
  *Sets the parameters that will be plotted on the value and difference graphs.\
  **linear** implies xx, xy and yy-channel values will be plotted.\
  **stokes** implies that Stokes U- V- I- and Q-channels will be plotted.\
  **all** implies that all seven channels will be plotted.\
  An individual channel name means to plot that channel alone.\
  **each** is a modifier that requires that appropriate plots are plotted separately instead of overlaid*
  
  --plots [{rmse,corr,value,diff} [{rmse,corr,value,diff} ...]], \
  -p [{rmse,corr,value,diff} [{rmse,corr,value,diff} ...]]\
*Sets which plots will be shown.  Default is to show all plots and calculations\
**rmse** shows plots of RMSE (overall, per time and per freq as appropriate)\
**corr** shows plots of corrlation (overall, per time and per freq as appropriate)\
**value** shows plots of the values of the channels (per time and per freq as appropriate)\
**diff** shows plots of the differences in values of the channels (per time and per freq as appropriate)*

  --freq [FREQ [FREQ ...]], -f [FREQ [FREQ ...]]\
*set a frequency filter to and display the channels for.   Must supply a float or collection of floats separated by space.*

  --freq_file FREQ_FILE, -F FREQ_FILE\
*set a file containing multiple frequencies to filter to and display the channels for.\
The file must contain one float per line in text format.*
