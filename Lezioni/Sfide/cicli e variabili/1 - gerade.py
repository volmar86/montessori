# ============================================================
#  MEINE GERADE — eine Funktion zeichnen
#
#  Für jedes x rechnet der Computer das y aus:
#  y = steigung * x + achsenabschnitt
# ============================================================

from turtle import *

setup(700, 700)
tracer(0)         # Achsen: nicht jeden Strich einzeln zeigen (schnell)

# ============================================================
#  HIER WIRD ALLES EINGESTELLT
# ============================================================

steigung = 2            # <-- wie steil die Gerade ist
achsenabschnitt = -6    # <-- wo die Gerade die y-Achse schneidet
x_von = -4              # <-- die Gerade beginnt bei diesem x
x_bis = 8               # <-- die Gerade endet bei diesem x
massstab = 20           # <-- so viele Pixel ist eine Einheit
achse = 15              # <-- so weit gehen die Achsen
farbe = "crimson"       # <-- Farbe der Geraden
tempo = 3               # <-- wie schnell die Gerade gezeichnet wird (1 = langsam)

# ============================================================

# --- Die Achsen ---
pensize(2)
penup()
goto(-achse * massstab, 0)
pendown()
goto(achse * massstab, 0)
penup()
goto(0, -achse * massstab)
pendown()
goto(0, achse * massstab)

# --- Striche und Zahlen auf den Achsen ---
for zahl in range(-achse, achse + 1):
    penup()
    goto(zahl * massstab, -4)
    pendown()
    goto(zahl * massstab, 4)
    penup()
    goto(zahl * massstab, -20)
    write(zahl, align="center", font=("Arial", 8, "normal"))
    goto(-4, zahl * massstab)
    pendown()
    goto(4, zahl * massstab)
    penup()
    goto(-8, zahl * massstab - 5)
    write(zahl, align="right", font=("Arial", 8, "normal"))

# --- Die Gerade: für jedes x ein Punkt ---
color(farbe)
pensize(3)
penup()
goto(x_von * massstab, (steigung * x_von + achsenabschnitt) * massstab)
update()          # die Achsen jetzt auf einmal zeigen
tracer(1)         # ab hier kannst du beim Zeichnen zuschauen
speed(tempo)
pendown()
for x in range(x_von, x_bis + 1):
    y = steigung * x + achsenabschnitt
    goto(x * massstab, y * massstab)

hideturtle()  # Pfeil ausblenden
done()

# ============================================================
#  MISSIONEN FÜR DICH
#  1. Ändere die Steigung (1, 3, -1). Was passiert?
#  2. Wo kreuzt die Gerade die x-Achse? Dort ist y = 0. Rechne nach!
#  3. Zu steil? Mach x_von und x_bis kleiner.
# ============================================================
