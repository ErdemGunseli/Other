
max_sum = 0
for a in range(1, 100):
    for b in range(1, 100):
        current_sum = sum([int(digit) for digit in str(a**b)])

        if max_sum < current_sum: max_sum = current_sum
print(max_sum)
