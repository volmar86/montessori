# ============================================================
#  QUADRAT — ein buntes Quadrat
#
#  Probier mal: alle vier Zahlen auf 200.
#  Und dann: eine davon auf 50.
# ============================================================

from turtle import *

speed(1)          # 0 = sofort, 1 = langsam zum Zuschauen

# --- Das Quadrat ---
color("black", "orange")     # <-- Strichfarbe, Füllfarbe
begin_fill()
forward(150)                 # <-- die vier Seiten
left(90)
forward(150)
left(90)
forward(150)
left(90)
forward(150)
left(90)
end_fill()

done()