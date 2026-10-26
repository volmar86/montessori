# ============================================================
#  HAUS MIT VARIABLEN
#
#  Oben stehen drei Zahlen. Alles andere rechnet sich daraus aus.
#  Ändere NUR die drei Zahlen oben und drück Play.
# ============================================================

from turtle import *

speed(0)          # 0 = sofort, 1 = langsam zum Zuschauen

# ============================================================
#  HIER WIRD ALLES EINGESTELLT
# ============================================================

groesse = 120      # <-- wie groß das Haus ist
start_x = -60      # <-- wo es steht: links / rechts
start_y = -120     # <-- wo es steht: unten / oben

# ============================================================

# --- An den Start ---
penup()
goto(start_x, start_y)
pendown()
setheading(0)

# --- Die Wände ---
color("black", "firebrick")
begin_fill()
forward(groesse)
left(90)
forward(groesse)
left(90)
forward(groesse)
left(90)
forward(groesse)
left(90)
end_fill()

# --- Nach oben zum Dach, ohne zu zeichnen ---
penup()
left(90)
forward(groesse)
right(90)
pendown()

# --- Das Dach ---
color("black", "sienna")
begin_fill()
left(60)
forward(groesse)
right(120)
forward(groesse)
right(120)
forward(groesse)
end_fill()

# --- Die Tür ---
penup()
goto(start_x + groesse * 0.4, start_y)
pendown()
setheading(90)
color("black", "saddlebrown")
begin_fill()
forward(groesse * 0.45)
right(90)
forward(groesse * 0.2)
right(90)
forward(groesse * 0.45)
end_fill()

# --- Das Fenster ---
penup()
goto(start_x + groesse * 0.4, start_y + groesse * 0.6)
pendown()
setheading(0)
color("black", "lightblue")
begin_fill()
forward(groesse * 0.2)
left(90)
forward(groesse * 0.2)
left(90)
forward(groesse * 0.2)
left(90)
forward(groesse * 0.2)
left(90)
end_fill()

done()
