import math


def is_prime(n):
    if n < 2: return False

    for i in range(2, math.ceil(math.sqrt(n)) + 1):
        if n % i == 0: return False
    return True


longest_prime_sequence = 0
product = 0

for a in range(-999, 1000):
    # abs(b) has to be prime since when n=0, expression simplifies to b:
    for b in [num for num in range(-1000, 1001) if is_prime(abs(num))]:

        done = False
        current_sequence_length = 0

        while not done:
            result = (current_sequence_length ** 2) + a * current_sequence_length + b
            if is_prime(result): current_sequence_length += 1
            else: done = True

        if longest_prime_sequence < current_sequence_length:
            longest_prime_sequence = current_sequence_length
            product = a * b

print(product)
