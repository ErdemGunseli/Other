def is_prime(n):
    if n < 2: return False

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True


def get_pandigital_nums(n):
    # The map function applies the input function to each item in the list and returns the resulting iterable:
    # list(map(f, vals)) == [f(val) for val in vals]
    return [int("".join(map(str, permutation))) for permutation in get_permutations(list(range(1, n + 1)))]


def get_permutations(values):
    if not values: return [[]]

    result = []

    for value in values:
        values_copy = values.copy()
        values_copy.remove(value)
        current_permutation = get_permutations(values_copy)

        for permutation in current_permutation:
            result.append([value] + permutation)

    return result


# A number is divisible by 3 if the sum of its digits is divisible by 3.
# For this reason, all 1-8 and 1-9 pandigital numbers are divisible by 3
# Flattening the 2D list of all pandigital numbers:
pandigital_numbers = [item for sublist in [get_pandigital_nums(i) for i in range(1, 8)] for item in sublist]
pandigital_primes = [p for p in pandigital_numbers if is_prime(p)]
print(f"Max: {max(pandigital_primes)}")


