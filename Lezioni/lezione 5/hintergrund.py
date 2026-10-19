# ============================================================
#  HINTERGRUND — Himmel, Wiese und Sonne
#
#  Das hier ist schon fertig. Nicht ändern.
#  DEIN BILD KOMMT GANZ UNTEN, wo es steht.
# ============================================================

from turtle import *

setup(900, 650)
bgcolor("skyblue")
speed(1)          # 0 = sofort, 1 = langsam zum Zuschauen
hideturtle()
pensize(3)

# --- Die Wiese ---
penup()
goto(-450, -325)
pendown()
setheading(0)
color("darkgreen", "yellowgreen")
begin_fill()
forward(900)
left(90)
forward(200)
left(90)
forward(900)
left(90)
forward(200)
left(90)
end_fill()

# --- Die Sonne ---
penup()
goto(300, 180)
pendown()
setheading(0)
color("orange", "gold")
begin_fill()
circle(45)
end_fill()


# ============================================================
#  AB HIER BIST DU DRAN
#  Schreib deinen Namen in die Überschrift.
# ============================================================

# --- Mein Bild (______________) ---
penup()
goto(-200, -125)      # <-- wo dein Bild anfängt
pendown()
setheading(0)

# hier kommen deine Befehle





done()