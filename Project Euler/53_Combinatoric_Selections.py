import math

math.comb(5, 3)

total = 0
for r in range(1, 101):
    for n in range(r + 1, 101):
        if 1_000_000 < math.comb(n, r):
            total += 101 - n
            break

print(total)
