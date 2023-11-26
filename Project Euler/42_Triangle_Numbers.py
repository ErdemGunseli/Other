
def word_val(word):
    return sum([ord(c) - 64 for c in word])


def is_triangular(num):
    n = int((2 * num)**0.5)
    return num == int(0.5 * n * (n + 1))


with open("Problem_Files/42_words.txt") as w:
    words = w.read()
    words_list = [name.strip().replace('"', '') for name in words.split(',')]
    words_list.sort()

count = 0
for word in words_list:
    if is_triangular(word_val(word)): count += 1
print(count)

