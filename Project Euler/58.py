
def is_prime(num):
    for i in range(1, int(num**0.5) + 1):
        if num % i == 0: return False
    return True
