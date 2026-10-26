# HERAUSFORDERUNG 6 — Der Stern
# Nicht zur nächsten Ecke, sondern über welche hinweg.
from turtle import *

ecken = 7
sprung = 3

penup()
goto(-100, -120)
pendown()
setheading(0)
pensize(3)
color("darkred")
for i in range(ecken):
    forward(220)
    right(360 * sprung / ecken)

done()
