# HERAUSFORDERUNG 7 — Das Schachbrett
# Eine Schleife IN einer Schleife. if / else entscheidet die Farbe.
from turtle import *

felder = 8
feld = 50
start_x = -200
start_y = -200

speed(0)
hideturtle()
pensize(1)
color("black")

for zeile in range(felder):
    for spalte in range(felder):

        if (zeile + spalte) % 2 == 0:
            fillcolor("white")
        else:
            fillcolor("black")

        penup()
        goto(start_x + spalte * feld, start_y + zeile * feld)
        pendown()
        setheading(0)
        begin_fill()
        for i in range(4):
            forward(feld)
            left(90)
        end_fill()

done()
