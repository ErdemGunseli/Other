import string

offset = 5 #any offset can be entered

input_string = input("Please enter your input: ").lower()
alphabet_list = [char for char in string.ascii_lowercase] #Each member of the list will be a lowercase letter from a to z.
for i in input_string:
    if i == " ":
        print(" ", end ="")
    else:
        try:
            print(alphabet_list[alphabet_list.index(i) + offset], end ="") #Prints the letter after the offset is applied.
        except IndexError:
            print(alphabet_list[(alphabet_list.index(i) + offset) - len(alphabet_list)], end="")#If there is an index error, it will loop back to the top of the list to give the correct value.
    #endif
#loop


## Good work