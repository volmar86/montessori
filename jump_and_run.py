# ============================================================
#  ROBO HÜPFT – ein Jump'n'Run
#  Sammle die Münzen, spring über die Gruben, hüpf den
#  Matschis auf den Kopf und erreiche die Tür.
#
#  Laufen:  Pfeil links / Pfeil rechts  oder  A / D
#  Springen: Pfeil hoch, W oder Leertaste
#  Pause:    P
#
#  DAS BESTE: Das Level ist nur ein Bild aus Buchstaben (LEVEL).
#  Du kannst dein eigenes Level bauen!
#
#  WICHTIG: Klick einmal ins Spielfenster, damit die Tasten
#  funktionieren.
# ============================================================

import turtle

# ====== EINSTELLUNGEN – hier darfst du Zahlen und Farben ändern ======
SCHWERKRAFT = 0.8          # so stark zieht es Robo nach unten
SPRUNGKRAFT = 13           # so hoch springt Robo
LAUFTEMPO = 4.5            # so schnell läuft Robo
GEGNER_TEMPO = 1.2         # so schnell laufen die Matschis
LEBEN = 3

FARBE_HIMMEL = "lightskyblue"
FARBE_ERDE = "saddlebrown"
FARBE_GRAS = "limegreen"

# Das Level. Jede Zeile muss gleich lang sein.
#   #  = Block           o = Münze
#   S  = Start von Robo  E = Matschi (Gegner)
#   Z  = Ziel-Tür        Leerzeichen = Luft
LEVEL = [
    "                          ",
    "                          ",
    "                        Z ",
    "                    ######",
    "               E          ",
    "             ####         ",
    "                          ",
    "         ooo       ooo    ",
    "        ####       ####   ",
    "                          ",
    "   oooo                   ",
    "   ####                   ",
    "        o       o         ",
    " S          E        E    ",
    "#######   #####   ########",
    "#######   #####   ########",
]
# =====================================================================

TAKT = 16
FELD = 30                  # ein Buchstabe im Level = 30 x 30 Pixel
ROBO_BREITE = 24
ROBO_HOEHE = 30
GEGNER_BREITE = 28
GEGNER_HOEHE = 22
HOECHSTES_FALLTEMPO = 15   # schneller fällt Robo nie (sonst fällt er durch den Boden)

# Das Level vorbereiten: alle Zeilen gleich lang machen
laengste = max(len(zeile) for zeile in LEVEL)
LEVEL = [zeile.ljust(laengste) for zeile in LEVEL]
SPALTEN = laengste
ZEILEN = len(LEVEL)
BREITE = SPALTEN * FELD
HOEHE = ZEILEN * FELD
LINKS = -BREITE / 2
OBEN = HOEHE / 2 - 20

fenster = turtle.Screen()
fenster.title("Robo hüpft")
fenster.bgcolor(FARBE_HIMMEL)
fenster.setup(BREITE + 40, HOEHE + 100)
fenster.tracer(0)


# ---------- Figuren aus Pixeln ----------
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


ROBO_BILD = [
    "...RR...",
    "...GG...",
    ".GGGGGG.",
    ".GCGGCG.",
    ".GGGGGG.",
    "..GGGG..",
    ".BBBBBB.",
    "GBBYYBBG",
    ".BB..BB.",
    ".DD..DD.",
]
ROBO_FARBEN = {"R": "red", "G": "silver", "C": "cyan", "B": "royalblue",
               "Y": "gold", "D": "dimgray"}

MATSCHI_BILD = [
    "..PPPP..",
    ".PPPPPP.",
    "PPWKPWKP",
    "PPPPPPPP",
    "PPPPPPPP",
    "P.P..P.P",
]
MATSCHI_FARBEN = {"P": "mediumorchid", "W": "white", "K": "black"}

TUER_BILD = [
    ".BBBB.",
    "BHHHHB",
    "BHHHHB",
    "BHHHHB",
    "BHHHYB",
    "BHHHHB",
    "BHHHHB",
    "BBBBBB",
]
TUER_FARBEN = {"B": "saddlebrown", "H": "peru", "Y": "gold"}

figur_anmelden("robo", ROBO_BILD, ROBO_FARBEN, 3)
figur_anmelden("matschi", MATSCHI_BILD, MATSCHI_FARBEN, 4)
figur_anmelden("tuer", TUER_BILD, TUER_FARBEN, 5)


def neue_figur(form):
    t = turtle.Turtle()
    t.shape(form)
    t.setheading(90)       # damit das Bild richtig herum steht
    t.penup()
    return t


# ---------- Umrechnen: Feld im Level <-> Pixel ----------
def feld_mitte(spalte, zeile):
    return LINKS + spalte * FELD + FELD / 2, OBEN - zeile * FELD - FELD / 2


def ist_block(spalte, zeile):
    if spalte < 0 or spalte >= SPALTEN:
        return True                    # links und rechts ist eine unsichtbare Wand
    if zeile < 0 or zeile >= ZEILEN:
        return False                   # oben ist Luft, unten ist die Grube
    return LEVEL[zeile][spalte] == "#"


def spalte_von(x):
    return int((x - LINKS) // FELD)


def zeile_von(y):
    return int((OBEN - y) // FELD)


def beruehrt_block(x, y, breite, hoehe):
    """Berührt ein Rechteck (Mitte x, y) irgendeinen Block?"""
    for spalte in range(spalte_von(x - breite / 2), spalte_von(x + breite / 2 - 0.01) + 1):
        for zeile in range(zeile_von(y + hoehe / 2 - 0.01), zeile_von(y - hoehe / 2 + 0.01) + 1):
            if ist_block(spalte, zeile):
                return True
    return False


# ---------- Die Welt zeichnen (nur einmal) ----------
def welt_zeichnen():
    wolke = turtle.Turtle()
    wolke.hideturtle()
    wolke.penup()
    for x, y in [(-250, 150), (-220, 160), (-190, 150), (120, 200), (150, 210), (180, 200)]:
        wolke.goto(x, y)
        wolke.dot(50, "white")

    erde = turtle.Turtle()
    erde.hideturtle()
    erde.penup()
    erde.shape("square")
    for zeile in range(ZEILEN):
        for spalte in range(SPALTEN):
            if LEVEL[zeile][spalte] == "#":
                x, y = feld_mitte(spalte, zeile)
                erde.shapesize((FELD - 1) / 20)
                erde.color(FARBE_ERDE)
                erde.goto(x, y)
                erde.stamp()
                if not ist_block(spalte, zeile - 1):      # oben frei: Gras
                    erde.shapesize(stretch_wid=8 / 20, stretch_len=(FELD - 1) / 20)
                    erde.color(FARBE_GRAS)
                    erde.goto(x, y + FELD / 2 - 4)
                    erde.stamp()


# ---------- Spielzustand ----------
robo = neue_figur("robo")
start = (LINKS + FELD, OBEN - FELD)
tuer = None
muenzen = []               # jede Münze: eine Schildkröte
matschis = []              # jeder Matschi: [schildkröte, tempo, start_x, start_y]
tempo_x = 0.0
tempo_y = 0.0
am_boden = False
leben = LEBEN
gesammelt = 0
laeuft = False
pausiert = False
unverwundbar = 0           # nach einem Treffer kurz unverwundbar
gedrueckt = set()

anzeige = turtle.Turtle()
anzeige.hideturtle()
anzeige.penup()


def anzeige_zeigen(extra=""):
    """Die Zeile oben: Münzen und Leben, oder eine Meldung."""
    anzeige.clear()
    anzeige.color("black")
    if pausiert:
        text = "PAUSE   P = weiter"
    elif extra != "":
        text = extra
        anzeige.color("darkblue")
    else:
        text = "Münzen: " + str(gesammelt) + " / " + str(len(muenzen)) + "      Leben: " + str(leben)
    anzeige.goto(0, OBEN + 15)
    anzeige.write(text, align="center", font=("Arial", 16, "bold"))


def level_aufbauen():
    global start, tuer
    for zeile in range(ZEILEN):
        for spalte in range(SPALTEN):
            zeichen = LEVEL[zeile][spalte]
            x, y = feld_mitte(spalte, zeile)
            if zeichen == "S":
                start = (x, y)
            elif zeichen == "o":
                m = turtle.Turtle()
                m.shape("circle")
                m.color("goldenrod", "gold")
                m.shapesize(0.6)
                m.penup()
                m.goto(x, y)
                muenzen.append(m)
            elif zeichen == "E":
                g = neue_figur("matschi")
                g.goto(x, y - FELD / 2 + GEGNER_HOEHE / 2)
                matschis.append([g, GEGNER_TEMPO, x, y - FELD / 2 + GEGNER_HOEHE / 2])
            elif zeichen == "Z":
                tuer = neue_figur("tuer")
                tuer.goto(x, y - FELD / 2 + 20)       # steht auf dem Boden


def robo_an_den_start():
    global tempo_x, tempo_y, am_boden
    robo.goto(start[0], start[1] - FELD / 2 + ROBO_HOEHE / 2)
    tempo_x = 0
    tempo_y = 0
    am_boden = False


def neues_spiel():
    global leben, gesammelt, laeuft, pausiert, unverwundbar
    leben = LEBEN
    gesammelt = 0
    pausiert = False
    unverwundbar = 0
    for m in muenzen:
        m.showturtle()
    for gegner in matschis:
        gegner[0].goto(gegner[2], gegner[3])
        gegner[0].showturtle()
        gegner[1] = GEGNER_TEMPO
    robo.showturtle()
    robo_an_den_start()
    laeuft = True
    anzeige_zeigen()


def leben_verlieren():
    global leben, laeuft, unverwundbar
    leben = leben - 1
    if leben == 0:
        laeuft = False
        robo.hideturtle()
        anzeige_zeigen("GAME OVER   Leertaste = nochmal")
    else:
        robo_an_den_start()
        unverwundbar = 90
        anzeige_zeigen()


def robo_bewegen():
    global tempo_x, tempo_y, am_boden
    # Laufen
    tempo_x = 0
    if "links" in gedrueckt:
        tempo_x = -LAUFTEMPO
    if "rechts" in gedrueckt:
        tempo_x = LAUFTEMPO

    # Erst waagrecht bewegen, dann an Wänden stoppen
    x, y = robo.pos()
    x = x + tempo_x
    if beruehrt_block(x, y, ROBO_BREITE, ROBO_HOEHE):
        if tempo_x > 0:
            x = LINKS + spalte_von(x + ROBO_BREITE / 2) * FELD - ROBO_BREITE / 2
        elif tempo_x < 0:
            x = LINKS + (spalte_von(x - ROBO_BREITE / 2) + 1) * FELD + ROBO_BREITE / 2

    # Dann senkrecht: Schwerkraft
    tempo_y = tempo_y - SCHWERKRAFT
    if tempo_y < -HOECHSTES_FALLTEMPO:
        tempo_y = -HOECHSTES_FALLTEMPO
    y = y + tempo_y
    am_boden = False
    if beruehrt_block(x, y, ROBO_BREITE, ROBO_HOEHE):
        if tempo_y < 0:                            # gelandet
            zeile = zeile_von(y - ROBO_HOEHE / 2)
            y = OBEN - zeile * FELD + ROBO_HOEHE / 2
            am_boden = True
        else:                                      # Kopf gestoßen
            zeile = zeile_von(y + ROBO_HOEHE / 2)
            y = OBEN - (zeile + 1) * FELD - ROBO_HOEHE / 2
        tempo_y = 0
    robo.goto(x, y)


def matschis_bewegen():
    for gegner in matschis:
        g = gegner[0]
        if not g.isvisible():
            continue
        x = g.xcor() + gegner[1]
        vorne = x + (GEGNER_BREITE / 2) * (1 if gegner[1] > 0 else -1)
        fuesse = g.ycor() - GEGNER_HOEHE / 2
        wand = ist_block(spalte_von(vorne), zeile_von(g.ycor()))
        abgrund = not ist_block(spalte_von(vorne), zeile_von(fuesse - 1))
        if wand or abgrund:
            gegner[1] = -gegner[1]             # umdrehen
        else:
            g.setx(x)


def zusammenstoesse(alt_y):
    global gesammelt, tempo_y, laeuft
    x, y = robo.pos()

    for m in muenzen:
        if m.isvisible() and abs(m.xcor() - x) < 20 and abs(m.ycor() - y) < 22:
            m.hideturtle()
            gesammelt = gesammelt + 1
            anzeige_zeigen()

    for gegner in matschis:
        g = gegner[0]
        if not g.isvisible():
            continue
        nah_x = abs(g.xcor() - x) < (GEGNER_BREITE + ROBO_BREITE) / 2
        nah_y = abs(g.ycor() - y) < (GEGNER_HOEHE + ROBO_HOEHE) / 2
        if nah_x and nah_y:
            von_oben = alt_y - ROBO_HOEHE / 2 >= g.ycor() + GEGNER_HOEHE / 2 - 6
            if tempo_y <= 0 and von_oben:
                g.hideturtle()                 # draufgesprungen!
                tempo_y = SPRUNGKRAFT * 0.6
            elif unverwundbar == 0:
                leben_verlieren()
                return

    if tuer is not None and abs(tuer.xcor() - x) < 20 and abs(tuer.ycor() - y) < 30:
        laeuft = False
        anzeige_zeigen("GESCHAFFT! " + str(gesammelt) + " von " + str(len(muenzen))
                       + " Münzen.   Leertaste = nochmal")


def takt():
    global unverwundbar
    if laeuft and not pausiert:
        alt_y = robo.ycor()
        robo_bewegen()
        matschis_bewegen()
        if unverwundbar > 0:
            unverwundbar = unverwundbar - 1
            if unverwundbar % 10 < 5:          # blinken
                robo.hideturtle()
            else:
                robo.showturtle()
            if unverwundbar == 0:
                robo.showturtle()
        if robo.ycor() < -HOEHE / 2 - 60:      # in die Grube gefallen
            leben_verlieren()
        else:
            zusammenstoesse(alt_y)
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


def springen():
    global tempo_y, am_boden
    if pausiert or not laeuft:
        return
    if am_boden:
        tempo_y = SPRUNGKRAFT
        am_boden = False


def leertaste():
    if not laeuft:
        neues_spiel()
    else:
        springen()


def pause():
    global pausiert
    if not laeuft:
        return
    pausiert = not pausiert
    anzeige_zeigen()


for taste in ["Up", "w", "W"]:
    fenster.onkeypress(springen, taste)
fenster.onkeypress(leertaste, "space")
fenster.onkeypress(pause, "p")
fenster.onkeypress(pause, "P")
fenster.listen()

welt_zeichnen()
level_aufbauen()
neues_spiel()
takt()
turtle.done()
