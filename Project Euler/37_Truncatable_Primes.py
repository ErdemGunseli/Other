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


def is_prime(num):
    if num < 2: return False

    for i in range(2, int(num**0.5) + 1):
        if num % i == 0: return False
    return True


def is_truncatable(num):
    num_str = str(num)

    if not is_prime(num): return False

    for i in range(1, len(num_str)):
        if not(is_prime(int(num_str[:-i])) and is_prime(int(num_str[i:]))): return False
    return True


# 2, 3, 5 and 7 are not truncatable:
primes = get_primes(1_000_000)[4::]

result = [i for i in primes if is_truncatable(i)]
print(f"Sum: {sum(result)}, Result: {result}")
