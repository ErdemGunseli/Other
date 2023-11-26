def is_leap_year(year):
    return (year % 4 == 0) and (year % 100 != 0) or (year % 400 == 0)


# 1 Jan 1901 was a Tuesday:
day_of_week = 2
sunday_count = 0
for year in range(1901, 2001):
    for month in range(1, 13):
        if day_of_week == 7:
            sunday_count += 1

        if month == 2:
            day_of_week += 1 if is_leap_year(year) else 0  # 29 (mod 7) and 28 (mod 7)
        elif month in [4, 6, 9, 11]:
            day_of_week += 2  # 30 (mod 7)
        else:  # The rest of the months
            day_of_week += 3  # 31 (mod 7)

        if day_of_week > 7: day_of_week -= 7

# Print the final count of Sundays

print(sunday_count)
