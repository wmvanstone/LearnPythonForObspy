#L09a filtering
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
import numpy as np
import matplotlib.pyplot as plt
# set up station parameters
CLIENT=Client("RASPISHAKE")
STATION='R7FA5'
STARTTIME=UTCDateTime("2020-02-06 12:55:00")
COLORS=('k', 'r', 'g', 'b', 'm', 'c', 'y')
# import data, merge if they have become fragmented and return the mean value to the origin
st=CLIENT.get_waveforms('AM',STATION,'00','EHZ',STARTTIME,STARTTIME+3600)
st.merge(method=0, fill_value='latest')
st.detrend(type='demean')
# make four more copies of the raw data to show the effects of the different filters
for i in range(4):
    st += st[0].copy()
# Filter each of the traces, adding the filter details to the filters list using filters.append() 
filters=[]
st[0].filter("lowpass", freq=0.7, corners=2, zerophase=True)
filters.append("Lowpass filter, freq=0.7, corners=2, zerophase=True")
st[1].filter("bandpass", freqmin=0.7, freqmax=3.0, corners=4, zerophase=True)
filters.append("Bandpass filter, freqmin=0.7, freqmax=3.0, corners=4, zerophase=True")
st[2].filter("bandpass", freqmin=3.0, freqmax=20.0, corners=4, zerophase=True)
filters.append("Bandpass filter, freqmin=3.0, freqmax=20.0, corners=4, zerophase=True")
st[3].filter("highpass", freq=20.0, corners=2, zerophase=True)
filters.append("Highpass filter, freq=20.0, corners=2, zerophase=True")
filters.append("Raw Data")
# Set up the figure for printing
fig = plt.figure(1, figsize=(16, 9))
# Use Numpy to create an array of time values using the statistics from the trace header
t = np.arange(0, st[0].stats.npts / st[0].stats.sampling_rate, st[0].stats.delta)
for i in range(len(st)):
    if i == len(st)-1: # For the last plot in the list, add tick values and axis label
        ax = plt.subplot(5, 1, i+1) # use a grid that is 5 subplots x 1 subplot, indexed using i
        plt.xlabel('Time [s]')
    else: # suppress numbers on the axis for all but the bottom x-axis
        ax = plt.subplot(5, 1, i+1)
        plt.setp(ax.get_xticklabels(), visible=False)
    plt.plot(t, st[i], COLORS[i]) # plot using colors from the COLORS tuple defined above
    plt.ylabel(filters[i][0:8]) # show what filter has been used on the y-axis label
    # show the filter details in a subtitle for each subplot
    ax.text(0.5, 1.01, filters[i], transform=ax.transAxes, ha='center', va='bottom')
# add an overall title for the plots
plt.suptitle("Comparison of filtering for Raspberry Shake " + STATION + " from "
             + str(STARTTIME.date) + " " +str(STARTTIME.time))
# Save the plot to file, then print to screen
plt.savefig('Filter-Summary.png')
plt.show()
