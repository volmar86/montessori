# HERAUSFORDERUNG 9 — Der Pythagoras-Jäger
# Teil 1: alle rechtwinkligen Dreiecke mit ganzen Zahlen suchen.
# Teil 2: eines davon zeichnen und von Python nachmessen lassen.
from turtle import *

bis = 30

print("a    b    c")
for a in range(1, bis + 1):
    for b in range(a, bis + 1):
        for c in range(b, 2 * bis):
            if a * a + b * b == c * c:
                print(a, " ", b, " ", c)

# --- jetzt eines davon zeichnen ---

a = 9
b = 12
faktor = 20

start_x = -100
start_y = -120

speed(0)
pensize(3)
penup()
goto(start_x, start_y)
pendown()
setheading(0)

color("firebrick")
forward(a * faktor)     # die liegende Kathete
left(90)                # der rechte Winkel
forward(b * faktor)     # die stehende Kathete

print("gemessene Hypotenuse:", distance(start_x, start_y))

color("steelblue")
goto(start_x, start_y)  # die Hypotenuse

done()
