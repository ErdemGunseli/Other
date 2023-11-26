
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

    b = len(pentagonals) - 2
    found = False
    while -1 < b and not found:
        p_b = pentagonals[b]

        total = p_a + p_b
        difference = p_a - p_b

        if is_pentagonal(total) and is_pentagonal(difference) and difference < min_difference:
            min_difference = difference
            found = True

print(min_difference)
