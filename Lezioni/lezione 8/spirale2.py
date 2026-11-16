# ============================================================
#  SPIRALE 2 — Jede Linie ist länger als die davor
#
#  Die erste Linie ist 1 mal schritt lang, die zweite
#  2 mal schritt, die dritte 3 mal schritt, und so weiter.
#  Ändere EINE Zahl und wette: Wird das Bild größer,
#  kleiner oder bleibt es gleich?
# ============================================================

from turtle import *

setup(700, 700)   # Fenstergröße
speed(0)          # 0 = sofort, 1 = langsam zum Zuschauen
pensize(3)

# ============================================================
#  HIER WIRD ALLES EINGESTELLT
# ============================================================

schritt = 10         # <-- so viel länger wird jede neue Linie
winkel = 90          # <-- so weit biegt die Schildkröte ab
farbe = "crimson"    # <-- Farbe, englisch und in Gänsefüßchen: "red", "blue"

# ============================================================

color(farbe)

for i in range(1, 31):         # <-- 30 Linien (die letzte Zahl zählt nicht mit)
    forward(i * schritt)
    left(winkel)

hideturtle()  # Pfeil ausblenden
done()


# ============================================================
#  WETT-MISSIONEN
#  Erst wetten (▲ größer, ▼ kleiner, ＝ gleich), dann ändern
#  und ausführen (Run). Wer hat richtig gewettet?
#
#  1. schritt = 20
#  2. schritt = 5
#  3. farbe = "blue"
#  4. schritt = 0         (Achtung: was passiert hier?)
#  5. winkel = 120
#  6. winkel = -90
#  7. range(1, 41)        (statt range(1, 31))
# ============================================================
