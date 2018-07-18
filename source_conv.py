#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 18:25:07 2018

@author: creanero
"""
from ilisa.observations.observing import stdPointings

import argparse

def conv_arg_parser():
    parser = argparse.ArgumentParser()
###############################################################################
#Difference options
###############################################################################    
    
    #adds an optional argument for the mechanism for comparing scope with model
    parser.add_argument("target", default = "",
                        help = '''
this is the name of the target object.  The program will return its coordinates
                        ''')
    
###############################################################################
#Using the arguments
###############################################################################
    #passes these arguments to a unified variable
    args = parser.parse_args()
    target =args.target   
    return (target)


def main():
    #gets the command line arguments and parses them into the modes dictionary
    target =conv_arg_parser()
    
    target_ra_rad=float(stdPointings(target).split(",")[0])
    target_dec_rad=float(stdPointings(target).split(",")[1])
    
    CelDir=" ".join([str(target_ra_rad),str(target_dec_rad)])
    
    return(CelDir)
    
if __name__ == "__main__":
    print(main())

    
