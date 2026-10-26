# HERAUSFORDERUNG 2 — Das Haus im Schrägbild
# versatz: gleich viel nach rechts wie nach oben. Das ist der 45-Grad-Trick.
from turtle import *

speed(0)
pensize(3)

breite = 160
hoehe = 140
dach = 80
versatz = 56       # <-- probier 30, 56, 90
start_x = -170
start_y = -150

def nach(x, y):
    penup()
    goto(x, y)
    pendown()
    setheading(0)

def tief(x, y):
    """die Tiefenkante: gleich viel nach rechts wie nach oben"""
    nach(x, y)
    goto(x + versatz, y + versatz)

color("firebrick")

# die vordere Wand
nach(start_x, start_y)
forward(breite)
left(90)
forward(hoehe)
left(90)
forward(breite)
left(90)
forward(hoehe)
left(90)

# die hintere Wand, verschoben
nach(start_x + versatz, start_y + versatz)
forward(breite)
left(90)
forward(hoehe)
left(90)
forward(breite)
left(90)
forward(hoehe)
left(90)

# die vier Tiefenkanten
tief(start_x, start_y)
tief(start_x + breite, start_y)
tief(start_x + breite, start_y + hoehe)
tief(start_x, start_y + hoehe)

color("sienna")

# das vordere Dach
nach(start_x, start_y + hoehe)
goto(start_x + breite / 2, start_y + hoehe + dach)
goto(start_x + breite, start_y + hoehe)

# das hintere Dach
nach(start_x + versatz, start_y + hoehe + versatz)
goto(start_x + breite / 2 + versatz, start_y + hoehe + dach + versatz)
goto(start_x + breite + versatz, start_y + hoehe + versatz)

# der Dachfirst
tief(start_x + breite / 2, start_y + hoehe + dach)

done()
