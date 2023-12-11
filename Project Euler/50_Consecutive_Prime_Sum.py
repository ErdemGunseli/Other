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


def is_prime(n, primes):
    if n < 2: return False

    index = 0
    while primes[index] ** 2 <= n:
        if n % primes[index] == 0: return False
        index += 1
    return True


primes = get_primes(10_000)

sequence_length = len(primes)
maximum_length = 0
maximum_prime = 0

found = False
while not found and 0 < sequence_length:

    i = 0
    while not found and i < len(primes) - sequence_length:
        current_val = sum(primes[i: i + sequence_length])

        if current_val < 1_000_000 and is_prime(current_val, primes):
            maximum_length = sequence_length
            maximum_prime = current_val
            found = True

        i += 1

    sequence_length -= 1

print(f"{maximum_prime}, {maximum_length}")
