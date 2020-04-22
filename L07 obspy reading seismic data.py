# Python Lesson 7: reading and writing seismic data with obspy
# Import the FDSN Web service client for obspy, UTCDateTime and read classes
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
# set the start of the data window, which is an earthquake rupture time in Japan
starttime = UTCDateTime("2020-04-18 08:25:37")
# Import data from the FDSN Web service for Raspberry Shake R38DC in Mishima, Japan
# Lat:35.1351 Lon:138.9269, 497km from the epicentre, network=AM, stationID=R38DC, location=00, channel=EHZ
st = Client("RASPISHAKE").get_waveforms('AM', 'R38DC', '00', 'EHZ', starttime, starttime + 500)
# Look at details of the stream object. A stream object can contain many traces. 
input("Hit enter to see details of the stream object\n")
print(st)
input("\nHit enter to print the statistics associated with the first (and only) trace in this stream.\n")
# the stats are accessed from the trace object using dot notation with the stats keyword
# tr.stats.mseed is a dictionary, which is yet aother collection data type in Python
tr = st[0]
print(tr.stats)
input("\nHit enter to print details of specific items of data using their keywords.\n")
print("Station:", tr.stats.station)
input("\nHit enter to access the actual waveform data via the data keyword on the trace.\n")
# Trace data is held in an array, which behaves like an immutable list, containing data of one type. 
print("The trace data:", tr.data)
# the index [0:4] selects the first four items from the array, [0], [1], [2], [3]
print("The first four data points are: ", tr.data[0:4])
# len is a Python function which prints out the length of data in the variable that's passed to it
print("The length of the trace is: ", len(tr), "points")
input("\nHit enter to see a preview plot of the actual seismic data, with the y-axis scale in counts.\n")
print("Click x to close the plot, to continue program execution.")
st.plot()