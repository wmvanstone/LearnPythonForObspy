import requests
from csv import DictReader
import obspy
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
from obspy.geodetics import gps2dist_azimuth
from obspy.geodetics.base import locations2degrees
from obspy.clients.fdsn import RoutingClient
from obspy.taup import TauPyModel
model = TauPyModel(model='iasp91')
# URL for Geonet Earthquake data
START = '2020-01-01T00:00:00'
END = '2020-07-12T20:30:00'
DURATION = 240
MINMAG="5.5"
CLIENT = RoutingClient("iris-federator")
data_url = 'https://quakesearch.geonet.org.nz/csv?bbox=164.00391,-49.18170,182.54883,-32.28713&minmag=' + MINMAG + '&startdate=' + START + '&enddate=' + END
# Peform the query
resp = requests.get(data_url)
quakes = list(DictReader(resp.text.splitlines()))
# pick the most recent earthquake
starttime = UTCDateTime(quakes[0]['origintime'])
inventory = CLIENT.get_stations(channel="HHZ", network="NZ", station="*", starttime=starttime, latitude=quakes[0][' latitude'], longitude=quakes[0]['longitude'], minradius=0, maxradius=10)
#print(len(inventory.networks[0]))
mindist = 1e100
closest_station = ""
for station in inventory.networks[0]:
    dist, _, _ = gps2dist_azimuth(float(quakes[0][' latitude']), float(quakes[0]['longitude']), station.latitude, station.longitude, a=6378137.0, f=0.0033528106647474805)
    if dist < mindist:
        mindist = dist
        closest_station = station
seismometer = closest_station.code
dist_degrees = locations2degrees(float(quakes[0][' latitude']), float(quakes[0]['longitude']), closest_station.latitude, closest_station.longitude)
arrivals=model.get_travel_times(source_depth_in_km=float(quakes[0][' depth']), distance_in_degree=dist_degrees)
first_arrival = float(str(arrivals[0]).split(" ")[4])
client=Client("GEONET")
filename = "NewZealand.png"
st = client.get_waveforms('NZ', seismometer, '*', 'HHZ', starttime + first_arrival - 5, starttime + DURATION + first_arrival - 5) 
st.merge(method=0, fill_value='latest')
st.detrend(type='demean')
st.filter("bandpass", freqmin=0.9, freqmax = 10.0, corners=4)
st.plot(outfile=filename)
st.plot()