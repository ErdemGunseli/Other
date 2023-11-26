def sum_of_squares(n):
    return sum([num ** 2 for num in range(1, n + 1)])


def square_of_sum(n):
    return (n * (n + 1) // 2) ** 2


print(sum_of_squares(100) - square_of_sum(100))
