#Lesson 12a: Automated section plotter that doesn't download excess traces
from obspy.clients.fdsn import RoutingClient
from obspy import UTCDateTime, Stream
from obspy.geodetics.base import locations2degrees
import matplotlib.pyplot as plt
from matplotlib.transforms import blended_transform_factory
CLIENT = RoutingClient("iris-federator")
# Set up the event properties from https://earthquake.usgs.gov/earthquakes/eventpage/ci39406880/executive
START_TIME = UTCDateTime("2020-04-27 03:46:00")           # time of the earthquake
EQNAME = "M4 - 13km SW of Searles Valley CA"              # name of the earthquake
EQLAT = 35.674                                            # latitude of the epicentre
EQLON = -117.496                                          # longitude of the epicentre
MIN_RADIUS = 0                                            # minimum radius in degrees
MAX_RADIUS = 5                                           # maximum radius to search for in degrees
SEPARATION = 0.05                                         # minimum distance between traces in degrees
EXCLUDE = ['BUCR', 'TCHL', 'TWIT', 'JEPS', 'FARB', 'BRK', 'BABI'] # list of stations to exclude from the plot for noise
DURATION = 200                                            # Duration of trace shown on section in seconds
F1 = 1.0                                                  # Highpass filter corner in Hz
F2 = 6.0                                                  # Lowpass filter corner in Hz
# collect the station data
inventory = CLIENT.get_stations(channel="BHZ", network="*", station="*", starttime=START_TIME-10, endtime= START_TIME + DURATION + 10,
    latitude=EQLAT, longitude=EQLON, minradius=MIN_RADIUS, maxradius=MAX_RADIUS)
stations = []
for network in inventory:
    for station in network:
        distance = locations2degrees(EQLAT, EQLON, station.latitude, station.longitude) # find distance in degrees
        stations.append([distance, station.code, network.code, station.latitude, station.longitude])
stations.sort() # sort the stations by distance from the epicentre
last_distance=-10
st = Stream()
# Only find and load traces from stations that are further than SEPARATION from the previous loaded station
for station in stations:
    if last_distance + SEPARATION <= station[0] and station[1] not in EXCLUDE:
        try:
            tr=CLIENT.get_waveforms(channel="BHZ",station=station[1],network=station[2],location="*", starttime=START_TIME-10,endtime=START_TIME+DURATION+10)
        except:
            print("Can't load " + station[1])
        else:
            if len(tr) > 0:
                tr.merge(method=0, fill_value='latest')
                tr.detrend(type='demean')
                last_distance = station[0]
                tr[0].stats["coordinates"] = {}  # add the coordinates to the dictionary, needed for the section plot
                tr[0].stats["coordinates"]["latitude"] = station[3]
                tr[0].stats["coordinates"]["longitude"] = station[4]
                tr[0].stats["distance"] = station[0]
                st+=tr[0].copy()
                print(station)
if len(st) > 0:
    # filter
    st.filter("bandpass", freqmin=F1, freqmax=F2, corners=2, zerophase=True)
    # Create the section plot
    fig = plt.figure(figsize=(16, 12), dpi=80)
    plt.title('Section plot for '+EQNAME+" "+str(START_TIME.date)+" "+str(START_TIME.time)+" lat:"+str(EQLAT)+" lon:"+str(EQLON), fontsize=12, y=1.07)
    # plot the data
    st.plot(size=(960,720), type='section', recordlength=DURATION, linewidth=1.5, grid_linewidth=.5, show=False, fig=fig, color='black',
                  method='full', starttime=START_TIME, plot_dx=0.25, ev_coord = (EQLAT, EQLON), dist_degree=True, alpha=0.50, time_down=True)
    ax = fig.axes[0]
    transform = blended_transform_factory(ax.transData, ax.transAxes) # set up plotting coordinates with x-axis in data coordinates and y-axis not
    for tr in st: # for each trace, add the name of the trace at the top of the graph, along the x-axis
        ax.text(float(tr.stats.distance), 1.0, tr.stats.station, rotation=270, va="bottom", ha="center", transform=transform, zorder=10, fontsize=12)
    # add the filter details at the bottom left of the graph using data coordinates
    plt.text(0, DURATION *1.05, "Bandpass filter, maxfrequency = " + str(F2) + "Hz, minfrequency = " + str(F1) + "Hz")
    # save the file and show the plot on scren
    plt.savefig(EQNAME+'-Section.png')
    plt.show()
else:
    print("No traces returned")