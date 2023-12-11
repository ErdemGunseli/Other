
from fractions import Fraction


def next_term(last_term=None):
    if last_term is None: return Fraction(3, 2)
    return 1 + Fraction(1, 1 + last_term)


term = None
index = 0
count = 0
while index < 1001:
    term = next_term(term)

    if len(str(term.numerator)) > len(str(term.denominator)): count += 1
    index += 1

print(count)

