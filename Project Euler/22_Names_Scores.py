total_name_scores = 0
with open("Problem_Files/22_names.txt", 'r') as n:
    names = n.read()
    names_list = [name.strip().replace('"', '') for name in names.split(',')]
    names_list.sort()

    for index, name in enumerate(names_list):
        # All characters are capital, and 'A' has unicode value of 65:
        total_name_scores += (index + 1) * sum([ord(c) - 64 for c in name])

print(total_name_scores)
