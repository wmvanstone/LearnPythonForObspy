from obspy.clients.fdsn import Client               # for seismic data download
from obspy import UTCDateTime                       # for turning the date/time into a datetime object
import numpy as np                                  # for more advanced maths functions
import matplotlib.pyplot as plt                     # for graph plotting
from obspy.taup import TauPyModel                   # source of the phase arrival information
from matplotlib.cm import get_cmap                  # colourmap for coloured lines
from obspy.geodetics.base import locations2degrees  # for distance in degrees
from obspy.geodetics import gps2dist_azimuth        # for distance in metres
import matplotlib.transforms as transforms          # for plotting in data or plot coordinates
model = TauPyModel(model='iasp91')                  # The model containing the phase arrivals
client=Client("RASPISHAKE")                         # the seismic data client

# EQ details and paramaters for data selection and plotting
EQNAME = "M6.2 Java, Indonesia"
EQLAT = -6.073
EQLON = 113.116
EQTIME = "2020-02-05 18:12:37"
EQZ=589.6
STARTTIME = UTCDateTime(EQTIME)
PSTART = 500
PEND = 3500
DURATION = PEND-PSTART

# Home station
NETWORK = 'AM'   # AM = RaspberryShake network
STATION = "RD5F3"  # Station code of local station to plot
STA_LAT = 34.76576577   # Latitude of local station  
STA_LON = -112.5250159  # Longitude of local station
CHANNEL = 'EHZ'  # channel to grab data for (e.g. EHZ, SHZ, EHE, EHN)
LOCATION = "Chino Valley"
DISTANCE=locations2degrees(EQLAT, EQLON, STA_LAT, STA_LON) # Station dist in degrees from epicentre
STA_DIST, _, _ = gps2dist_azimuth(STA_LAT, STA_LON, EQLAT, EQLON)   # Station dist in m from epicentre

# Pretty paired colors. Reorder to have saturated colors first and remove some colors at the end.
CMAP = get_cmap('Paired', lut=12)
COLORS = ['#%02x%02x%02x' % tuple(int(col * 255) for col in CMAP(i)[:3]) for i in range(12)]
COLORS = COLORS[1:][::2][:-1] + COLORS[::2][:-1]

# get the data, detrend and filter
st=client.get_waveforms('AM',STATION,'00','EHZ',STARTTIME+PSTART,STARTTIME+PEND)
st.merge(method=0, fill_value='latest')
st.detrend(type='demean')
st.filter("bandpass", freqmin=0.8, freqmax = 3.0, corners=2, zerophase=True)
FILTERLABEL = 'bandpass, freqmin=0.8, freqmax=3.0'

# Plot figure with subplots of different sizes
fig = plt.figure(1, figsize=(19, 11))
ax = fig.add_axes([0.1, 0.1, 0.7, 0.8]) # left margin, bottom margin, width, height
time = np.arange(PSTART, PEND+0.01, 0.01) # A list of elapsed times for the stream file

# set up plot parameters
ax.set_xlim([PSTART, PEND])
ax.tick_params(axis="both", direction="in", which="both", right=True, top=True)
# plot the data
ax.plot(time, st[0], linewidth=0.75)
plt.text(0.5, 1.07, "Core phases from iasp91 model for " + str(EQZ) + "km deep " + EQNAME + " earthquake on " + EQTIME +
         "\nrecorded on Raspberry Shake " + STATION + " in " + LOCATION + " at " + str(STA_DIST//1000) +"km, or " + str(round(DISTANCE,1)) +
         "° from the epicentre.\nFilter: " + FILTERLABEL, transform=ax.transAxes, horizontalalignment='center', verticalalignment='top')
plt.text(0.5, -0.05, "Elapsed time [s]", transform=ax.transAxes, horizontalalignment='center', verticalalignment='top')
plt.text(-0.05, 0.5, "Counts", rotation=90, va="center", ha="center", transform=ax.transAxes, zorder=10, fontsize=10)
# Find the arrivals for this epicentral distance and earthquake depth
arrivals = model.get_travel_times(source_depth_in_km=EQZ, distance_in_degree=DISTANCE)
plotted_arrivals=[]
if arrivals:
    for j, phase in enumerate(arrivals):
        color = COLORS[j%10]
        instring = str(arrivals[j])
        phaseline = instring.split(" ")
        phasetime = float(phaseline[4])
        if PSTART <  phasetime < PEND:
            plotted_arrivals.append([round(float(phaseline[4]), 2), phaseline[0], color])
# If there are arrivals here, plot them
if plotted_arrivals:
    plotted_arrivals.sort()   #sorts the arrivals to be plotted by arrival time
    trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)
    lineNo = 0
    # x and y axis labels
    plt.text(PEND+(0.02*DURATION), 1.03, "Elapsed time [s]", alpha=1.0, c="black", fontsize=11, ha='left', va='bottom', zorder=1, transform=trans)
    plt.text(PEND+(0.12*DURATION), 1.03, "Phase name", alpha=1.0, c="black", fontsize=11, ha='left', va='bottom', zorder=1, transform=trans)
    # Plot the phases on the graph
    for phase_time, phase_name, color_plot in plotted_arrivals:
        # Phase line and label
        ax.vlines(phase_time, ymin=0, ymax=1, alpha=.50, color=color_plot, ls='--', zorder=1, transform=trans)
        plt.text(phase_time, 0.98-(lineNo*0.02), phase_name+" ", alpha=.50, c=color_plot, fontsize=11, ha='right', va='bottom', zorder=1, transform=trans)
        # Entry on printed table to right of plot
        plt.text(PEND+(0.02*DURATION), 0.98-(lineNo*0.02), str(phase_time) + "s", alpha=1.0, c=color_plot, fontsize=11, ha='left', va='bottom', zorder=1, transform=trans)
        plt.text(PEND+(0.12*DURATION), 0.98-(lineNo*0.02), phase_name, alpha=1.0, c=color_plot, fontsize=11, ha='left', va='bottom', zorder=1, transform=trans)
        # Increment the counter for the line number of the label
        lineNo+=1
        if lineNo == 21: # step over the plotted trace with the phase labels
            lineNo += 8
# Save the plot to file, then print to screen
plt.savefig('Earthquake-phases.png')
plt.show()