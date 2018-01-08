import os
import asyncio
from collections import defaultdict

filep = os.path.join(os.path.dirname(os.path.abspath(__file__)), "names", "yob")
s_name = str()
top_names_m = dict()  # year, percentage
top_names_f = dict()


@asyncio.coroutine
def parsefile(i):
    curpath = f"{filep}{i}.txt"
    sumf = 0
    summ = 0
    with open(curpath) as f:
        lines = []
        for text in f.readlines():
            lines.append(text.rstrip('\n').split(','))
        row = 0
        namef = defaultdict(lambda: defaultdict(float))
        namem = defaultdict(lambda: defaultdict(float))
        set_namef = set()
        set_namem = set()
        global top_names_m
        global top_names_f
        while lines[row][1] == 'F':
            count = float(lines[row][2])
            sumf += count
            if not(lines[row][0] not in top_names_f or count / sumf < top_names_f[lines[row][0]][1]):
                namef[lines[row][0]][i] = count
                set_namef.add(lines[row][0])
            row += 1
        while row < len(lines) and lines[row][1] == 'M':
            count = float(lines[row][2])
            summ += count
            if not(lines[row][0] in top_names_m and count / summ > top_names_m[lines[row][0]][1]):
                namem[lines[row][0]][i] = count
                set_namem.add(lines[row][0])
            row += 1
        for name in set_namef:
            percent = namef[name][i] / sumf * 100
            if name not in top_names_f or percent > top_names_f[name][1]:
                top_names_f[name] = (i, percent)
        for name in set_namem:
            percent = namem[name][i] / summ * 100
            if name not in top_names_m or percent > top_names_m[name][1]:
                top_names_m[name] = (i, percent)


@asyncio.coroutine
def inp():
    global s_name
    s_name = input("Enter a first name: ")


loop = asyncio.get_event_loop()
tasks = [inp()]
for i in range(1880, 2014):
    tasks.append(parsefile(i))
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

if s_name not in top_names_f:
    print(f"In all years, {s_name} was never given as a female name.")
else:
    print(
        f"In terms of frequency, {s_name} was the most popular as a female name first in the year {top_names_f[s_name][0]}.")
    print(f"\t It then accounted for {top_names_f[s_name][1]:.2f}% of all female names")
if s_name not in top_names_m:
    print(f"In all years, {s_name} was never given as a male name.")
else:
    print(
        f"In terms of frequency, {s_name} was the most popular as a male name first in the year {top_names_m[s_name][0]}.")
    print(f"\t It then accounted for {top_names_m[s_name][1]:.2f}% of all male names")
