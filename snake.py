# ============================================================
#  SNAKE
#  Steuerung:  Pfeiltasten oder W A S D
#  Neues Spiel: Leertaste
#  Pause: P
#
#  Wie auf dem Nokia 3310: raus auf einer Seite, rein auf der
#  anderen. Wer die tödliche Wand will: DURCH_DIE_WAND = False
#
#  WICHTIG: Klick einmal ins Spielfenster, damit die Tasten
#  funktionieren.
# ============================================================

import turtle
import random

# ====== EINSTELLUNGEN – hier darfst du Zahlen und Farben ändern ======
GESCHWINDIGKEIT = 120      # Millisekunden pro Schritt: kleiner = schneller
KAESTCHEN = 20             # Größe eines Feldes in Pixeln
BREITE = 30                # Spielfeld: so viele Felder breit ...
HOEHE = 22                 # ... und so viele Felder hoch
START_LAENGE = 3           # So lang ist die Schlange am Anfang
WACHSTUM = 1               # So viele Felder wächst sie pro Futter
DURCH_DIE_WAND = True      # True = durch die Wand auf die andere Seite
                           # False = die Wand ist tödlich

FARBE_KOPF = "darkgreen"
FARBE_KOERPER = "limegreen"
FARBE_FUTTER = "red"
FARBE_HINTERGRUND = "black"
FARBE_RAND = "white"
# =====================================================================


# ---------- Fenster ----------
fenster = turtle.Screen()
fenster.title("Snake")
fenster.bgcolor(FARBE_HINTERGRUND)
fenster.setup(BREITE * KAESTCHEN + 60, HOEHE * KAESTCHEN + 140)
fenster.tracer(0)          # alles erst zeichnen, dann auf einmal zeigen

# Ein Stift, der Quadrate "stempelt" (für Schlange und Futter)
stempel = turtle.Turtle()
stempel.hideturtle()
stempel.penup()
stempel.shape("square")
stempel.shapesize(KAESTCHEN / 20 * 0.9)

# Ein Stift für Text (Punkte und Meldungen)
schreiber = turtle.Turtle()
schreiber.hideturtle()
schreiber.penup()
schreiber.color("white")


def pixel(feld):
    """Rechnet ein Feld (Spalte, Zeile) in Pixel auf dem Bildschirm um."""
    spalte, zeile = feld
    x = (spalte - BREITE / 2 + 0.5) * KAESTCHEN
    y = (zeile - HOEHE / 2 + 0.5) * KAESTCHEN - 20
    return x, y


def rand_zeichnen():
    rand = turtle.Turtle()
    rand.hideturtle()
    rand.penup()
    rand.color(FARBE_RAND)
    if DURCH_DIE_WAND:
        rand.color("gray")     # graue Wand: man kann durch
    rand.pensize(2)
    links = -BREITE / 2 * KAESTCHEN
    unten = -HOEHE / 2 * KAESTCHEN - 20
    rand.goto(links, unten)
    rand.pendown()
    for i in range(2):
        rand.forward(BREITE * KAESTCHEN)
        rand.left(90)
        rand.forward(HOEHE * KAESTCHEN)
        rand.left(90)


# ---------- Spielzustand ----------
schlange = []              # Liste von Feldern, der Kopf ist schlange[0]
richtung = (1, 0)          # (1, 0) = nach rechts
naechste_richtung = (1, 0)
futter = (0, 0)
punkte = 0
rekord = 0
laeuft = False
noch_wachsen = 0
pausiert = False


def neues_futter():
    """Legt das Futter auf ein freies Feld."""
    freie = []
    for spalte in range(BREITE):
        for zeile in range(HOEHE):
            if (spalte, zeile) not in schlange:
                freie.append((spalte, zeile))
    if len(freie) == 0:
        return None        # das ganze Feld ist voll: gewonnen!
    return random.choice(freie)


def zeichnen():
    stempel.clearstamps()
    if futter is not None:
        stempel.color(FARBE_FUTTER)
        stempel.goto(pixel(futter))
        stempel.stamp()
    for nummer in range(len(schlange)):
        if nummer == 0:
            stempel.color(FARBE_KOPF)
        else:
            stempel.color(FARBE_KOERPER)
        stempel.goto(pixel(schlange[nummer]))
        stempel.stamp()

    schreiber.clear()
    schreiber.goto(0, HOEHE / 2 * KAESTCHEN - 10)
    schreiber.write("Punkte: " + str(punkte) + "     Rekord: " + str(rekord),
                    align="center", font=("Arial", 16, "bold"))
    fenster.update()


def meldung(text):
    schreiber.goto(0, -HOEHE / 1.9 * KAESTCHEN - 50)
    schreiber.write(text, align="center", font=("Arial", 14, "bold"))
    fenster.update()


def neues_spiel():
    global schlange, richtung, naechste_richtung, futter, punkte
    global laeuft, noch_wachsen
    mitte_spalte = BREITE // 2
    mitte_zeile = HOEHE // 2
    schlange = []
    for i in range(START_LAENGE):
        schlange.append((mitte_spalte - i, mitte_zeile))
    richtung = (1, 0)
    naechste_richtung = (1, 0)
    punkte = 0
    noch_wachsen = 0
    futter = neues_futter()
    laeuft = True
    zeichnen()
    fenster.ontimer(schritt, GESCHWINDIGKEIT)


def schritt():
    global richtung, futter, punkte, rekord, laeuft, noch_wachsen
    if not laeuft:
        return
    if pausiert:
        fenster.ontimer(schritt, GESCHWINDIGKEIT)   # warten, aber nicht bewegen
        return

    richtung = naechste_richtung
    kopf = schlange[0]
    neuer_kopf = (kopf[0] + richtung[0], kopf[1] + richtung[1])

    # Die Wand: durch sie hindurch, oder Autsch?
    spalte, zeile = neuer_kopf
    if DURCH_DIE_WAND:
        neuer_kopf = (spalte % BREITE, zeile % HOEHE)   # auf der anderen Seite wieder rein
    elif spalte < 0 or spalte >= BREITE or zeile < 0 or zeile >= HOEHE:
        spiel_vorbei("Autsch, die Wand!")
        return

    # In sich selbst? (Das Schwanzende rückt weiter, außer die Schlange wächst.)
    frisst = (neuer_kopf == futter)
    if frisst or noch_wachsen > 0:
        koerper = schlange
    else:
        koerper = schlange[:-1]
    if neuer_kopf in koerper:
        spiel_vorbei("Autsch, in den eigenen Schwanz!")
        return

    schlange.insert(0, neuer_kopf)

    if frisst:
        punkte = punkte + 1
        noch_wachsen = noch_wachsen + WACHSTUM
        futter = neues_futter()

    if noch_wachsen > 0:
        noch_wachsen = noch_wachsen - 1     # Schwanz bleibt: die Schlange wächst
    else:
        schlange.pop()                      # Schwanz rückt nach

    if futter is None:
        zeichnen()
        spiel_vorbei("GEWONNEN! Das Feld ist voll!")
        return

    zeichnen()
    fenster.ontimer(schritt, GESCHWINDIGKEIT)


def spiel_vorbei(text):
    global laeuft, rekord
    laeuft = False
    if punkte > rekord:
        rekord = punkte
    zeichnen()
    meldung(text + "\nLeertaste = neues Spiel")


# ---------- Tasten ----------
def lenken(neue):
    """Ändert die Richtung, aber nie direkt rückwärts in sich selbst."""
    global naechste_richtung
    if (neue[0] + richtung[0], neue[1] + richtung[1]) != (0, 0):
        naechste_richtung = neue


def hoch():
    lenken((0, 1))


def runter():
    lenken((0, -1))


def links():
    lenken((-1, 0))


def rechts():
    lenken((1, 0))


def pause():
    global pausiert
    if not laeuft:
        return                 # nach Game Over gibt es nichts zu pausieren
    pausiert = not pausiert
    if pausiert:
        meldung("PAUSE\nP = weiter")
    else:
        zeichnen()             # wischt den Pause-Text weg


def leertaste():
    if not laeuft:
        neues_spiel()


fenster.onkeypress(hoch, "Up")
fenster.onkeypress(runter, "Down")
fenster.onkeypress(links, "Left")
fenster.onkeypress(rechts, "Right")
fenster.onkeypress(hoch, "w")
fenster.onkeypress(runter, "s")
fenster.onkeypress(links, "a")
fenster.onkeypress(rechts, "d")
fenster.onkeypress(hoch, "W")          # falls die Feststelltaste (Caps Lock) an ist
fenster.onkeypress(runter, "S")
fenster.onkeypress(links, "A")
fenster.onkeypress(rechts, "D")
fenster.onkeypress(leertaste, "space")
fenster.onkeypress(pause, "p")
fenster.onkeypress(pause, "P")
fenster.listen()

rand_zeichnen()
neues_spiel()
turtle.done()
