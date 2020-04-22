# Lesson 5b: Packages need to be imported into Thonny using Tools | Manage Packages.
# Plot multiple stations, centred on the United Downs Deep Geothermal Project
import folium
# Set up a list of stations. This is a list of lists, a 2 dimensional list.
STATIONS = [
['RB30C','Falmouth',50.149,-5.095],
['RB5E8','Penzance',50.118,-5.539],
['RD93E','Redruth',50.234,-5.238],
['R82BD','Richard Lander',50.26,-5.103],
['R7FA5','Truro School',50.261,-5.043],
['R0353','Penair',50.267,-5.03],
['R9FEE','Truro High',50.257,-5.057]
]
# The following arguments will centre the map on United Downs Deep Geothermal Project, zooming in to Cornwall.
map = folium.Map(location=[50.230, -5.166],zoom_start=11,tiles='Stamen Terrain')
# Now you can add markers to show each station in turn
# station is a simple list showing the stationID, location, lat, long, for each station in turn
for station in STATIONS:
    folium.Marker(location=[station[2], station[3]], popup=station[1], icon=folium.Icon(color='orange')).add_to(map)
# Finally, add a red marker for UDDGP, the deepest borehole in mainland UK
folium.Marker(location=[50.230, -5.166], popup='UDDGP', icon=folium.Icon(color='red')).add_to(map)
# save the file to disk as a web page.
map.save('cornish-stations.html')
# Locate the file and double click on it. You have an interactive map showing the cornish Raspberry Shake stations.
# You can zoom in and out, as well as clicking on the markers to see the popup text. 
