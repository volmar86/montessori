# HERAUSFORDERUNG 5 — Das Vieleck im Kreis
# Das Vieleck soll genau IM Kreis sitzen: jede Ecke berührt die Kreislinie.
from turtle import *

radius = 200
ecken = 6          # <-- probier 3, 5, 8, 12

speed(0)
hideturtle()
pensize(2)

# der Kreis (grau)
color("gray")
penup()
goto(radius, 0)
pendown()
setheading(90)
circle(radius)

# das Vieleck (rot) — die DRITTE Zahl sagt, wie viele Ecken
color("firebrick")
penup()
goto(radius, 0)
pendown()
setheading(90)
circle(radius, 360, ecken)

done()
