**ACC to CSV converter\
Version 0.0\
16^th^ February 2018\
Oisin Creaner**

This program extracts data from ACC files and adds it to a CSV file
which includes header and structured data elements.

**Outline**

The system opens the raw data file, reads in the floating-point data for
one covariance matrix at a time and converts it to an array of complex
numbers. The program then iterates over the array and creates data rows
consisting of subband, RCU information and the complex covariance
coefficient for the given pair of RCUs. These are then written to a CSV
file. The draft version includes hard-coded elements for demonstration
purposes

**Design Diagram**

Figure 1: Outline of the design of the conversion from ACC file to CSV

**Operation**

1.  Variables to control the program are set

    1.  Input filename (*Currently hard coded for testing purposes*)

    2.  Output filename (replace .dat extension of input file with .csv)

    3.  RCU Count (*n*: *Hard Coded to 192*)

        1.  Count (size of the covariance matrix: 2*n*^2^)

        2.  Count string (format string for reading using struct.unpack
            method)

    4.  Number of Subbands (*N*: *Hard coded to 512*)

    5.  Float Size (*f*: *Hard coded to 8 -- probably possible to do
        this automatically*)

2.  Checks the inputs:

    6.  Output file name different from input

    7.  Input file of the correct size (2 *Nf n*^2^)

3.  Opens the input and output files

4.  Loops over each subband

    8.  Reads the covariance matrix for a given subband from the input
        file and stores it in an array

        3.  Converts the data type of that array to complex

    9.  Creates a string to output the covariance matrix to text

    10. Loops over each RCU (i)

        4.  Loops over each RCU (j) against which a covariance has been
            calculated

            1.  Creates a string containing the subband number, RCU(i),
                RCU(j) and the complex covariance coefficient between i
                and j

            2.  Appends this string to the output string

    11. Writes the output string to the Output file

5.  Closes the files

**Sample Output**

**Subband,RCU(i),RCU(j),Covariance**

**1,0,0,(13329498112+0j)**

**1,0,1,(4605345792-4394118j)**

**1,0,2,(1124073472+1775524j)**

**1,0,3,(2499805184-88966j)**

**1,0,4,(-3196059648-1525678j)**

**...**

**34,20,180,(1806+1769j)**

**34,20,181,(-1133+308j)**

**34,20,182,(-660+939j)**

**34,20,183,(-973-640j)**

**...**

**512,191,187,(-2813-1055j)**

**512,191,188,(88-641j)**

**512,191,189,(497+120j)**

**512,191,190,(190-1699j)**

**512,191,191,(798519+0j)**
