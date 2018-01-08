import turtle
from math import sin, cos, pi
from os import remove
import subprocess

#
cyc_type = ""


#


def gcd(a, b):
    if a == b:
        return a
    if a < b:
        a, b = b, a
    while b > 0:
        a, b = b, a % b
    return a


def coord(ang):
    if cyc_type == 'h':
        x = (R - r) * cos(ang) + d * cos((R - r) / r * ang)
        y = (R - r) * sin(ang) - d * sin((R - r) / r * ang)
    elif cyc_type == 'e':
        x = (R + r) * cos(ang) - d * cos((R + r) / r * ang)
        y = (R + r) * sin(ang) - d * sin((R + r) / r * ang)
    else:
        return 0, 0
    return x, y


def sav():
    ts = turtle.getscreen().getcanvas().postscript(file="cyc.ps", colormode='color')
    if cyc_type == 'h':
        name = f"Hypotrochoid_{R:.0f}_{r:.0f}_{d:.0f}.pdf"
    else:
        name = f"Epitrochoid{R:.0f}_{r:.0f}_{d:.0f}.pdf"
    proc=subprocess.Popen(["ps2pdf", "cyc.ps", name], shell=True)
    proc.wait()
    '''img = Image.open("cyc.eps")
    img.save(name, "PDF")
    img.close()'''
    remove("cyc.ps")


t = turtle.Turtle()
wind = turtle.Screen()
dim = 300
wind.screensize(dim, dim)
while cyc_type != 'e' and cyc_type != 'h':
    cyc_type = wind.textinput("Hypotrochoid or epitrochoid?", "Input H for Hypotrochoid, E for epitrochoid: ")
    cyc_type = cyc_type[0].lower()
R = 0
r = 0
d = -1
while R < 10 or R > 290:
    R = wind.numinput("Fixed circle", "Radius R between 10 and 290: ", minval=10, maxval=290)
while r < 10 or r > 250:
    r = wind.numinput("Rolling circle", "Radius r between 10 and 250: ", minval=10, maxval=250)
while d < 0 or d > 218:
    d = wind.numinput("Point", "Distance to centre of rolling circle between 0 and 218: ", minval=0, maxval=218)
period = r / gcd(R, r)
if cyc_type == 'h':
    name = "Hypotrochoid"
else:
    name = "Epitrochoid"
wind.title(name + " for R= " + str(R) + ", r= " + str(r) + ", d= " + str(d) + " -- Period = " + str(period))
period = period * 2 * pi
ang = 0
t.pencolor("black")
if cyc_type == 'h':
    t.fillcolor("#33cc8c")
else:
    t.fillcolor("#00FF00")
t.speed(0)
t.hideturtle()
t.penup()
x, y = coord(0)
t.goto(x, y)
t.pendown()
t.begin_fill()
while ang <= period:
    x, y = coord(ang)
    t.goto(x, y)
    ang += 0.01
t.penup()
t.end_fill()
turtle.onkey(sav, 'S')
turtle.onkey(sav, 's')
turtle.listen()

# end
turtle.done()
