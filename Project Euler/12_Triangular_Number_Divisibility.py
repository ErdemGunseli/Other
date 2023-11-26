def get_triangular_number(n):
    return (n + 1) * n // 2


n = 3
factor_count = 0
triangular_number = 0
while factor_count < 500:

    # 1 and the number itself are factors:
    factor_count = 2
    triangular_number = get_triangular_number(n)

    for num in range(2, int(triangular_number ** 0.5)):
        if triangular_number % num == 0: factor_count += 2

    n += 1

print(triangular_number)
