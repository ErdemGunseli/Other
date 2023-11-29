

def is_pandigital(num, degree=None):
    num_str = str(num)
    if degree is None: degree = len(num_str)

    return all([num_str.count(str(digit)) == 1 for digit in range(1, degree + 1)])


products = set()
for a in range(1, 100):
    for b in range(100, 10000//a):
        c = a * b
        if is_pandigital(str(a) + str(b) + str(c), degree=9):
            products.add(c)

print(sum(products))

