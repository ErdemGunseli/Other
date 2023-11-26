result = []
for num in range(2, 1_000_000):
    if num == sum([int(digit)**5 for digit in str(num)]):
        result.append(num)
print(sum(result))