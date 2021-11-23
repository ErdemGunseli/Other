unsorted = []
sorted = []

for i in range(3):
    unsorted.append(int(input("Please enter a number: "))) #Enters the input numbers to the unsorted list.
#loop


# Sort the numbers
for i in range(2): #Looks for the biggest number, removes it from the unsorted list, adds it to the beginning of the sorted list. Only repeated 2 times because when there is 1 number remaining, it will obviously be the biggest number remaining.
    max = unsorted[0]
    for i in unsorted:
        if i > max:
            max = i
    sorted.append(max)
    unsorted.remove(max)
#loop


for i in range(2):
    print(sorted[i], end=", ") #Prints the sorted list.
#loop
print(unsorted[0]) #Prints the last number remaining in the unsorted list.

#I didn't want to do it through brute-force or use the sort() function.

## ACS - Thjat's fine. We will look at sorting algorithms soon anyway!
