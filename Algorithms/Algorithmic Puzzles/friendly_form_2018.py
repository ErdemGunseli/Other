# For 0 < q < 1, express q as a finite sum of reciprocals fof distinct positive integers.
def friendly(q):
    # This list will be used to output the number in friendly form:
    m_values = []

    # Starting from 2 since 0 < q < 1:
    m = 2

    # Using a small threshold to handle floating-point precision:
    while 1e-10 < q:

        # Finding the smallest natural m for which 1/m <= q:
        # This means that q - 1/m is another rational number:
        if 1 / m <= q:

            # Setting q to its new value:
            q -= 1 / m
            m_values.append(m)

            # Setting m back to 2:
            m = 2
        else:
            # Incrementing m until it meets the condition:
            m += 1

    return " + ".join([f"1/{m}" for m in m_values])


if __name__ == "__main__":
    for i in range(2, 10):
        for j in range(i, 10):
            if i != j: print(f"{i}/{j} = {friendly(i / j)}")
