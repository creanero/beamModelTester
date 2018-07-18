#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 12:32:27 2018

@author: creanero
"""

from ilisa.observations.dataIO import parse_accfolder
#from ..iLiSA.scripts.acc2bst import main as acc2bst_main
from ..iLiSA.scripts import acc2bst
from ilisa.observations.observing import stdPointings


from dreamBeam.scripts.pointing_jones import main as db_main

import argparse

def wrap_arg_parser():
    parser = argparse.ArgumentParser()
    
###############################################################################
#ACC Folder
###############################################################################    
    #creates a group for the acc folder
    acc_model = parser.add_mutually_exclusive_group()
    
    #gives positional and optional ways of providing the raw data 
    acc_model.add_argument("acc_p",nargs="?", default=None, 
                             help='''
The directory containing the ACC output files
                             ''')
    acc_model.add_argument("--acc","-i", 
                             help='''
Alternative way of specifying the directory containing the ACC output files
                             ''')    
    
###############################################################################
#Frequencies
###############################################################################
    #creates a group for the chosen frequency or frequencies
    group_freq = parser.add_mutually_exclusive_group()
    #adds an optional argument for the frequency to filter to
    group_freq.add_argument("--freq","-f", default = [0.0], 
                            type=float, nargs="*",
                        help = '''
set a frequency filter to and display the channels for.   
Must supply a float or collection of floats separated by spaces.
                        ''')
#    #adds an optional argument for a file containing a set of frequencies 
#    #to filter to
#    group_freq.add_argument("--freq_file","-F", default = "", 
#                            help = '''
#set a file containing multiple frequencies to filter to and display the 
#channels for.  The file must contain one float per line in text format.
#                            ''')    
    
        
    #passes these arguments to a unified variable
    args = parser.parse_args()

    freq=args.freq
    #modes['freq_file']=args.freq_file

    #outputs the filename for the model to a returnable variable
    if args.acc_p != None:
        acc=args.acc
    elif args.acc != None:
        acc=args.acc
    else:
        acc=""    
    
    return (acc, freq)

def rcu_to_band(rcu_in):
    '''
    converts from RCU mode to HBA/LBA
    '''
    band_out=""
    if 3==rcu_in:
        band_out="LBA"
    elif 5==rcu_in:
        band_out="HBA"
    elif 7==rcu_in:
        band_out="HBA"
    
    return (band_out)
        
        
def main():
    #gets the command line arguments and parses them into the modes dictionary
    acc, freq =wrap_arg_parser()
    
       
    st_time, rcu_mode, calsrc, duration, stnid =parse_accfolder(acc)
    
    #execfile('/mnt/home_cr/creanero/iLiSA/scripts/acc2bst.py', args=acc+" "+calsrc)
    acc2bst.main(acc,calsrc)
    
    action="print"
    telescopeName="LOFAR"
    band=rcu_to_band(rcu_mode)
    antmodel="Hamaker"
    step_time="519"#519
    target_ra_rad=float(stdPointings(calsrc).split(",")[0])
    target_dec_rad=float(stdPointings(calsrc).split(",")[1])
    epoch=stdPointings(calsrc).split(",")[2]
    CelDir=(target_ra_rad,target_dec_rad,epoch)
    #CelDir=" ".join([str(target_ra_rad),str(target_dec_rad)])
    
#    execfile('/mnt/home_cr/creanero/dreamBeam/scripts/pointing_jones.py', 
#              args=" ".join([out_type,telescopeName, band,  stnid, antmodel, 
#                            st_time, duration, step_time, CelDir]))
    main(telescopeName, band, antmodel, stnid, st_time, duration, step_time,CelDir)
    
if __name__ == "__main__":
    main()

    

