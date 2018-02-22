**Comparison Module (*Design*)\
Version 0.1\
22ⁿᵈ February 2018\
Oisin Creaner**

This module takes input from a model of telescope performance and
compares it with calibration data from real telescopes to generate
metrics for the deviation of the model from reality

**Outline**

This (R Script) module reads in input from a modelling system and input from a real
telescope and compares the two against one another. This module assumes
that the inputs have been brought to a common format, with common
independent variables (e.g. position, time, frequency) and at least one
common dependent variable to be compared. Outputs include a plot of the
variation of the dependent variable, a calculated value of Root
Mean-Square Error (RMSE), and a calculated value for the correlation of
the variables. (*These outputs can be expanded in Future*)

**Design Diagram**

![Design Diagram](images/comparison_module_fig1.PNG)

Figure 1: Outline of the comparison Module

**Operation**

1.  Read in the data from the model file (*assumed to be CSV format*) and store the contents in a dataframe
   
2.  Read in the data from the telescope file (*assumed to be CSV format*) and store the contents in a
    dataframe

3.  Merge the dataframes using an inner join to ensure only data points
    where a common value(s) for the independent variable(s) exists
    
    3.1.  (*Option: consider including statistics of this operation in the outputs?*)

4.  The difference between the two sets of values for the dependent
    variable is calculated and stored as a vector in the merged dataframe

5.  From this vector, outputs can be calculated. The outputs are as follows

    1.  A plot of the differences against the independent variable

    2.  A calculation of the RMSE

    3.  A calculation of the correlation coefficient for the model
        against the real data

**Assumptions**

1.  Model data and telescope data can be made available

2.  The datasets have common independent variables with which to match
    the datasets

3.  The datasets have a comparable dependent variable (equivalent
    property, similar units etc)

