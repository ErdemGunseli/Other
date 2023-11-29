
def get_pentagonal(n):
    return n * (3 * n - 2) // 2


def is_pentagonal(num):
    n = (1 + (24 * num + 1) ** 0.5) / 6
    return n.is_integer()


pentagonals = []
min_difference = float("inf")
for a in range(1, 99_999):
    p_a = get_pentagonal(a)
    pentagonals.append(p_a)

    b = a + 1
    found = False
    while b < 99_999 and not found:
        p_b = get_pentagonal(b)

        total = p_a + p_b
        difference = p_b - p_a

        if is_pentagonal(total) and is_pentagonal(difference):
            found = True

            if difference < min_difference:
                min_difference = difference

        b += 1

print(min_difference)
