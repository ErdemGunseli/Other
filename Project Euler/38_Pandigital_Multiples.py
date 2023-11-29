
def is_pandigital(num):
    num_str = str(num)
    degree = len(num_str)
    return all([num_str.count(str(digit)) == 1 for digit in range(1, degree + 1)])


num = 1
n = 2
maximum = 0
# If the number itself is 5 digits, when n=2 is concatenated, result will be 10 digits:
while len(str(num)) < 5:
    current = num
    n = 2

    while len(str(current)) < 10:
        # Concatenating n * num:
        current = int(str(current) + str(n * num))

        # If we have a 9-digit pandigital number greater than the previous maximum, updating it:
        if len(str(current)) == 9 and maximum < current and is_pandigital(current): maximum = current
        n += 1

    num += 1

print(maximum)
