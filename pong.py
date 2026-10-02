# ============================================================
#  PONG für zwei Spieler an einer Tastatur
#
#  Links:   W = hoch,  S = runter
#  Rechts:  Pfeil hoch, Pfeil runter
#  Neues Spiel: Leertaste
#
#  WICHTIG: Klick einmal ins Spielfenster, damit die Tasten
#  funktionieren.
# ============================================================

import turtle
import random

# ====== EINSTELLUNGEN – hier darfst du Zahlen und Farben ändern ======
BREITE = 800               # Spielfeld in Pixeln
HOEHE = 500
SCHLAEGER_HOEHE = 100      # größer = leichter
SCHLAEGER_TEMPO = 9        # wie schnell sich die Schläger bewegen
BALL_TEMPO = 5             # Anfangstempo des Balls
BESCHLEUNIGUNG = 1.06      # nach jedem Treffer wird der Ball schneller
GEWINNPUNKTE = 5           # wer zuerst so viele Punkte hat, gewinnt

FARBE_LINKS = "deepskyblue"
FARBE_RECHTS = "orange"
FARBE_BALL = "white"
FARBE_HINTERGRUND = "black"
# =====================================================================

TAKT = 16                  # Millisekunden pro Bild (etwa 60 Bilder pro Sekunde)
HOECHSTTEMPO = 25          # schneller wird der Ball nie (sonst fliegt er durch den Schläger)

fenster = turtle.Screen()
fenster.title("Pong")
fenster.bgcolor(FARBE_HINTERGRUND)
fenster.setup(BREITE + 40, HOEHE + 40)
fenster.tracer(0)

# Mittellinie
linie = turtle.Turtle()
linie.hideturtle()
linie.color("gray")
linie.penup()
linie.goto(0, HOEHE / 2)
linie.setheading(270)
for i in range(int(HOEHE / 40)):
    linie.pendown()
    linie.forward(20)
    linie.penup()
    linie.forward(20)


def schlaeger_bauen(x, farbe):
    s = turtle.Turtle()
    s.shape("square")
    s.color(farbe)
    s.shapesize(stretch_wid=SCHLAEGER_HOEHE / 20, stretch_len=1)
    s.penup()
    s.goto(x, 0)
    return s


links = schlaeger_bauen(-BREITE / 2 + 30, FARBE_LINKS)
rechts = schlaeger_bauen(BREITE / 2 - 30, FARBE_RECHTS)

ball = turtle.Turtle()
ball.shape("circle")
ball.color(FARBE_BALL)
ball.penup()

anzeige = turtle.Turtle()
anzeige.hideturtle()
anzeige.penup()
anzeige.color("white")

# ---------- Spielzustand ----------
punkte_links = 0
punkte_rechts = 0
tempo_x = 0.0
tempo_y = 0.0
laeuft = False
gedrueckt = set()          # welche Tasten gerade gedrückt sind


def punkte_zeigen(extra=""):
    anzeige.clear()
    anzeige.goto(0, HOEHE / 2 - 45)
    anzeige.write(str(punkte_links) + "    " + str(punkte_rechts),
                  align="center", font=("Courier", 32, "bold"))
    if extra != "":
        anzeige.goto(0, -30)
        anzeige.write(extra, align="center", font=("Arial", 20, "bold"))


def ball_aufschlag(nach_rechts):
    """Ball in die Mitte, schräg in eine zufällige Richtung."""
    global tempo_x, tempo_y
    ball.goto(0, 0)
    tempo_x = BALL_TEMPO if nach_rechts else -BALL_TEMPO
    tempo_y = random.choice([-1, 1]) * random.uniform(2, 4)


def neues_spiel():
    global punkte_links, punkte_rechts, laeuft
    punkte_links = 0
    punkte_rechts = 0
    links.sety(0)
    rechts.sety(0)
    punkte_zeigen()
    ball_aufschlag(random.choice([True, False]))
    ball.showturtle()
    laeuft = True
    fenster.ontimer(takt, TAKT)


def schlaeger_bewegen(schlaeger, hoch_taste, runter_taste):
    grenze = HOEHE / 2 - SCHLAEGER_HOEHE / 2
    y = schlaeger.ycor()
    if hoch_taste in gedrueckt:
        y = y + SCHLAEGER_TEMPO
    if runter_taste in gedrueckt:
        y = y - SCHLAEGER_TEMPO
    if y > grenze:
        y = grenze
    if y < -grenze:
        y = -grenze
    schlaeger.sety(y)


def trifft(schlaeger):
    """Berührt der Ball den Schläger?"""
    nah_x = abs(ball.xcor() - schlaeger.xcor()) < 20
    nah_y = abs(ball.ycor() - schlaeger.ycor()) < SCHLAEGER_HOEHE / 2 + 10
    return nah_x and nah_y


def takt():
    global tempo_x, tempo_y, punkte_links, punkte_rechts, laeuft
    if not laeuft:
        return

    schlaeger_bewegen(links, "w", "s")
    schlaeger_bewegen(rechts, "Up", "Down")

    ball.goto(ball.xcor() + tempo_x, ball.ycor() + tempo_y)

    # Oben und unten abprallen
    if ball.ycor() > HOEHE / 2 - 10:
        ball.sety(HOEHE / 2 - 10)
        tempo_y = -tempo_y
    if ball.ycor() < -HOEHE / 2 + 10:
        ball.sety(-HOEHE / 2 + 10)
        tempo_y = -tempo_y

    # Schläger: nur abprallen, wenn der Ball auf ihn zufliegt
    if tempo_x < 0 and trifft(links):
        tempo_x = min(-tempo_x * BESCHLEUNIGUNG, HOECHSTTEMPO)
        tempo_y = tempo_y * BESCHLEUNIGUNG
    if tempo_x > 0 and trifft(rechts):
        tempo_x = -min(tempo_x * BESCHLEUNIGUNG, HOECHSTTEMPO)
        tempo_y = tempo_y * BESCHLEUNIGUNG

    # Punkt?
    if ball.xcor() > BREITE / 2:
        punkte_links = punkte_links + 1
        ball_aufschlag(nach_rechts=False)
        punkte_zeigen()
    if ball.xcor() < -BREITE / 2:
        punkte_rechts = punkte_rechts + 1
        ball_aufschlag(nach_rechts=True)
        punkte_zeigen()

    # Gewonnen?
    if punkte_links >= GEWINNPUNKTE:
        laeuft = False
        ball.hideturtle()
        punkte_zeigen("Links gewinnt!\nLeertaste = neues Spiel")
    elif punkte_rechts >= GEWINNPUNKTE:
        laeuft = False
        ball.hideturtle()
        punkte_zeigen("Rechts gewinnt!\nLeertaste = neues Spiel")

    fenster.update()
    if laeuft:
        fenster.ontimer(takt, TAKT)


# ---------- Tasten: gedrückt halten = weiter bewegen ----------
def taste_merken(taste, name):
    fenster.onkeypress(lambda: gedrueckt.add(name), taste)
    fenster.onkeyrelease(lambda: gedrueckt.discard(name), taste)


for taste in ["w", "s", "Up", "Down"]:
    taste_merken(taste, taste)
taste_merken("W", "w")     # falls die Feststelltaste (Caps Lock) an ist
taste_merken("S", "s")


def leertaste():
    if not laeuft:
        neues_spiel()


fenster.onkeypress(leertaste, "space")
fenster.listen()

neues_spiel()
turtle.done()
