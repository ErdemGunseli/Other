def is_palindrome(val):
    string = str(val)
    length = len(string)
    midpoint = length // 2
    return string[:midpoint] == string[length - midpoint:][::-1]


def is_lychrel(num):
    for iteration in range(50):
        num += int(str(num)[::-1])
        if is_palindrome(num): return False
    return True


print(sum([is_lychrel(num) for num in range(10_000)]))
