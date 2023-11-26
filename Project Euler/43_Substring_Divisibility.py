
def get_permutations(values):
    if not values: return [[]]

    result = []

    for value in values:
        values_copy = values.copy()
        values_copy.remove(value)
        current_permutation = get_permutations(values_copy)

        for permutation in current_permutation:
            result.append([value] + permutation)

    return result


def is_valid(p):
    # 0 cannot be the first digit:
    if p[0] == 0: return False

    primes = [2, 3, 5, 7, 11, 13, 17]

    # Concatenation of 3 adjacent digits must be divisible with the current prime:
    for i in range(7):
        if int(str(p[1 + i]) + str(p[2 + i]) + str(p[3 + i])) % primes[i] != 0:
            return False
    return True


permutations = get_permutations(list(range(10)))
valid_permutations = [int(''.join(map(str, p))) for p in permutations if is_valid(p)]
print(sum(valid_permutations))
