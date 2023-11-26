
import math


def get_proper_factors(n):
    factors = [1]

    for num in range(2, int(math.sqrt(n)) + 1):
        if n % num == 0:
            factors.append(num)

            if n // num != num:
                factors.append(n // num)

    return factors


def is_abundant(n):
    return n < sum(get_proper_factors(n))


abundant_numbers_set = {num for num in range(12, 28_124) if is_abundant(num)}

non_abundant_sums = [i for i in range(1, 28_123) if not any((i - num in abundant_numbers_set)
                                                             for num in abundant_numbers_set if num <= i / 2)]

print(sum(non_abundant_sums))
