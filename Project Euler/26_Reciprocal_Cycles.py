
def cycle_length(divisor):
    # A dictionary storing each remainder and the last index at which they were seen:
    remainders = {}
    current_remainder = 1
    index = 0

    while current_remainder not in remainders:
        remainders[current_remainder] = index

        # Simulating how the remainder changes during long division:
        current_remainder = (10 * current_remainder) % divisor
        index += 1

    return index - remainders.get(current_remainder)


max_length = 0
max_length_d = 0
for d in range(2, 1_000):
    length = cycle_length(d)

    if max_length < length:
        max_length = length
        max_length_d = d

print(f"The maximum sequence has length {max_length} and occurs when d={max_length_d}")
