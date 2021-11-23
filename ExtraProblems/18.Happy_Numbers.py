count = 0
sumOfDigits^2 = 0
number = 1
while count < 8:
    happyLogic = 0
    sumOfDigitsSquared = 0
    digitsList = [char for char in str(number)]
    
while sumOfDigitsSquared != 1:
    for i in (digitsList):
        sumOfDigitsSquared += int(i**2)
    
    print(sumOfDigitsSquared)
    digitsList = [char for char in str(sumOfDigitsSquared)]
    

