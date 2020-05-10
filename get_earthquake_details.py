# importing the required libraries for requesting the data
import requests
from csv import DictReader

# URL for USGS Earthquake data
DATA_URL = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.csv'
print("Downloading", DATA_URL)
resp = requests.get(DATA_URL)
quakes = list(DictReader(resp.text.splitlines()))
for i, quake in enumerate(quakes):
    print(i, quake['mag'], quake['place'], quake['time'])
choice = int(input("Which quake do you want? "))

# Print out the earthquake details
print("")
print("URL = https://earthquake.usgs.gov/earthquakes/eventpage/"+ quakes[choice]['id'] + "/executive")
print("EQNAME = 'M" + quakes[choice]['mag'] + " - " + quakes[choice]['place'] + "'")
print("EQLAT =", quakes[choice]['latitude'])
print("EQLON =", quakes[choice]['longitude'])
print("EQZ =", quakes[choice]['depth'])
print("EQTIME = '" + quakes[choice]['time'] + "'")
print("FILE_STEM = '" + quakes[choice]['place'].split(", ")[-1] + "-" + quakes[choice]['time'][0:10] + "'")