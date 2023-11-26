def move(discs, start, end):
    # Obtaining the disc to be moved:
    disc = discs[start][-1]

    # Deleting the disc from its starting position:
    del discs[start][-1]

    # Adding the disc to the target peg:
    discs[end].append(disc)
    print(discs)


def transfer(disc_count, discs=None, start=0, target=2, temp=1):
    # Creating a 2D array, representing the discs within the pegs:
    # [[n, ..., 3, 2, 1] [] []]
    if discs is None:
        discs = [[], [], []]
        discs[start] = list(range(disc_count, 0, -1))

    # If there is 1 disc, the problem is trivial, and we just move the disc to the target:
    if disc_count == 1:
        move(discs, start, target)
    else:
        # 1) Transferring n−1 discs from start to temp:
        transfer(disc_count - 1, discs, start=start, target=temp, temp=target)

        # 2) Moving the largest disc from start to target:
        move(discs, start, target)

        # 3) Transferring n−1 discs from temp to target:
        transfer(disc_count - 1, discs, start=temp, target=target, temp=start)


if __name__ == "__main__":
    transfer(25)
