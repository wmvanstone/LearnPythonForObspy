# Lesson 5: Packages need to be imported into Thonny using Tools | Manage Packages.
# Search for Folium in PyPI and install the package before running this program.
# Folium contains a toolkit of mapping functions that you can use once the package is imported.
import folium
# First we enter earthquake details and paramaters for data selection and plotting.
# Constants contain data that does not change during program execution. They are named using upper case. 
EQ_NAME = "Mw 5.4 Nikol'skoye"
EQ_LAT = 54.831
EQ_LON = 166.175
# Details of your station
STATION = "R7FA5"  # Station code of local station to plot
STA_LAT = 50.2609  # Latitude of local station  
STA_LON = -5.0434  # Longitude of local station
# Now you can plot the epicentre and seismometer on the map.
# First, set up the map, centred on the earthquake epicentre.
# Map() is a function which is found in the folium package, location, zoom_start and tiles are arguments.
# dot notation is used to identify that Map is found inside folium. folium.Map() returns a map object.
map = folium.Map(location=[EQ_LAT, EQ_LON],zoom_start=2,tiles='Stamen Terrain')
# Now you can add an orange marker at the earthquake epicentre onto the map. Marker is a function in folium.
folium.Marker(location=[EQ_LAT, EQ_LON], popup=EQ_NAME, icon=folium.Icon(color='orange')).add_to(map)
# You can also add a red marker at the seismometer.
folium.Marker(location=[STA_LAT, STA_LON], popup=STATION, icon=folium.Icon(color='red')).add_to(map)
# save the file to disk as a web page.
map.save('earthquakemap.html')
# Locate the file and double click on it. You have an interactive map showing the epicentre and seismometer.
# You can zoom in and out, as well as clicking on the markers to see the popup text. 
