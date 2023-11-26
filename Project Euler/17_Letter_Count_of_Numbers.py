def get_letter_count(n):
    # A dictionary of the number of letters corresponding to key numbers:
    letter_counts = {1: 3, 2: 3, 3: 5, 4: 4, 5: 4, 6: 3, 7: 5, 8: 5, 9: 4, 10: 3, 11: 6, 12: 6, 13: 8, 14: 8, 15: 7,
                     16: 7, 17: 9, 18: 8, 19: 8, 20: 6, 30: 6, 40: 5, 50: 5, 60: 5, 70: 7, 80: 6, 90: 6, 100: 10,
                     200: 10, 300: 12, 400: 11, 500: 11, 600: 10, 700: 12, 800: 12, 900: 11, 1000: 11}
    keys = list(letter_counts.keys())

    letter_count = 0
    # Adding 3 to the letter count if the number is not divisible by 100, since there will be 'and':
    if n > 100 and n % 100 != 0: letter_count += 3

    index = len(keys) - 1
    while 0 < n:
        num = keys[index]
        current_num_letter_count = letter_counts[num]

        if num <= n:
            letter_count += current_num_letter_count
            n -= num
        elif index > 0:
            index -= 1
        else:
            index = len(keys) - 1

    return letter_count


print(sum(get_letter_count(num) for num in range(1, 1001)))
