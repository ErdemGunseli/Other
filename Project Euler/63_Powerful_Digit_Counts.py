
values = []
for num in range(1, 100_000):
    for n in range(1, 100):
        if len(str(num ** n)) == n: values.append(num)
print(len(values))
