def linear_search(values, target):
    index = 0

    while index < len(values):
        if values[index] == target: return index
        index += 1
    return -1

def recursive_binary_search(values, target, start, end):
    if start > end: return -1

    midpoint = (start + end) // 2

    if target < values[midpoint]:
        return recursive_binary_search(values, target, start, midpoint - 1)
    elif values[midpoint] < target:
        return recursive_binary_search(values, target, midpoint + 1, end)
    else:
        return midpoint
    
def iterative_binary_search(values, target):
    start = 0
    end = len(values) - 1

    # The inverse of start > end is start <= end:
    while start <= end:
        midpoint = (start + end) // 2

        if target < values[midpoint]:
            end = midpoint - 1
        elif values[midpoint] < target:
            start = midpoint + 1
        else:
            return midpoint
    return -1

def bubble_sort(values):
    sorted = False

    while not sorted:
        sorted = True

        index = 0
        # Index increases as much as len(values) - 2 due to the "<":
        # This allows us to access the next index without going out of bounds:
        while index < len(values) - 1:
            # Changing the sign from ">" to "<" will convert from ascending to descending order:
            if values[index] > values[index + 1]:
                # Swapping elements:
                temp = values[index]
                values[index] = values[index + 1]
                values[index + 1] = temp

                # Swap made so not sorted:
                sorted = False
            index += 1

        return values

def insertion_sort(values):
    index = 1

    while index < len(values):
        current_value = values[index]
        position = index

        # Position can decrease down to 1, within bounds when accessing position - 1:
        while position > 0 and (current_value < values[position - 1]):
            # Shifting all values:
            values[position] = values[position - 1]
            position -= 1
        
        # Inserting:
        values[position] = current_value
        index += 1
    
    return values

def to_octal(denaryValue):
    output = ""

    if denaryValue < 0: 
        negative = True
        denaryValue = -denaryValue
    else:
        negative = False
        
    while denaryValue > 7:
        remainder = denaryValue % 8
        denaryValue = denaryValue // 8
        output = str(remainder) + output
    output = str(denaryValue) + output

    if negative: output = "-" + output

    return int(output)
    
print(to_octal(-8))