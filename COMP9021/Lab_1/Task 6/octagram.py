from turtle import *
from math import cos

size = 100
dist = 180
vertices = []
tri_top = []



def gen_poly():
    penup()
    # radius is the distance from vertices of the n-polygon to centre
    radius = size # in this way the result shape fits with your example
    # radius = size / cos(pi / n) # in this way, it fits with your description, but the triangles are slightly "shorter"
    speed(0)    # turtle is hidden during background generation of vertices
    ang = 90
    for i in range(n):
        home()
        setheading(ang)
        forward(radius)
        vertices.append(pos())
        ang -= 360 / n  # offset angle 360 / n across each edge


def set_tri_top():
    speed(0)
    penup()
    ang = 90 - 180 / n
    for i in range(n):
        home()
        setheading(ang)
        forward(dist)
        tri_top.append(pos())
        ang -= 360 / n  # offset angle 360 / n across each edge


def draw():
    speed(2)    # normal speed to display the drawing process
    color("yellow")
    goto(vertices[0])
    pendown()
    begin_fill()
    for i in range(1, n):
        goto(vertices[i])
    end_fill()
    penup()
    for i in range(n):
        if i % 2 == 1:
            color("red")
        else:
            color("blue")
        goto(vertices[i])
        begin_fill()
        pendown()
        j = i + 1   # i+1 will cause an array overflow, use j instead
        if j == n:
            j = 0
        goto(vertices[j])
        goto(tri_top[i])
        end_fill()
        penup()


# main program
n = 8   # Number of polygon edges
gen_poly()
set_tri_top()
draw()
hideturtle()
done()  # the graph will not disappear when drawing complete