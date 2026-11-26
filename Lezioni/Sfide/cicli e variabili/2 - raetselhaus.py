# ============================================================
#  RÄTSELHAUS — rechne, dann schließt sich die Form
#
#  Die Schildkröte läuft eine Runde und dreht sich dabei
#  insgesamt 360 Grad. Rechne die fehlenden Winkel aus!
# ============================================================

# ============================================================
#  RASTER — das Gitter im Hintergrund.
#  Es passt sich der Fenstergröße an.
#  In deiner Datei reicht oben:   import raster
# ============================================================
from turtle import *

setup(900, 700)        # <-- hier die Fenstergröße ändern
hideturtle()
tracer(0)              # erst alles zeichnen, dann EINMAL zeigen

schritt = 50
rechts = int(window_width() / 2)
oben = int(window_height() / 2)

spalten = rechts // schritt
zeilen = oben // schritt

# die feinen Linien
pensize(1)
color("lightblue")

for i in range(-spalten, spalten + 1):
    penup()
    goto(i * schritt, -oben)
    pendown()
    goto(i * schritt, oben)

for i in range(-zeilen, zeilen + 1):
    penup()
    goto(-rechts, i * schritt)
    pendown()
    goto(rechts, i * schritt)

# die zwei Achsen
pensize(2)
color("gray")
penup()
goto(-rechts, 0)
pendown()
goto(rechts, 0)
penup()
goto(0, -oben)
pendown()
goto(0, oben)

# die Zahlen, alle 100
penup()
for i in range(-(spalten // 2), spalten // 2 + 1):
    x = i * 100
    if x != 0 and abs(x) < rechts - 25:
        goto(x, -20)
        write(x, align="center", font=("Arial", 9, "normal"))
for i in range(-(zeilen // 2), zeilen // 2 + 1):
    y = i * 100
    if abs(y) < oben - 12:
        goto(8, y - 6)
        write(y, align="left", font=("Arial", 9, "normal"))

update()
tracer(1)

# so wie am Anfang: Mitte, nach rechts schauen, Stift unten
color("black")
pensize(3)
goto(0, 0)
setheading(0)
pendown()

showturtle()

# ============================================================
#  HIER WIRD ALLES EINGESTELLT
# ============================================================

speed(3)                 # 0 = sofort, 1 = langsam zum Zuschauen
pensize(3)
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
