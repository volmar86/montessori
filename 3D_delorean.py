# ============================================================
#  DELOREAN 88 MPH CHALLENGE – PSEUDO-3D / MODE 7
#
#  Steuerung:
#    - A / D oder Pfeiltasten zum Lenken
#    - Touch / Maus: waagerecht ziehen, das Auto folgt der Bewegung
#    - ENTER, R oder Tippen für Menü / Neustart
#    - M: Musik An/Aus
# ============================================================

import pygame
import random
import math
import os
import time
import sys

# ====== EINSTELLUNGEN ======
BREITE = 800
HOEHE = 600
FPS = 60
HORIZONT_Y = 220                  # hier treffen sich Himmel und Boden

FARBE_RASEN_1 = (34, 139, 34)
FARBE_RASEN_2 = (25, 110, 25)
FARBE_STRASSE_1 = (50, 50, 55)
FARBE_STRASSE_2 = (60, 60, 65)
FARBE_BORDSTEIN_1 = (0, 255, 255)
FARBE_BORDSTEIN_2 = (0, 150, 200)
FARBE_MITTELLINIE = (235, 235, 235)
FARBE_DUNST = (95, 55, 105)       # so sieht alles ganz hinten am Horizont aus (Nebel/Dunst)
FARBE_TEXT = (255, 215, 0)

# ---------- Spielablauf ----------
LENK_TEMPO = 3.5                  # wie schnell man lenkt (ursprünglich 2.5)
TOUCH_EMPFINDLICHKEIT = 4.0       # Lenken mit Finger/Maus: so viele Spuren-Einheiten pro Bildschirmbreite Ziehen (spieler_x geht von -1.8 bis 1.8)
ENDE_SPERRE = 0.8                 # Sekunden nach Crash/Sieg, in denen ein Tippen noch ignoriert wird
TRAVEL_DAUER = 6.5                # so viele Sekunden dauert es vom Trigger bis 88 mph (Länge von 80to88)

# Schwierigkeitsgrade: (Startgeschwindigkeit mph, Beschleunigung mph pro Sekunde,
#                       Spawn-Faktor [kleiner = mehr Autos], Trigger-mph: ab hier läuft 80to88 und die
#                       Geschwindigkeit steigt im Takt des Sounds auf 88,
#                       Scroll-Faktor [1.0 = Straße und Autos so schnell wie ursprünglich, kleiner = langsamer = leichter])
# Dieselben Werte wie in delorean_pygame.py. Dort ist die Beschleunigung "pro Bild" (0.08 / 0.05 / 0.03),
# hier "pro Sekunde": dasselbe mal 60 (= 4.8 / 3.0 / 1.8).
# Spieldauer: Anfänger ~14 s, Mittel ~21 s, Experte ~34 s.
SCHWIERIGKEITEN = {
    "Anfänger": (40.0, 4.8, 1.4, 75.0, 0.6),
    "Mittel":   (25.0, 3.0, 1.0, 70.0, 0.8),
    "Experte":  (15.0, 1.8, 0.6, 65.0, 1.0),
}

# ---------- Hindernisse ----------
# Neue Autos kommen nach Zeit (nicht mehr "3 % pro Bild"), und jedes liegt weit genug neben dem vorigen:
# so entsteht keine Wand aus Autos, und es bleibt immer ein Weg frei.
SPAWN_ABSTAND_SEK = (0.9, 1.6)    # so viele Sekunden (zufällig zwischen den Werten) bis zum nächsten Auto
SPAWN_START_SEK = 1.5             # Pause am Anfang, bevor das erste Auto kommt
SPAWN_ENTFERNUNG = 400.0          # so weit vor dem Spieler erscheint ein Auto
SPUR_MAX = 0.75                   # äußerste Spur links/rechts
MIN_SPUR_ABSTAND = 0.5            # ein neues Auto muss mindestens so weit neben dem vorigen liegen

# ---------- Audio-Dateinamen ----------
AUDIO_MUSIK = "bttf midi.mp3"
AUDIO_TIME_CIRCUITS = "time_circuits.mp3"
AUDIO_TRAVEL = "80to88.mp3"

MUSIK_LAUTSTAERKE = 0.35   # normale Lautstärke der Musik (0.0 bis 1.0)
FADE_CRASH = 5.0           # so viele Sekunden wird die Musik nach einem Crash leiser
FADE_SIEG = 10.0           # ... und nach dem Sieg
FADE_TASTE_M = 1.0         # ... und wenn man mit M die Musik ausschaltet
TRAVEL_ENDE_MS = 400       # die letzten Millisekunden von 80to88 abschneiden (gegen das Knacksen am Ende)

# Größerer Audio-Puffer (Standard: 512): die Musik gracht nicht mehr, wenn das Spiel kurz beschäftigt ist.
# Preis: etwas mehr Verzögerung (~46 ms), bei Musik und Soundeffekten nicht zu hören.
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
try:
    pygame.mixer.init()
except Exception as e:
    print(f"[AUDIO WARNUNG] Kein Audiogerät: {e}")
fenster = pygame.display.set_mode((BREITE, HOEHE))
pygame.display.set_caption("DeLorean 88 mph Challenge – Pseudo-3D")
uhr = pygame.time.Clock()

font_ui = pygame.font.SysFont("Courier", 22, bold=True)
font_titel = pygame.font.SysFont("Courier", 32, bold=True)
font_sub = pygame.font.SysFont("Courier", 16, bold=True)


# ---------- Pfad-Finder für Audio ----------
def hole_audio_pfad(dateiname):
    """Ermittelt den Pfad der Audiodatei im 'Music'-Ordner oder im Hauptordner."""
    skript_ordner = os.path.dirname(os.path.abspath(__file__))
    mögliche_namen = [dateiname]
    if "_" in dateiname:
        mögliche_namen.append(dateiname.replace("_", ""))
    elif "80to88" in dateiname:
        mögliche_namen.append("80_to_88.mp3")

    for name in mögliche_namen:
        pfad_music = os.path.join(skript_ordner, "Music", name)
        pfad_direkt = os.path.join(skript_ordner, name)
        if os.path.exists(pfad_music):
            return pfad_music
        if os.path.exists(pfad_direkt):
            return pfad_direkt
    return os.path.join(skript_ordner, dateiname)


# ---------- Audio-Manager (Pygame Mixer, wie in delorean_pygame.py) ----------
sound_tc = None
sound_travel = None
musik_aktiv = True
musik_laeuft = False
musik_pausiert = False     # True = angehalten, läuft beim nächsten Start an derselben Stelle weiter
fade_start = None          # Zeitpunkt, an dem das Ausblenden begann (None = kein Ausblenden)
fade_dauer = FADE_CRASH

try:
    pfad_tc = hole_audio_pfad(AUDIO_TIME_CIRCUITS)
    if os.path.exists(pfad_tc):
        sound_tc = pygame.mixer.Sound(pfad_tc)

    pfad_tr = hole_audio_pfad(AUDIO_TRAVEL)
    if os.path.exists(pfad_tr):
        sound_travel = pygame.mixer.Sound(pfad_tr)

    pfad_bgm = hole_audio_pfad(AUDIO_MUSIK)
    if os.path.exists(pfad_bgm):
        pygame.mixer.music.load(pfad_bgm)
except Exception as e:
    print(f"[AUDIO WARNUNG] Audio konnte nicht vollständig geladen werden: {e}")


def sfx_time_circuits_starten():
    if musik_aktiv and sound_tc:
        sound_tc.stop()
        sound_tc.play()

def sfx_travel_starten():
    if musik_aktiv and sound_travel:
        sound_travel.stop()
        sound_travel.play(maxtime=max(1, int(sound_travel.get_length() * 1000) - TRAVEL_ENDE_MS))   # Ende abschneiden

def musik_starten():
    """Startet die Musik – oder lässt sie dort weiterlaufen, wo sie angehalten wurde."""
    global musik_laeuft, musik_pausiert, fade_start
    if not musik_aktiv:
        return
    fade_start = None                    # ein laufendes Ausblenden abbrechen
    try:
        if musik_pausiert:
            pygame.mixer.music.set_volume(MUSIK_LAUTSTAERKE)
            pygame.mixer.music.unpause()     # weiter an derselben Stelle
            musik_pausiert = False
        elif not musik_laeuft and os.path.exists(hole_audio_pfad(AUDIO_MUSIK)):
            pygame.mixer.music.set_volume(MUSIK_LAUTSTAERKE)
            pygame.mixer.music.play(-1)      # Endlosschleife, von vorne
            musik_laeuft = True
        else:
            pygame.mixer.music.set_volume(MUSIK_LAUTSTAERKE)
    except Exception as e:
        print(f"[AUDIO] Fehler beim Starten der Musik: {e}")

def musik_stoppen(dauer=FADE_CRASH):
    """Blendet die Musik langsam aus und hält sie dann an (Pause, nicht Stopp)."""
    global fade_start, fade_dauer
    if musik_laeuft and not musik_pausiert and fade_start is None:
        fade_start = time.time()
        fade_dauer = dauer

def musik_fade_aktualisieren():
    """Wird in jedem Bild aufgerufen: macht die Musik ein bisschen leiser."""
    global fade_start, musik_pausiert
    if fade_start is None:
        return
    verstrichen = time.time() - fade_start
    if verstrichen < fade_dauer:
        pygame.mixer.music.set_volume(MUSIK_LAUTSTAERKE * (1.0 - verstrichen / fade_dauer))
    else:
        pygame.mixer.music.pause()           # anhalten, die Stelle bleibt gemerkt
        musik_pausiert = True
        fade_start = None


# ====== GAME VARIABLES ======
pos_z = 0.0
spieler_x = 0.0
geschwindigkeit_mph = 30.0
ziel_geschwindigkeit = 88.0
status = "MENÜ"
kurven_neigung = 0.0

schwierigkeitsgrade = list(SCHWIERIGKEITEN)
schwierigkeit_index = 1

start_travel_zeit = 0.0     # Zeitpunkt, an dem 80to88 gestartet wurde
spawn_timer = SPAWN_START_SEK   # Sekunden bis zum nächsten Auto
letzte_spur = 0.0           # Spur des zuletzt erzeugten Autos
ende_zeit = 0.0             # Zeitpunkt von Crash oder Sieg (damit ein Tippen nicht sofort das Menü öffnet)
touch_richtung = 0.0        # nur für die Neigung des Autos beim Ziehen: +1 = nach links, -1 = nach rechts, klingt ab

hindernisse = []   # Liste von [pos_z, spur]   spur: -1 = linker Rand, 0 = Mitte, +1 = rechter Rand


# ---------- Die Straße: wie breit und wo, in einer bestimmten Bildschirmzeile ----------
def strassen_breite(perspektive):
    """perspektive: 0 = ganz hinten am Horizont, 1 = ganz unten am Bildschirm."""
    return 100 + perspektive * 550


def strassen_mitte(perspektive):
    """Wenn man lenkt, bewegt sich die Straße – vorne mehr als hinten."""
    return BREITE / 2 + spieler_x * perspektive * 120


def mischen(farbe1, farbe2, anteil):
    """Mischt zwei Farben: anteil 0 = nur farbe1, anteil 1 = nur farbe2."""
    return tuple(int(a + (b - a) * anteil) for a, b in zip(farbe1, farbe2))


# ---------- Himmel (wird nur EINMAL gezeichnet) ----------
def erstelle_himmel():
    himmel = pygame.Surface((BREITE, HORIZONT_Y))

    # Farbverlauf: oben Nachtblau, in der Mitte Lila, am Horizont Orange-Rosa
    oben, mitte, unten = (8, 6, 28), (60, 22, 90), (255, 120, 90)
    for y in range(HORIZONT_Y):
        t = y / HORIZONT_Y
        if t < 0.55:
            farbe = mischen(oben, mitte, t / 0.55)
        else:
            farbe = mischen(mitte, unten, (t - 0.55) / 0.45)
        pygame.draw.line(himmel, farbe, (0, y), (BREITE, y))

    # Sterne (immer an denselben Stellen)
    zufall = random.Random(88)
    for i in range(90):
        x = zufall.randint(0, BREITE)
        y = zufall.randint(0, int(HORIZONT_Y * 0.6))
        hell = zufall.randint(120, 255)
        himmel.set_at((x, y), (hell, hell, hell))
        if zufall.random() < 0.15:                       # ein paar größere Sterne
            pygame.draw.circle(himmel, (hell, hell, hell), (x, y), 1)

    # Die 80er-Jahre-Sonne: halbe Scheibe mit Streifen
    sonne_r = 75
    for y in range(HORIZONT_Y - sonne_r, HORIZONT_Y):
        halbe_breite = math.sqrt(max(0, sonne_r ** 2 - (y - HORIZONT_Y) ** 2))   # Kreis: x² + y² = r²
        t = (y - (HORIZONT_Y - sonne_r)) / sonne_r       # 0 = oben, 1 = unten
        streifen = (y - (HORIZONT_Y - sonne_r)) % 12      # Lücken werden nach unten dicker
        if t > 0.4 and streifen < (t - 0.4) * 12:
            continue
        farbe = mischen((255, 230, 90), (255, 60, 140), t)
        pygame.draw.line(himmel, farbe, (BREITE / 2 - halbe_breite, y), (BREITE / 2 + halbe_breite, y))
    return himmel


def erstelle_berge(breite, hoehe_max, farbe, saat):
    """Eine Bergkette als Silhouette (breiter als der Bildschirm, damit sie sich verschieben kann)."""
    surf = pygame.Surface((breite, hoehe_max), pygame.SRCALPHA)
    zufall = random.Random(saat)
    punkte = [(0, hoehe_max)]
    x = 0
    while x <= breite:
        punkte.append((x, zufall.randint(int(hoehe_max * 0.25), hoehe_max - 8)))
        x += zufall.randint(30, 70)
    punkte.append((breite, hoehe_max))
    pygame.draw.polygon(surf, farbe, punkte)
    return surf


def erstelle_stadt(breite, hoehe):
    """Eine kleine Stadt-Silhouette mit Uhrturm."""
    surf = pygame.Surface((breite, hoehe), pygame.SRCALPHA)
    zufall = random.Random(1955)
    farbe = (25, 12, 40)
    x = breite // 2 - 170
    while x < breite // 2 + 170:
        w = zufall.randint(14, 30)
        h = zufall.randint(10, 32)
        pygame.draw.rect(surf, farbe, (x, hoehe - h, w, h))
        for i in range(zufall.randint(0, 3)):           # ein paar beleuchtete Fenster
            fx = x + zufall.randint(2, max(3, w - 4))
            fy = hoehe - zufall.randint(4, max(5, h - 3))
            surf.set_at((fx, fy), (255, 210, 120))
        x += w + zufall.randint(0, 4)
    # der Uhrturm
    tx = breite // 2 - 60
    pygame.draw.rect(surf, farbe, (tx - 14, hoehe - 40, 28, 40))
    pygame.draw.rect(surf, farbe, (tx - 9, hoehe - 62, 18, 24))
    pygame.draw.polygon(surf, farbe, [(tx - 11, hoehe - 62), (tx + 11, hoehe - 62), (tx, hoehe - 78)])
    pygame.draw.circle(surf, (255, 235, 170), (tx, hoehe - 50), 6)       # leuchtendes Zifferblatt
    pygame.draw.line(surf, farbe, (tx, hoehe - 50), (tx, hoehe - 54), 1)  # Zeiger
    pygame.draw.line(surf, farbe, (tx, hoehe - 50), (tx + 3, hoehe - 50), 1)
    return surf


himmel_img = erstelle_himmel()
berge_hinten = erstelle_berge(BREITE + 200, 70, (70, 30, 90), saat=7)
berge_vorne = erstelle_berge(BREITE + 200, 45, (45, 20, 65), saat=21)
stadt_img = erstelle_stadt(BREITE + 200, 80)


def zeichne_himmel():
    fenster.blit(himmel_img, (0, 0))
    # Parallaxe: was weiter weg ist, bewegt sich beim Lenken weniger
    fenster.blit(berge_hinten, (-100 + spieler_x * 8, HORIZONT_Y - 70))
    fenster.blit(stadt_img, (-100 + spieler_x * 14, HORIZONT_Y - 80))
    fenster.blit(berge_vorne, (-100 + spieler_x * 20, HORIZONT_Y - 45))


# ---------- Boden und Straße (jede Bildschirmzeile einzeln) ----------
# Fast alles pro Zeile ändert sich nie (Perspektive, Breite, Dunst-Farben). Das wird nur EINMAL berechnet:
# so bleibt pro Bild nur noch das Nötige übrig, und das Spiel (und die Musik daneben) hat mehr Luft.
def erstelle_zeilen_tabelle():
    zeilen = []
    farb_paare = [(FARBE_RASEN_1, FARBE_STRASSE_1, FARBE_BORDSTEIN_1),      # "hell"  (abwechseln = True)
                  (FARBE_RASEN_2, FARBE_STRASSE_2, FARBE_BORDSTEIN_2)]      # "dunkel"
    for y in range(HORIZONT_Y, HOEHE):
        perspektive = (y - HORIZONT_Y) / (HOEHE - HORIZONT_Y)
        # Dunst: ganz hinten verschwimmen die Farben mit dem Horizont
        dunst = max(0.0, 1.0 - (y - HORIZONT_Y) / 110)
        farben = [(mischen(rasen, FARBE_DUNST, dunst),
                   mischen(strasse, FARBE_DUNST, dunst * 0.8),
                   mischen(bord, FARBE_DUNST, dunst * 0.6)) for rasen, strasse, bord in farb_paare]
        zeilen.append((
            y,
            (1.0 / (perspektive + 0.001)) * 20.0,              # Versatz für die Streifen
            strassen_breite(perspektive) / 2,                  # halbe Straßenbreite in dieser Zeile
            perspektive * 120,                                 # wie stark die Straße beim Lenken wandert
            max(1, perspektive * 5),                           # halbe Breite der Mittellinie
            mischen(FARBE_MITTELLINIE, FARBE_DUNST, dunst),    # Farbe der Mittellinie
            farben[0],
            farben[1],
        ))
    return zeilen


ZEILEN_TABELLE = erstelle_zeilen_tabelle()


def zeichne_pseudo_3d_welt():
    zeichne_himmel()

    mitte_basis = BREITE / 2
    for y, z_versatz, halbe_breite, lenk_faktor, halb, linie, farben_hell, farben_dunkel in ZEILEN_TABELLE:
        abwechseln = int((pos_z + z_versatz) / 15.0) % 2 == 0
        rasen, strasse, bord = farben_hell if abwechseln else farben_dunkel
        mitte = mitte_basis + spieler_x * lenk_faktor

        # fill() mit einem 1 Pixel hohen Rechteck ist schneller als draw.line() und ergibt dasselbe Bild.
        # (x0 nie kleiner als 0: pygame schneidet ein Rechteck, das links aus dem Bild ragt, rechts nicht richtig ab)
        fenster.fill(rasen, (0, y, BREITE, 1))
        pygame.draw.line(fenster, bord, (mitte - halbe_breite - 12, y), (mitte + halbe_breite + 12, y), 2)
        x0 = max(0, int(mitte - halbe_breite))
        fenster.fill(strasse, (x0, y, int(mitte + halbe_breite) - x0 + 1, 1))

        # gestrichelte Mittellinie (wird vorne breiter)
        if abwechseln:
            x0 = max(0, int(mitte - halb))
            fenster.fill(linie, (x0, y, int(mitte + halb) - x0 + 1, 1))


# ---------- Autos ----------
def erstelle_delorean_sprite():
    """Erstellt das DeLorean-Sprite für die 3D-Ansicht (von hinten)."""
    surf = pygame.Surface((80, 45), pygame.SRCALPHA)
    pygame.draw.rect(surf, (200, 200, 205), (10, 12, 60, 25), border_radius=4)
    pygame.draw.rect(surf, (40, 40, 50), (18, 15, 44, 12), border_radius=2)
    pygame.draw.rect(surf, (220, 20, 60), (12, 32, 18, 4))
    pygame.draw.rect(surf, (220, 20, 60), (50, 32, 18, 4))
    pygame.draw.rect(surf, (20, 20, 20), (2, 22, 10, 18), border_radius=2)
    pygame.draw.rect(surf, (20, 20, 20), (68, 22, 10, 18), border_radius=2)
    return surf


def erstelle_auto_rot_sprite():
    """Das rote Hindernis-Auto, von hinten gesehen."""
    surf = pygame.Surface((80, 45), pygame.SRCALPHA)
    pygame.draw.rect(surf, (20, 20, 20), (4, 26, 12, 17), border_radius=2)      # Reifen
    pygame.draw.rect(surf, (20, 20, 20), (64, 26, 12, 17), border_radius=2)
    pygame.draw.rect(surf, (190, 0, 0), (8, 14, 64, 26), border_radius=6)       # Karosserie
    pygame.draw.rect(surf, (225, 35, 35), (18, 4, 44, 16), border_radius=5)     # Dach
    pygame.draw.rect(surf, (40, 50, 60), (22, 7, 36, 10), border_radius=3)      # Heckscheibe
    pygame.draw.rect(surf, (255, 200, 60), (11, 28, 13, 5), border_radius=1)    # Rücklichter
    pygame.draw.rect(surf, (255, 200, 60), (56, 28, 13, 5), border_radius=1)
    return surf


delorean_base = erstelle_delorean_sprite()
auto_rot_base = erstelle_auto_rot_sprite()


# ---------- Feuerspuren (bei 88 mph: die DeLorean verschwindet, zwei Flammenlinien bleiben auf der Straße) ----------
FEUER_FARBEN = [(255, 69, 0), (255, 140, 0), (255, 215, 0)]
FEUER_AUTO_Y = 520                # Höhe auf dem Bildschirm, wo die DeLorean steht (wie beim Zeichnen des Autos)
FEUER_REIFEN_ABSTAND = 30         # so viele Pixel liegen die Reifen links/rechts von der Auto-Mitte


def feuer_spuren_zeichnen():
    """Zwei Flammenlinien von den Reifen bis zum Horizont. Sie laufen in der Perspektive zusammen
    (gleiche Formeln wie bei der Straße) und flackern in jedem Bild neu."""
    p0 = (FEUER_AUTO_Y - HORIZONT_Y) / (HOEHE - HORIZONT_Y)           # Perspektive auf Höhe des Autos
    halbe_breite0 = strassen_breite(p0) / 2
    spur_auto = (BREITE / 2 - strassen_mitte(p0)) / halbe_breite0     # auf welcher Spur das Auto stand

    for seite in (-1, 1):
        spur = spur_auto + seite * FEUER_REIFEN_ABSTAND / halbe_breite0
        p = p0
        while p > 0.04:                                               # vom Auto (nah) zum Horizont (fern)
            y = HORIZONT_Y + p * (HOEHE - HORIZONT_Y)
            x = strassen_mitte(p) + spur * strassen_breite(p) / 2
            dunst = max(0.0, 1.0 - p / 0.25) * 0.7                    # ganz hinten verschwimmt das Feuer im Dunst

            for _ in range(2):                                        # zwei Flammen pro Schritt: dichter und lebendiger
                r = max(1, int(p * 14 * random.uniform(0.6, 1.25)))
                fx = x + random.uniform(-1, 1) * p * 7
                fy = y - random.uniform(0, 1) * p * 16                # Flammen züngeln nach oben
                farbe = mischen(random.choice(FEUER_FARBEN), FARBE_DUNST, dunst)
                pygame.draw.circle(fenster, mischen((170, 25, 0), FARBE_DUNST, dunst), (fx, fy), int(r * 1.6) + 1)   # Glut-Rand
                pygame.draw.circle(fenster, farbe, (fx, fy), r)                                                      # Flamme
                if random.random() < 0.6:
                    pygame.draw.circle(fenster, mischen((255, 245, 190), FARBE_DUNST, dunst), (fx, fy), max(1, r // 2))   # heißer Kern
            p *= 0.93


# ---------- Tachometer (unten links) ----------
# Nachgebaut nach dem Film-Tacho: weiße mph-Zahlen 15 bis 95 (55 rot, ganz oben),
# innen blaue km/h-Zahlen, unten eine Digitalanzeige.
TACHO_X = 95                      # Mitte des Tachos
TACHO_Y = HOEHE - 95
TACHO_RADIUS = 80
TACHO_ANFANG = 15                 # kleinste Zahl (unten links)
TACHO_MAX = 95                    # größte Zahl (unten rechts). Im Film: extra gebauter Tacho bis 95 mph
TACHO_OBEN = 55                   # diese Zahl steht ganz oben
TACHO_GRAD_PRO_MPH = 3.05                                   # so viele Grad dreht der Zeiger pro mph
TACHO_ZAHLEN = [15, 25, 35, 45, 55, 65, 75, 85, 95]         # weiße mph-Zahlen
TACHO_ROTE_ZAHLEN = [55]                                    # diese Zahlen sind rot
TACHO_KMH = [40, 60, 80, 100, 120, 140, 160]                # blaue km/h-Zahlen innen
FARBE_KMH = (122, 167, 224)

font_tacho = pygame.font.SysFont("Arial", 13, bold=True)
font_kmh = pygame.font.SysFont("Arial", 9, bold=True)
font_tacho_klein = pygame.font.SysFont("Arial", 9)
font_mph = pygame.font.SysFont("Arial", 12, bold=True)
font_digital = pygame.font.SysFont("Courier", 22, bold=True)


def tacho_winkel(mph, begrenzen=True):
    """Rechnet mph in einen Winkel um: 55 mph = oben (90°), kleiner = weiter links, größer = weiter rechts."""
    if begrenzen:
        mph = max(TACHO_ANFANG - 5, min(mph, TACHO_MAX + 4))   # der Zeiger bleibt an den Enden stehen
    return 90 - (mph - TACHO_OBEN) * TACHO_GRAD_PRO_MPH


def punkt_auf_kreis(mitte_x, mitte_y, winkel, abstand):
    """Ein Punkt in Richtung 'winkel'. Achtung: in pygame zeigt y nach UNTEN, deshalb minus."""
    w = math.radians(winkel)
    return mitte_x + abstand * math.cos(w), mitte_y - abstand * math.sin(w)


def erstelle_tacho_surface():
    """Zeichnet das Zifferblatt EINMAL auf ein eigenes Bild (das ist schneller als jedes Mal neu)."""
    groesse = TACHO_RADIUS * 2 + 10
    surf = pygame.Surface((groesse, groesse), pygame.SRCALPHA)
    m = groesse // 2                                       # Mitte auf diesem kleinen Bild
    pygame.draw.circle(surf, (192, 192, 192), (m, m), TACHO_RADIUS + 4)   # silberner Rand
    pygame.draw.circle(surf, (17, 17, 17), (m, m), TACHO_RADIUS)         # dunkle Scheibe

    # weiße Striche alle 5 mph: lang bei den Zahlen (15, 25 ...), kurz dazwischen (20, 30 ...)
    for mph in range(TACHO_ANFANG, TACHO_MAX + 1, 5):
        w = tacho_winkel(mph)
        lang = mph in TACHO_ZAHLEN
        innen = punkt_auf_kreis(m, m, w, TACHO_RADIUS - (13 if lang else 8))
        aussen = punkt_auf_kreis(m, m, w, TACHO_RADIUS - 3)
        pygame.draw.line(surf, (255, 255, 255), innen, aussen, 4 if lang else 2)

    # weiße (und rote) mph-Zahlen
    for mph in TACHO_ZAHLEN:
        x, y = punkt_auf_kreis(m, m, tacho_winkel(mph), TACHO_RADIUS - 25)
        farbe = (255, 40, 40) if mph in TACHO_ROTE_ZAHLEN else (255, 255, 255)
        zahl = font_tacho.render(str(mph), True, farbe)
        surf.blit(zahl, zahl.get_rect(center=(x, y)))

    # blaue km/h-Zahlen mit kleinem Quadrat (1 mph = 1.609 km/h)
    for kmh in TACHO_KMH:
        w = tacho_winkel(kmh / 1.609344, begrenzen=False)
        qx, qy = punkt_auf_kreis(m, m, w, TACHO_RADIUS - 16)
        pygame.draw.rect(surf, FARBE_KMH, (qx - 2, qy - 2, 5, 5))
        x, y = punkt_auf_kreis(m, m, w, TACHO_RADIUS - 40)
        zahl = font_kmh.render(str(kmh), True, FARBE_KMH)
        surf.blit(zahl, zahl.get_rect(center=(x, y)))

    # Beschriftung unten: km/h klein, MPH groß
    kmh_text = font_tacho_klein.render("km/h", True, (140, 140, 140))
    surf.blit(kmh_text, kmh_text.get_rect(center=(m, m + 21)))
    mph_text = font_mph.render("MPH", True, (255, 255, 255))
    surf.blit(mph_text, mph_text.get_rect(center=(m, m + 33)))

    # Rahmen der Digitalanzeige (unten im Tacho)
    rahmen = pygame.Rect(0, 0, 58, 26)
    rahmen.center = (m, m + 56)
    pygame.draw.rect(surf, (26, 0, 0), rahmen)
    pygame.draw.rect(surf, (105, 105, 105), rahmen, 2)
    return surf


tacho_img = erstelle_tacho_surface()


def tacho_zeichnen(mph):
    """Zifferblatt, Zeiger und Digitalanzeige auf den Bildschirm."""
    fenster.blit(tacho_img, tacho_img.get_rect(center=(TACHO_X, TACHO_Y)))
    w = tacho_winkel(mph)
    hinten = punkt_auf_kreis(TACHO_X, TACHO_Y, w + 180, 12)      # kurzes Stück hinter der Mitte
    spitze = punkt_auf_kreis(TACHO_X, TACHO_Y, w, TACHO_RADIUS - 12)
    pygame.draw.line(fenster, (255, 69, 0), hinten, spitze, 3)
    pygame.draw.circle(fenster, (192, 192, 192), (TACHO_X, TACHO_Y), 6)   # Kappe in der Mitte

    zahl = font_digital.render(str(int(mph)), True, (255, 69, 0))     # int(): 87.9 zeigt 87, erst bei 88 steht 88
    fenster.blit(zahl, zahl.get_rect(center=(TACHO_X, TACHO_Y + 56)))


def hole_schwierigkeits_parameter():
    """Gibt (Startgeschwindigkeit, Beschleunigung, Spawn-Faktor, Trigger-Geschwindigkeit, Scroll-Faktor) zurück."""
    return SCHWIERIGKEITEN[schwierigkeitsgrade[schwierigkeit_index]]


def schwierigkeit_wechseln():
    global schwierigkeit_index
    schwierigkeit_index = (schwierigkeit_index + 1) % len(schwierigkeitsgrade)


def musik_umschalten():
    global musik_aktiv
    musik_aktiv = not musik_aktiv
    if musik_aktiv:
        musik_starten()
    else:
        musik_stoppen(FADE_TASTE_M)


def spiel_starten():
    global status, geschwindigkeit_mph, pos_z, spieler_x, spawn_timer, letzte_spur, kurven_neigung
    status = "LÄUFT"
    geschwindigkeit_mph = hole_schwierigkeits_parameter()[0]
    pos_z = 0.0
    spieler_x = 0.0
    kurven_neigung = 0.0
    hindernisse.clear()
    spawn_timer = SPAWN_START_SEK
    letzte_spur = 0.0
    if sound_tc:
        sound_tc.stop()
    if sound_travel:
        sound_travel.stop()


def zum_menue():
    """Zurück ins Menü (nach Crash oder Sieg)."""
    global status
    status = "MENÜ"
    hindernisse.clear()
    if sound_travel:
        sound_travel.stop()
    if musik_aktiv:
        musik_starten()          # Time-Circuits-Sound nur beim allerersten Start, nicht bei jedem Menü


def text_mit_glanz_zeichnen(text, font, farbe, x, y):
    """Zeichnet einen retro Neon-Text mit Schatten-Effekt."""
    schatten = font.render(text, True, (0, 0, 0))
    vordergrund = font.render(text, True, farbe)
    fenster.blit(schatten, schatten.get_rect(center=(x + 2, y + 2)))
    fenster.blit(vordergrund, vordergrund.get_rect(center=(x, y)))


def menue_zeichnen():
    box = pygame.Surface((520, 360), pygame.SRCALPHA)
    box.fill((0, 0, 0, 220))
    fenster.blit(box, (140, 120))

    text_mit_glanz_zeichnen("⚡ DELOREAN 88 MPH ⚡", font_titel, FARBE_TEXT, 400, 160)
    text_mit_glanz_zeichnen("[ ENTER / TIPPEN ] SPIEL STARTEN", font_ui, (255, 255, 255), 400, 230)

    diff_str = f"[ D ] SCHWIERIGKEIT: < {schwierigkeitsgrade[schwierigkeit_index]} >"
    text_mit_glanz_zeichnen(diff_str, font_ui, (0, 255, 255), 400, 290)

    m_farbe = (144, 238, 144) if musik_aktiv else (220, 20, 60)
    m_str = f"[ M ] MUSIK: < {'AN' if musik_aktiv else 'AUS'} >"
    text_mit_glanz_zeichnen(m_str, font_ui, m_farbe, 400, 350)

    sub = font_sub.render("Steuerung: A/D, Pfeiltasten oder Finger ziehen", True, (180, 180, 180))
    fenster.blit(sub, sub.get_rect(center=(400, 430)))


# ====== HAUPTSCHLEIFE ======
laufend = True
if musik_aktiv:
    sfx_time_circuits_starten()      # Time-Circuits-Sound nur beim allerersten Start
    musik_starten()

while laufend:
    dt = uhr.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            laufend = False
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RETURN, pygame.K_r]:
                if status == "MENÜ":
                    spiel_starten()
                elif status in ["CRASH", "SIEG"]:
                    zum_menue()
            elif event.key == pygame.K_d and status == "MENÜ":
                schwierigkeit_wechseln()
            elif event.key == pygame.K_m:
                musik_umschalten()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos           # bei Touch ist das die Stelle, wo der Finger tippt
            if status == "MENÜ":
                if 200 < mx < 600 and 200 < my < 260:
                    spiel_starten()
                elif 200 < mx < 600 and 270 < my < 330:
                    schwierigkeit_wechseln()
                elif 200 < mx < 600 and 340 < my < 400:
                    musik_umschalten()
            elif status in ["CRASH", "SIEG"] and time.time() - ende_zeit > ENDE_SPERRE:
                zum_menue()              # Tippen = zurück ins Menü

        # Lenken mit dem Finger: waagerecht ziehen, das Auto bewegt sich mit (relativ, der Finger muss nicht auf dem Auto sein).
        # Achtung: spieler_x ist "falsch herum": nach rechts ziehen = spieler_x kleiner (die Straße wandert nach links).
        elif event.type == pygame.FINGERMOTION and status == "LÄUFT":
            spieler_x -= event.dx * TOUCH_EMPFINDLICHKEIT
            if event.dx:
                touch_richtung = -1.0 if event.dx > 0 else 1.0

        # Dasselbe mit der Maus (Ziehen mit gedrückter linker Taste); vom Finger erzeugte Mausereignisse werden übersprungen
        elif event.type == pygame.MOUSEMOTION and status == "LÄUFT":
            if event.buttons[0] and not getattr(event, "touch", False):
                spieler_x -= event.rel[0] / BREITE * TOUCH_EMPFINDLICHKEIT
                if event.rel[0]:
                    touch_richtung = -1.0 if event.rel[0] > 0 else 1.0

    if status == "MENÜ":
        pos_z += 120.0 * dt                  # die Straße rollt langsam im Hintergrund des Menüs

    elif status == "LÄUFT":
        _, beschleunigung, spawn_faktor, trigger_mph, scroll_faktor = hole_schwierigkeits_parameter()

        if geschwindigkeit_mph < trigger_mph:
            geschwindigkeit_mph += beschleunigung * dt
            if geschwindigkeit_mph >= trigger_mph:
                geschwindigkeit_mph = trigger_mph
                start_travel_zeit = time.time()
                sfx_travel_starten()
        else:
            # Von hier bis 88 mph vergehen genau TRAVEL_DAUER Sekunden: im Takt des 80to88-Sounds
            verstrichen = time.time() - start_travel_zeit
            geschwindigkeit_mph = trigger_mph + (verstrichen / TRAVEL_DAUER) * (ziel_geschwindigkeit - trigger_mph)
            if geschwindigkeit_mph >= ziel_geschwindigkeit:
                geschwindigkeit_mph = ziel_geschwindigkeit
                status = "SIEG"
                ende_zeit = time.time()
                musik_stoppen(FADE_SIEG)

        pos_z += geschwindigkeit_mph * 5.0 * dt * scroll_faktor      # scroll_faktor: Straße und Autos langsamer (leichter)

        # Lenkung & F-Zero Neigungseffekt
        tasten = pygame.key.get_pressed()
        lenk_richtung = 0
        if tasten[pygame.K_a] or tasten[pygame.K_LEFT]:
            lenk_richtung = 1
        if tasten[pygame.K_d] or tasten[pygame.K_RIGHT]:
            lenk_richtung = -1

        spieler_x += lenk_richtung * LENK_TEMPO * dt
        spieler_x = max(-1.8, min(1.8, spieler_x))
        touch_richtung *= 0.8                                    # die Neigung vom Ziehen klingt von selbst ab
        kurven_neigung = -max(-1.0, min(1.0, lenk_richtung + touch_richtung)) * 12.0

        # Spawnen von Hindernissen (spur: wo auf der Straße, -0.75 = links ... +0.75 = rechts)
        # Nach Zeit, nicht nach Bildern; und die neue Spur liegt immer mindestens MIN_SPUR_ABSTAND neben der vorigen.
        spawn_timer -= dt
        if spawn_timer <= 0:
            spur = random.uniform(-SPUR_MAX, SPUR_MAX)
            while abs(spur - letzte_spur) < MIN_SPUR_ABSTAND:
                spur = random.uniform(-SPUR_MAX, SPUR_MAX)
            hindernisse.append([pos_z + SPAWN_ENTFERNUNG, spur])
            letzte_spur = spur
            # Geteilt durch scroll_faktor: läuft die Straße langsamer, kommen auch die Autos seltener,
            # sonst stünden sie enger hintereinander und das Spiel wäre nicht leichter
            spawn_timer = random.uniform(*SPAWN_ABSTAND_SEK) * spawn_faktor / scroll_faktor

    # 1. Pseudo-3D Welt rendern
    zeichne_pseudo_3d_welt()

    # 2. Hitbox der DeLorean auf dem Bildschirm
    spieler_rect = pygame.Rect(BREITE // 2 - 35, 500, 70, 35)

    # 3. Hindernisse: erst die weit entfernten zeichnen, dann die nahen (sonst überdecken die fernen die nahen)
    hindernisse.sort(key=lambda h: -h[0])
    for h in hindernisse[:]:
        rel_z = h[0] - pos_z

        # Sobald das Hindernis hinter der Kamera ist, sofort löschen
        if rel_z <= 12.0:
            hindernisse.remove(h)
            continue

        if rel_z < 400.0:
            perspektive = 20.0 / rel_z                       # dieselbe Formel wie bei den Straßenstreifen
            screen_y = HORIZONT_Y + perspektive * (HOEHE - HORIZONT_Y)
            # Das Auto steht AUF der Straße: Mitte der Straße + Spur * halbe Straßenbreite
            screen_x = strassen_mitte(perspektive) + h[1] * strassen_breite(perspektive) / 2
            auto_breite = max(6, int(strassen_breite(perspektive) * 0.15))
            auto_hoehe = max(3, int(auto_breite * 45 / 80))

            if screen_y < HOEHE + 50:
                h_rect = pygame.Rect(0, 0, auto_breite, auto_hoehe)
                h_rect.midbottom = (screen_x, screen_y)
                bild = pygame.transform.smoothscale(auto_rot_base, (auto_breite, auto_hoehe))
                fenster.blit(bild, h_rect)

                # Faire Kollision: echte Überlappung auf dem Bildschirm, etwas verkleinert
                if status == "LÄUFT" and spieler_rect.inflate(-12, -12).colliderect(h_rect.inflate(-6, -4)):
                    status = "CRASH"
                    ende_zeit = time.time()
                    if sound_travel:
                        sound_travel.stop()      # nach einem Crash gibt es keine Zeitreise
                    musik_stoppen(FADE_CRASH)

    # Musik ausblenden (nach Crash, Sieg oder Taste M)
    musik_fade_aktualisieren()

    # Feuerspuren nach dem Zeitsprung (die DeLorean ist dann verschwunden)
    if status == "SIEG":
        feuer_spuren_zeichnen()

    # 4. DeLorean zeichnen
    if status != "SIEG":
        gedrehtes_auto = pygame.transform.rotate(delorean_base, kurven_neigung)
        rect = gedrehtes_auto.get_rect(center=(BREITE // 2, 520))
        fenster.blit(gedrehtes_auto, rect)

    # 5. Tacho und Text (im Menü kein Tacho: die Menü-Box würde ihn überdecken)
    if status == "MENÜ":
        menue_zeichnen()
    else:
        tacho_zeichnen(min(geschwindigkeit_mph, ziel_geschwindigkeit))

    if status == "CRASH":
        txt_c = font_titel.render("CRASH! [ENTER / TIPPEN]", True, (255, 69, 0))
        fenster.blit(txt_c, txt_c.get_rect(center=(BREITE // 2, 300)))
    elif status == "SIEG":
        txt_s = font_titel.render("88 MPH! ZEITREISE! [ENTER / TIPPEN]", True, FARBE_TEXT)
        fenster.blit(txt_s, txt_s.get_rect(center=(BREITE // 2, 300)))

    pygame.display.flip()

pygame.quit()
sys.exit()
