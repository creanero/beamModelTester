# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 16:22:34 2018

@author: User
"""

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("model_p",nargs='?', default=None, help="echo the string you use here")
parser.add_argument("scope_p",nargs='?', default=None, help="echo the string you use here")
parser.add_argument("--scope","-s", help="echo the string you use here")
parser.add_argument("--model","-m", help="echo the string you use here")
args = parser.parse_args()

if args.model_p != None:
    in_file_model=args.model_p
elif args.model != None:
    in_file_model=args.model
else:
    in_file_model=raw_input("No model")

print(in_file_model)

if args.scope_p != None:
    print (args.scope_p)
elif args.scope != None:
    print (args.scope)
else:
    print("test scope")