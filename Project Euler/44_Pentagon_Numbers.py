
def get_pentagonal(n):
    return n * (3 * n - 1) // 2


def is_pentagonal(num):
    n = (1 + (24 * num + 1) ** 0.5) / 6
    return n.is_integer(), n


min_difference = float("inf")
for a in range(1, 10_000):

    b = a + 1
    done = False
    while b < 10_000 and not done:
        p_a = get_pentagonal(a)
        p_b = get_pentagonal(b)

        total = p_a + p_b
        difference = p_b - p_a

        # If the difference is already larger than the minimum, we can break early:
        if min_difference < difference: done = True

        if is_pentagonal(total)[0] and is_pentagonal(difference)[0] and difference < min_difference:
            min_difference = difference

        b += 1

print(min_difference)
