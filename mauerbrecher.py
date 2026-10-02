# ============================================================
#  MAUERBRECHER
#  Schlag den Ball gegen die Mauer und zerstöre alle Steine.
#
#  Steuerung:   Pfeil links / Pfeil rechts  oder  A / D
#  Ball starten: Leertaste
#  Pause:        P
#
#  Tipp: Wo der Ball den Schläger trifft, bestimmt die Richtung.
#  Mitte = gerade hoch, Rand = schräg.
#
#  WICHTIG: Klick einmal ins Spielfenster, damit die Tasten
#  funktionieren.
# ============================================================

import turtle
import math

# ====== EINSTELLUNGEN – hier darfst du Zahlen und Farben ändern ======
BREITE = 700               # Spielfeld in Pixeln
HOEHE = 560
REIHEN = 5                 # so viele Reihen Steine
SPALTEN = 10               # so viele Steine pro Reihe
SCHLAEGER_BREITE = 110     # größer = leichter
SCHLAEGER_TEMPO = 10
BALL_TEMPO = 6             # Anfangstempo des Balls
BESCHLEUNIGUNG = 1.01      # nach jedem Stein wird der Ball ein bisschen schneller
LEBEN = 3

FARBEN_REIHEN = ["red", "orange", "gold", "limegreen", "deepskyblue"]
FARBE_SCHLAEGER = "white"
FARBE_BALL = "white"
FARBE_HINTERGRUND = "black"
# =====================================================================

TAKT = 16                  # Millisekunden pro Bild
HOECHSTTEMPO = 12          # schneller wird der Ball nie
STEIN_HOEHE = 20
BALL_RADIUS = 10

fenster = turtle.Screen()
fenster.title("Mauerbrecher")
fenster.bgcolor(FARBE_HINTERGRUND)
fenster.setup(BREITE + 40, HOEHE + 80)
fenster.tracer(0)

OBEN = HOEHE / 2
UNTEN = -HOEHE / 2
LINKS = -BREITE / 2
RECHTS = BREITE / 2

# Rahmen
rahmen = turtle.Turtle()
rahmen.hideturtle()
rahmen.color("gray")
rahmen.pensize(2)
rahmen.penup()
rahmen.goto(LINKS, UNTEN)
rahmen.pendown()
rahmen.goto(LINKS, OBEN)
rahmen.goto(RECHTS, OBEN)
rahmen.goto(RECHTS, UNTEN)

# Schläger
schlaeger = turtle.Turtle()
schlaeger.shape("square")
schlaeger.color(FARBE_SCHLAEGER)
schlaeger.shapesize(stretch_wid=0.8, stretch_len=SCHLAEGER_BREITE / 20)
schlaeger.penup()
SCHLAEGER_Y = UNTEN + 40

# Ball
ball = turtle.Turtle()
ball.shape("circle")
ball.color(FARBE_BALL)
ball.penup()

# Ein Stift, der die Steine stempelt
maurer = turtle.Turtle()
maurer.hideturtle()
maurer.penup()
maurer.shape("square")
STEIN_BREITE = BREITE / SPALTEN
maurer.shapesize(stretch_wid=(STEIN_HOEHE - 4) / 20, stretch_len=(STEIN_BREITE - 4) / 20)

# Text
anzeige = turtle.Turtle()
anzeige.hideturtle()
anzeige.penup()
anzeige.color("white")

# ---------- Spielzustand ----------
steine = []                # jeder Stein: [x, y, stempel_nummer]
tempo_x = 0.0
tempo_y = 0.0
punkte = 0
leben = LEBEN
laeuft = False             # läuft das Spiel (oder ist es vorbei)?
ball_klebt = True          # wartet der Ball auf dem Schläger?
pausiert = False
gedrueckt = set()


def anzeige_zeigen(extra=""):
    anzeige.clear()
    anzeige.goto(0, OBEN + 12)
    text = "Punkte: " + str(punkte) + "      Leben: " + str(leben)
    if pausiert:
        text = "PAUSE   P = weiter"
    anzeige.write(text, align="center", font=("Arial", 16, "bold"))
    if extra != "":
        anzeige.goto(0, -60)
        anzeige.write(extra, align="center", font=("Arial", 20, "bold"))


def mauer_bauen():
    maurer.clearstamps()
    steine.clear()
    for reihe in range(REIHEN):
        farbe = FARBEN_REIHEN[reihe % len(FARBEN_REIHEN)]
        y = OBEN - 60 - reihe * STEIN_HOEHE
        for spalte in range(SPALTEN):
            x = LINKS + STEIN_BREITE / 2 + spalte * STEIN_BREITE
            maurer.color(farbe)
            maurer.goto(x, y)
            nummer = maurer.stamp()
            steine.append([x, y, nummer])


def ball_auf_schlaeger():
    global ball_klebt, tempo_x, tempo_y
    ball_klebt = True
    tempo_x = 0
    tempo_y = 0
    ball.goto(schlaeger.xcor(), SCHLAEGER_Y + 20)


def neues_spiel():
    global punkte, leben, laeuft, pausiert
    punkte = 0
    leben = LEBEN
    pausiert = False
    schlaeger.goto(0, SCHLAEGER_Y)
    mauer_bauen()
    ball.showturtle()
    ball_auf_schlaeger()
    laeuft = True
    anzeige_zeigen("Leertaste = Ball starten")
    fenster.update()


def abschiessen():
    global ball_klebt, tempo_x, tempo_y
    ball_klebt = False
    tempo_x = BALL_TEMPO * 0.5
    tempo_y = BALL_TEMPO
    anzeige_zeigen()


def tempo():
    return math.sqrt(tempo_x * tempo_x + tempo_y * tempo_y)


def schlaeger_bewegen():
    x = schlaeger.xcor()
    if "links" in gedrueckt:
        x = x - SCHLAEGER_TEMPO
    if "rechts" in gedrueckt:
        x = x + SCHLAEGER_TEMPO
    grenze = RECHTS - SCHLAEGER_BREITE / 2
    if x > grenze:
        x = grenze
    if x < -grenze:
        x = -grenze
    schlaeger.setx(x)


def stein_treffen():
    """Prüft, ob der Ball einen Stein berührt. Höchstens ein Stein pro Bild."""
    global tempo_x, tempo_y, punkte
    for stein in steine:
        x, y, nummer = stein
        abstand_x = abs(ball.xcor() - x) - (STEIN_BREITE / 2 + BALL_RADIUS)
        abstand_y = abs(ball.ycor() - y) - (STEIN_HOEHE / 2 + BALL_RADIUS)
        if abstand_x < 0 and abstand_y < 0:
            # Von der Seite oder von oben/unten getroffen?
            if abstand_x > abstand_y:
                tempo_x = -tempo_x
            else:
                tempo_y = -tempo_y
            maurer.clearstamp(nummer)
            steine.remove(stein)
            punkte = punkte + 10
            if tempo() < HOECHSTTEMPO:
                tempo_x = tempo_x * BESCHLEUNIGUNG
                tempo_y = tempo_y * BESCHLEUNIGUNG
            anzeige_zeigen()
            return


def takt():
    global tempo_x, tempo_y, leben, laeuft
    if laeuft and not pausiert:
        schlaeger_bewegen()
        if ball_klebt:
            ball.goto(schlaeger.xcor(), SCHLAEGER_Y + 20)
        else:
            ball.goto(ball.xcor() + tempo_x, ball.ycor() + tempo_y)

            # Wände links, rechts, oben
            if ball.xcor() < LINKS + BALL_RADIUS:
                ball.setx(LINKS + BALL_RADIUS)
                tempo_x = abs(tempo_x)
            if ball.xcor() > RECHTS - BALL_RADIUS:
                ball.setx(RECHTS - BALL_RADIUS)
                tempo_x = -abs(tempo_x)
            if ball.ycor() > OBEN - BALL_RADIUS:
                ball.sety(OBEN - BALL_RADIUS)
                tempo_y = -abs(tempo_y)

            # Schläger: die Trefferstelle bestimmt den Winkel
            if tempo_y < 0:
                nah_y = abs(ball.ycor() - SCHLAEGER_Y) < BALL_RADIUS + 8
                versatz = ball.xcor() - schlaeger.xcor()
                if nah_y and abs(versatz) < SCHLAEGER_BREITE / 2 + BALL_RADIUS:
                    anteil = versatz / (SCHLAEGER_BREITE / 2)   # -1 = ganz links, +1 = ganz rechts
                    if anteil > 1:
                        anteil = 1
                    if anteil < -1:
                        anteil = -1
                    winkel = math.radians(anteil * 60)
                    v = tempo()
                    tempo_x = v * math.sin(winkel)
                    tempo_y = v * math.cos(winkel)
                    ball.sety(SCHLAEGER_Y + BALL_RADIUS + 8)

            stein_treffen()

            # Unten raus: ein Leben weniger
            if ball.ycor() < UNTEN:
                leben = leben - 1
                if leben == 0:
                    laeuft = False
                    ball.hideturtle()
                    anzeige_zeigen("GAME OVER   Leertaste = neues Spiel")
                else:
                    ball_auf_schlaeger()
                    anzeige_zeigen("Leertaste = Ball starten")

            # Alle Steine weg?
            if len(steine) == 0 and laeuft:
                laeuft = False
                ball.hideturtle()
                anzeige_zeigen("GEWONNEN!   Leertaste = neues Spiel")

        fenster.update()
    fenster.ontimer(takt, TAKT)


# ---------- Tasten ----------
def taste_merken(taste, name):
    fenster.onkeypress(lambda: gedrueckt.add(name), taste)
    fenster.onkeyrelease(lambda: gedrueckt.discard(name), taste)


for taste in ["Left", "a", "A"]:
    taste_merken(taste, "links")
for taste in ["Right", "d", "D"]:
    taste_merken(taste, "rechts")


def leertaste():
    if not laeuft:
        neues_spiel()
    elif ball_klebt and not pausiert:
        abschiessen()


def pause():
    global pausiert
    if not laeuft:
        return
    pausiert = not pausiert
    anzeige_zeigen()
    fenster.update()


fenster.onkeypress(leertaste, "space")
fenster.onkeypress(pause, "p")
fenster.onkeypress(pause, "P")
fenster.listen()

neues_spiel()
takt()
turtle.done()
