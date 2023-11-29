
def phis(limit):
    result = list(range(limit + 1))

    for i in range(2, limit + 1):

        # If result[i] == i, the number has not been marked by any smaller prime factors,
        # so i must be a prime number.
        if result[i] == i:

            # The phi of the number n is n * (1 - 1/p) for each prime factor of n:
            for j in range(i, limit + 1, i):
                result[j] = result[j] * (i - 1) // i

    return result


phi_values = phis(1_000_000)

maximum = 0
n_maximum = 0
for n in range(2, len(phi_values)):

    current = n / phi_values[n]

    if maximum < current:
        maximum = current
        n_maximum = n

print(f"Maximum result is {maximum}, occurring when n={n_maximum}")
