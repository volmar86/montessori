# ============================================================
#  SCHILDKRÖTENRENNEN
#  Du wettest auf eine Farbe. Dann laufen fünf Schildkröten los,
#  jede macht bei jedem Schritt eine zufällige Anzahl Pixel.
#
#  Neues Rennen: Leertaste
#
#  Fast alles hier kennst du schon: for, if, randint, input.
#  Neu ist: mehrere Schildkröten auf einmal – und das ganze
#  Rennen steckt in einer Funktion, damit man es wiederholen kann.
#
#  WICHTIG: Klick einmal ins Spielfenster, damit die Leertaste
#  funktioniert.
# ============================================================

from turtle import *
from random import randint

# ====== EINSTELLUNGEN – hier darfst du ändern ======
namen = ["rot", "blau", "gruen", "orange", "lila"]
farben = ["red", "blue", "green", "orange", "purple"]
START = -300               # x-Position der Startlinie
ZIEL = 300                 # x-Position der Ziellinie
GROESSTER_SCHRITT = 10     # so weit kann eine Schildkröte pro Runde höchstens laufen
# ===================================================

setup(760, 440)
title("Schildkrötenrennen")
bgcolor("lightyellow")
speed(0)
hideturtle()

# --- Rennbahn zeichnen (nur einmal) ---
penup()
for zeile in range(len(namen) + 1):
    y = 100 - zeile * 50 + 25
    goto(START, y)
    pendown()
    forward(ZIEL - START)
    penup()

# Start- und Ziellinie
pensize(4)
goto(START, 150)
pendown()
goto(START, -150)
penup()
color("red")
goto(ZIEL, 150)
pendown()
goto(ZIEL, -150)
penup()
color("black")
goto(ZIEL, 160)
write("ZIEL", align="center", font=("Arial", 14, "bold"))

# Ein eigener Stift nur für Text: den kann man löschen,
# ohne dass die Rennbahn verschwindet
schreiber = Turtle()
schreiber.hideturtle()
schreiber.penup()

# --- Schildkröten bauen (nur einmal) ---
laeufer = []
for nummer in range(len(namen)):
    t = Turtle()
    t.shape("turtle")
    t.color(farben[nummer])
    t.penup()
    laeufer.append(t)

laeuft = False             # damit die Leertaste nicht mitten im Rennen stört


def rennen():
    global laeuft
    if laeuft:
        return
    laeuft = True

    # --- Alles auf Anfang ---
    schreiber.clear()
    for nummer in range(len(laeufer)):
        t = laeufer[nummer]
        t.speed(0)                        # ohne Animation zurück an den Start
        t.shapesize(1.5)
        t.goto(START, 100 - nummer * 50)
        t.speed("normal")                 # im Rennen wieder normal laufen

    # --- Wette ---
    wette = textinput("Deine Wette", "Auf welche Farbe wettest du?\n"
                      + ", ".join(namen))
    if wette is None:
        wette = ""
    wette = wette.strip().lower().replace("ü", "ue")

    if wette not in namen:
        schreiber.color("black")
        schreiber.goto(0, -190)
        schreiber.write("Diese Farbe läuft nicht mit. Das Rennen startet trotzdem!",
                        align="center", font=("Arial", 12, "normal"))

    # --- Das Rennen ---
    sieger = None
    while sieger is None:
        for t in laeufer:
            t.forward(randint(1, GROESSTER_SCHRITT))

        # Wer ist über der Ziellinie? Der Weiteste gewinnt.
        for nummer in range(len(laeufer)):
            if laeufer[nummer].xcor() >= ZIEL:
                if sieger is None or laeufer[nummer].xcor() > laeufer[sieger].xcor():
                    sieger = nummer

    # --- Ergebnis ---
    laeufer[sieger].shapesize(2.5)
    schreiber.goto(0, 175)
    schreiber.color(farben[sieger])
    schreiber.write(namen[sieger].upper() + " GEWINNT!", align="center",
                    font=("Arial", 22, "bold"))

    schreiber.goto(0, -190)
    schreiber.color("black")
    if wette == namen[sieger]:
        schreiber.write("Richtig gewettet!", align="center", font=("Arial", 16, "bold"))
    elif wette in namen:
        schreiber.write("Leider verloren. Du hattest auf " + wette + " gewettet.",
                        align="center", font=("Arial", 16, "normal"))

    schreiber.goto(0, -215)
    schreiber.write("Leertaste = neues Rennen", align="center",
                    font=("Arial", 12, "normal"))

    laeuft = False


rennen()                   # das erste Rennen startet sofort
onkey(rennen, "space")     # danach: Leertaste = neues Rennen
listen()
done()
