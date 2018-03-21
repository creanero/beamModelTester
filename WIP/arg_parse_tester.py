# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 16:22:34 2018

@author: User
"""

import argparse

def beam_arg_parser():
    parser = argparse.ArgumentParser()
    
    #creates a group for the model filename
    group_model = parser.add_mutually_exclusive_group()
    
    #gives positional and optional ways of providing the model data 
    group_model.add_argument("model_p",nargs='?', default=None, 
                             help="The file containing the data from the model (Usually DreamBeam)")
    group_model.add_argument("--model","-m", 
                             help="Alternative way of specifying the file containing the data from the model")
    
    
    #creates a group for the scope filename
    group_scope = parser.add_mutually_exclusive_group()
    
    #gives positional and optional ways of providing the scope data 
    group_scope.add_argument("scope_p",nargs='?', default=None, 
                             help="The file containing the observed data from the telescope")
    group_scope.add_argument("--scope","-s", 
                             help="Alternative way of specifying the file containing the observed data from the telescope")
    
    
    #passes these arguments to a unified variable
    args = parser.parse_args()
    
    #outputs the filename for the model to a returnable variable
    if args.model_p != None:
        in_file_model=args.model_p
    elif args.model != None:
        in_file_model=args.model
    else:
        in_file_model=raw_input("No model filename specified:\n"
                                "Please enter the model filename:\n")
    
    
    #outputs the filename for the scope to a returnable variable
    if args.scope_p != None:
        in_file_scope=args.scope_p
    elif args.scope != None:
        in_file_scope=args.scope
    else:
        in_file_scope=raw_input("No filename specified for observed data from the telescope:\n"
                                "Please enter the telescope filename:\n")
    
    return(in_file_model,in_file_scope)
    
in_file_model,in_file_scope=beam_arg_parser()
print(in_file_model)
print(in_file_scope)
