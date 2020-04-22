# Lesson 6: Obspy and DateTime
# Obspy is a Python package containing software for processing and plotting seismic data
# You can read the documentation here: https://docs.obspy.org/contents.html
# Install obspy in Thonny using Tools | Manage Packages, search for obspy and click install
# now import the UTCDateTime class into your code. Importing just this class saves memory. 
from obspy import UTCDateTime
# UTCDateTime converts date-time text strings into a format that can be manipulated in your code
example = UTCDateTime("2020-04-21T16:35:00")
# \n is an escape character, it adds an extra newline character to your printout, spacing it neatly
print("The example is: " + str(example) + "\n")
# If you call UTCDateTime with no argument, it returns the current Coordinated Universal Time
datetime = UTCDateTime()
print("The current time is: " + str(datetime) + "\n")
# You can use dot notation to separate out different parts of the date-time
print("The year is: " + str(datetime.year))
print("The day of the year is: " + str(datetime.julday))
print("The seconds since 1970-01-01 00:00:00 is: " + str(datetime.timestamp))
print("The day of the week is: " + str(datetime.weekday))
# To name the day of the week, you can index a tuple, like a list, but immutable (not changeable)
weekdays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
print("Today is: " + weekdays[datetime.weekday] + "\n")
# You can add to the time in seconds. 900s is 15 minutes. 86400s is a day.
newtime = datetime + 900
print("In 15 minutes the time will be: " + str(newtime.time) + "\n")
# you can also subtract times to calculate a duration
eq_name = "M 6.6 - 209km W of Chichi-shima, Japan"
eq_time = UTCDateTime("2020-04-18 08:25:37")
elapsed_time = datetime - eq_time
print(str(elapsed_time) + "s have elapsed since the " + eq_name + " earthquake on "
      + weekdays[datetime.weekday] + " " + str(eq_time.date))