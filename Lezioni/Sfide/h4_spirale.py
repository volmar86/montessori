# HERAUSFORDERUNG 4 — Die Spirale
# Die Schleife zählt mit: i wird bei jedem Schritt größer.
from turtle import *

winkel = 89
schritte = 120

speed(0)
pensize(2)
color("purple")
penup()
goto(0, 0)
pendown()
for i in range(schritte):
    forward(i * 2)
    right(winkel)

done()
