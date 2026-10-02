# ============================================================
#  HÜPFVOGEL
#  Flieg durch die Lücken zwischen den Säulen.
#
#  Hüpfen:       Leertaste, Pfeil hoch oder W
#  Pause:        P
#
#  Der Vogel fällt immer nach unten (Schwerkraft). Jeder Hüpfer
#  gibt ihm Schwung nach oben. Mehr ist es nicht!
#
#  WICHTIG: Klick einmal ins Spielfenster, damit die Tasten
#  funktionieren.
# ============================================================

import turtle
import random

# ====== EINSTELLUNGEN – hier darfst du Zahlen und Farben ändern ======
SCHWERKRAFT = 0.5          # so stark zieht es den Vogel nach unten
SPRUNGKRAFT = 8            # so viel Schwung gibt ein Hüpfer
SAEULEN_TEMPO = 3          # so schnell kommen die Säulen
LUECKE = 170               # so groß ist die Lücke zwischen oberer und unterer Säule
SAEULEN_ABSTAND = 260      # Abstand zwischen zwei Säulen
SAEULEN_BREITE = 70

FARBE_HIMMEL = "skyblue"
FARBE_VOGEL = "mediumpurple"
FARBE_SAEULE = "slategray"
FARBE_BODEN = "sandybrown"
# =====================================================================

TAKT = 16
BREITE = 600
HOEHE = 600
BODEN = -HOEHE / 2 + 60    # hier ist der Boden
DECKE = HOEHE / 2
VOGEL_X = -150
VOGEL_RADIUS = 17

fenster = turtle.Screen()
fenster.title("Hüpfvogel")
fenster.bgcolor(FARBE_HIMMEL)
fenster.setup(BREITE, HOEHE)
fenster.tracer(0)

# ---------- Der Vogel: ein Bild aus Pixeln ----------
VOGEL_BILD = [
    "....KKKK....",
    "..KKVVVVKK..",
    ".KVVVVVWWVK.",
    "KVVVVVWKWVK.",
    "KHHVVVVWWVK.",
    "KHHHVVVVVKGG",
    ".KHHVVVVKGG.",
    "..KKVVVVK...",
    "....KKKK....",
]
VOGEL_FARBEN = {"K": "black", "V": FARBE_VOGEL, "H": "plum", "W": "white", "G": "gold"}


def figur_anmelden(name, bild, farben, pixel):
    """Macht aus einem Bild aus Buchstaben eine Figur für die Schildkröte.
    Nebeneinander liegende Pixel mit gleicher Farbe werden zu einem
    Rechteck zusammengefasst: das sieht gleich aus, ist aber schneller."""
    form = turtle.Shape("compound")
    hoehe = len(bild)
    breite = len(bild[0])
    for zeile in range(hoehe):
        spalte = 0
        while spalte < breite:
            zeichen = bild[zeile][spalte]
            ende = spalte
            while ende + 1 < breite and bild[zeile][ende + 1] == zeichen:
                ende = ende + 1
            if zeichen in farben:
                x1 = (spalte - breite / 2) * pixel
                x2 = (ende + 1 - breite / 2) * pixel
                y = (hoehe / 2 - zeile) * pixel
                rechteck = ((x1, y), (x2, y), (x2, y - pixel), (x1, y - pixel))
                form.addcomponent(rechteck, farben[zeichen], farben[zeichen])
            spalte = ende + 1
    fenster.register_shape(name, form)


figur_anmelden("vogel", VOGEL_BILD, VOGEL_FARBEN, 4)

vogel = turtle.Turtle()
vogel.shape("vogel")
vogel.setheading(90)       # damit das Bild richtig herum steht
vogel.penup()

# Boden
boden = turtle.Turtle()
boden.hideturtle()
boden.penup()
boden.color(FARBE_BODEN)
boden.goto(-BREITE / 2, BODEN)
boden.begin_fill()
for ecke in [(BREITE / 2, BODEN), (BREITE / 2, -HOEHE / 2), (-BREITE / 2, -HOEHE / 2), (-BREITE / 2, BODEN)]:
    boden.goto(ecke)
boden.end_fill()

anzeige = turtle.Turtle()
anzeige.hideturtle()
anzeige.penup()
anzeige.color("white")

# ---------- Spielzustand ----------
saeulen = []               # jede Säule: [oben_turtle, unten_turtle, schon_gezaehlt]
tempo_y = 0.0
punkte = 0
rekord = 0
zustand = "warten"         # "warten", "fliegen" oder "vorbei"
pausiert = False
vorbei_seit = 0            # damit ein Hüpfer nicht sofort ein neues Spiel startet


def saeulenstueck():
    r = turtle.Turtle()
    r.shape("square")
    r.color(FARBE_SAEULE)
    r.penup()
    return r


def saeule_setzen(saeule, x):
    """Stellt eine Säule mit zufälliger Lücke an die Stelle x."""
    oben, unten, gezaehlt = saeule
    luecke_mitte = random.randint(int(BODEN + LUECKE / 2 + 40), int(DECKE - LUECKE / 2 - 40))
    luecke_oben = luecke_mitte + LUECKE / 2
    luecke_unten = luecke_mitte - LUECKE / 2

    hoehe_oben = DECKE - luecke_oben
    oben.shapesize(stretch_wid=hoehe_oben / 20, stretch_len=SAEULEN_BREITE / 20)
    oben.goto(x, luecke_oben + hoehe_oben / 2)

    hoehe_unten = luecke_unten - BODEN
    unten.shapesize(stretch_wid=hoehe_unten / 20, stretch_len=SAEULEN_BREITE / 20)
    unten.goto(x, BODEN + hoehe_unten / 2)
    saeule[2] = False


def anzeige_zeigen(extra=""):
    anzeige.clear()
    anzeige.goto(0, DECKE - 50)
    if pausiert:
        text = "PAUSE   P = weiter"
    else:
        text = str(punkte)
    anzeige.write(text, align="center", font=("Arial", 28, "bold"))
    anzeige.goto(0, -HOEHE / 2 + 20)
    anzeige.write("Rekord: " + str(rekord), align="center", font=("Arial", 14, "bold"))
    if extra != "":
        anzeige.goto(0, 60)
        anzeige.write(extra, align="center", font=("Arial", 20, "bold"))


def neues_spiel():
    global tempo_y, punkte, zustand, pausiert
    tempo_y = 0
    punkte = 0
    pausiert = False
    zustand = "warten"
    vogel.goto(VOGEL_X, 0)
    for nummer in range(len(saeulen)):
        saeule_setzen(saeulen[nummer], BREITE / 2 + SAEULEN_BREITE + nummer * SAEULEN_ABSTAND)
    anzeige_zeigen("Leertaste = los!")
    fenster.update()


def trifft_saeule(stueck):
    """Berührt der Vogel dieses Säulenstück (ein Rechteck)?"""
    breite_halb = stueck.shapesize()[1] * 10
    hoehe_halb = stueck.shapesize()[0] * 10
    nah_x = abs(vogel.xcor() - stueck.xcor()) < breite_halb + VOGEL_RADIUS - 4
    nah_y = abs(vogel.ycor() - stueck.ycor()) < hoehe_halb + VOGEL_RADIUS - 4
    return nah_x and nah_y


def absturz():
    global zustand, rekord, vorbei_seit
    zustand = "vorbei"
    vorbei_seit = 0
    if punkte > rekord:
        rekord = punkte
    anzeige_zeigen("AUTSCH!   Leertaste = nochmal")


def takt():
    global tempo_y, punkte, vorbei_seit
    if zustand == "vorbei":
        vorbei_seit = vorbei_seit + 1
    if zustand == "fliegen" and not pausiert:
        # Schwerkraft
        tempo_y = tempo_y - SCHWERKRAFT
        vogel.sety(vogel.ycor() + tempo_y)
        if vogel.ycor() > DECKE - VOGEL_RADIUS:
            vogel.sety(DECKE - VOGEL_RADIUS)
            tempo_y = 0

        # Säulen nach links schieben
        for saeule in saeulen:
            oben, unten, gezaehlt = saeule
            neues_x = oben.xcor() - SAEULEN_TEMPO
            oben.setx(neues_x)
            unten.setx(neues_x)
            if neues_x < -BREITE / 2 - SAEULEN_BREITE:
                am_weitesten = max(r[0].xcor() for r in saeulen)
                saeule_setzen(saeule, am_weitesten + SAEULEN_ABSTAND)
            elif not gezaehlt and neues_x < VOGEL_X:
                saeule[2] = True
                punkte = punkte + 1
                anzeige_zeigen()

        # Zusammenstoß?
        if vogel.ycor() < BODEN + VOGEL_RADIUS:
            vogel.sety(BODEN + VOGEL_RADIUS)
            absturz()
        for saeule in saeulen:
            if trifft_saeule(saeule[0]) or trifft_saeule(saeule[1]):
                absturz()
                break
    fenster.update()
    fenster.ontimer(takt, TAKT)


# ---------- Tasten ----------
def huepfen():
    global tempo_y, zustand
    if pausiert:
        return
    if zustand == "vorbei":
        if vorbei_seit > 30:           # eine halbe Sekunde warten
            neues_spiel()
        return
    if zustand == "warten":
        zustand = "fliegen"
        anzeige_zeigen()
    tempo_y = SPRUNGKRAFT


def pause():
    global pausiert
    if zustand != "fliegen":
        return
    pausiert = not pausiert
    anzeige_zeigen()


for taste in ["space", "Up", "w", "W"]:
    fenster.onkeypress(huepfen, taste)
fenster.onkeypress(pause, "p")
fenster.onkeypress(pause, "P")
fenster.listen()

# So viele Säulen passen auf den Bildschirm (plus eine Reserve)
for i in range(int(BREITE / SAEULEN_ABSTAND) + 2):
    saeulen.append([saeulenstueck(), saeulenstueck(), False])

neues_spiel()
takt()
turtle.done()
