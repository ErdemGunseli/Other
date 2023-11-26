
def place_signs(n):
    r = n % 4

    # Sum of numbers n(n+1)/2 must be even, i.e. n(n+1)/4 must be an integer.
    # This means 4|n or 4|(n+1):
    if r not in [0, 3]: return None
    numbers = list(range(1, n + 1))

    if r == 0:
        # If 4|n:
        # Index 0 and n-1 positive
        # Index 1 and n-2 negative
        # Index 2 and n-3 positive...

        i = 1
        j = n - 2
        while i < j:
            numbers[i] = -numbers[i]
            numbers[j] = -numbers[j]
            i += 2
            j -= 2
    else:
        # If 4|(n+1):
        # We have 1+2 3 at the start (or equally -1-2+3)
        numbers[2] = -numbers[2]

        i = 4
        # The numbers after that are split into groups of 4:
        # First and fourth numbers are positive.
        # Second and third numbers are negative.
        while i < n - 1:
            numbers[i] = -numbers[i]
            numbers[i + 1] = -numbers[i + 1]

            i += 4

    return numbers


if __name__ == "__main__":
    for number in range(1, 100):
        result = place_signs(number)

        if result is not None:
            total = sum(place_signs(number))
            print(f"When n = {number}, the sum is {total}.")
