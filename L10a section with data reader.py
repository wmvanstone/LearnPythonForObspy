#Lesson 10a: Section plot with automatic data selection
from obspy.clients.fdsn import Client
from obspy import UTCDateTime, Stream
from obspy.geodetics.base import locations2degrees
from matplotlib.transforms import blended_transform_factory
import matplotlib.pyplot as plt
CLIENT=Client("RASPISHAKE")

# Details of the earthquake event from https://earthquake.usgs.gov/earthquakes/map/
EQLAT = 17.982
EQLON = -66.945
EQNAME = "M3.1 Puerto Rico"
START_TIME = UTCDateTime("2020-04-24 20:31:02")
DURATION = 50 # duration of record to download in seconds
MAX_DIST = 1 # Distance in degrees
MIN_DIST = 0 # Distance in degrees
EXCLUDE = ['S897D', 'R804D', 'R4DE3'] # Seismometers to exclude, which are noisy, or plot on top of each other
F1 = 1.0  # High-pass filter corner
F2 = 6.0  # Low-pass filter corner

# Get the list of seismometers from file, data downloaded from http://www.fdsn.org/networks/detail/AM/
allStations = [] # list to save stations
with open ("ShakeNetwork2020.csv", "r") as rd:
    for line in rd: # Read lines using a loop loop
        noCR = line.strip() # All lines (besides the last) will include  newline, so strip it off
        allStations.append(noCR.split(',')) # Parse the line using commas
        
# work out the distance of each seismometer from the epicentre and add them to the list if they are within the required range
seismometers = [] # empty list of seismometers
for station in allStations:
    if station[2] != "Latitude": # ignore the header line
        distance = locations2degrees(EQLAT, EQLON, float(station[2]), float(station[3])) # calculate the distance in degrees from the epicentre
        if (distance <= MAX_DIST and distance >= MIN_DIST and station[0] not in EXCLUDE):
            seismometers.append([station[0], round(float(station[2]),4), round(float(station[3]),4), round(distance,4)])
waveform = Stream() # set up a blank stream variable
for station in seismometers: # Run through the list of seismometers which are in the required range
    try: # Download and filter data
        st = CLIENT.get_waveforms("AM", station[0], "00", "EHZ", starttime=START_TIME, endtime=START_TIME + DURATION)
        st.merge(method=0, fill_value='latest')
        st.detrend(type='demean')
        st.filter('bandpass', freqmin=F1, freqmax=F2)
        print("Loaded station ", station[0])
    except:
        print("Unable to load station", station[0])
    else: # Add lat, long and distance to the trace 
        st[0].stats["coordinates"] = {} # add the coordinates to the dictionary, needed for the section plot
        st[0].stats["coordinates"]["latitude"] = station[1]
        st[0].stats["coordinates"]["longitude"] = station[2]
        st[0].stats["distance"] = station[3]
        waveform += st.copy()
        
# Create the section plot
fig = plt.figure(figsize=(16, 12), dpi=80)
plt.title('Section plot for '+EQNAME+" "+str(START_TIME.date)+" "+str(START_TIME.time)+" lat:"+str(EQLAT)+" lon:"+str(EQLON), fontsize=12, y=1.07)
plt.xlabel("Angle (degrees)")
plt.ylabel("Elapsed time (seconds)")

# print the data
waveform.plot(size=(960,720), type='section', recordlength=DURATION, linewidth=1.5, grid_linewidth=.5, show=False, fig=fig, color='black',
              method='full', starttime=START_TIME, plot_dx=0.25, ev_coord = (EQLAT, EQLON), dist_degree=True, alpha=0.50, time_down=True)
ax = fig.axes[0]
transform = blended_transform_factory(ax.transData, ax.transAxes) # set up plotting coordinates with x-axis in data coordinates and y-axis not
for tr in waveform: # for each trace, add the name of the trace at the top of the graph, along the x-axis
    ax.text(float(tr.stats.distance), 1.0, tr.stats.station, rotation=270, va="bottom", ha="center", transform=transform, zorder=10, fontsize=12)
# add the filter details at the bottom left of the graph using data coordinates
plt.text(0, DURATION *1.05, "Bandpass filter, maxfrequency = " + str(F2) + "Hz, minfrequency = " + str(F1) + "Hz")

# save the file and show the plot on scren
plt.savefig(EQNAME+'-Section.png')
plt.show()