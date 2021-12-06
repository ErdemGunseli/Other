def calc (n):
	if n > 0:
		n = n + calc (n - 1)
	return n

print(calc(5))