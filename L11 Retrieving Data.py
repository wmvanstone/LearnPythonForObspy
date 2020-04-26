# Lesson 11: Retrieving data
# In addition to Raspberry Shakes, I have downloaded data from the BGS and USGS
from obspy.clients.fdsn import Client
from obspy import UTCDateTime

# Use IRIS as the source for data from the BGS Carnmenellis seismometer
print("Plot records from the BGS sesimometer at Carnmenellis for the Cornish earthquake of 2019-08-08")
# set the data window
starttime=UTCDateTime("2019-08-08 16:52:00")
endtime=starttime+60
# read in BGS seismometer at Carnmenellis
client=Client("IRIS")
waveform=client.get_waveforms('GB','CCA1','--','HHZ',starttime,endtime)
waveform.plot(size=(1024,800),type='normal', automerge=True, equal_scale=False, starttime=starttime)

# Use FTP (File Transfer Protocol) to get data from the BGS seismometer at Hartland
from ftplib import FTP
from obspy import read
print("Plot records from the BGS seismometer HTL at Hartland for the Somerset earthquake of 2019-12-05")
starttime=UTCDateTime("2019-12-05 22:49:30")
endtime=starttime+60
# Firstly download the file NETWORK.SEISMOMETER.LOCATION.CHANNEL.D.YEAR.DAYNO
filename = 'GB.HTL.00.HHZ.D.2019.339'
# Log in to the BGS service
ftp = FTP('seiswav.bgs.ac.uk')
ftp.login()
# Change working directory to the Hartland 2019 data folder
ftp.cwd('2019')
ftp.cwd('HTL')
ftp.cwd('HHZ.D')
# copy the file to your computer to a folder called Data on your computer, in binary mode and close the connection
fp = open("../Data/" + filename, 'wb')
ftp.retrbinary('RETR '+ filename, fp.write, 1024)
ftp.quit()
fp.close()
# read the local file, filter and plot
st = read("../Data/" + filename)
st.detrend(type='demean')
st.filter("bandpass", freqmin=1.0, freqmax = 10.0, corners=4)
waveform = st.slice(starttime, endtime)
waveform.plot(size=(1024,800),type='normal', automerge=True, equal_scale=False, starttime=starttime)

# Use IRIS to retrieve data from the ANMO seismometer in New Mexico
print("Plot records from the Albuquerque, NM seismometer for M7.7 earthquake from Jamaica 2020-01-28 19:15:00")
client=Client("IRIS")
starttime=UTCDateTime("2020-01-28 19:15:00")
endtime=starttime+1200
waveform=client.get_waveforms('IU','ANMO','00','LHZ',starttime,endtime)
waveform.plot(size=(1024,800),type='normal', automerge=True, equal_scale=False, starttime=starttime)

# Use wild cards to get data from the iris federator for seismometers near a location in Nepal
print("Plot records from a station near Nepal for the M7.5 earthquake in the Kuril'sk Islands on 2020-02-13 10:33:44")
from obspy.clients.fdsn import RoutingClient
client = RoutingClient("iris-federator")
starttime = UTCDateTime("2020-02-13T10:33:44")
lat = 28.0
lon = 84.0
minradius = 0
maxradius = 10
st = client.get_waveforms(channel="BHZ", station="*", network="*", starttime=starttime, endtime=starttime+1200,
                          latitude=lat, longitude=lon, minradius=minradius, maxradius=maxradius)
print(st.__str__(extended=True))
st.filter("bandpass", freqmin=1.0, freqmax=4.0, corners=2, zerophase=False)
st[0].plot(size=(1024,800),type='normal', automerge=True, equal_scale=False, starttime=starttime)




