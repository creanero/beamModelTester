# Offsets and Scaling
In this tutorial, you will learn how to combine data from different sources with the same cadence by applying a time offset, and adjust the data scales to allow for different representations of the variation of the data.

## Time Offset
Time offsets are used to compare data from different sources with the same observation cadence taken at a different times.  These can be used for several purposes, for example, to observe changes over longer timescales, compare observations of different sources or, as we'll be doing here, comparing observations from different stations.

To this end, in addition to [the data you have previously used](https://zenodo.org/record/1744987#.XAEbpdv7SUk) for these tutorials, you should **[download this new data](https://zenodo.org/record/2650313#.XMCcnEMo8UE)**.  Both datasets represent observations of CasA taken from LOFAR HBA stations on 16th-17th March 2018, the first from station SE607 in Onsala, Sweden, and the second from IE613 in Birr, Ireland.  These observations were taken concurrently from the two stations, but a slight offset in start time means the two observations would not match perfectly for comparison purposes.  Thus, a slight offset must be provided to enable the data to be matched.

Start the program as usual.  Now, instead of selecting a CSV file as the model and a HDF5 file as the "scope" or observation, we'll select the HDF5 file from SE607 as the model, and the HDF5 file from IE613 as the scope file.  If you try to plot the data, you'll get an error as shown below.

![Error with unmatched data](/images/tutorial_7_1.png)

From the filenames, it can be seen that the two observations started at 11:49:21 and 15:58:25 (both are in UTC by convention). The source data is recorded at a cadence of one data point every 519 seconds (see [iLiSA](https://github.com/2baOrNot2ba/iLiSA) for more information).  Therefore to apply the correct offset, it is necessary to first find out the difference in time between the start of the two observations.  This can be calculated to be 14,944 seconds.  By taking the modulus of this mumber by 519, it can be calculated that the offset between the datasets is 412 seconds.  Since this is more than half way through an observation window, it would be more correct to apply an offset in the other direction, i.e. an offset of (519-412) 107 seconds.  Note that the offset is applied by subtracting the specified amount from the time of the scope data so when using this for yourself, you may need to be careful about the sign of the offset chosen.  In this case, the offset will be positive.

## Logarithmic Scales

## Percentage Scales

In [Tutorial 8](/tutorial_8.md), we will look at visual options, such as changes to the colourschemes and plot sizes.
