
import copy

with open("Problem_Files/67_triangle.txt") as f:
    triangle = [row.split() for row in f.read().split('\n') if row]

    for y in range(len(triangle)):
        for x in range(len(triangle[y])):
            triangle[y][x] = int(triangle[y][x])


# This array will contain the maximum sum that can be obtained when reaching each number from the top:
max_sums = copy.deepcopy(triangle)


x = 0
# The first row should be left as-is so starting from the second row:
y = 1
while y < len(triangle):
    x = 0

    while x < len(triangle[y]):
        # If we are at the start/end of the row, only one value:
        if x == 0:
            max_sums[y][x] += max_sums[y-1][x]
        elif x == len(triangle[y]) - 1:
            max_sums[y][x] += max_sums[y-1][x-1]
        else:
            max_sums[y][x] += max(max_sums[y-1][x-1], max_sums[y-1][x])

        x += 1
    y += 1

# The maximum value at the bottom row gives the maximum value that can be obtained:
print(max(max_sums[-1]))

