# ============================================================
#  TREPPE MIT SCHLEIFE
#
#  Letzte Woche: fünf Stufen, fünf Mal das Gleiche getippt.
#  Heute: einmal getippt, fünf Mal gemacht.
#
#  Und oben stehen die Zahlen, die du ändern darfst.
# ============================================================

from turtle import *

speed(0)          # 0 = sofort, 1 = langsam zum Zuschauen
pensize(5)
color("saddlebrown")

# ===== EINSTELLUNGEN =====
stufen = 5         # <-- wie viele Stufen
breite = 40        # <-- wie breit eine Stufe
hoehe = 40         # <-- wie hoch eine Stufe
start_x = -120     # <-- wo die Treppe anfängt
start_y = -120

# --- An den Start ---
penup()
goto(start_x, start_y)
pendown()
setheading(0)

# --- Die Stufen ---
for i in range(stufen):
    forward(breite)
    left(90)
    forward(hoehe)
    right(90)

done()
