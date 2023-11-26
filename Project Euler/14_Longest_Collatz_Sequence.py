def next_collatz(n):
    if n == 1:
        return None
    elif n % 2 == 0:
        return n // 2
    return 3 * n + 1


def collatz_length(n, collatz_lengths):
    length = 1
    sequence = []
    done = False
    while next_collatz(n) is not None and not done:
        # Adding the term to the sequence:
        sequence.append(n)

        # If we already computed the length for this sequence, we can stop:
        if collatz_lengths.get(n) is not None:
            length += collatz_lengths.get(n)
            done = True

        # Getting the next term:
        n = next_collatz(n)
        length += 1

    # Updating the dictionary with the new lengths:
    for index, number in enumerate(sequence):
        collatz_lengths[number] = length - index

    return length


# A dictionary of numbers and the length of the resulting sequence:
lengths = {1: 1}

num = 2
max_length = 1
# The number that produced the maximum length sequence:
max_length_num = 1

while num < 1_000_000:
    current_length = collatz_length(num, lengths)

    if max_length < current_length:
        max_length_num = num
        max_length = current_length

    num += 1

print(max_length_num)
