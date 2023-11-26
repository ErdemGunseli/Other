"""
Generate hexagonal numbers, check if pentagonal and triangular.
"""


def is_triangular(num):
    n = int((2 * num) ** 0.5)
    return num == int(0.5 * n * (n + 1))


def is_pentagonal(num):
    n = (1 + (24 * num + 1) ** 0.5) / 6
    return n.is_integer()


def get_hexagonal(n):
    return n * (2 * n - 1)


for n in range(999_999):
    num = get_hexagonal(n)

    if is_pentagonal(num) and is_triangular(num):
        print(num)
