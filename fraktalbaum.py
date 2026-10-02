# ============================================================
#  FRAKTALBAUM
#  Ein Ast teilt sich in zwei kleinere Äste. Jeder davon teilt
#  sich wieder in zwei kleinere Äste. Und so weiter.
#
#  Das Programm benutzt dafür eine Funktion, die sich selbst
#  aufruft. Das nennt man Rekursion.
# ============================================================

from turtle import *
from random import randint

# ====== EINSTELLUNGEN – probier verschiedene Zahlen aus ======
TIEFE = 9           # wie oft sich die Äste teilen (mehr als 11 dauert lange!)
STAMM = 150         # Länge des Stamms
WINKEL = 25         # wie weit die Äste auseinander gehen
SCHRUMPFEN = 0.72   # jeder neue Ast ist so viel mal so lang wie der alte
ZUFALL = 0          # 0 = ordentlicher Baum, 10 = etwas wild, 25 = sehr wild
# =============================================================


def ast(laenge, tiefe):
    if tiefe == 0:
        return                           # ganz außen: nichts mehr zeichnen

    # Dicke und Farbe: unten dicker Stamm, oben grüne Blätter
    pensize(tiefe)
    if tiefe <= 2:
        color("forestgreen")
    else:
        color("saddlebrown")

    forward(laenge)

    links_winkel = WINKEL + randint(-ZUFALL, ZUFALL)
    rechts_winkel = WINKEL + randint(-ZUFALL, ZUFALL)

    left(links_winkel)
    ast(laenge * SCHRUMPFEN, tiefe - 1)  # der linke Ast ist wieder ein kleiner Baum
    right(links_winkel + rechts_winkel)
    ast(laenge * SCHRUMPFEN, tiefe - 1)  # der rechte Ast auch
    left(rechts_winkel)

    penup()
    backward(laenge)                     # zurück zum Anfang dieses Astes
    pendown()


setup(800, 700)
title("Fraktalbaum")
bgcolor("lightcyan")
hideturtle()
speed(0)
delay(1)             # Pause pro Strich in Millisekunden: 0 = sofort fertig, 5 = sehr langsam

penup()
goto(0, -300)
setheading(90)       # nach oben schauen
pendown()

ast(STAMM, TIEFE)

update()
done()
