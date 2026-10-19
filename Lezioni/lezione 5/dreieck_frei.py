# ============================================================
#  DREIECK FREI — ein Dreieck, das du selbst bestimmst
#
#  Hier gibt es KEINE Winkel und KEINE Seitenlängen.
#  Du sagst nur: hier, hier und hier sind die drei Ecken.
#  Den Rest rechnet der Computer.
#
#  Probier mal: ändere nur die erste Zahl von der Spitze.
# ============================================================

from turtle import *

speed(1)          # 0 = sofort, 1 = langsam zum Zuschauen

# --- Die drei Ecken ---
color("darkblue", "lightblue")

penup()
goto(-100, -80)        # <-- Ecke 1: unten links
pendown()
begin_fill()
goto(100, -80)         # <-- Ecke 2: unten rechts
goto(0, 90)            # <-- Ecke 3: die Spitze
goto(-100, -80)        # wieder zur Ecke 1 — sonst ist es nicht zu
end_fill()

done()