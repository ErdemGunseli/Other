def get_nth_prime(n, search_limit=999_999):
    if n < 1: return None

    # A boolean array stores whether the number of the current index is a prime:
    # Going 1 above the limit so each number matches its index:
    numbers = [True] * (search_limit + 1)
    numbers[0] = numbers[1] = False

    for number in range(2, int(search_limit ** 0.5) + 1):
        # If the current number is marked as prime, setting all of its multiples as not prime:
        if numbers[number]:
            # Using list slicing to set multiples to false:
            numbers[number * 2: search_limit + 1: number] = [False] * ((search_limit - number) // number)

    # Extracting the value alongside its index using enumerate:
    # If the number is prime (i.e. the value is true), including that number in the new list:
    primes = [i for i, is_prime in enumerate(numbers) if is_prime]

    if n < len(primes):
        return primes[n - 1]


print(get_nth_prime(10_001))
