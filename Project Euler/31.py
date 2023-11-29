
def arrangements(value, memory):
    if value == 0: return 1
    elif value < 0: return 0
    elif value in memory: return memory[value]
    else:
        result = sum([arrangements(value - coin, memory) for coin in coins])
        memory[value] = result
        return result


coins = [1, 2, 5, 10, 20, 50, 100, 200]
print(arrangements(200, {}))
