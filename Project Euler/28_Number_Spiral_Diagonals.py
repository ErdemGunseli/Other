"""
Each of the following is done 4 times:
+2, +4, +6, ...

We have 2n - 1 diagonal numbers in an n x n grid.
"""

sum_of_diagonals = 1
current_term = 1

for step in range(2000):
    current_term += (2 + 2 * (step // 4))
    sum_of_diagonals += current_term

print(sum_of_diagonals)
