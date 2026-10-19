# ============================================================
#  STERN — ein Stern mit fünf Zacken
#
#  Die 144 ist das Geheimnis. Probier auch mal 150 oder 140.
# ============================================================

from turtle import *

speed(1)          # 0 = sofort, 1 = langsam zum Zuschauen

# --- Der Stern ---
color("darkred", "gold")     # <-- Strichfarbe, Füllfarbe
begin_fill()
forward(200)
right(144)                   # <-- das Geheimnis
forward(200)
right(144)
forward(200)
right(144)
forward(200)
right(144)
forward(200)
right(144)
end_fill()

done()