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


def is_circular_prime(prime, prime_set):
    prime_str = str(prime)

    for i in range(len(prime_str)):
        rotated = int(prime_str[i:] + prime_str[:i])

        if rotated not in prime_set:
            return False
    return True


primes = get_primes(1_000_000)
prime_set = set(primes)

# Count circular primes.
circular_primes = [prime for prime in primes if is_circular_prime(prime, prime_set)]

# The total number of circular primes below one million.
print(len(circular_primes))
