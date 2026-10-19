# ============================================================
#  DREIECK — ein Dreieck mit drei gleichen Seiten
#
#  WICHTIG, sonst geht es nie zu:
#  Alle drei Seiten sind GLEICH LANG, und jedes Mal
#  dreht man sich um 120 nach links.  360 : 3 = 120
#
#  Wenn du ein anderes Dreieck willst — breiter, flacher,
#  schief — dann geht das so nicht. Dafür gibt es dreieck_frei.py
# ============================================================

from turtle import *

speed(1)          # 0 = sofort, 1 = langsam zum Zuschauen

# --- Das Dreieck ---
color("darkgreen", "lightgreen")     # <-- Strichfarbe, Füllfarbe
begin_fill()
forward(150)                         # <-- Seite 1
left(120)
forward(150)                         # <-- Seite 2: GLEICHE Zahl
left(120)
forward(150)                         # <-- Seite 3: GLEICHE Zahl
left(120)
end_fill()

done()