def get_combinations(n):
    # Bottom-up approach, array storing the number of ways to numbers to reach the target:
    combinations = [0] * (n + 1)

    # There is 1 way to make 0, which is by having nothing:
    combinations[0] = 1

    for i in range(1, n + 1):
        for j in range(i, n + 1):
            combinations[j] += combinations[j - i]

    return combinations[n]


# Just 100 itself does not count as a partition:
print(get_combinations(100) - 1)
