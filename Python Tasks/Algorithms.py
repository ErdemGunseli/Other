import random


# Searching Algorithms:

from random import randint
from turtle import pos, position


def linearSearch(list, target):
    # Not using For / For Each loop:
    index = 0
    while index < len(list):
        if (list[index] == target): return index
        index += 1
    return -1

def binarySearch(list, startIndex, endIndex, target):
    # startIndex and endIndex are redundant for the first call
    midpoint = (startIndex + endIndex) // 2

    if (list[midpoint] > target):
        return binarySearch(list, startIndex, midpoint - 1, target)
    elif (list[midpoint] < target):
        return binarySearch(list, midpoint + 1, endIndex, target)    
    else:
        return midpoint

# Sorting Algorithms:

def bubbleSort(list):
    done = False
    while not done:
        done = True
        index = 0
        while (index < len(list) - 1):
            
            firstItem = list[index]
            secondItem = list[index + 1]

            if firstItem > secondItem:
                # Swapping items
                list[index] = secondItem
                list[index + 1] = firstItem
                done = False

                print(list)
            index += 1 
      
    return list   

def insertionSort(list):
    index = 1

    while (index < len(list)):
        currentValue = list[index]
        position = index
        while (position > 0 and currentValue < list[position - 1]):
            # Shifting all values
            list[position] = list[position - 1]
            position -= 1

        # Inserting
        list[position] = currentValue
        index += 1      

    return list            


def mergeSort(list):
    pass


def quickSort():
    pass


# Generates a random list of integers of the specified size:
def randomList(length, ordered):
    list = []
    for index in range(length):
        list.append(random.randint(0, 100))
    
    if (ordered): return insertionSort(list)
    return list