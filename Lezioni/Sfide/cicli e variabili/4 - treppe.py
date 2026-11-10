# ============================================================
#  TREPPE AUS QUADRATEN
#
#  Stufe 1 hat 1 Quadrat, Stufe 2 hat 2 Quadrate, usw.
#  Der Computer zählt mit, wie viele Quadrate es sind.
# ============================================================

from turtle import *

speed(0)          # 0 = sofort, 1 = langsam zum Zuschauen
pensize(2)

# ============================================================
#  HIER WIRD ALLES EINGESTELLT
# ============================================================

stufen = 6            # <-- wie viele Stufen die Treppe hat
seite = 30            # <-- Kantenlänge eines Quadrats
farbe = "gold"        # <-- Farbe der Quadrate
start_x = -100        # <-- wo die Treppe anfängt: links / rechts
start_y = -120        # <-- wo die Treppe anfängt: unten / oben

# ============================================================

gesamt = 0            # hier zählt der Computer alle Quadrate

color("black", farbe)

# --- Die Treppe: eine Spalte pro Stufe ---
for stufe in range(1, stufen + 1):

    # Stufe 3 hat 3 Quadrate übereinander.
    for reihe in range(stufe):
        penup()
        goto(start_x + (stufe - 1) * seite, start_y + reihe * seite)
        setheading(0)
        pendown()
        begin_fill()
        for kante in range(4):
            forward(seite)
            left(90)
        end_fill()
        gesamt = gesamt + 1

# --- Ergebnis aufschreiben ---
penup()
goto(start_x, start_y - 50)
write("Quadrate: " + str(gesamt), font=("Arial", 18, "bold"))

hideturtle()  # Pfeil ausblenden
done()

# ============================================================
#  MISSIONEN FÜR DICH
#  1. Rate: Wie viele Quadrate bei 10 Stufen? Dann ausprobieren!
#  2. Finde eine Regel: Stufen und Quadrate in eine Tabelle.
#  3. Probiere auch 2, 3, 4 und 5 Stufen.
# ============================================================