valid = "false"

while valid == "false":
    try:
        option = int(input("Please enter a number between 1 and 3 (inclusive): ")) #If the user does not enter an integer, the code will loop back.
    except ValueError: #catch
        continue

    if option > 0 and option < 4: #If the user has selected option 1, 2 or 3, the loop will end.
        valid = "true"
    #endif
#endwhile

print("You have selected option nuber {}.".format(option))

## ACS - I likt the error trapping. I prefer comments before the line rathyer than on it (just makes lines less long!)
