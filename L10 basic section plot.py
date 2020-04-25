#Lesson 10: basic section plot
from obspy.clients.fdsn import Client
from obspy import UTCDateTime, Stream
from obspy.geodetics import gps2dist_azimuth # a function for calculating the distance between a seismometer and quake in metres
CLIENT=Client("RASPISHAKE")

# Details of the earthquake event from https://earthquake.usgs.gov/earthquakes/map/
EQLAT = 17.982
EQLON = -66.945
EQNAME = "M3.1 Puerto Rico"
START_TIME = UTCDateTime("2020-04-24 20:31:02")
DURATION = 50 # duration of record to download in seconds

# Filtering parameters
F1 = 1.0  # High-pass filter corner
F2 = 6.0  # Low-pass filter corner 

# Seismometers to load (see http://www.fdsn.org/networks/detail/AM/ for a list of all stations)
seismometers = [
[ 'R4DB9' , 18.018 , -66.8386 ],
[ 'RD17E' , 18.0811 , -67.0314 ],
[ 'RCCD1' , 17.991 , -66.6108 ],
[ 'REA26' , 18.4414 , -67.1532 ],
[ 'R2974' , 18.4595 , -66.3415 ],
[ 'S4051' , 18.3063 , -66.0759 ],
[ 'RA906' , 18.4324 , -66.0588 ]]

# Load the data
waveform = Stream() # set up a blank stream variable
for station in seismometers:
    # Download and filter data
    st = CLIENT.get_waveforms("AM", station[0], "00", "EHZ", starttime=START_TIME, endtime=START_TIME + DURATION)
    st.merge(method=0, fill_value='latest')
    st.detrend(type='demean')
    st.filter('bandpass', freqmin=F1, freqmax=F2)
    # Add the coordinates of the stations and distance in metres from the earthquake, needed for the section plot
    st[0].stats["coordinates"] = {}
    st[0].stats["coordinates"]["latitude"] = station[1]
    st[0].stats["coordinates"]["longitude"] = station[2]
    distance = gps2dist_azimuth(station[1], station[2], EQLAT, EQLON) # (great circle distance in m, azimuth A->B, azimuth B->A)
    st[0].stats["distance"] = distance[0]
    # Add this processed stream to the waveform stream
    waveform += st.copy()

# plot the section
waveform.plot(type='section', orientation='horizontal')