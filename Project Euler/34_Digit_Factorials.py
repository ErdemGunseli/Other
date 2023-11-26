def compute_factorials(limit):
    factorials = [0] * (limit + 1)
    factorials[0] = factorials[1] = 1
    index = 2

    while index <= limit:
        factorials[index] = index * factorials[index - 1]
        index += 1

    return factorials


# A list where the index corresponds to the factorial of that number:
factorials = compute_factorials(10)
total = 0
for num in range(1, 100_000):
    if sum([factorials[int(val)] for val in str(num)]) == num:
        total += num

# Problem says to exclude 1! == 1 and 2! == 2:
print(total - 3)
