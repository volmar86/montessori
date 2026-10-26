# HERAUSFORDERUNG 8 — Miss Pi
# Python zeichnet EINE Seite und misst sie selbst nach.
from turtle import *

radius = 200
ecken = 6          # <-- probier 6, 12, 24, 48, 96, 360

speed(0)
hideturtle()
pensize(2)
color("firebrick")

penup()
goto(radius, 0)
setheading(90)

anfang = pos()
pendown()
circle(radius, 360 / ecken, 1)    # genau EINE Seite
seite = distance(anfang)

umfang = seite * ecken
durchmesser = 2 * radius

print("Ecken:", ecken)
print("eine Seite:", seite)
print("Umfang:", umfang)
print("Umfang / Durchmesser:", umfang / durchmesser)

# und jetzt das ganze Vieleck dazu
penup()
goto(radius, 0)
pendown()
setheading(90)
circle(radius, 360, ecken)

done()
