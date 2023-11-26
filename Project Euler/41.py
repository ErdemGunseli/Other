
def is_pandigital(num):
    num_str = str(num)
    degree = len(num_str)
    return all([str(digit) in num_str for digit in range(1, degree + 1)])


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

# Pandigital numbers can be 8-digits max:
primes = get_primes(987_654_321)
largest = max([prime for prime in primes if is_pandigital(prime)])
