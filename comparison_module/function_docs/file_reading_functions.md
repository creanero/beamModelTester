**Comparison Module \
File reading functions\
Version 0.3\
23ʳᵈ March 2018\
Oisin Creaner**

This set of functions describes the file reading elements of the [comparison module](/comparison_module/Comparison_Module.md).

**Functions**\
read_var_file\
read_dreambeam_csv\
read_OSO_h5

**Dependencies**\
pandas\
h5py\
numpy

**Outline**\
These functions form the file entry component of the 
[comparison module](/comparison_module/Comparison_Module.md) of 
[beamModelTester](/README.md)
Depending on the file type provided, the system uses one of several (currently two) options
to read the file into memory as a dataframe suitable for futher processing.

**Design Diagram**\
![Design Diagram](/images/comparison_module_read_functions_fig1_v3.PNG)

**Operation**

1.  The function parses the extension from the filename provided.
2.  If the suffix is "csv", execute read_dreambeam_csv:
    1.  This means the data must be of [dreamBeam output format](/data_descriptions/DreamBeam_Source_data_description.md)
    2.  This function calls the pandas read_csv method with the following arguments
        1.  converters to read in the Jones matrix elements as complex numbers
        2.  A date parser for the Time column
        3.  An argument to specify to skip initial spaces if needed.
    3.  Each of the linear polarisation channels (xx, xy, yy) are calculated.
        1.  XX= (J11 * conj(J11))+ (J12 * conj(J12))
        2.  XY= (J11 * conj(J21))+ (J12 * conj(J22))
        3.  YY= (J21 * conj(J21))+ (J22 * conj(J22))
    4.  Returns the Dataframe to read_var_file
3.  If the suffix is "hdf5", execute read_OSO_h5:
    1.  This means the data must be of [OSO HDF5 format](/data_descriptions/OSO_HDF5.md)
    2.  Call the h5py File method in read mode
    3.  Creates lists to hold the data from the file
    4.  Creates a time index
    5.  Calculate the minimum (start) time
    6.  Iterates over the time values in the file
        1.  Creates a Frequency index
        2.  Iterates over the frequency values in the file
            1.  Converts the time to a pandas timestamp and appends the time to the time list
            2.  Calculates the time since the start time and appends the time to the d_time list
            3.  the frequency is read from the file data and appended to the list
            4.  Reads the XX, XY and YY values from the file by the indices and appends them to their respective lists
            5.  Increments the Frequency index
        3.  Increments the Time index
    7.  Creates a dataframe from the lists
    8.  Returns the Dataframe to read_var_file
4.  Calculates the Stokes Parameters (U, V, I and Q) for the dataframe using calc_stokes
    1.  U= real(xy)
    2.  V= imaginary(xy)
    3.  I= xx+yy
    4.  Q= xx-yy
5.  Returns the Dataframe to the function that called read_var_file
