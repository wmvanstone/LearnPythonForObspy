# Python 3 iteration and lists
# ITERATION is how programs repeat a procedure over and over again.
# Definite iteration is where the number of repetitions is defined in advance.
# Definite iteration can be performed using a for loop or a while loop (in a future lesson)
# Here a variable i is incremented from 0 to 9, producing 10 numbers, which are printed
for i in range(10):
    print(i)
print("")
# By default, the range() function counts from zero to one less than its argument
input("Press enter to continue to the ten times table")
print("")

# The next script prints the ten times table, from 1x10 to 12x10
timestable = 10
print(" " + str(timestable) + " Times Table")
print("")
# here, the for loop interated from 1 to 12 (one less than 13)
for i in range(1, 13):
    print(str(i) + " x " + str(timestable) + " = " + str(i*timestable))
print("")
input("Press enter to print out the seismometers")
print("")

# for loops can also iterate through lists containing text.
# seislist is a list of Raspberry Shake seismometer names.
seislist=['RB30C','RB5E8','RD93E','R82BD','R7FA5','R0353','R9FEE']
# the name of each seismometer in turn is passed to the stationID variable and printed.
for stationID in seislist:
    # If the seismometer is this specific one, then it is identified as the home station.
    if stationID == 'R7FA5':
        print(stationID + " home")
    else:
        print(stationID)