
def are_permutations(list):
    signatures = [get_signature(val) for val in list]
    return all([signature == signatures[0] for signature in signatures])


def get_signature(val):
    return "".join(sorted(str(val)))


found = False
x = 0
while not found:
    x += 1
    if are_permutations([x * val for val in range(1, 7)]): found = True

print(x)
