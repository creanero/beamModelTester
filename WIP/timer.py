#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 23:21:22 2018

@author: creanero
"""

def timer (function_to_run,args_funct):
    import datetime
    start=datetime.datetime.now()
    output=function_to_run(args_funct)
    end=datetime.datetime.now()
    diff=end-start
    print (diff)
    return(output)