import math


def get_proper_factors(n):
    factors = [1]

    for num in range(2, int(math.sqrt(n)) + 1):
        if n % num == 0:
            factors.append(num)

            if n // num != num:
                factors.append(n // num)

    return factors


amicable_numbers = set()
for i in range(2, 10_001):
    sum_of_proper_factors = sum(get_proper_factors(i))
    if i != sum_of_proper_factors and i == sum(get_proper_factors(sum_of_proper_factors)) and sum_of_proper_factors < 10_001:
        amicable_numbers.add(i)
        amicable_numbers.add(sum_of_proper_factors)


print(sum(amicable_numbers))
