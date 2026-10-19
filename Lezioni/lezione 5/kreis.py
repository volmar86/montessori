# ============================================================
#  KREIS — ein bunter Kreis
#
#  Das Programm läuft schon. Ändere die Zahlen,
#  drück Play und schau, was passiert.
# ============================================================

from turtle import *

speed(1)          # 0 = sofort, 1 = langsam zum Zuschauen

# --- Der Kreis ---
color("blue", "skyblue")     # <-- Strichfarbe, Füllfarbe
begin_fill()
circle(100)                  # <-- wie groß
end_fill()

done()