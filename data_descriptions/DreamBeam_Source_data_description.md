**DreamBeam Source data\
Version 0.0\
29^th^ March 2018\
Oisin Creaner**

This describes the formats for output from DreamBeam in its current
state

**Abstract**

Output from dreamBeam works in two main modes: Pointing and FoV. These
modes produce data that describes the Jones matrix elements for two
different operational requirements. Both modes provide options for
plotting this data visually or outputting it to std.out, This output can
then be redirected to a file if needed.

Pointing mode defines the Jones matrix elements for a given target based
on its celestial coordinates and calculates how these change over a user
defined period in user defined intervals. Optionally, this mode may
calculate the Jones matrix elements for a single user-defined frequency,
or for a variety of frequencies across the bandwidth of the telescope if
the user does not supply a frequency.

FoV mode defines the Jones matrix elements for the whole sky at a given
instant for a given frequency.

**Outline of Modes**

![Outline of modes](/images/DB_SOURCE_Fig1.PNG)

Figure 1: Outline of modes

**Details of Outputs**

1.  Pointing Mode\
    Pointing Mode plots the light curves as observed from a given
    station in a given band over a given time period at given
    intervals. Frequency is an optional parameter which allows a user to
    either specify a frequency to work at (1-*ν*, below) or to require
    that the system calculate the Jones Matrices for all frequencies in
    the system by leaving out this parameter. (n-*ν*, below)

    1.  1-*ν*\
        In this mode, the light-curve in Jones matrix terms is
        calculated for a single frequency over time
        1.  Print\
            The print output for this mode consists of 
            -   a header describing the content *Time, Freq, J11, J12, J21, J22*
            -   a row for each time interval, with each row consisting of the following
            elements, separated by commas.
            -   Frequency (print-formatted Python float)
            -   Time (print-formatted Python datetime *YYYY-MM-DDTHH:MM:SS*)
            -   Four Jones Matrix elements (print-formatted Python
                complex numbers using the notation (*X.xxxx*+*Y.yyyy*j)
                in the order
                -   \[1,1\]
                -   \[1,2\]
                -   \[2,1\]
                -   \[2,2\]
                
![1-frequency print output](/images/DB_SOURCE_Fig2_v2.PNG)

Figure 2: Schematic of Print output for single-frequency use of Pointing
mode

**Sample Output**

Time, Freq, J11, J12, J21, J22\
2018-03-01T00:00:00,100000000.0,(-0.332417348324-0.00174180468029j),(-0.151027693651-0.00224741459058j),(0.248921114269+0.000678606249047j),(-0.274213110649-0.00267578547374j)\
2018-03-01T00:01:00,100000000.0,(-0.330965823806-0.00173312560831j),(-0.152454209941-0.00225879860975j),(0.250232467494+0.000690120685984j),(-0.272889641047-0.00266605130817j)\
2018-03-01T00:02:00,100000000.0,(-0.329512964372-0.00172439925913j),(-0.153873968917-0.002270162415j),(0.251539358186+0.000701583461056j),(-0.271563428615-0.00265627153832j)

2.  Plot\
    The plot mode produces an image of the trajectory of the selected
    pointing and a set of plots of the light curves for that object at
    the given frequency over the given interval

    The trajectory plot (as shown in Figure 3) shows the apparent
    position of the object at each point in time. *Note: In LOFAR, for a
    non-core station, these coordinates will not be centred on the pole
    as the orientation is set for the LOFAR core*

![track of the coordinates](/images/DB_SOURCE_Fig3.png)

Figure 3: Sample of plot output of the track of the coordinates of the
target object for pointing mode

The Light curve plot displays the p-channel
(p=|J\[1,1\]|² +|J\[1,2\]|²) 
and q-channel
(q=|J\[2,1\]|² +|J\[2,2\]|²) 
calculated for each point in time against time for the given
frequency. *Note: These channels refer to the power over time of the polarised channels: 
p- and -q can be arbitrary channels, including left and right polarised or 
x- and y- polarised.  The current system outputs for x and y*

![1-frequency plot output](/images/DB_SOURCE_Fig4.png)

Figure 4: Sample of Plot output for lightcurve for a single frequency in
pointing mode. Time is plotted on the x-axis, p- and q-channel normalised detected power values
are plotted on the y-axis.

2.  n-*ν\
    *In this mode, the light-curve in Jones matrix terms is calculated
    for a number of (*all possible? -- to check*) frequencies over time
    3.  Print\
        The print output for this mode consists of 
        -   a header to describe the columns.
        -   a row for each time interval/frequency combination  
        -   Each row consists of the following elements, separated by commas
            -   Time (print-formatted Python datetime
                *YYYY-MM-DD*T*HH:MM:SS*)
            -   Frequency (print-formatted Python float)
            -   Four Jones Matrix elements (print-formatted Python complex
                numbers using the notation (X.xxxx+Y.yyyyj) in the order
                -   \[1,1\]
                -   \[1,2\]
                -   \[2,1\]
                -   \[2,2\]
            
![N-frequency print output](/images/DB_SOURCE_Fig5.PNG)

Figure 5: Schematic of Print output for multi-frequency use of Pointing
mode

Sample Output

Time, Freq, J11, J12, J21, J22\
2018-03-01T00:00:00,100000000.0,(-0.332417348324-0.00174180468029j),(-0.151027693651-0.00224741459058j),(0.248921114269+0.000678606249047j),(-0.274213110649-0.00267578547374j)\
2018-03-01T00:00:00,100195312.5,(-0.332523995452-0.00172552582091j),(-0.151147212914-0.00223710070454j),(0.248971710186+0.00066751702167j),(-0.274364953445-0.00266045605641j)\
2018-03-01T00:00:00,100390625.0,(-0.332631104279-0.00170950100127j),(-0.151266877453-0.00222685026169j),(0.249022699449+0.000656640777448j),(-0.274517129125-0.00264528363489j)\
2018-03-01T00:00:00,100585937.5,(-0.332738673914-0.00169372847052j),(-0.151386689649-0.00221666186212j),(0.249074080125+0.000645976454977j),(-0.274669639399-0.00263026630536j)

1.  Plot\
    The plot mode produces an image of the trajectory of the selected
    pointing and a set of plots of the light curves for that object at
    the given frequency over the given interval

    The trajectory plot (as shown in Figure 3) shows the apparent
    position of the object at each point in time. *Note: In LOFAR, for a
    non-core station, these coordinates will not be centred on the pole
    as the orientation is set for the LOFAR core*

![track of the coordinates](/images/DB_SOURCE_Fig6.png)

Figure 6: Sample of plot output of the track of the coordinates of the
target object for pointing mode for n-frequencies

The Light curve plot displays the p-channel
(p=|J\[1,1\]|² +|J\[1,2\]|²) 
and q-channel
(q=|J\[2,1\]|² +|J\[2,2\]|²) values calculated for each point in time against time for each frequency.  The plot then shows the values in colour, with the time and frequency as x- and y-axes respectively

![n-frequency Lightcurve](/images/DB_SOURCE_Fig7.png)

Figure 7: Sample of Plot output for lightcurve for multiple frequency in
pointing mode. Time is plotted on the x-axis, frequency on the y-axis,
p- and q-channel values are plotted on the z-axis (colour).

1.  FoV Mode
    1.  Print\
        The print output for this mode consists of a pair of rows for
        each time interval, with each alternating row consisting of the
        following elements, separated by spaces. *Note: this mode
        produces output with labels for each row.*
        -   First Row
            -   Label (az, el: )
            -   Azimuth (print-formatted Python float)
            -   Elevation (print-formatted Python float) (*Alternative term for Altitude*)
        -   Alternate Rows
            -   Label (Jones: )
            -   Four Jones Matrix elements (print-formatted Python
                complex numbers using the notation (*X.xxxx*+*Y.yyyy*j)
                in the order
                -   \[1,1\]
                -   \[1,2\]
                -   \[2,1\]
                -   \[2,2\]

![FOV Print](/images/DB_SOURCE_Fig8.PNG)

Figure 8: Schematic of Print output for single-frequency use of Pointing
mode

Sample Output \
*these values include negative elevations.  This is because the print model does not include a mask for the data for the horizon.  This is implemented in the plotting system.* \
*Some of these seem to show different Jones values at different RA values at DEC 90. This is a known issue with the Hamaker model, which is limited close to the Zenith.  While approximations may be reasonable close to the Zenith in some systems, this can be a serious issue for telescopes which are not mechanically steered.*)

az, el: 0.0 1.57079632679\
Jones: (0.808438378389-0.0536168902205j)
(-0.174461109928-0.0550466007067j) (0.176809726227-0.0764445107476j)
(0.810303656386-0.044823755958j)\
az, el: 0.0245436926062 1.57079632679\
Jones: (0.803911684752-0.0549513922064j)
(-0.19424874567-0.0537143676432j) (0.196640074711-0.0775212195077j)
(0.80572271751-0.0429343667736j)

2.  Plot

    The Light curve plot for FoV Mode plots the I, q, u and v parameters
    as colour against RA and DEC.\
    *A potential extension is to include Alt/Azimuth based plots instead of RA/DEC*

![plot output for FoV mode](/images/DB_SOURCE_Fig9.png)

Figure 9: Sample of plot output for FoV mode. In each plot, RA is used as
the x-axis, and DEC as the y-axis. The Stokes parameters, calculated
from the Jones Matrices, are plotted on the z-axis (colour)
