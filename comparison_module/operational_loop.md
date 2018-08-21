# Operational Loop of the Comparison Module
1.  Identify the channels to plot
2.  Merge the dataframes using an inner join to ensure only data points
    where a common value(s) for the independent variable(s) exists using 
    the flexible dataframe merger function, 
    [merge_dfs](/comparison_module/function_docs/merge_dfs.md)
3.  Depending on whether the user has specified a frequency filter (as a file or parameter)
    1.  Runs the Filter Frequencies function to drop all frequencies from the dataframe except those specified.
4.  if there is any data left:
    1.  Calculates Alt-Az Coordinates and values
    2.  Runs the Analysis Function.  Depending on whether there is a single value for frequency or multiple values, 
          the program will perform different analyses.  
          In addition, if the plots are to be separated, these functions are run with one channel at a time as arguments.  
          Otherwise they are run with all channels to be plotted as the argument.
        1.  [one-frequency mode](/comparison_module/function_docs/analysis_1d.md) 
        produces outputs suitable for single frequency operations 
        2.  [multi-frequency mode](/comparison_module/function_docs/analysis_nd.md)
            produces outputs suitable for multiple frequency operations 
    3.  If the user has specified an output directory and requested file output of the dataframe, 
    the merged data is written to an output file.
   
