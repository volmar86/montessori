# ============================================================
#  MEIN BILD
#  raster.py muss im selben Ordner liegen.
# ============================================================
from turtle import *
import raster

# ---- ab hier zeichnest du ----

color("firebrick")
penup()
goto(-150, -100)
pendown()
setheading(0)
for i in range(4):
    forward(200)
    left(90)

done()