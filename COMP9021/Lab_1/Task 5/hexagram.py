from turtle import *

unit = 70


def draw_triangle(clr):
    color(clr)
    for i in range(3):
        right(120)
        pendown()
        forward(unit)
        penup()
        forward(unit)
        pendown()
        forward(unit)
        penup()


# move to the top of the star
penup()
setheading(120)
forward(unit)
right(60)
forward(unit)
draw_triangle("red")
# reset direction at the top of the star. Then move to top-right point of the blue star
setheading(300)
forward(unit)
left(60)
forward(unit)
draw_triangle("blue")
hideturtle()
done()
