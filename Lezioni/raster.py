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