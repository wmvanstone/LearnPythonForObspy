#Lesson 09: Filtering - adapted from:
# https://docs.obspy.org/tutorial/code_snippets/filtering_seismograms.html
import numpy as np # numpy is a library of numerical functions
import matplotlib.pyplot as plt # matplot lib is a plotting library
from obspy.clients.fdsn import Client
from obspy import UTCDateTime

# set up station parameters
CLIENT=Client("RASPISHAKE")
STATION='R7FA5'
STARTTIME=UTCDateTime("2020-02-06 13:43:10")

# import a trace, merge if it has become fragmented and return the mean value to the origin
st=CLIENT.get_waveforms('AM',STATION,'00','EHZ',STARTTIME,STARTTIME+1000)
st.merge(method=0, fill_value='latest')
st.detrend(type='demean')

# There is only one trace in the Stream object, let's work on that trace...
tr = st[0]

# Filtering with a lowpass on a copy of the original Trace
tr_filt = tr.copy() 
# Filter the data with bandpass, bandstop, lowpass or highpass filtering
# zerophase applies the filter twice, both forward and backward to eliminate phase changes
tr_filt.filter('lowpass', freq=4.0, corners=2, zerophase=True)

# Now let's plot the raw and filtered data...
# set up an array containing values corresponding to the sample times
t = np.arange(0, tr.stats.npts / tr.stats.sampling_rate, tr.stats.delta)
plt.subplot(211) # divide the plot area into 2 plots high by one wide and work with plot 1
plt.plot(t, tr.data, 'k') # plot the trace data in block
plt.ylabel('Raw Data') # add a y-axis label
plt.subplot(212) # work with plot 2
plt.plot(t, tr_filt.data, 'k') # plot the filtered data in black
plt.ylabel('Lowpassed Data') # add a y-axis label
plt.xlabel('Time [s]') # add the x-axis label
plt.suptitle(tr.stats.starttime) # add a main title for the graphs
plt.show() # display on screen