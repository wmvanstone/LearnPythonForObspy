# Use input() function to collect string input
# assign the string to the variable name using =
name = input("Hello, what is your name? ")
# Convert from string to integer (whole number) using int().
# Assign the input to the variable age using an = sign.
age = int(input("Hello " + name + " how old are you in years? "))
# perform a calcualation to find birth year
year = 2020 - age
# print the results, using string concatenation with +
# and type casting, from integer to string, using str()
print("You were born in " + str(year-1) + " or " + str(year))