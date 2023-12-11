
import math

n_product = 1
d_product = 1

for n in range(10, 100):
    for d in range(n + 1, 100):
        value = n / d

        n_digits = list(str(n))
        d_digits = list(str(d))
        repeated_digit = [x for x in n_digits if x in d_digits and x != '0']

        if repeated_digit:
            n_digits.remove(repeated_digit[0])
            d_digits.remove(repeated_digit[0])

            if int(d_digits[0]) != 0 and int(n_digits[0]) / int(d_digits[0]) == value:
                n_product *= n
                d_product *= d

gcd = math.gcd(n_product, d_product)
print(f"{n_product//gcd}/{d_product//gcd}")
