a = 1
b = 1
total = 0

while b < 4_000_000:
    if b % 2 == 0: total += b
    a, b = b, a + b
print(total)


