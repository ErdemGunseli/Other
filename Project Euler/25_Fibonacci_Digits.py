
a = b = 1
index = 2
while len(str(b)) < 1000:
    a, b = b, b + a
    index += 1
print(index)
