import sys
from math import log10


def text_month(jandays, month):
    text = []
    jandays += sum(days_m[:month])
    weekday = jandays % 7
    text.append("Mo Tu We Th Fr Sa Su")
    st = str()
    for i in range(weekday):
        st += "   "
    for i in range(1, days_m[month] + 1):
        if i < 10:
            st += ' '
        st += str(i)
        if (i + weekday) % 7 != 0:
            st += ' '
        else:
            text.append(st)
            st = str()
    text.append(st)
    return text


month_num = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10,
             "nov": 11, "dec": 12}
month_name = "January, February, March, April, May, June, July, August, September, October, November, December".split(
    ',')
days_m = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
print("I will display a calendar, either for a year or for a month in a year.")
print("The earliest year should be 1753.")
print("For the month, input at least the first three letters of the month’s name.")
s = input("Input year, or year and month, or month and year: ")
s = s.split(' ')
if len(s) > 2:
    print("Invalid input, giving up...")
    sys.exit()
if len(s) == 2 and not s[0].isdigit() and not s[1].isdigit():
    print("Invalid input, giving up...")
    sys.exit()
first_year = 1753  # 1/1/1753 was a Monday

if len(s) == 2 and s[1].isdigit() and not s[0].isdigit():
    s[0], s[1] = s[1], s[0]
try:
    year = int(s[0])
except ValueError:
    print("Invalid input, giving up...")
    sys.exit()
if year < first_year:
    print("Invalid input, giving up...")
    sys.exit()
days = 365 * (year - first_year)
if year - first_year >= 3:
    days += (year - first_year + 1) // 4
if year >= 1800:
    days -= (year - first_year - 47) // 100
if year >= 2000:
    days += (year - 2000) // 400

if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    days_m[1] = 29

text = []

if len(s) == 2:
    month = s[1][:3].lower()
    if month not in month_num:
        print("Invalid input, giving up...")
        sys.exit()
    month = month_num[month] - 1
    s = ' ' * ((20 - len(month_name[month]) - 2 - int(log10(year))) // 2)
    s += f"{month_name[month]} {year}"
    text.append(s)
    text1 = text_month(days, month)
    for line in text1:
        text.append(line)


elif len(s) == 1:
    text.append(' ' * 30 + str(year) + '\n')
    month = 0
    monthtext = []
    while month < 12:
        st = ' ' * ((20 - len(month_name[month])) // 2) + month_name[month] + ' ' * (20 - len(month_name[month]) - (
            (20 - len(month_name[month])) // 2))
        tex = [st]
        text1 = text_month(days, month)
        for i in range(len(text1)):
            if i == len(text1) - 1:
                spaces = ' ' * (20 - len(text1[i]))
                t = text1[i] + spaces
                tex.append(t)
            else:
                tex.append(text1[i])
        monthtext.append(tex)
        if month % 3 == 2:
            for r in range(8):
                row = str()
                for i in range(3):
                    if len(monthtext[i]) > r:
                        row += monthtext[i][r]
                    else:
                        row += (' ' * 20)
                    if i < 3:
                        row += '  '
                text.append(row)
            monthtext.clear()
        month += 1
else:
    print("Invalid input, giving up...")
    sys.exit()

##
for line in text:
    print(line)
