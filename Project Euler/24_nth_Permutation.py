# There are 10! permutations starting with 0, and 10! > 1_000_000, so the first digit is 0.
# There are 9! permutations starting with 01, 9! starting with 02 and so on, so second digit is 3.
# We can find it this way, but here is a general-purpose algorithm to find any permutation.

def factorial(n):
    if n < 1: return 0
    elif n == 1: return 1
    return n * factorial(n - 1)


def find_nth_permutation(n, characters):
    result = []

    # Permutations are 0-indexed (i.e. 0th permutation is 0123456789), so subtracting 1 from n:
    n -= 1

    current_factorial = len(characters) - 1
    while 0 < n:

        factorial_value = factorial(current_factorial)
        index = n // factorial_value
        n %= factorial_value

        result.append(characters[index])
        characters.remove(characters[index])
        current_factorial -= 1

    result.extend(characters)
    return "".join(result)


print(find_nth_permutation(1_000_000, [str(num) for num in range(10)]))




