# ============================================================
#  HAUS — ein Haus mit Dach
#
#  Zwei Blöcke: erst die Wände, dann das Dach.
#  Ändere die Farben. Und probier mal, das Haus größer zu machen:
#  dann musst du ALLE 120 ändern, nicht nur eine.
# ============================================================

from turtle import *

speed(1)          # 0 = sofort, 1 = langsam zum Zuschauen

# --- Die Wände ---
color("black", "firebrick")
begin_fill()
forward(120)
left(90)
forward(120)
left(90)
forward(120)
left(90)
forward(120)
left(90)
end_fill()

# --- Nach oben, ohne zu zeichnen ---
penup()
left(90)
forward(120)
right(90)
pendown()

# --- Das Dach ---
color("black", "sienna")
begin_fill()
left(60)
forward(120)
right(120)
forward(120)
right(120)
forward(120)
end_fill()

done()