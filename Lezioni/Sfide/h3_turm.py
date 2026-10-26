# HERAUSFORDERUNG 3 — Der Turm
# Eine Schleife baut Stockwerk auf Stockwerk.
# if / else gibt jedem zweiten eine andere Farbe.
from turtle import *

kante = 100
versatz = 38
stockwerke = 4      # <-- probier 2, 4, 6
start_x = -140
start_y = -200

speed(0)
pensize(3)

for stock in range(stockwerke):

    if stock % 2 == 0:
        color("darkblue")
    else:
        color("firebrick")

    x = start_x
    y = start_y + stock * kante

    # vorne
    penup()
    goto(x, y)
    pendown()
    setheading(0)
    for i in range(4):
        forward(kante)
        left(90)

    # hinten
    penup()
    goto(x + versatz, y + versatz)
    pendown()
    setheading(0)
    for i in range(4):
        forward(kante)
        left(90)

    # die Tiefenkanten
    for ecke in [(x, y), (x + kante, y),
                 (x + kante, y + kante), (x, y + kante)]:
        penup()
        goto(ecke)
        pendown()
        goto(ecke[0] + versatz, ecke[1] + versatz)

done()
