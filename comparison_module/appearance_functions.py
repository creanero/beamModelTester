# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 13:13:45 2018

@author: User
"""

def gen_pretty_name(key,units=False):
    '''
    This function generates suitable names for graph titles and axes from the 
    keys used to access elements of the dataframe in the system. 
    
    e.g. Freq => Frequency
    '''
    pretty_name = key
    if key =='Freq':
        pretty_name = 'Frequency'
        if units == True:
            units = "MHz"
    if key =='d_Time':
        pretty_name = 'Time since start'
        if units == True:
            units = "s"
    
    if key =='Time':
        pretty_name = 'Time'
        if units == True:
            units = "UTC"
    
    elif key =='alt':
        pretty_name = 'Altitude'
        if units == True:
            units = "degrees"             
        
    elif key =='az':
        pretty_name = 'Azimuth'
        if units == True:
            units = "0 to 360 degrees"        
    elif key =='az_ew':
        pretty_name = 'Azimuth'        
        if units == True:
            units = "-180 to +180 degrees"
            
    elif key =='stn_alt':
        pretty_name = 'LOFAR Station Altitude'
        if units == True:
            units = "degrees"            
    elif key =='stn_az':
        pretty_name = 'LOFAR Station Azimuth'
        if units == True:
            units = "0 to 360 degrees"
    elif key =='stn_az_ew':
        pretty_name = 'LOFAR Station Azimuth'
        if units == True:
            units = "-180 to +180 degrees"

    elif key =='scope':
        pretty_name = 'Observed value'
    elif key =='model':
        pretty_name = 'Model value'
    elif key =='diff':
        pretty_name = 'Difference between Observed and Model values'            

    elif key =='rmse':
        pretty_name = 'Root Mean Square Error'    
    elif key =='corr':
        pretty_name = "Pearson's Correlation"            
    if units:
        pretty_name=add_units (pretty_name,units)
    
    return(pretty_name)
    
def add_units(key,units):
    '''
    minor function that adds units in brackets after the key provided
    '''
    new_key = key+' ('+units+')'
    return(new_key)
    
###############################################################################
#
#colour setting functions
#    
###############################################################################    

 
def colour_models(colour_id):
    '''
    The colours used are defined in a function that returns the colour strings
    '''
    #sets oranges for various applications for the p channel
    if 'p'==colour_id:
        return('orange')
    if 'p_light'==colour_id:
        return('sandybrown')
    if 'p_dark'==colour_id:
        return('darkorange')
    if 'p_s'==colour_id:
        return('Oranges')
        
    #sets greens for various applications of the q channel    
    if 'q'==colour_id:
        return('green')
    if 'q_light'==colour_id:
        return('limegreen')
    if 'q_dark'==colour_id:
        return('darkgreen')
    if 'q_s'==colour_id:
        return('Greens')
    
    #sets reds for various applications of the XX channel 
    if 'xx'==colour_id:
        return('red')   
    if 'xx_light'==colour_id:
        return('orangered')
    if 'xx_dark'==colour_id:
        return('darkred')
    if 'xx_s'==colour_id:
        return('Reds')
    
    
    #sets purples for various applications of the XY channel 
    if 'xy'==colour_id:
        return('darkviolet')
    if 'xy_light'==colour_id:
        return('mediumorchid')
    if 'xy_dark'==colour_id:
        return('purple')
    if 'xy_s'==colour_id:
        return('Purples')
    
    
    #sets greens for various applications of the YY channel 
    if 'yy'==colour_id:
        return('blue')
    if 'yy_light'==colour_id:
        return('deepskyblue')
    if 'yy_dark'==colour_id:
        return('darkblue')
    if 'yy_s'==colour_id:
        return('Blues')
        
    #sets golds/yellows for various applications of stokes U
    if 'U'==colour_id:
        return('gold')
    if 'U_light'==colour_id:
        return('goldenrod')
    if 'U_dark'==colour_id:
        return('darkgoldenrod')
    if 'U_s'==colour_id:
        return('YlOrBr')
        
    #sets oranges for various applications for the Stokes V
    if 'V'==colour_id:
        return('darkorange')
    if 'V_light'==colour_id:
        return('sandybrown')
    if 'V_dark'==colour_id:
        return('chocolate')
    if 'V_s'==colour_id:
        return('Oranges')        

    #sets cyans for various applications for the Stokes I
    if 'I'==colour_id:
        return('c')
    if 'I_light'==colour_id:
        return('aquamarine')
    if 'I_dark'==colour_id:
        return('teal')
    if 'I_s'==colour_id:
        return('winter')   

    #sets greens for various applications for the Stokes Q
    #note the distinction from the generic q-channel
    if 'Q'==colour_id:
        return('green')
    if 'Q_light'==colour_id:
        return('limegreen')
    if 'Q_dark'==colour_id:
        return('darkgreen')
    if 'Q_s'==colour_id:
        return('Greens')           

    #sets black/grey for various applications for altitude
    if colour_id in ['alt','stn_alt']:
        return('black')
    if colour_id in ['alt_light','stn_alt_light']:
        return('grey')
    if colour_id in ['alt_dark','stn_alt_dark']:
        return('darkslategrey')
    if colour_id in ['alt_s','stn_alt_s']:
        return('Greys')     
    
    #sets browns for various applications for azimuth
    if colour_id in ['az','az_ew','stn_az','stn_az_ew']:
        return('brown')
    if colour_id in ['az_light','az_ew_light','stn_az_light','stn_az_ew_light']:
        return('chocolatebrown')
    if colour_id in ['az_dark','az_ew_dark','stn_az_dark','stn_az_ew_dark']:
        return('saddlebrown')
    if colour_id in ['az_s','az_ew_s','stn_az_s','stn_az_ew_s']:
        return('Copper')     
    
    #sets grey values for other plots, where there are partial matches.
    if '_light' in colour_id:
        print("Warning: Colour incompletely specified as:\n\n\t"+colour_id+              
              "\n\n'light' found in colourstring.\n"
              "Defaulting to grey\n")
        return ('grey')    
    if '_dark' in colour_id:
        print("Warning: Colour incompletely specified as:\n\n\t"+colour_id+              
              "\n\n'dark' found in colourstring.\n"
              "Defaulting to darkeslategrey\n")
        return ('darkslategrey')  
    if '_s' in colour_id:    
        print("Warning: Colour incompletely or inaccurately specified as:\n\n\t"+colour_id+              
              "\n\n'_s' found in colourstring.\n"
              "Defaulting to Greys\n")
        return ('Greys')      
    
    #returns black as a final default
    else:
        print("Warning: Colour incorrectly specified as:\n\n\t"+colour_id+              
              "\n\nDefaulting to black\n")
        return ('black')    


def channel_maker(channels,modes,sep_str="_"):
    str_channel = ""
    if "each" not in modes ['values']:
        if "all" in modes ['values']:
            str_channel = "all"
        
        elif "stokes" in modes['values']:
            str_channel = "stokes"
        
        elif "linear" in modes['values']:
            str_channel = "linear"
        else:
            str_channel=list_to_string (channels, sep_str)
        return(str_channel)
    else:
        str_channel=list_to_string (channels, sep_str)
                
    return (str_channel)

def list_to_string (m_keys, sep_str="_"):
    
    '''
    creates an output-friendly string for the channel
    '''
    str_channel = str(m_keys)
    for char in (["[","]","'"]):
        str_channel = str_channel.replace(char,'',)
    str_channel.replace(", ",sep_str)    
    
    return (str_channel)