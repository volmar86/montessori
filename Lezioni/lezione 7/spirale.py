# ============================================================
#  SPIRALE — Die große Wette
#
#  Die Schildkröte läuft eine Linie, biegt ab, läuft wieder.
#  Jedes Mal wird die Linie ein bisschen länger.
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

anzahl = 20          # <-- wie viele Linien
start_laenge = 10    # <-- Länge der ersten Linie
wachstum = 15        # <-- so viel länger wird jede neue Linie
winkel = 90          # <-- so weit biegt die Schildkröte ab
farbe = "crimson"    # <-- Farbe der Linie

# ============================================================

color(farbe)

laenge = start_laenge

# --- Linien zeichnen ---
for nummer in range(anzahl):
    forward(laenge)
    left(winkel)
    laenge = laenge + wachstum    # die nächste Linie wird länger

hideturtle()  # Pfeil ausblenden
done()


# ============================================================
#  WETT-MISSIONEN
#  Erst wetten (▲ größer, ▼ kleiner, ＝ gleich), dann ändern
#  und ausführen (Run). Wer hat richtig gewettet?
#
#  1. anzahl = 40
#  2. wachstum = 0        (Achtung: was passiert hier?)
#  3. winkel = 60
#  4. start_laenge = 100
#  5. winkel = 91         (nur ein Grad mehr — und?)
#  6. Suche selbst eine Einstellung, die die Größe GLEICH lässt.
# ============================================================
