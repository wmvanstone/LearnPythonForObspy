#Lesson 14: finding arrival times using TauP
from obspy import UTCDateTime
from obspy.taup import TauPyModel
from obspy.geodetics.base import locations2degrees
from obspy.geodetics import gps2dist_azimuth

# EQ details and paramaters for data selection and plotting
EQNAME = "M 6.6 - 89km S of Ierapetra, Greece"
EQLAT = 34.205
EQLON = 25.712
EQTIME = "2020-05-02 12:51:06"
EQZ = 17

# Home station
STA_LAT = 50.2609  # Latitude of local station  
STA_LON = -5.0434  # Longitude of local station
LOCATION = "TRURO SCHOOL"
DEGREES = locations2degrees(EQLAT, EQLON, STA_LAT, STA_LON) # Station dist in degrees from epicentre
DISTANCE, _, _ = gps2dist_azimuth(STA_LAT, STA_LON, EQLAT, EQLON)   # Station dist in m from epicentre

# Model phases
model = TauPyModel(model='iasp91')
PHASES = sorted(["P", "pP", "PP", "S", "Pdiff", "PKP", "PKIKP", "PcP", "ScP", "ScS", "PKiKP", "SKiKP", "SKP", "SKS"]) # list of phases

# Find the arrival times
arrival_list=[]
for phase in PHASES:
    arrivals = model.get_travel_times(source_depth_in_km=EQZ, distance_in_degree=DEGREES, phase_list=[phase])
    if arrivals:
        for arrival in arrivals:
            phasestring = str(arrival) # arrivals are in this format "P phase arrival at 345.851 seconds"
            phaseline = phasestring.split(" ")
            phasetime = float(phaseline[4])
            arrival_list.append([phasetime, phaseline[0]])

# Print out the earthquake details, station details and phases in order
print("For " + EQNAME + " at " + EQTIME)
print("Distance to " + LOCATION + " is " + str(round(DISTANCE/1000, 1)) + "km, or " + str(round(DEGREES, 1)) + "°\n")
print("The phases arriving at this location, in time order are:")
arrival_list.sort()
for arrival in arrival_list:
    arrival_time = (UTCDateTime(EQTIME)+arrival[0])
    print(arrival[1] + " phase arrival after " + str(round(arrival[0], 0)) + "s at " + (arrival_time.strftime("%Y-%m-%d %H:%M:%S")))