# Python Lesson 7a: reading and writing seismic data with obspy
# Import the FDSN Web service client for obspy, UTCDateTime and read classes
from obspy.clients.fdsn import Client
from obspy import UTCDateTime, read, Stream
# set the start of the data window, which is an earthquake rupture time in Japan
starttime = UTCDateTime("2020-04-18 08:25:37")
# Import data from the FDSN Web service for three Raspberry shakes close to an earthquake in Japan
seismolist = ['REC8D', 'R38DC', 'R0BEF']
st = Stream()
for seismometer in seismolist:
    waveform = Client("RASPISHAKE").get_waveforms('AM', seismometer, '00', 'EHZ', starttime, starttime + 500)
    waveform.write(seismometer + ".mseed", format="MSEED")
    # Write this stream to file, in the same folder as your program file, for later use, in MSEED format
    st += waveform
# Look at details of the stream object, which now contains three traces
input("Hit enter to see details of the stream object\n")
print(st)
input("\nHit enter to print the station names, accessed using their keywords.\n")
for tr in st:
    print("Station:", tr.stats.station)
input("\nHit enter to read the traces from file again (not really necessary) and see a preview plot.\n")
# += adds what is on the right to the variable on the left, in this case, the stream that we saved earlier
st = Stream()
for seismometer in seismolist:
    st += read(seismometer + ".mseed")
print("Click x to close the plot and finish.")
st.plot()
