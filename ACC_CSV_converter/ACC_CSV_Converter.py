# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 16:25:32 2018

@author: Oisin Creaner
This program is designed to read in an ACC file from LOFAR and convert it to 
a csv file with the same name but different extension
"""
import struct
import numpy as np
import os
import sys

#definitions of file names
#hard coded for demo purposes, can edit - this probably should be a parameter
test_file='C:\\Users\\User\\Dropbox\\Work\\DIAS\\RINGS\\BeamModelling\\ACC_Files\\20120513_052251_acc_512x192x192.dat'
out_file=test_file.replace(".dat",".csv")

#defines parameters to do with the RCU count - this could be a parameter
rcu_count=192 #defined for LBA stations
count=(rcu_count**2)*2  #size of covariance matrix: NxN complex (float x 2) elements
count_string="<%dd"%count #"<73728d" format string for unpack: Little endian 73728 floats

#sets the number of subbands - could be parameterised
subbands=1#512 
float_size=8 #Is this fully portable?  Is there an automatic way of handling this?

#sets up a variable for subband index
subband_index=0

#sets up variables to be used to do some stats on the correlation matrices.  Not currently used
#mean_list=[]
#sd_list=[]

#checks that the filename has been successfully changed for the output
if test_file==out_file:
    sys.exit("Incorrect File Type")

#tests to see if the file is right
in_size= os.path.getsize(test_file)
expected_size=count*subbands*float_size
if in_size < expected_size:
    print("file too small")
    sys.exit()
    
    
#opens the input file
try:
    test_fv=open(test_file, "rb")
except IOError:
    print("File not found")
    sys.exit("Unable to open "+test_file)

#opens the output file
try:
    out_fv=open(out_file, "w")
except IOError:
    print("File not found")
    sys.exit("Unable to open "+out_file)

#writes the header to it
out_fv.write("Subband,RCU(i),RCU(j),Covariance\n")




#goes through the subbands one at a time per loop
while subband_index < subbands: 
    #reads a covariance matrix from the input file, unpacks it according to the format string
    #and converts it to an array in numpy
    test_value = np.array(struct.unpack(count_string,test_fv.read(float_size*count)))
    
    #converts the array to an array of complex numbers.  
    test_value.dtype = complex
    
    #increments the suband index - could probably do this better in a for loop
    subband_index = subband_index + 1
    #resets the output string every subband
    test_out=""
    
    #some code to do stats on the file.  Probably not correct use - to delete in future versions
#    mean_list.append(np.mean(test_value))
#    sd_list.append(np.std(test_value))
    
    #goes through each row of the covariance matrix
    for i in range(rcu_count):
        #goes through the columns of the covariance matrix
        for j in range (rcu_count):
            #1-d implementation - needs to calculate index.  Would prefer to make a 2-d array from the start
            element_number = i*rcu_count+j
            #converts the element to a row suitable for molten data
            out_string = str(subband_index)+","+str(i)+","+str(j)+","+str(test_value[element_number])+"\n"
            #adds it to an output string
            test_out=test_out+out_string
    #writes one subband at a time - preserves memory            
    out_fv.write(test_out)    
    

#closes the files
test_fv.close()
out_fv.close()

#print mean_list
#print sd_list



