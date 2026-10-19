# ============================================================
#  BOGEN — ein Tor mit zwei Säulen und einem dicken Bogen
#
#  Vier Blöcke: linke Säule, rechte Säule, der Bogen, der Balken.
#
#  Der Bogen ist dick, weil er aus ZWEI Halbkreisen besteht:
#  der äußere ist groß (130), der innere ist klein (80).
#  Dazwischen wird ausgemalt.
# ============================================================

from turtle import *

speed(1)          # 0 = sofort, 1 = langsam zum Zuschauen
pensize(3)
color("dimgray", "lightgray")

# --- Die linke Säule ---
penup()
goto(-130, -170)
pendown()
setheading(0)
begin_fill()
forward(50)
left(90)
forward(170)
left(90)
forward(50)
left(90)
forward(170)
left(90)
end_fill()

# --- Die rechte Säule ---
penup()
goto(80, -170)
pendown()
setheading(0)
begin_fill()
forward(50)
left(90)
forward(170)
left(90)
forward(50)
left(90)
forward(170)
left(90)
end_fill()

# --- Der dicke Bogen ---
penup()
goto(130, 0)
pendown()
setheading(90)
begin_fill()
circle(130, 180)     # <-- der äußere Halbkreis
left(90)
forward(50)          # <-- nach innen
left(90)
circle(-80, 180)     # <-- der innere Halbkreis, zurück
left(90)
forward(50)
end_fill()

# --- Der Balken oben ---
penup()
goto(-160, 118)
pendown()
setheading(0)
color("dimgray", "silver")
begin_fill()
forward(320)
left(90)
forward(45)
left(90)
forward(320)
left(90)
forward(45)
left(90)
end_fill()

done()