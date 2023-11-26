
def generate_champernowne(limit):
    sequence = ""
    length = 0
    num = 1

    while length < limit:
        num_str = str(num)
        sequence = sequence + num_str
        length += len(num_str)
        num += 1

    return sequence


d = generate_champernowne(1_000_000)

product = 1
for val in [d[i - 1] for i in [1, 10, 100, 1000, 10_000, 100_000, 1_000_000]]:
    product *= int(val)

print(product)
