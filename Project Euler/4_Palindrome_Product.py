def number_is_palindrome(n):
    # Converting the integer to a string to iterate over the digits more easily:
    x_string = str(n)

    # Flag to determine result:
    is_palindrome = True

    # Left and right pointers:
    start = 0
    end = len(x_string) - 1

    while start <= end and is_palindrome:
        if x_string[start] == x_string[end]:
            # Incrementing pointers:
            start += 1
            end -= 1
        else:
            # If characters are not the same, it is not a palindrome:
            is_palindrome = False

    return is_palindrome


maximum = 0
for i in range(100, 1_000):
    for j in range(i, 1_000):
        product = i * j
        if number_is_palindrome(product) and maximum < product:
            maximum = product

print(maximum)
