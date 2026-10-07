# ============================================================
#  FLIPPER
#  Halte die Kugel im Spiel und triff die Pilze (Bumper)!
#
#  Linker Flipper:   Pfeil links  oder  A
#  Rechter Flipper:  Pfeil rechts oder  D
#  Kugel abschießen: Leertaste gedrückt halten (spannen),
#                    dann loslassen
#  Pause:            P
#
#  Die Kugel fällt immer nach unten (Schwerkraft, wie beim
#  Hüpfvogel) und prallt von den Wänden ab (wie beim
#  Mauerbrecher). Neu sind die Flipper: Sie drehen sich und
#  schleudern die Kugel wieder nach oben.
#
#  WICHTIG: Klick einmal ins Spielfenster, damit die Tasten
#  funktionieren.
# ============================================================

import turtle
import math

# ====== EINSTELLUNGEN – hier darfst du Zahlen und Farben ändern ======
SCHWERKRAFT = 0.22         # so stark zieht es die Kugel nach unten
ABPRALL = 0.6              # wie stark die Kugel von Wänden abprallt (0 = gar nicht, 1 = voll)
BUMPER_STOSS = 10          # so fest stößt ein Bumper die Kugel weg
FLIPPER_TEMPO = 15         # so schnell schlagen die Flipper hoch (Grad pro Bild)
FLIPPER_LAENGE = 86        # länger = leichter
MAX_KRAFT = 20             # so fest kann man die Kugel höchstens abschießen
KUGELN = 3                 # so viele Kugeln hast du
PUNKTE_BUMPER = 100        # so viele Punkte gibt ein Bumper

FARBE_TISCH = "midnightblue"
FARBE_WAND = "white"
FARBE_FLIPPER = "orange"
FARBE_KUGEL = "silver"
FARBE_BUMPER = "crimson"
# =====================================================================

TAKT = 16                  # Millisekunden pro Bild
SCHRITTE = 5               # jedes Bild wird in 5 kleine Schritte geteilt (sonst fliegt die Kugel durch die Wand)
HOECHSTTEMPO = 24          # schneller wird die Kugel nie
KUGEL_RADIUS = 9
FLIPPER_DICKE = 7          # halbe Dicke eines Flippers
BUMPER_RADIUS = 24

# Der Tisch
LINKS = -210               # linke Wand
SPUR = 210                 # Wand zwischen Spielfeld und Abschuss-Spur
AUSSEN = 250               # rechte Außenwand
OBEN = 280
UNTEN = -290
BODEN_SPUR = -255          # hier liegt die Kugel in der Abschuss-Spur
ZUG = 30 / MAX_KRAFT       # so weit sinkt der Kolben beim Spannen (Pixel pro Kraft)

fenster = turtle.Screen()
fenster.title("Flipper")
fenster.bgcolor(FARBE_TISCH)
fenster.setup(AUSSEN * 2 + 40, 650)
fenster.tracer(0)

# Die Wände: jede Wand ist eine Strecke von Punkt A nach Punkt B
waende = [
    ((LINKS, -150), (LINKS, 200)),             # links
    ((LINKS, 200), (-130, OBEN)),              # Ecke oben links
    ((-130, OBEN), (170, OBEN)),               # oben
    ((170, OBEN), (AUSSEN, 200)),              # Ecke oben rechts
    ((AUSSEN, 200), (AUSSEN, UNTEN)),          # rechts außen
    ((SPUR, UNTEN), (SPUR, 150)),              # Wand der Abschuss-Spur
    ((LINKS, -150), (-100, -211)),             # Schräge links unten (endet knapp über dem Flipper)
    ((SPUR, -150), (100, -211)),               # Schräge rechts unten
    ((-100, -220), (-100, UNTEN)),             # unter dem linken Flipper: das Loch in der Mitte
    ((100, -220), (100, UNTEN)),               # unter dem rechten Flipper
]
# Die Klappe schließt die Spur, sobald die Kugel im Spielfeld ist
KLAPPE = ((SPUR, 150), (AUSSEN, 190))

# Die Bumper (Mitte x, Mitte y)
bumper_orte = [(-70, 110), (70, 110), (0, 25)]

# Die Flipper: Drehpunkt, Winkel in Ruhe, Winkel oben, Taste
flipper = [
    {"x": -100, "y": -220, "ruhe": -30, "hoch": 30, "taste": "links", "winkel": -30, "dreh": 0},
    {"x": 100, "y": -220, "ruhe": 210, "hoch": 150, "taste": "rechts", "winkel": 210, "dreh": 0},
]

# ---------- Den Tisch zeichnen (nur einmal) ----------
tisch = turtle.Turtle()
tisch.hideturtle()
tisch.penup()
tisch.color(FARBE_WAND)
tisch.pensize(3)
for a, b in waende:
    tisch.goto(a)
    tisch.pendown()
    tisch.goto(b)
    tisch.penup()

bumper = []
for x, y in bumper_orte:
    b = turtle.Turtle()
    b.shape("circle")
    b.shapesize(BUMPER_RADIUS / 10)
    b.pensize(3)
    b.color("gold", FARBE_BUMPER)
    b.penup()
    b.goto(x, y)
    bumper.append({"turtle": b, "x": x, "y": y, "leuchten": 0})

klappe = turtle.Turtle()       # zeichnet die Klappe
klappe.hideturtle()
klappe.penup()
klappe.color(FARBE_WAND)
klappe.pensize(3)

maler = turtle.Turtle()        # zeichnet die Flipper (in jedem Bild neu)
maler.hideturtle()
maler.penup()
maler.color(FARBE_FLIPPER)

kolben = turtle.Turtle()       # der Kolben unter der Kugel
kolben.shape("square")
kolben.shapesize(stretch_wid=0.6, stretch_len=1.6)
kolben.color("gray")
kolben.penup()

kugel = turtle.Turtle()
kugel.shape("circle")
kugel.shapesize(KUGEL_RADIUS / 10)
kugel.color(FARBE_KUGEL)
kugel.penup()

anzeige = turtle.Turtle()
anzeige.hideturtle()
anzeige.penup()

# ---------- Spielzustand ----------
kugel_x = 0.0
kugel_y = 0.0
tempo_x = 0.0
tempo_y = 0.0
kugel_bereit = True        # liegt die Kugel in der Spur und wartet?
kraft = 0.0                # so stark ist die Feder gespannt
klappe_zu = False
punkte = 0
kugeln = KUGELN
rekord = 0
laeuft = False
pausiert = False
vorbei_seit = 0
gedrueckt = set()


def anzeige_zeigen(extra=""):
    anzeige.clear()
    anzeige.color("white")
    anzeige.goto(0, OBEN + 12)
    if pausiert:
        text = "PAUSE   P = weiter"
    else:
        text = ("Punkte: " + str(punkte) + "      Kugeln: " + str(kugeln)
                + "      Rekord: " + str(rekord))
    anzeige.write(text, align="center", font=("Arial", 16, "bold"))
    if extra != "":
        anzeige.color("yellow")
        anzeige.goto(0, -110)
        anzeige.write(extra, align="center", font=("Arial", 14, "bold"))


def klappe_zeichnen():
    klappe.clear()
    if klappe_zu:
        klappe.goto(KLAPPE[0])
        klappe.pendown()
        klappe.goto(KLAPPE[1])
        klappe.penup()


def flipper_spitze(f):
    winkel = math.radians(f["winkel"])
    return (f["x"] + FLIPPER_LAENGE * math.cos(winkel),
            f["y"] + FLIPPER_LAENGE * math.sin(winkel))


def bild_zeichnen():
    """Flipper, Kugel und Kolben an ihre neuen Plätze malen."""
    maler.clear()
    maler.pensize(FLIPPER_DICKE * 2)
    for f in flipper:
        maler.goto(f["x"], f["y"])
        maler.pendown()
        maler.goto(flipper_spitze(f))
        maler.penup()
        maler.goto(f["x"], f["y"])
        maler.dot(8, "white")             # der Drehpunkt

    kugel.goto(kugel_x, kugel_y)

    # Der Kolben: je fester gespannt, desto tiefer und röter
    if kugel_bereit:
        oben = BODEN_SPUR - kraft * ZUG
    else:
        oben = BODEN_SPUR
    kolben.goto((SPUR + AUSSEN) / 2, oben - 6)
    if kraft > MAX_KRAFT * 0.66:
        kolben.color("red")
    elif kraft > MAX_KRAFT * 0.33:
        kolben.color("orange")
    else:
        kolben.color("gray")

    for b in bumper:                      # getroffene Bumper leuchten kurz
        if b["leuchten"] > 0:
            b["leuchten"] = b["leuchten"] - 1
            b["turtle"].color("gold", "yellow")
        else:
            b["turtle"].color("gold", FARBE_BUMPER)
    fenster.update()


def neue_kugel():
    """Legt eine Kugel in die Abschuss-Spur."""
    global kugel_x, kugel_y, tempo_x, tempo_y, kugel_bereit, kraft, klappe_zu
    kugel_x = (SPUR + AUSSEN) / 2
    kugel_y = BODEN_SPUR + KUGEL_RADIUS
    tempo_x = 0
    tempo_y = 0
    kugel_bereit = True
    kraft = 0
    klappe_zu = False
    klappe_zeichnen()
    anzeige_zeigen("Leertaste halten ... und loslassen!")


def neues_spiel():
    global punkte, kugeln, laeuft, pausiert
    punkte = 0
    kugeln = KUGELN
    pausiert = False
    laeuft = True
    kugel.showturtle()
    neue_kugel()


def abschiessen():
    global tempo_y, kugel_bereit, kraft
    tempo_y = kraft
    kugel_bereit = False
    kraft = 0
    anzeige_zeigen()


def kugel_verloren():
    global kugeln, laeuft, rekord, vorbei_seit
    kugeln = kugeln - 1
    if kugeln == 0:
        laeuft = False
        vorbei_seit = 0
        kugel.hideturtle()
        if punkte > rekord:
            rekord = punkte
        anzeige_zeigen("GAME OVER   Leertaste = nochmal")
    else:
        neue_kugel()


# ---------- Abprallen ----------
def naechster_punkt(ax, ay, bx, by):
    """Der Punkt auf der Strecke von A nach B, der am nächsten an der Kugel liegt."""
    dx = bx - ax
    dy = by - ay
    t = ((kugel_x - ax) * dx + (kugel_y - ay) * dy) / (dx * dx + dy * dy)
    if t < 0:
        t = 0
    if t > 1:
        t = 1
    return ax + t * dx, ay + t * dy


def abprallen(px, py, abstand, wand_tempo_x=0, wand_tempo_y=0, abprall=ABPRALL):
    """Ist die Kugel näher als `abstand` am Punkt (px, py)? Dann wird sie
    hinausgeschoben und prallt ab. Gibt True zurück, wenn sie abgeprallt ist."""
    global kugel_x, kugel_y, tempo_x, tempo_y
    dx = kugel_x - px
    dy = kugel_y - py
    d = math.sqrt(dx * dx + dy * dy)
    if d >= abstand or d == 0:
        return False
    nx = dx / d                     # die Richtung von der Wand zur Kugel
    ny = dy / d
    kugel_x = px + nx * abstand     # Kugel aus der Wand schieben
    kugel_y = py + ny * abstand
    # Wie schnell fliegt die Kugel auf die Wand zu (die Wand kann sich bewegen)?
    auf_die_wand = (tempo_x - wand_tempo_x) * nx + (tempo_y - wand_tempo_y) * ny
    if auf_die_wand >= 0:
        return False                # sie fliegt schon weg
    tempo_x = tempo_x - (1 + abprall) * auf_die_wand * nx
    tempo_y = tempo_y - (1 + abprall) * auf_die_wand * ny
    return True


def flipper_drehen(f):
    """Dreht einen Flipper ein kleines Stück nach oben oder unten."""
    if f["taste"] in gedrueckt and laeuft:
        ziel = f["hoch"]
        schritt = FLIPPER_TEMPO / SCHRITTE
    else:
        ziel = f["ruhe"]
        schritt = FLIPPER_TEMPO * 0.5 / SCHRITTE   # runter etwas langsamer
    alt = f["winkel"]
    if f["winkel"] < ziel:
        f["winkel"] = min(ziel, f["winkel"] + schritt)
    else:
        f["winkel"] = max(ziel, f["winkel"] - schritt)
    f["dreh"] = math.radians(f["winkel"] - alt) * SCHRITTE   # Drehtempo pro Bild


def kleiner_schritt():
    """Ein Fünftel eines Bildes: Schwerkraft, bewegen, abprallen."""
    global kugel_x, kugel_y, tempo_x, tempo_y, punkte, kugel_bereit, klappe_zu

    tempo_y = tempo_y - SCHWERKRAFT / SCHRITTE
    kugel_x = kugel_x + tempo_x / SCHRITTE
    kugel_y = kugel_y + tempo_y / SCHRITTE

    # Wände
    for a, b in waende:
        px, py = naechster_punkt(a[0], a[1], b[0], b[1])
        abprallen(px, py, KUGEL_RADIUS + 1)
    if klappe_zu:
        px, py = naechster_punkt(KLAPPE[0][0], KLAPPE[0][1], KLAPPE[1][0], KLAPPE[1][1])
        abprallen(px, py, KUGEL_RADIUS + 1)

    # Bumper: abprallen und dann noch einen Stoß dazu
    for b in bumper:
        if abprallen(b["x"], b["y"], KUGEL_RADIUS + BUMPER_RADIUS):
            dx = kugel_x - b["x"]
            dy = kugel_y - b["y"]
            d = math.sqrt(dx * dx + dy * dy)
            weg = tempo_x * dx / d + tempo_y * dy / d
            if weg < BUMPER_STOSS:
                tempo_x = tempo_x + (BUMPER_STOSS - weg) * dx / d
                tempo_y = tempo_y + (BUMPER_STOSS - weg) * dy / d
            b["leuchten"] = 6
            punkte = punkte + PUNKTE_BUMPER
            anzeige_zeigen()

    # Flipper: eine dicke Wand, die sich dreht und die Kugel mitnimmt
    for f in flipper:
        sx, sy = flipper_spitze(f)
        px, py = naechster_punkt(f["x"], f["y"], sx, sy)
        wand_tempo_x = -f["dreh"] * (py - f["y"])
        wand_tempo_y = f["dreh"] * (px - f["x"])
        abprallen(px, py, KUGEL_RADIUS + FLIPPER_DICKE, wand_tempo_x, wand_tempo_y, 0.4)

    # Zurück in die Spur gefallen? Dann liegt sie wieder auf dem Kolben.
    if kugel_x > SPUR and kugel_y < BODEN_SPUR + KUGEL_RADIUS and tempo_y < 0:
        kugel_y = BODEN_SPUR + KUGEL_RADIUS
        tempo_x = 0
        tempo_y = -tempo_y * 0.3
        if tempo_y < 1:
            neue_kugel()

    # Die Kugel ist im Spielfeld: Klappe zu
    if not klappe_zu and kugel_x < SPUR - 15:
        klappe_zu = True
        klappe_zeichnen()

    # Nicht schneller als das Höchsttempo
    tempo = math.sqrt(tempo_x * tempo_x + tempo_y * tempo_y)
    if tempo > HOECHSTTEMPO:
        tempo_x = tempo_x * HOECHSTTEMPO / tempo
        tempo_y = tempo_y * HOECHSTTEMPO / tempo


def takt():
    global kraft, kugel_y, vorbei_seit
    if not laeuft:
        vorbei_seit = vorbei_seit + 1
    if not pausiert:
        for i in range(SCHRITTE):
            for f in flipper:
                flipper_drehen(f)
            if laeuft and not kugel_bereit:
                kleiner_schritt()

        if laeuft and kugel_bereit:
            if "feder" in gedrueckt:              # Feder spannen
                kraft = min(MAX_KRAFT, kraft + 0.4)
            kugel_y = BODEN_SPUR + KUGEL_RADIUS - kraft * ZUG

        if laeuft and kugel_y < UNTEN - 20:       # durch die Mitte gefallen
            kugel_verloren()

        bild_zeichnen()
    fenster.ontimer(takt, TAKT)


# ---------- Tasten ----------
def taste_merken(taste, name):
    fenster.onkeypress(lambda: gedrueckt.add(name), taste)
    fenster.onkeyrelease(lambda: gedrueckt.discard(name), taste)


for taste in ["Left", "a", "A"]:
    taste_merken(taste, "links")
for taste in ["Right", "d", "D"]:
    taste_merken(taste, "rechts")


def leertaste_gedrueckt():
    if not laeuft:
        if vorbei_seit > 30:               # eine halbe Sekunde warten
            neues_spiel()
        return
    gedrueckt.add("feder")


def leertaste_losgelassen():
    global kraft
    gedrueckt.discard("feder")
    if laeuft and kugel_bereit and not pausiert:
        if kraft >= 3:
            abschiessen()
        else:
            kraft = 0                      # zu schwach: nochmal spannen


def pause():
    global pausiert
    if not laeuft:
        return
    pausiert = not pausiert
    anzeige_zeigen()
    fenster.update()


fenster.onkeypress(leertaste_gedrueckt, "space")
fenster.onkeyrelease(leertaste_losgelassen, "space")
fenster.onkeypress(pause, "p")
fenster.onkeypress(pause, "P")
fenster.listen()

neues_spiel()
takt()
turtle.done()
