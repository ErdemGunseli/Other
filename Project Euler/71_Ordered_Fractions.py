

min_difference = float("inf")
min_difference_fraction = ""
current_difference = None

# Iterating through denominators 1-1,000,000:
for d in range(1, 1_000_000):
    # Calculating the greatest fraction with this denominator that is less than 3/7
    n = (d * 3) // 7
    difference = 3 / 7 - n / d

    # The difference will be 0 if our fraction is 3/7
    if 0 < difference < min_difference:
        min_difference = difference
        min_difference_fraction = f"{n}/{d}"

print(f"The fraction is {min_difference_fraction}")

