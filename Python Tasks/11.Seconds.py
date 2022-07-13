input_time = str(input("Please enter the time: ")).split(":") #Splits the input from the semicolons and adds it into a list.

hours = int(input_time[0]) #First member of the list will be hours, second member will be minutes, third member will be seconds.
minutes = int(input_time[1])
seconds = int(input_time[2])

print("{} seconds".format(hours * 3600 + minutes * 60 + seconds)) #Converts everything to seconds and prints it.


## ACS Good