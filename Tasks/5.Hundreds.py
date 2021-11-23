input_integer = int(input("Please enter an integer between 100 and 999: "))

hundreds = input_integer // 100 #Calculates the hudreds
tens = (input_integer - 100 * hundreds) // 10 #Calculates the tens
units = (input_integer - hundreds * 100 - tens * 10) #Calculates the units

print("{} hundreds, {} tens, and {} units".format(hundreds, tens, units))


## ACS - well done good work