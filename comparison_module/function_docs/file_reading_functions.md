**Comparison Module \
File reading functions\
Version 0.3\
23ʳᵈ March 2018\
Oisin Creaner**

This set of functions describes the file reading elements of the [comparison module](/comparison_module/Comparison_Module.md).

**Functions**\
read_var_file\
read_dreambeam_csv\
read_OSO_h5\

**Dependencies**\
pandas\
h5py\
Numpy

**Outline**\
These functions form the file entry component of the 
[comparison module](/comparison_module/Comparison_Module.md) of 
[beamModelTester](/README.md)
Depending on the file type provided, the system uses one of several (currently two) options
to read the file into memory as a dataframe suitable for futher processing.

**Design Diagram**\
![Design Diagram](/images/comparison_module_read_functions_fig1_v1.PNG)

**Operation**

1.  The function parses the extension from the filename provided.
2.  If the suffix is "csv", execute read_dreambeam_csv:
    1.  This means the data must be of [dreamBeam output format](/data_descriptions/DreamBeam_Source_data_description.md)
    2.  This function calls the pandas read_csv method with the following arguments
        1.  converters to read in the Jones matrix elements as complex numbers
        2.  A date parser for the Time column
        3.  An argument to specify to skip initial spaces if needed.
    3.  This function returns the dataframe containing the output from dreamBeam
3.  If the suffix is "hdf5", execute read_OSO_h5:
    1.  This means the data must be of [OSO HDF5 format](/data_descriptions/OSO_HDF5.md)
    2.  Call the h5py File method in read mode
    3.  Creates lists to hold the data from the file
    4.  Creates a time index
    5.  Calculate the minimum (start) time
    6.  *Temporary for calibration mismatch:* Calculate the minimum Frequency
    7.  Iterates over the time values in the file
        1.  Creates a Frequency index
        2.  Iterates over the frequency values in the file
            1.  Converts the time to a pandas timestamp and appends the time to the time list
            2.  Calculates the time since the start time and appends the time to the d_time list
            3.  *Temporary for calibration mismatch:* Calculates the frequency 
            based on the minimum frequency and frequency index and appends it to the freq_list
                1.  *when calibration is fixed, this should be:* the frequency is read from the file data and appended to the list
            4.  Reads the XX, XY and YY values from the file by the indices and appends them to their respective lists
            5.  Increments the Frequency index
        3.  Increments the Time index
    8.  Creates a dataframe from the lists
    9.  Returns the Dataframe
4. Returns the Dataframe
