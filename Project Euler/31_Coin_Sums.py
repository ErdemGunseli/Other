

def get_coin_combinations(value):
    # Bottom-up approach, array storing the number of ways to combine coins to get the index:
    coin_combinations = [0] * (value + 1)

    # There is 1 way to make 0p - to have nothing at all:
    coin_combinations[0] = 1

    # A(n) = A(n - a) + A(n - b)...
    # where a, b... are the coin values smaller than or equal to n.

    # We are computing the number of ways to obtain each value using each coin value one by one:
    for coin in coins:
        for i in range(coin, value + 1):
            coin_combinations[i] += coin_combinations[i - coin]

    return coin_combinations[value]


coins = [1, 2, 5, 10, 20, 50, 100, 200]
print(get_coin_combinations(200))
