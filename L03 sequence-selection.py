# Lesson 3 - sequence and selection
# The SEQUENCE of program flow is from top to bottom and left to right
authorised_user = "Mark"
name = input("Please enter your name: ")
# Program flow branches at if statements. If allows SELECTION to be performed.
# The == operator tests for equality. Are name and authorised user the same?
# If the condition is matched, then the subsequent indented block of code is run.
# I always use a tab character for the indent. The colon : here is essential.
if name == authorised_user:
    print("Good morning " + name)
    print("You are welcome to explore my facilities")
# elif stands for else if. It is only tested when the first if condition is not met.
elif name == "Dr Chandra":
    print("Good morning Dr Chandra, this is HAL")
    print("I am ready for my first lesson")
# You can have multiple elif statements
elif name == "Superuser":
    print("Good morning " + name)
    print("You have administrator access")
# else is what happens if neither if or elif conditions are met.
else:
    print("Good morning " + name)
    print("You have guest access.")
# You don't need to capture the return value from the input() function
input("Press Enter to continue")
# triple-quoted strings can be split across multiple lines
print('''
TTTTT  H   H  EEEEE    EEEEE  N   N  DDD
  T    H   H  E        E      NN  N  D  D
  T    HHHHH  EEE      EEE    N N N  D   D
  T    H   H  E        E      N  NN  D  D
  T    H   H  EEEEE    EEEEE  N   N  DDD  ''')
    
    