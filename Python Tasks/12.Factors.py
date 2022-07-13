input_integer = int(input("Please enter an integer: "))
output = []

for i in range(2,input_integer): #Starts from 2 and ends at input_integer - 1 so that 1 and the number itself are not written as factors, which is how it is done in the example.
    if input_integer % (i) == 0: #If the input_integer can be divided with a number and there is no remainder, that number is a factor.
        print(i, end=", ") #Prints the factors.
    #endif
#loop


## ACS Don't forget 1 and 48 they are noth factors of 48!