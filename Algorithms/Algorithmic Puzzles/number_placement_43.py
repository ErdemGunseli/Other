def place_numbers(signs, numbers):
    result = []
    numbers = sorted(numbers)

    while len(signs) > 0:
        if signs[0] == ">":
            # Finding the largest number and removing it:
            number = numbers[-1]
            numbers.pop(-1)
        else:
            # Finding the smallest number and removing it:
            number = numbers[0]
            numbers.pop(0)

        # Removing the first sign:
        signs = signs[1:]
        result.append(number)

    # Adding the final number to the result (since there is 1 more number than there are signs):
    result.append(numbers[0])
    return result


if __name__ == "__main__":
    print(place_numbers("<><", [2, 5, 1, 0]))
