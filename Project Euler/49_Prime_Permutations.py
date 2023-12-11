
def is_prime(n):
    if n < 2: return False

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0: return False
    return True


def get_primes(limit):
    if limit < 2: return []

    # A boolean array stores whether the number of the current index is a prime:
    # Going 1 above the limit so each number matches its index:
    numbers = [True] * (limit + 1)
    numbers[0] = numbers[1] = False

    for number in range(2, int(limit ** 0.5) + 1):
        # If the current number is marked as prime, setting all of its multiples as not prime:
        if numbers[number]:
            # Using list slicing to set multiples to false:
            numbers[number * 2: limit + 1: number] = [False] * ((limit - number) // number)

    # Extracting the value alongside its index using enumerate:
    # If the number is prime (i.e. the value is true), including that number in the new list:
    return [i for i, is_prime in enumerate(numbers) if is_prime]


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


def get_triplet_with_common_difference(values):
    for i in range(len(values)):
        i_val = values[i]

        for j in range(i + 1, len(values)):
            j_val = values[j]

            lower_third = 2 * i_val - j_val
            if lower_third in values and lower_third not in [i_val, j_val]:
                return [i_val, j_val, lower_third]

            upper_third = 2 * j_val - i_val
            if upper_third in values and upper_third not in [i_val, j_val]:
                return [i_val, j_val, upper_third]

    return None


primes = get_primes(10_000)

i = 0
while i < len(primes):
    current_prime = primes[i]

    permutations = [int("".join(p)) for p in get_permutations(list(str(current_prime)))]
    prime_permutations = [p for p in permutations if is_prime(p)]

    # Find if 3 of the permutations have the same difference:
    triplet = get_triplet_with_common_difference(prime_permutations)
    if triplet is not None and all([len(str(num)) == 4 for num in triplet]): print(triplet)

    i += 1
