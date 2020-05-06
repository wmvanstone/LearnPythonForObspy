#Lesson 12b: Automated section plotter with arrival lines that doesn't download excess traces
from obspy.clients.fdsn import RoutingClient
from obspy import UTCDateTime, Stream
from obspy.geodetics.base import locations2degrees
import matplotlib.pyplot as plt
from matplotlib.transforms import blended_transform_factory
from obspy.taup import TauPyModel
from matplotlib import cm
from numpy import linspace
CLIENT = RoutingClient("iris-federator")
# Set up the event properties from https://earthquake.usgs.gov/earthquakes/eventpage/ci39406880/executive
START_TIME = UTCDateTime("2020-04-27 03:46:00")           # time of the earthquake
EQNAME = "M4 - 13km SW of Searles Valley CA"              # name of the earthquake
EQLAT = 35.674                                            # latitude of the epicentre
EQLON = -117.496                                          # longitude of the epicentre
EVT_Z = 8.8
MIN_RADIUS = 0                                            # minimum radius in degrees
MAX_RADIUS = 5                                           # maximum radius to search for in degrees
SEPARATION = 0.05                                         # minimum distance between traces in degrees
EXCLUDE = ['BUCR', 'TCHL', 'TWIT', 'JEPS', 'FARB', 'BRK', 'BABI'] # list of stations to exclude from the plot for noise
EXCLUDE += ['B917', 'MCA', 'WCT', 'POC', 'SCH', 'WMD', 'ORC', 'MGN', 'ANT', 'ADH', 'HCK', 'LHV', 'BHU', 'BHP', 'FLV', 'BEN', 'BON', 'MCC', 'LUL', 'CPX', 'REDF', 'MPT', 'GVAR1']
DURATION = 200                                            # Duration of trace shown on section in seconds
F1 = 1.0                                                  # Highpass filter corner in Hz
F2 = 6.0                                                  # Lowpass filter corner in Hz
PHASES = ["P", "S"] # list of phases for which to compute theoretical times
PHASE_PLOT = "line" # choose lines or spots for phases 
MODEL = 'iasp91'
COLORS = [ cm.plasma(x) for x in linspace(0, 0.8, len(PHASES)) ] # colours from 0.8-1.0 are not very visible
# define functions
def plottext(xtxt, ytxt, phase, vertical, horizontal, color, textlist):
    clash = True
    while clash == True:
        clash = False
        for i in range(len(textlist)):
            while textlist[i][0] > (xtxt - 0.1) and textlist[i][0] < (xtxt + 0.1) and textlist[i][1] > (ytxt - 0.7) and textlist[i][1] < (ytxt + 0.7):
                clash = True
                ytxt -= 0.1
    plt.text(xtxt, ytxt, phase, verticalalignment=vertical, horizontalalignment=horizontal, color=color, fontsize=10)
    textlist.append((xtxt, ytxt))
    
# collect the station data, can include Raspishake using ?HZ for the channel, to include BHZ and EHZ
inventory = CLIENT.get_stations(channel="?HZ", network="*", station="*", starttime=START_TIME-10, endtime= START_TIME + DURATION + 10,
    latitude=EQLAT, longitude=EQLON, minradius=MIN_RADIUS, maxradius=MAX_RADIUS, level="channel")
inventory_dictionary=inventory.get_contents()
stations = []
for channel in inventory_dictionary['channels']:
    metadata = inventory.get_channel_metadata(channel)
    distance = locations2degrees(EQLAT, EQLON, metadata['latitude'], metadata['longitude']) # find distance in degrees
    stationID = channel.split(".")
    if stationID[3] in ['EHZ', 'BHZ', 'HHZ']:
        stations.append([distance, stationID[1] , stationID[0], stationID[2], stationID[3], metadata['latitude'], metadata['longitude']])
stations.sort() # sort the stations by distance from the epicentre
last_distance=-10
st = Stream()
# Only find and load traces from stations that are further than SEPARATION from the previous loaded station
for station in stations:
    if last_distance + SEPARATION <= station[0] and station[1] not in EXCLUDE:
        try:
            tr=CLIENT.get_waveforms(station=station[1],network=station[2],location=station[3],channel=station[4],starttime=START_TIME-10,endtime=START_TIME+DURATION+10)
        except:
            print("Can't load " + station[1])
        else:
            if len(tr) > 0:
                tr.merge(method=0, fill_value='latest')
                tr.detrend(type='demean')
                last_distance = station[0]
                tr[0].stats["coordinates"] = {}  # add the coordinates to the dictionary, needed for the section plot
                tr[0].stats["coordinates"]["latitude"] = station[5]
                tr[0].stats["coordinates"]["longitude"] = station[6]
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
    plt.text(0.1, DURATION *1.05, "Bandpass filter, maxfrequency = " + str(F2) + "Hz, minfrequency = " + str(F1) + "Hz")
    # save the file and show the plot on screen
    textlist = [] # list of text on plot, to avoid over-writing
    for j, color in enumerate(COLORS):
        phase = PHASES[j]
        model = TauPyModel(model=MODEL)
        x=[]
        y=[]
        for dist in range(int(MIN_RADIUS*10), int((MAX_RADIUS*10)+1), 1):
            arrivals = model.get_travel_times(source_depth_in_km=EVT_Z,distance_in_degree=dist/10, phase_list=[phase])
            printed = False
            for i in range(len(arrivals)):
                instring = str(arrivals[i])
                phaseline = instring.split(" ")
                if phaseline[0] == phase and printed == False and int(dist/10) >= 0 and int(dist/10) <= 180 and float(phaseline[4])>=0 and float(phaseline[4])<=DURATION:
                    x.append(float(dist/10))
                    y.append(float(phaseline[4]))
                    printed = True
            if PHASE_PLOT == "spots":
                plt.scatter(x, y, color=color, alpha=0.5, s=1)
            else:
                plt.plot(x, y, color=color, linewidth=1.0, linestyle='solid', alpha=0.5)
        if len(x) > 0 and len(y) > 0: # this function prevents text being overwritten
            plottext(x[0], y[0], phase, 'top', 'right', color, textlist)
            plottext(x[len(x)-1], y[len(y)-1], phase, 'top', 'left', color, textlist)
    plt.savefig(EQNAME+'-Lines-Section.png')
    plt.show()
else:
    print("No traces returned")