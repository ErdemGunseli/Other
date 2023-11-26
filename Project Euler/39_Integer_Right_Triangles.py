
max_solutions = 0
max_solutions_p = 0
for p in range(12, 1_000):
    solutions = 0

    # a is the smallest side, so p//3 max:
    for a in range(1, p//3):

        # b is the second-smallest side:
        for b in range(a, (p - a)//2 + 1):

            # If the calculated value of c is equal to the required value
            # due to the perimeter value, we have found another solution:
            if a**2 + b**2 == (p - a - b)**2:
                solutions += 1

    if max_solutions < solutions:
        max_solutions = solutions
        max_solutions_p = p

print(f"p={max_solutions_p} gives {max_solutions}")
