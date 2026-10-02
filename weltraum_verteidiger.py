# ============================================================
#  WELTRAUM-VERTEIDIGER
#  Die Außerirdischen kommen! Schieß sie ab, bevor sie unten
#  ankommen – und weich ihren Bomben aus.
#
#  Fliegen:   Pfeil links / Pfeil rechts  oder  A / D
#  Schießen:  Leertaste, Pfeil hoch oder W
#  Pause:     P
#
#  Nach jeder Welle kommt die nächste – ein bisschen schneller.
#
#  WICHTIG: Klick einmal ins Spielfenster, damit die Tasten
#  funktionieren.
# ============================================================

import turtle
import random

# ====== EINSTELLUNGEN – hier darfst du Zahlen und Farben ändern ======
REIHEN = 4                 # so viele Reihen Außerirdische
SPALTEN = 8                # so viele pro Reihe
SCHIFF_TEMPO = 6           # so schnell fliegt dein Raumschiff
SCHUSS_TEMPO = 10          # so schnell fliegen deine Schüsse
BOMBEN_TEMPO = 4           # so schnell fallen die Bomben
BOMBEN_CHANCE = 0.02       # wie oft die Außerirdischen Bomben werfen (0 = nie)
LANGSAMKEIT = 30           # am Anfang: so viele Bilder bis zum nächsten Schritt der Außerirdischen
LEBEN = 3

FARBE_WELTRAUM = "black"
# =====================================================================

TAKT = 16
BREITE = 700
HOEHE = 600
OBEN = HOEHE / 2 - 40
UNTEN = -HOEHE / 2
SCHIFF_Y = UNTEN + 40
SCHRITT = 10               # so weit gehen die Außerirdischen pro Schritt zur Seite
RUNTER = 16                # so weit gehen sie am Rand nach unten
MAX_SCHUESSE = 3
MAX_BOMBEN = 5

fenster = turtle.Screen()
fenster.title("Weltraum-Verteidiger")
fenster.bgcolor(FARBE_WELTRAUM)
fenster.setup(BREITE + 40, HOEHE + 40)
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


SCHIFF_BILD = [
    "......W......",
    ".....WWW.....",
    ".....WBW.....",
    "....WWWWW....",
    ".R..WWWWW..R.",
    ".WWWWWWWWWWW.",
    "WWWWWWWWWWWWW",
    "..OO.....OO..",
]
SCHIFF_FARBEN = {"W": "white", "B": "deepskyblue", "R": "red", "O": "orange"}

# Zwei Außerirdische, jeder mit zwei Bildern (so bewegen sie sich)
UFO_BILD_1 = [
    "....CCC....",
    "...CCCCC...",
    ".SSSSSSSSS.",
    "SYSSYSSYSSS",
    ".SSSSSSSSS.",
    "..S.....S..",
]
UFO_BILD_2 = [
    "....CCC....",
    "...CCCCC...",
    ".SSSSSSSSS.",
    "SSSYSSYSSYS",
    ".SSSSSSSSS.",
    "...S...S...",
]
UFO_FARBEN = {"C": "cyan", "S": "silver", "Y": "yellow"}

GLUBSCH_BILD_1 = [
    "....A....",
    "....A....",
    "..OOOOO..",
    ".OOWWWOO.",
    ".OOWKWOO.",
    ".OOOOOOO.",
    "..OOOOO..",
    ".O.O.O.O.",
]
GLUBSCH_BILD_2 = [
    "....A....",
    "...A.....",
    "..OOOOO..",
    ".OOWWWOO.",
    ".OOKWWOO.",
    ".OOOOOOO.",
    "..OOOOO..",
    "..O.O.O..",
]
GLUBSCH_FARBEN = {"A": "white", "O": "orange", "W": "white", "K": "black"}

figur_anmelden("schiff", SCHIFF_BILD, SCHIFF_FARBEN, 3)
figur_anmelden("ufo1", UFO_BILD_1, UFO_FARBEN, 3)
figur_anmelden("ufo2", UFO_BILD_2, UFO_FARBEN, 3)
figur_anmelden("glubsch1", GLUBSCH_BILD_1, GLUBSCH_FARBEN, 3)
figur_anmelden("glubsch2", GLUBSCH_BILD_2, GLUBSCH_FARBEN, 3)


def neue_figur(form):
    t = turtle.Turtle()
    t.shape(form)
    t.setheading(90)       # damit das Bild richtig herum steht
    t.penup()
    return t


# Sterne im Hintergrund
sterne = turtle.Turtle()
sterne.hideturtle()
sterne.penup()
random.seed(7)             # immer die gleichen Sterne
for i in range(60):
    sterne.goto(random.randint(-BREITE // 2, BREITE // 2), random.randint(int(UNTEN), int(OBEN)))
    sterne.dot(random.choice([2, 2, 3]), random.choice(["white", "lightgray", "lightyellow"]))
random.seed()

schiff = neue_figur("schiff")

# Die Außerirdischen sind "Stempel": Bilder, die nur dann neu gezeichnet
# werden, wenn sie einen Schritt machen. Das macht das Spiel viel schneller.
maler = turtle.Turtle()
maler.hideturtle()
maler.penup()
maler.setheading(90)


def strich(farbe):
    """Ein kleiner Strich: für Schüsse und Bomben."""
    t = turtle.Turtle()
    t.shape("square")
    t.color(farbe)
    t.shapesize(stretch_wid=0.6, stretch_len=0.15)
    t.penup()
    t.hideturtle()
    return t


schuesse = [strich("yellow") for i in range(MAX_SCHUESSE)]
bomben = [strich("red") for i in range(MAX_BOMBEN)]

anzeige = turtle.Turtle()
anzeige.hideturtle()
anzeige.penup()

# ---------- Spielzustand ----------
feinde = []                # jeder Außerirdische: {"x", "y", "art", "punkte", "spalte", "stempel"}
richtung = 1               # 1 = nach rechts, -1 = nach links
bild_nummer = 1            # welches der zwei Bilder gerade gezeigt wird
schritt_zaehler = 0
langsamkeit_welle = LANGSAMKEIT
anzahl_welle = 0
punkte = 0
leben = LEBEN
welle = 1
laeuft = False
pausiert = False
nachladen = 0              # Bilder bis zum nächsten Schuss
unverwundbar = 0
vorbei_seit = 0
gedrueckt = set()


def anzeige_zeigen(extra=""):
    anzeige.clear()
    anzeige.goto(0, OBEN + 12)
    if pausiert:
        text = "PAUSE   P = weiter"
        anzeige.color("white")
    elif extra != "":
        text = extra
        anzeige.color("yellow")
    else:
        text = "Punkte: " + str(punkte) + "      Leben: " + str(leben) + "      Welle: " + str(welle)
        anzeige.color("white")
    anzeige.write(text, align="center", font=("Arial", 16, "bold"))


def feind_zeichnen(f):
    maler.shape(f["art"] + str(bild_nummer))
    maler.goto(f["x"], f["y"])
    f["stempel"] = maler.stamp()


def neue_welle():
    global richtung, schritt_zaehler, anzahl_welle, bild_nummer
    maler.clearstamps()
    feinde.clear()
    bild_nummer = 1
    for reihe in range(REIHEN):
        if reihe % 2 == 0:
            art = "ufo"
            wert = 20
        else:
            art = "glubsch"
            wert = 10
        for spalte in range(SPALTEN):
            f = {"x": -SPALTEN * 25 + 25 + spalte * 50, "y": OBEN - 40 - reihe * 40,
                 "art": art, "punkte": wert, "spalte": spalte, "stempel": None}
            feind_zeichnen(f)
            feinde.append(f)
    anzahl_welle = len(feinde)
    richtung = 1
    schritt_zaehler = 0
    for b in bomben:
        b.hideturtle()
    for s in schuesse:
        s.hideturtle()


def neues_spiel():
    global punkte, leben, welle, laeuft, pausiert, langsamkeit_welle, unverwundbar
    punkte = 0
    leben = LEBEN
    welle = 1
    pausiert = False
    unverwundbar = 0
    langsamkeit_welle = LANGSAMKEIT
    schiff.goto(0, SCHIFF_Y)
    schiff.showturtle()
    neue_welle()
    laeuft = True
    anzeige_zeigen()


def spiel_vorbei(text):
    global laeuft, vorbei_seit
    laeuft = False
    vorbei_seit = 0
    anzeige_zeigen(text + "   Punkte: " + str(punkte) + "   Leertaste = nochmal")


def schiff_bewegen():
    x = schiff.xcor()
    if "links" in gedrueckt:
        x = x - SCHIFF_TEMPO
    if "rechts" in gedrueckt:
        x = x + SCHIFF_TEMPO
    grenze = BREITE / 2 - 25
    if x > grenze:
        x = grenze
    if x < -grenze:
        x = -grenze
    schiff.setx(x)


def feinde_bewegen():
    """Alle Außerirdischen machen zusammen einen Schritt."""
    global richtung, schritt_zaehler, bild_nummer
    # Je weniger übrig sind, desto schneller werden sie
    warten = max(2, round(langsamkeit_welle * len(feinde) / anzahl_welle))
    schritt_zaehler = schritt_zaehler + 1
    if schritt_zaehler < warten:
        return
    schritt_zaehler = 0

    bild_nummer = 3 - bild_nummer          # 1 wird 2, 2 wird 1
    ganz_links = min(f["x"] for f in feinde)
    ganz_rechts = max(f["x"] for f in feinde)
    am_rand = (richtung > 0 and ganz_rechts + SCHRITT > BREITE / 2 - 25) or \
              (richtung < 0 and ganz_links - SCHRITT < -BREITE / 2 + 25)
    maler.clearstamps()
    for f in feinde:
        if am_rand:
            f["y"] = f["y"] - RUNTER
        else:
            f["x"] = f["x"] + richtung * SCHRITT
        feind_zeichnen(f)
    if am_rand:
        richtung = -richtung


def schiessen():
    global nachladen
    if nachladen > 0:
        return
    for s in schuesse:
        if not s.isvisible():
            s.goto(schiff.xcor(), SCHIFF_Y + 15)
            s.showturtle()
            nachladen = 15
            return


def bombe_werfen():
    """Ein zufälliger Außerirdischer, der ganz unten in seiner Spalte ist, wirft."""
    if random.random() > BOMBEN_CHANCE + 0.004 * (welle - 1):
        return
    unterste = {}
    for f in feinde:
        spalte = f["spalte"]
        if spalte not in unterste or f["y"] < unterste[spalte]["y"]:
            unterste[spalte] = f
    werfer = random.choice(list(unterste.values()))
    for b in bomben:
        if not b.isvisible():
            b.goto(werfer["x"], werfer["y"] - 15)
            b.showturtle()
            return


def getroffen():
    global leben, unverwundbar
    leben = leben - 1
    for b in bomben:
        b.hideturtle()
    if leben == 0:
        schiff.hideturtle()
        spiel_vorbei("GAME OVER!")
    else:
        unverwundbar = 90
        anzeige_zeigen()


def takt():
    global nachladen, punkte, welle, langsamkeit_welle, unverwundbar, vorbei_seit
    if not laeuft:
        vorbei_seit = vorbei_seit + 1
    if laeuft and not pausiert:
        schiff_bewegen()
        if nachladen > 0:
            nachladen = nachladen - 1

        # Schüsse fliegen nach oben und treffen vielleicht
        for s in schuesse:
            if not s.isvisible():
                continue
            s.sety(s.ycor() + SCHUSS_TEMPO)
            if s.ycor() > OBEN:
                s.hideturtle()
                continue
            for f in feinde:
                if abs(f["x"] - s.xcor()) < 18 and abs(f["y"] - s.ycor()) < 16:
                    maler.clearstamp(f["stempel"])
                    feinde.remove(f)
                    s.hideturtle()
                    punkte = punkte + f["punkte"]
                    anzeige_zeigen()
                    break

        # Welle geschafft?
        if len(feinde) == 0:
            welle = welle + 1
            langsamkeit_welle = max(8, int(langsamkeit_welle * 0.8))
            neue_welle()
            anzeige_zeigen()
        else:
            feinde_bewegen()
            bombe_werfen()

            # Sind sie unten angekommen?
            if min(f["y"] for f in feinde) < SCHIFF_Y + 30:
                spiel_vorbei("SIE SIND GELANDET!")

        # Bomben fallen
        for b in bomben:
            if not b.isvisible():
                continue
            b.sety(b.ycor() - BOMBEN_TEMPO)
            if b.ycor() < UNTEN:
                b.hideturtle()
            elif laeuft and unverwundbar == 0 and abs(b.xcor() - schiff.xcor()) < 18 and abs(b.ycor() - SCHIFF_Y) < 14:
                getroffen()
                break

        # Nach einem Treffer kurz blinken
        if unverwundbar > 0 and laeuft:
            unverwundbar = unverwundbar - 1
            if unverwundbar % 10 < 5:
                schiff.hideturtle()
            else:
                schiff.showturtle()
            if unverwundbar == 0:
                schiff.showturtle()
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


def feuer():
    if not laeuft:
        if vorbei_seit > 30:               # eine halbe Sekunde warten
            neues_spiel()
        return
    if not pausiert:
        schiessen()


def pause():
    global pausiert
    if not laeuft:
        return
    pausiert = not pausiert
    anzeige_zeigen()


for taste in ["space", "Up", "w", "W"]:
    fenster.onkeypress(feuer, taste)
fenster.onkeypress(pause, "p")
fenster.onkeypress(pause, "P")
fenster.listen()

neues_spiel()
takt()
turtle.done()
