# ============================================================
#  RÄTSELHAUS — rechne, dann schließt sich die Form
#
#  Die Schildkröte läuft eine Runde und dreht sich dabei
#  insgesamt 360 Grad. Rechne die fehlenden Winkel aus!
# ============================================================

from turtle import *

speed(0)          # 0 = sofort, 1 = langsam zum Zuschauen
pensize(3)

# ============================================================
#  HIER WIRD ALLES EINGESTELLT
# ============================================================

seite = 100              # <-- Länge jeder Kante

# Ersetze die 100 durch deine Lösung:
winkel_dreieck = 100     # <-- RÄTSEL 1:  3 * w = 360
winkel_sechseck = 100    # <-- RÄTSEL 2:  6 * w = 360
dachwinkel = 100         # <-- RÄTSEL 3:  90 + 30 + w + 30 + 90 = 360

# ============================================================

# --- Rätsel 1: Dreieck ---
penup()
goto(-330, -100)
setheading(0)
pendown()
for kante in range(3):
    forward(seite)
    left(winkel_dreieck)

# --- Rätsel 2: Sechseck ---
penup()
goto(-180, -100)
setheading(0)
pendown()
for kante in range(6):
    forward(seite)
    left(winkel_sechseck)

# --- Rätsel 3: Haus (Dach in der Mitte) ---
penup()
goto(110, -100)
setheading(0)
pendown()
forward(seite)
left(90)
forward(seite)
left(30)
forward(seite)
left(dachwinkel)
forward(seite)
left(30)
forward(seite)
left(90)

hideturtle()  # Pfeil ausblenden
done()

# ============================================================
#  SCHAFFST DU ES? Alle drei Formen sind zu, wenn
#  die Zahlen stimmen. Wenn nicht: nochmal nachrechnen!
# ============================================================
