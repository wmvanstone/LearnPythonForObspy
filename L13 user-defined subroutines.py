#!/usr/bin/env python
"""
Lesson 13: User-defined functions
Mark Vanstone
Truro School, Cornwall
April 2020
"""
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Raspberry Shake section plotter") # tool for getting place names

# Subroutine for getting station address details. One parameter, station, a list [ID, lat, lon]
# This subroutine does not return a value
def find_address(station):
    try:
        location = str(geolocator.reverse(str(station[1]) + ", " + str(station[2])))
    except:
        print("No address found for " + station[0])
        output = "No address found"
    else:
        address = location.split(", ")
        output = address[0] + ", " + address[1] + ", " + address[2] + ", " + address[-1]
    print(output)

# Subroutine for reading Raspberry Shake ID, Lat, Long data, returns a list with this data
# This subroutine has no parameters. It returns a list. 
def read_stations():
    output = []
    with open ("ShakeNetwork2020.csv", "r") as rd:
        for line in rd: # Read lines using a loop loop
            noCR = line.strip() # All lines (besides the last) will include  newline, so strip it off
            tempString = noCR.split(',') # Parse the line using commas
            output.append([tempString[0], tempString[2], tempString[3]])
    return output

# Subroutine the returns the Cornish Raspberry Shakes
def cornish_stations():
    STATIONS = [['RB30C',50.149,-5.095],['RB5E8',50.118,-5.539],['RD93E',50.234,-5.238],
    ['R82BD',50.26,-5.103],['R7FA5',50.261,-5.043],['R0353',50.267,-5.03],['R9FEE',50.257,-5.057]]
    return STATIONS    

# Main program
if __name__ == "__main__":
    print("\nDisplay the addresses of Cornish Stations\n")
    stations = cornish_stations()
    # find the station address and print it to screen
    for station in stations:
        find_address(station)
    
    print("\nDisplay the addresses of Worldwide Stations\n")
    # Get the list of seismometers from file, data downloaded from http://www.fdsn.org/networks/detail/AM/
    stations = read_stations() # list to save stations
    # find the station address and print it to screen
    for i in range(1, 11):
        find_address(stations[i])