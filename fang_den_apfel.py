# ============================================================
#  FANG DEN APFEL
#
#  Pfeiltasten = laufen. Fang so viele Äpfel wie möglich!
#  WICHTIG: Klick einmal ins Fenster, damit die Tasten gehen.
# ============================================================

from turtle import *
from random import randint

# ============================================================
#  HIER WIRD ALLES EINGESTELLT
# ============================================================

spielzeit = 30                     # <-- so viele Sekunden dauert das Spiel
schritt = 20                       # <-- so weit läuft die Schildkröte pro Tastendruck
treffer_abstand = 25               # <-- wie nah du am Apfel sein musst (kleiner = schwerer)
wand = 240                         # <-- wie weit die Schildkröte vom Start laufen darf
feld = 210                         # <-- wie weit weg vom Start ein Apfel erscheinen kann
farbe_spieler = "green"            # <-- Farbe der Schildkröte
farbe_apfel = "red"                # <-- Farbe des Apfels
farbe_wand = "saddlebrown"         # <-- Farbe der Wand
farbe_hintergrund = "lightyellow"  # <-- Farbe vom Hintergrund

# ============================================================

# --- Fenster ---
setup(600, 600)
title("Fang den Apfel")
bgcolor(farbe_hintergrund)

# --- Die Wand: ein Quadrat um das Spielfeld ---
rahmen = Turtle()
rahmen.speed(0)
rahmen.hideturtle()
rahmen.color(farbe_wand)
rahmen.pensize(6)
rahmen.penup()
rahmen.goto(-wand, -wand)
rahmen.pendown()
for seite in range(4):
    rahmen.forward(2 * wand)
    rahmen.left(90)

# --- Die Schildkröte ---
spieler = Turtle()
spieler.speed(0)
spieler.shape("turtle")
spieler.color(farbe_spieler)
spieler.penup()

# --- Der Apfel: erscheint an einem zufälligen Ort ---
apfel = Turtle()
apfel.speed(0)
apfel.shape("circle")
apfel.color(farbe_apfel)
apfel.penup()
apfel.goto(randint(-feld, feld), randint(-feld, feld))

# --- Der Schreiber: zeigt Punkte und Zeit ---
schreiber = Turtle()
schreiber.speed(0)
schreiber.hideturtle()
schreiber.penup()

punkte = 0
zeit = spielzeit


def anzeigen():
    # Alten Text löschen und neu schreiben.
    schreiber.clear()
    schreiber.goto(-280, 255)
    schreiber.write("Punkte: " + str(punkte) + "   Zeit: " + str(zeit),
                    font=("Arial", 16, "bold"))


def begrenzen():
    # Die Schildkröte ist etwa 30 breit. Darum bleibt sie 15 vor
    # der Wand stehen, sonst ragt sie über die Wand hinaus.
    grenze = wand - 15
    if spieler.xcor() > grenze:
        spieler.setx(grenze)
    if spieler.xcor() < -grenze:
        spieler.setx(-grenze)
    if spieler.ycor() > grenze:
        spieler.sety(grenze)
    if spieler.ycor() < -grenze:
        spieler.sety(-grenze)


def pruefen():
    # Nah genug am Apfel? Dann ein Punkt und der Apfel springt woandershin.
    global punkte
    if spieler.distance(apfel) < treffer_abstand:
        punkte = punkte + 1
        apfel.goto(randint(-feld, feld), randint(-feld, feld))
        anzeigen()


def laufen(richtung):
    # Erst in die Richtung drehen, dann einen Schritt machen.
    spieler.setheading(richtung)
    spieler.forward(schritt)
    begrenzen()
    pruefen()


def hoch():
    laufen(90)


def runter():
    laufen(270)


def links():
    laufen(180)


def rechts():
    laufen(0)


def spiel_ende():
    # Tasten ausschalten und das Ergebnis zeigen.
    for taste in ["Up", "Down", "Left", "Right"]:
        onkeypress(None, taste)
    schreiber.goto(0, 0)
    schreiber.write("Zeit ist um! " + str(punkte) + " Punkte", align="center",
                    font=("Arial", 28, "bold"))


def tick():
    # Wird jede Sekunde aufgerufen: Zeit runterzählen.
    global zeit
    zeit = zeit - 1
    anzeigen()
    if zeit > 0:
        ontimer(tick, 1000)
    else:
        spiel_ende()


# --- Tasten und Start ---
onkeypress(hoch, "Up")
onkeypress(runter, "Down")
onkeypress(links, "Left")
onkeypress(rechts, "Right")

anzeigen()
ontimer(tick, 1000)
listen()
done()

# ============================================================
#  MISSIONEN FÜR DICH
#  1. Mach das Spiel schwer: kleine Zahl bei treffer_abstand.
#  2. Mach es schnell: spielzeit = 10 und schritt = 40.
#  3. Mach das Feld klein: wand = 100 und feld = 80.
# ============================================================