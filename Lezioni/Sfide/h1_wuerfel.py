# HERAUSFORDERUNG 1 — Der Würfel im Schrägbild
# versatz: gleich viel nach rechts wie nach oben. Das sind die 45 Grad.
from turtle import *

kante = 150
versatz = 56        # <-- probier 30, 56, 90
start_x = -160
start_y = -140

speed(0)
pensize(3)
color("darkblue")

# die vordere Fläche
penup()
goto(start_x, start_y)
pendown()
setheading(0)
for i in range(4):
    forward(kante)
    left(90)

# die hintere Fläche, verschoben
penup()
goto(start_x + versatz, start_y + versatz)
pendown()
setheading(0)
for i in range(4):
    forward(kante)
    left(90)

# die vier Tiefenkanten
for ecke in [(start_x, start_y),
             (start_x + kante, start_y),
             (start_x + kante, start_y + kante),
             (start_x, start_y + kante)]:
    penup()
    goto(ecke)
    pendown()
    goto(ecke[0] + versatz, ecke[1] + versatz)

done()
