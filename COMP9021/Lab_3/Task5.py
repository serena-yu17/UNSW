from random import SystemRandom

from pygal import Bar
from pygal.style import Style
from webbrowser import open_new_tab
from os import path

#
# IO
dice = [6]
string = input("Enter N strictly positive integers (number of sides of N dice): ")
if string == "":
    print("You did not enter any value, a single standard six-sided die will be rolled.")
else:
    dice.clear()
    i = 0
    six = 0
    while i < len(string):
        start = i
        flag = 1
        while i < len(string) and string[start] == ' ':
            start += 1
            i += 1
        while i < len(string) and string[i] != ' ':
            if not string[i].isdigit():
                flag = 0
            i += 1
        if flag == 0:
            six = 1
            dice.append(6)
        else:
            if start < i:
                num = int(string[start: i])
                if num <= 0:
                    six = 1
                    num = 6
                dice.append(num)
    if six == 1:
        print("Some of the values, incorrect, have been replaced with the default value of 6.")
n = 1000
string = input("Enter the desired number of rolls: ")
if string == "":
    print("Input was not provided or invalid, so the default value of 1,000 will be used.")
else:
    try:
        n = int(string)
    except ValueError:
        print("Input was not provided or invalid, so the default value of 1,000 will be used.")
    if n <= 0:
        print("Input was not provided or invalid, so the default value of 1,000 will be used.")
        n = 1000
#
#
lb = len(dice)
ub = sum(dice)
count = [0] * (ub + 1)
rand = SystemRandom()
for i in range(n):
    sm = 0
    for sn in dice:
        if sn == 1:
            sm = 1
        else:
            sm += rand.randint(1, sn)
    count[sm] += 1
#
# Graph preparation
xlab = []
items = []
begin = lb
end = ub
while count[begin] == 0:
    begin += 1
while count[end] == 0:
    end -= 1
for i in range(begin, end):
    xlab.append(i)
    dic = {"value": count[i],
           "label": f"Frequency: {count[i] / n:.2f}"}
    items.append(dic)
#
# Render
barch = Bar()
barch.title = f"Simulation for {n} rolls of the dice: {dice}"
barch.x_labels = xlab
barch.x_title = "Possible sums"
barch.y_title = "Counts"
barch.show_legend = False
barch.force_uri_protocol = "http"
barch.add('', items)
barch.style = Style(colors=("#228B22",),
                    label_font_size=12)
barch.render()
barch.render_to_file("dice_rolls.svg")
#
# Open browser window
open_new_tab("file://" + path.realpath("dice_rolls.svg"))
