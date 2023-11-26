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


def get_prime_factors(n):
    primes = get_primes(int(n**0.5) + 1)
    prime_factors = []

    index = 0
    while index < len(primes) and 1 < n and primes[index] <= n:
        if n % primes[index] == 0:
            n = n // primes[index]
            prime_factors.append(primes[index])
        else:
            index += 1

    if 1 < n: prime_factors.append(n)
    return prime_factors


print(max(get_prime_factors(600851475143)))

