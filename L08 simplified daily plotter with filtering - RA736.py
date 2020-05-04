# Python Lesson 8: daily plot of unfiltered data
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
# set up plotting parameters
START = UTCDateTime("2020-05-04 00:00:00")
DAYS = 1
SEISMOMETER = 'RA736'
CLIENT = Client('RASPISHAKE')
# choose whether to include worldwide earthquake events on the plot.
# .upper() changes the response to upper case, so "y" or "Y" will be acceptable
printevents = input("Do you want to print worldwide earthquake events? Y/N ").upper()
if printevents == "Y":
    # set the minimum magnitude of events to 5. Events come from obspy.clients.fdsn
    events = {'min_magnitude': 5}
else:
    # don't plot events
    events = []
# loop through the required number of days from the start date/time
for day in range(DAYS):
    starttime = START + (day * 86400)
    endtime = starttime + 86400
    # Read the seismic stream
    # try: ... except: ... else: will capture and report an error loading a trace without the program crashing
    try: 
        st = CLIENT.get_waveforms('AM', SEISMOMETER, '00', 'EHZ', starttime, endtime)
        # merge fragmented traces and interpolate across any gaps
        st.merge(method=0, fill_value='latest')
    # if there is an error, report it, skip else: and continue with next day
    except:
        print("Unable to load trace data for day: " + str(day))
    # else: will run if no errors occurred in try:
    else:
        filename = SEISMOMETER + "-" + str(starttime.date) + ".png"
        print("Printing: " + filename)
        # write plot to file
        st.plot(type="dayplot", interval=60, right_vertical_labels=True, one_tick_per_line = True, size=(1920,1080),
                color = ['k', 'r', 'b', 'g'], show_y_UTC_label=True, vertical_scaling_range=2000, events=events,
                outfile="unfiltered-"+filename)
        # print to screen
        st.plot(type="dayplot", interval=60, right_vertical_labels=True, one_tick_per_line = True, size=(1000,800),
                color = ['k', 'r', 'b', 'g'], show_y_UTC_label=True, vertical_scaling_range=2000, events=events)
        # filter
        st.filter("bandpass", freqmin=0.9, freqmax = 3.0, corners=4)
        # write plot to file
        st.plot(type="dayplot", interval=60, right_vertical_labels=True, one_tick_per_line = True, size=(1920,1080),
                color = ['k', 'r', 'b', 'g'], show_y_UTC_label=True, vertical_scaling_range=400, events=events,
                outfile="filtered-"+filename)
        # print to screen
        st.plot(type="dayplot", interval=60, right_vertical_labels=True, one_tick_per_line = True, size=(1000,800),
                color = ['k', 'r', 'b', 'g'], show_y_UTC_label=True, vertical_scaling_range=400, events=events)
