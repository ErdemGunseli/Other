def is_palindrome(string):
    length = len(string)
    midpoint = length // 2
    return string[:midpoint] == string[length - midpoint:][::-1]


def binary(decimal):
    if decimal == 0: return 0

    result = []

    while 0 < decimal:
        result.append(str(decimal % 2))
        decimal = decimal // 2

    return "".join(result[::-1])


palindromes = []
# Palindromes must end in 1 since leading zeros don't count, so only need to check odd numbers:
for number in range(1, 1_000_000, 2):
    if is_palindrome(str(number)) and is_palindrome(binary(number)):
        palindromes.append(number)

print(sum(palindromes))
