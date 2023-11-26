def factorial_digit_sum(n):
    total = 1
    for value in range(2, n + 1):
        total *= value
    return sum(int(digit) for digit in str(total))


# The sum of digits in 100 is the same as 99!:
print(factorial_digit_sum(99))
