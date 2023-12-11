def get_combinations(values):
    # C(n) = [n[0] + c for c in C(n[1:])] + C(n[1:])

    if not values: return [[]]

    lower_combinations = get_combinations(values[1:])
    choose_first = [[values[0]] + combination for combination in lower_combinations]

    result = choose_first + lower_combinations

    # Returning all non-empty combinations:
    return [c for c in result if c]


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


def get_variations(string, replacement_indices):
    result = []

    for replacement in range(10):
        current = string
        for index in replacement_indices:
            current = current[:index] + str(replacement) + current[index + 1:]

        # Avoiding leading 0s:
        if current[0] != '0': result.append(current)

    return result


# Skipping 2, 3, 5, 7:
primes = get_primes(10_000_000)[4:]
primes_set = set(primes)

found = False
i = 0
while not found and i < len(primes):
    prime = primes[i]
    prime_str = str(prime)

    j = 0
    index_combinations = get_combinations(list(range(len(prime_str) - 1)))
    while not found and j < len(index_combinations):
        replacement_indices = index_combinations[j]

        # Not replacing the last digit since the even values cannot be primes, so cannot reach 8-family:
        variations = get_variations(prime_str, replacement_indices)
        variations = [int(v) for v in variations if v is not None]
        prime_variations = [v for v in variations if v in primes_set]

        if len(set(prime_variations)) == 8:
            print(f"The prime {prime_str} gives variations {prime_variations} when the indices "
                  f"{replacement_indices} are replaced. "
                  f"The smallest out of these primes is {min(prime_variations)}")

            found = True

        j += 1

    i += 1