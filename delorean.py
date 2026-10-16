# ============================================================
#  DELOREAN 88 MPH CHALLENGE – MIT STARTMENÜ & DYNAMISCHEM AUDIO
#  
#  Menü-Steuerung:
#    - ENTER oder Klick auf START: Spiel beginnen
#    - Taste D oder Klick: Schwierigkeit ändern (Anfänger / Mittel / Experte)
#    - Taste M oder Klick: Musik An/Aus
#  
#  Spiel-Steuerung:
#    - A / D oder Pfeiltasten zum Lenken
#    - R oder ENTER nach Spielende für Neustart / Menü
# ============================================================

import turtle
import random
import time
import os
import ctypes
import math

# ====== EINSTELLUNGEN ======
BREITE = 800
HOEHE = 600
FPS_TAKT = 16  # ca. 60 FPS

FARBE_STRASSE = "#323232"
FARBE_RASEN = "#228B22"
FARBE_NEON_BLAU = "#00FFFF"
FARBE_FEUER_ORANGE = "#FF4500"

# ---------- Audio-Dateinamen ----------
AUDIO_MUSIK = "bttf midi.mp3"
AUDIO_TIME_CIRCUITS = "time_circuits.mp3"
AUDIO_TRAVEL = "80to88.mp3"

MUSIK_LAUTSTAERKE = 350   # normale Lautstärke der Musik (MCI: 0 bis 1000)
FADE_CRASH = 5.0          # so viele Sekunden wird die Musik nach einem Crash leiser
FADE_SIEG = 10.0          # ... und nach dem Sieg
FADE_TASTE_M = 1.0        # ... und wenn man mit M die Musik ausschaltet
TRAVEL_ENDE_MS = 400      # die letzten Millisekunden von 80to88 abschneiden (gegen das Knacksen am Ende)
AUDIO_DEBUG = False       # True = Audio-Meldungen in der Shell anzeigen (zum Fehlersuchen)

musik_aktiv = True
musik_laeuft = False      # Boolean-Flag: Ist die Hintergrundmusik geöffnet und gestartet?
musik_pausiert = False    # True = angehalten, läuft beim nächsten Start an derselben Stelle weiter
fade_start = None         # Zeitpunkt, an dem das Ausblenden begann (None = kein Ausblenden)
fade_dauer = FADE_CRASH
letzter_vol_wert = MUSIK_LAUTSTAERKE  # Lautstärke-Tracker für stufenloses Fade-Out
sfx_travel_offen = False  # True = der Zeitsprung-Sound ist in MCI geöffnet
sfx_travel_laenge = 0     # Länge von 80to88 in Millisekunden (0 = unbekannt)
audio_startzeit = time.time()

def audio_meldung(text):
    """Schreibt eine Audio-Meldung mit Uhrzeit in die Shell (nur wenn AUDIO_DEBUG = True)."""
    if AUDIO_DEBUG:
        print(f"[AUDIO {time.time() - audio_startzeit:7.2f} s] {text}")

def hole_audio_pfad(dateiname):
    """Ermittelt den Pfad der Audiodatei (sucht in 'Music' und im Hauptordner)."""
    try:
        skript_ordner = os.path.dirname(os.path.abspath(__file__))
    except Exception:
        skript_ordner = os.getcwd()
    
    # Unterstützt sowohl '80to88.mp3' als auch '80_to_88.mp3'
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


# ---------- MCI Audio Funktionen (Windows) ----------
def sfx_time_circuits_starten():
    """Spielt den Time-Circuits Sound im Menü ab."""
    if not musik_aktiv:
        return
    try:
        pfad = hole_audio_pfad(AUDIO_TIME_CIRCUITS)
        if os.path.exists(pfad):
            ctypes.windll.winmm.mciSendStringW('stop sfx_tc', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW('close sfx_tc', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW(f'open "{pfad}" type mpegvideo alias sfx_tc', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW('setaudio sfx_tc volume to 1000', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW('play sfx_tc', None, 0, 0)
    except Exception as e:
        print(f"[AUDIO SFX TC] Fehler: {e}")

def musik_starten():
    """Startet die Musik – oder lässt sie dort weiterlaufen, wo sie angehalten wurde."""
    global letzter_vol_wert, musik_laeuft, musik_pausiert, fade_start
    if not musik_aktiv:
        return
    fade_start = None                    # ein laufendes Ausblenden abbrechen
    try:
        # Wenn die Musik schon geöffnet ist: nicht neu starten!
        if musik_laeuft:
            ctypes.windll.winmm.mciSendStringW(f'setaudio bgm volume to {MUSIK_LAUTSTAERKE}', None, 0, 0)
            letzter_vol_wert = MUSIK_LAUTSTAERKE
            if musik_pausiert:
                # "play" ohne "from" spielt an der aktuellen Stelle weiter
                ctypes.windll.winmm.mciSendStringW('play bgm repeat', None, 0, 0)
                musik_pausiert = False
            return

        pfad = hole_audio_pfad(AUDIO_MUSIK)
        if os.path.exists(pfad):
            ctypes.windll.winmm.mciSendStringW('stop bgm', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW('close bgm', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW(f'open "{pfad}" type mpegvideo alias bgm', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW(f'setaudio bgm volume to {MUSIK_LAUTSTAERKE}', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW('play bgm repeat', None, 0, 0)  # Endlosschleife, von vorne
            letzter_vol_wert = MUSIK_LAUTSTAERKE  # Lautstärke-Tracker zurücksetzen
            musik_laeuft = True                   # Flag auf True setzen
    except Exception as e:
        print(f"[AUDIO BGM] Fehler: {e}")

def mci_frage(befehl):
    """Schickt eine Frage an MCI (z.B. 'status sfxtravel mode') und gibt die Antwort als Text zurück.
    (Bei einem Fehler kommt ein leerer Text zurück.)"""
    try:
        antwort = ctypes.create_unicode_buffer(64)
        ctypes.windll.winmm.mciSendStringW(befehl, antwort, 64, 0)
        return antwort.value
    except Exception:
        return ""

def mci_modus(alias):
    """Was macht ein Sound gerade? 'playing', 'stopped', 'paused' ..."""
    return mci_frage(f'status {alias} mode')

def mci_zahl(befehl):
    """Wie mci_frage, aber als Zahl (z.B. Position in Millisekunden). -1 = unbekannt."""
    text = mci_frage(befehl)
    return int(text) if text.isdigit() else -1

def sfx_travel_starten():
    """Spielt den Beschleunigungs- & Zeitsprung-Sound ab."""
    global sfx_travel_offen, sfx_travel_laenge
    if not musik_aktiv:
        return
    try:
        pfad = hole_audio_pfad(AUDIO_TRAVEL)
        if os.path.exists(pfad):
            ctypes.windll.winmm.mciSendStringW('stop sfxtravel', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW('close sfxtravel', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW(f'open "{pfad}" type mpegvideo alias sfxtravel', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW('set sfxtravel time format milliseconds', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW('setaudio sfxtravel volume to 1000', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW('play sfxtravel', None, 0, 0)
            sfx_travel_offen = True
            sfx_travel_laenge = max(0, mci_zahl('status sfxtravel length'))
            audio_meldung(f"80to88 startet (Länge laut MCI: {sfx_travel_laenge} ms)")
    except Exception as e:
        print(f"[AUDIO SFX TRAVEL] Fehler: {e}")

def sfx_leise_schliessen(alias):
    """Erst stumm schalten, dann stoppen und schließen.
    So kann beim Schließen kein Rest-Ton mehr herauskommen."""
    try:
        ctypes.windll.winmm.mciSendStringW(f'setaudio {alias} volume to 0', None, 0, 0)
        ctypes.windll.winmm.mciSendStringW(f'stop {alias}', None, 0, 0)
        ctypes.windll.winmm.mciSendStringW(f'close {alias}', None, 0, 0)
    except Exception:
        pass

def sfx_travel_stoppen():
    """Stoppt den Zeitsprung-Sound sofort (und schließt ihn, um MCI-Freezes zu verhindern)."""
    global sfx_travel_offen
    if sfx_travel_offen:
        position = mci_zahl('status sfxtravel position')
        audio_meldung(f"80to88 wird geschlossen (Position {position} von {sfx_travel_laenge} ms)")
    sfx_leise_schliessen("sfxtravel")
    sfx_travel_offen = False

def sfx_time_circuits_stoppen():
    sfx_leise_schliessen("sfx_tc")

def musik_stoppen(dauer=FADE_CRASH):
    """Blendet die Musik langsam aus und hält sie dann an (Pause, nicht Stopp)."""
    global fade_start, fade_dauer
    if musik_laeuft and not musik_pausiert and fade_start is None:
        fade_start = time.time()
        fade_dauer = dauer

def musik_fade_aktualisieren():
    """Wird in jedem Bild aufgerufen: macht die Musik ein bisschen leiser."""
    global fade_start, musik_pausiert, letzter_vol_wert
    if fade_start is None:
        return
    verstrichen = time.time() - fade_start
    try:
        if verstrichen < fade_dauer:
            neuer_vol = max(0, int(MUSIK_LAUTSTAERKE * (1.0 - verstrichen / fade_dauer)))
            if neuer_vol != letzter_vol_wert:     # nur senden, wenn sich etwas ändert
                letzter_vol_wert = neuer_vol
                ctypes.windll.winmm.mciSendStringW(f'setaudio bgm volume to {neuer_vol}', None, 0, 0)
        else:
            ctypes.windll.winmm.mciSendStringW('setaudio bgm volume to 0', None, 0, 0)   # ganz leise ...
            letzter_vol_wert = 0
            ctypes.windll.winmm.mciSendStringW('pause bgm', None, 0, 0)   # ... dann anhalten, die Stelle bleibt gemerkt
            musik_pausiert = True
            fade_start = None
            audio_meldung("Musik pausiert")
    except Exception:
        fade_start = None


# ---------- Spielfenster ----------
fenster = turtle.Screen()
fenster.title("DeLorean 88 mph Challenge ⚡")
fenster.bgcolor(FARBE_RASEN)
fenster.setup(BREITE, HOEHE)
fenster.tracer(0)


# ---------- Pixel-Art / Formen ----------
def figur_anmelden(name, bild, farben, pixel):
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


DELOREAN_BILD = [
    "..CCCC..", ".GGGGGG.", "KGGGGGGK", ".GCCGGCP",
    ".GGGGGG.", ".GGGGGG.", "KGGGGGGK", ".GGRRGG.", "..GSSG.."
]
DELOREAN_FARBEN = {"G": "silver", "C": "cyan", "K": "black", "P": "gold", "R": "crimson", "S": "dimgray"}

AUTO_ROT_BILD = [
    "..RRRR..", ".RRRRRR.", "KRRRRRRK", ".RCCCCR.",
    ".RRRRRR.", ".RRRRRR.", "KRRRRRRK", ".RWWWRR.", "..RRRR.."
]
AUTO_ROT_FARBEN = {"R": "darkred", "C": "lightblue", "K": "black", "W": "orange"}

figur_anmelden("delorean_top", DELOREAN_BILD, DELOREAN_FARBEN, 4)
figur_anmelden("auto_rot", AUTO_ROT_BILD, AUTO_ROT_FARBEN, 4)


# ---------- Zeichnen der Straße ----------
strasse_zeichnung = turtle.Turtle()
strasse_zeichnung.hideturtle()
strasse_zeichnung.penup()

def welt_zeichnen():
    strasse_zeichnung.clear()
    strasse_zeichnung.goto(-200, -300)
    strasse_zeichnung.color(FARBE_STRASSE)
    strasse_zeichnung.begin_fill()
    for _ in range(2):
        strasse_zeichnung.forward(400)
        strasse_zeichnung.left(90)
        strasse_zeichnung.forward(600)
        strasse_zeichnung.left(90)
    strasse_zeichnung.end_fill()

    strasse_zeichnung.color("white")
    strasse_zeichnung.pensize(5)
    for x_pos in [-195, 195]:
        strasse_zeichnung.goto(x_pos, -300)
        strasse_zeichnung.pendown()
        strasse_zeichnung.goto(x_pos, 300)
        strasse_zeichnung.penup()


streifen_liste = []
for i in range(7):
    s = turtle.Turtle()
    s.shape("square")
    s.color("white")
    s.shapesize(stretch_wid=2, stretch_len=0.4)
    s.penup()
    s.goto(0, -300 + i * 100)
    streifen_liste.append(s)


feuer_zeichnung = turtle.Turtle()
feuer_zeichnung.hideturtle()
feuer_zeichnung.penup()

def feuer_spuren_zeichnen(x_pos, y_start):
    feuer_zeichnung.clear()
    for offset_x in [-18, 18]:
        feuer_zeichnung.goto(x_pos + offset_x, y_start)
        feuer_zeichnung.pensize(8)
        for y_pos in range(int(y_start), -300, -15):
            colore = random.choice(["orange", "red", "yellow", "gold"])
            feuer_zeichnung.color(colore)
            feuer_zeichnung.pendown()
            feuer_zeichnung.goto(x_pos + offset_x + random.randint(-2, 2), y_pos - 15)
            feuer_zeichnung.penup()


spieler = turtle.Turtle()
spieler.shape("delorean_top")
spieler.setheading(90)
spieler.penup()

hindernisse = []

anzeige = turtle.Turtle()
anzeige.hideturtle()
anzeige.penup()


# ---------- Tachometer (links neben der Straße) ----------
# Nachgebaut nach dem Film-Tacho: weiße mph-Zahlen 15 bis 95 (55 rot, ganz oben),
# innen blaue km/h-Zahlen, unten eine Digitalanzeige.
TACHO_X = -300        # Mitte des Tachos
TACHO_Y = -195
TACHO_RADIUS = 85
TACHO_ANFANG = 15     # kleinste Zahl (unten links)
TACHO_MAX = 95        # größte Zahl (unten rechts). Im Film: extra gebauter Tacho bis 95 mph
                      # (der Serien-Tacho der DeLorean ging wegen eines US-Gesetzes von 1979 nur bis 85)
TACHO_OBEN = 55       # diese Zahl steht ganz oben
TACHO_GRAD_PRO_MPH = 3.05                                   # so viele Grad dreht der Zeiger pro mph
TACHO_ZAHLEN = [15, 25, 35, 45, 55, 65, 75, 85, 95]         # weiße mph-Zahlen
TACHO_ROTE_ZAHLEN = [55]                                    # diese Zahlen sind rot
TACHO_KMH = [40, 60, 80, 100, 120, 140, 160]                # blaue km/h-Zahlen innen
FARBE_KMH = "#7aa7e0"

tacho_blatt = turtle.Turtle()     # Zifferblatt: wird nur einmal pro Spiel gezeichnet
tacho_zeiger = turtle.Turtle()    # Zeiger: wird in jedem Bild neu gezeichnet
tacho_digital = turtle.Turtle()   # Digitalanzeige: Zahl in jedem Bild neu
for t in (tacho_blatt, tacho_zeiger, tacho_digital):
    t.hideturtle()
    t.penup()


def tacho_winkel(mph, begrenzen=True):
    """Rechnet mph in einen Winkel um: 55 mph = oben (90°), kleiner = weiter links, größer = weiter rechts."""
    if begrenzen:
        mph = max(TACHO_ANFANG - 5, min(mph, TACHO_MAX + 4))   # der Zeiger bleibt an den Enden stehen
    return 90 - (mph - TACHO_OBEN) * TACHO_GRAD_PRO_MPH


def punkt_auf_kreis(winkel, abstand):
    """Ein Punkt, der vom Tacho-Mittelpunkt aus in Richtung 'winkel' so weit weg ist."""
    w = math.radians(winkel)
    return TACHO_X + abstand * math.cos(w), TACHO_Y + abstand * math.sin(w)


def tacho_zeichnen():
    """Zeichnet das Zifferblatt: Scheibe, Striche, Zahlen, Rahmen der Digitalanzeige."""
    t = tacho_blatt
    t.clear()
    t.goto(TACHO_X, TACHO_Y)
    t.dot(TACHO_RADIUS * 2 + 8, "silver")      # Rand
    t.dot(TACHO_RADIUS * 2, "#111111")         # Scheibe

    # weiße Striche alle 5 mph: lang bei den Zahlen (15, 25 ...), kurz dazwischen (20, 30 ...)
    for mph in range(TACHO_ANFANG, TACHO_MAX + 1, 5):
        w = tacho_winkel(mph)
        lang = mph in TACHO_ZAHLEN
        t.color("white")
        t.pensize(4 if lang else 2)
        t.goto(punkt_auf_kreis(w, TACHO_RADIUS - (14 if lang else 9)))
        t.pendown()
        t.goto(punkt_auf_kreis(w, TACHO_RADIUS - 3))
        t.penup()

    # weiße (und rote) mph-Zahlen
    for mph in TACHO_ZAHLEN:
        x, y = punkt_auf_kreis(tacho_winkel(mph), TACHO_RADIUS - 26)
        t.goto(x, y - 7)                       # write() schreibt über dem Punkt: etwas tiefer setzen
        t.color("red" if mph in TACHO_ROTE_ZAHLEN else "white")
        t.write(str(mph), align="center", font=("Arial", 10, "bold"))

    # blaue km/h-Zahlen mit kleinem Quadrat (1 mph = 1.609 km/h)
    for kmh in TACHO_KMH:
        w = tacho_winkel(kmh / 1.609344, begrenzen=False)
        t.goto(punkt_auf_kreis(w, TACHO_RADIUS - 17))
        t.dot(5, FARBE_KMH)
        x, y = punkt_auf_kreis(w, TACHO_RADIUS - 43)
        t.goto(x, y - 5)
        t.color(FARBE_KMH)
        t.write(str(kmh), align="center", font=("Arial", 7, "bold"))

    # Beschriftung unten: km/h klein, MPH groß
    t.goto(TACHO_X, TACHO_Y - 25)
    t.color("gray")
    t.write("km/h", align="center", font=("Arial", 7, "normal"))
    t.goto(TACHO_X, TACHO_Y - 37)
    t.color("white")
    t.write("MPH", align="center", font=("Arial", 9, "bold"))

    # Rahmen der Digitalanzeige (unten im Tacho)
    t.goto(TACHO_X - 30, TACHO_Y - 66)
    t.color("dimgray", "#1a0000")
    t.pensize(2)
    t.pendown()
    t.begin_fill()
    for seite in (60, 26, 60, 26):
        t.forward(seite)
        t.left(90)
    t.end_fill()
    t.penup()


def tacho_anzeigen(mph):
    """Zeiger und Digitalanzeige auf die aktuelle Geschwindigkeit stellen."""
    w = tacho_winkel(mph)
    z = tacho_zeiger
    z.clear()
    z.color("orangered")
    z.pensize(3)
    z.goto(punkt_auf_kreis(w + 180, 12))       # kurzes Stück hinter der Mitte
    z.pendown()
    z.goto(punkt_auf_kreis(w, TACHO_RADIUS - 12))
    z.penup()
    z.goto(TACHO_X, TACHO_Y)
    z.dot(12, "silver")                        # Kappe in der Mitte

    d = tacho_digital
    d.clear()
    d.goto(TACHO_X, TACHO_Y - 64)
    d.color("orangered")
    d.write(str(int(mph)), align="center", font=("Courier", 16, "bold"))   # int(): 87.9 zeigt 87, erst bei 88 steht 88


def tacho_verstecken():
    tacho_blatt.clear()
    tacho_zeiger.clear()
    tacho_digital.clear()


schwierigkeitsgrade = ["Anfänger", "Mittel", "Experte"]
schwierigkeit_index = 1

geschwindigkeit_mph = 30.0
ziel_geschwindigkeit = 88.0
lenkung_x = 0
gedrueckt = set()

status = "MENÜ"
hindernis_timer = 0

# Timing & Audio-Synchronisations-Variablen
sfx_travel_gestartet = False
start_travel_zeit = 0.0
sieg_zeit = 0.0

def hole_schwierigkeits_parameter():
    # Gibt (Startgeschwindigkeit, Beschleunigung, Spawn-Faktor, Trigger-Geschwindigkeit) zurück
    # Beschleunigung = n * 62.5. Frame/Sec zu MPH/Sec
    if schwierigkeitsgrade[schwierigkeit_index] == "Anfänger":
        return 40, 0.03, 1.4, 65.0
    elif schwierigkeitsgrade[schwierigkeit_index] == "Mittel":
        return 25.0, 0.05, 1.0, 70.0
    else:  # Experte
        return 15.0, 0.08, 0.6, 75.0


def menue_anzeigen():
    anzeige.clear()
    fenster.bgcolor(FARBE_RASEN)
    welt_zeichnen()
    tacho_verstecken()                 # im Menü kein Tacho (die Menü-Box würde ihn überdecken)
    
    anzeige.goto(-260, -180)
    anzeige.color("black")
    anzeige.begin_fill()
    for _ in range(2):
        anzeige.forward(520)
        anzeige.left(90)
        anzeige.forward(380)
        anzeige.left(90)
    anzeige.end_fill()
    
    anzeige.goto(0, 140)
    anzeige.color("gold")
    anzeige.write("⚡ DELOREAN 88 MPH ⚡", align="center", font=("Courier", 26, "bold"))
    
    anzeige.goto(0, 60)
    anzeige.color("white")
    anzeige.write("[ ENTER / KLICK ]  SPIEL STARTEN", align="center", font=("Courier", 16, "bold"))
    
    anzeige.goto(0, 0)
    anzeige.color(FARBE_NEON_BLAU)
    aktuell_diff = schwierigkeitsgrade[schwierigkeit_index]
    anzeige.write(f"[ D ]  SCHWIERIGKEIT: < {aktuell_diff} >", align="center", font=("Courier", 16, "bold"))
    
    anzeige.goto(0, -60)
    musik_str = "AN" if musik_aktiv else "AUS"
    anzeige.color("lightgreen" if musik_aktiv else "crimson")
    anzeige.write(f"[ M ]  MUSIK: < {musik_str} >", align="center", font=("Courier", 16, "bold"))
    
    anzeige.goto(0, -140)
    anzeige.color("gray")
    anzeige.write("Steuerung: A/D oder Pfeiltasten zum Lenken", align="center", font=("Arial", 12, "italic"))


def schwierigkeit_wechseln():
    global schwierigkeit_index
    if status == "MENÜ":
        schwierigkeit_index = (schwierigkeit_index + 1) % len(schwierigkeitsgrade)
        menue_anzeigen()


def musik_togglen():
    global musik_aktiv
    musik_aktiv = not musik_aktiv
    if musik_aktiv:
        sfx_time_circuits_starten()
        musik_starten()
    else:
        sfx_time_circuits_stoppen()      # Soundeffekte sofort aus
        sfx_travel_stoppen()
        musik_stoppen(FADE_TASTE_M)      # Musik kurz ausblenden, dann Pause
    if status == "MENÜ":
        menue_anzeigen()


def spiel_starten():
    global status, geschwindigkeit_mph, hindernis_timer, sfx_travel_gestartet

    status = "LÄUFT"
    sfx_travel_gestartet = False

    # 1. Menü-Box sofort vom Bildschirm entfernen
    anzeige.clear()

    # 2. Menü-Sound stoppen, falls er noch läuft
    sfx_time_circuits_stoppen()

    start_spd, _, _, _ = hole_schwierigkeits_parameter()
    geschwindigkeit_mph = start_spd
    hindernis_timer = 0
    
    feuer_zeichnung.clear()
    
    for h in hindernisse:
        h.hideturtle()
    hindernisse.clear()
    
    spieler.goto(0, -210)
    spieler.showturtle()
    welt_zeichnen()
    tacho_zeichnen()
    tacho_anzeigen(geschwindigkeit_mph)


def tastenklick_klick(x, y):
    if status == "MENÜ":
        if -200 < x < 200 and 40 < y < 90:
            spiel_starten()
        elif -200 < x < 200 and -20 < y < 30:
            schwierigkeit_wechseln()
        elif -200 < x < 200 and -80 < y < -30:
            musik_togglen()


def tasten_druck(taste):
    gedrueckt.add(taste)

def tasten_freigabe(taste):
    gedrueckt.discard(taste)

def lenkung_verarbeiten():
    global lenkung_x
    lenkung_x = 0
    if "links" in gedrueckt:
        lenkung_x = -7
    if "rechts" in gedrueckt:
        lenkung_x = 7

def hindernis_erzeugen():
    h = turtle.Turtle()
    h.shape("auto_rot")
    h.setheading(270)
    h.penup()
    x_pos = random.randint(-155, 155)
    h.goto(x_pos, 340)
    hindernisse.append(h)


def ui_aktualisieren():
    anzeige.clear()
    tacho_anzeigen(min(geschwindigkeit_mph, ziel_geschwindigkeit))   # auch bei CRASH/SIEG: zeigt die letzte Geschwindigkeit

    if status == "LÄUFT":
        anzeige.goto(360, 250)
        anzeige.color("white")
        anzeige.write(f"MODUS: {schwierigkeitsgrade[schwierigkeit_index]}", align="right", font=("Courier", 14, "bold"))
    
    elif status == "CRASH":
        anzeige.goto(0, 50)
        anzeige.color(FARBE_FEUER_ORANGE)
        anzeige.write("CRASH! 💥", align="center", font=("Courier", 36, "bold"))
        anzeige.goto(0, -10)
        anzeige.color("white")
        anzeige.write("Drücke 'R' oder ENTER für Menü", align="center", font=("Courier", 18, "bold"))
    
    elif status == "SIEG":
        anzeige.goto(0, 50)
        anzeige.color("gold")
        anzeige.write("88 MPH! ZEITREISE IN DIE 50er! ⚡", align="center", font=("Courier", 20, "bold"))
        anzeige.goto(0, -10)
        anzeige.color("white")
        anzeige.write("Drücke 'R' oder ENTER für Menü", align="center", font=("Courier", 18, "bold"))


def spiel_schleife():
    global geschwindigkeit_mph, status, hindernis_timer, sfx_travel_gestartet, start_travel_zeit, sieg_zeit
    
    if status == "LÄUFT":
        _, beschleunigung, spawn_faktor, trigger_speed = hole_schwierigkeits_parameter()
        
        # Normale Beschleunigung unterhalb der dynamischen Trigger-Geschwindigkeit
        if geschwindigkeit_mph < trigger_speed:
            geschwindigkeit_mph += beschleunigung
            if geschwindigkeit_mph >= trigger_speed:
                geschwindigkeit_mph = trigger_speed
                sfx_travel_gestartet = True
                start_travel_zeit = time.time()
                sfx_travel_starten()
        else:
            # Synchronisation von Trigger-Speed bis 88 MPH auf genau 6.5 Sekunden
            verstrichen = time.time() - start_travel_zeit
            geschwindigkeit_mph = trigger_speed + (verstrichen / 6.5) * (ziel_geschwindigkeit - trigger_speed)
            if geschwindigkeit_mph >= ziel_geschwindigkeit:
                geschwindigkeit_mph = ziel_geschwindigkeit
                
        # Lenkung & Grenzen
        lenkung_verarbeiten()
        neue_x = spieler.xcor() + lenkung_x
        if neue_x < -170:
            neue_x = -170
        if neue_x > 170:
            neue_x = 170
        spieler.setx(neue_x)
        
        scrolling_tempo = geschwindigkeit_mph / 3.0
        for s in streifen_liste:
            s.sety(s.ycor() - scrolling_tempo)
            if s.ycor() < -300:
                s.sety(s.ycor() + 600)
        
        # Hindernisse
        hindernis_timer += 1
        spawn_intervall = max(12, int((60 - int(geschwindigkeit_mph / 2)) * spawn_faktor))
        if hindernis_timer >= spawn_intervall:
            hindernis_erzeugen()
            hindernis_timer = 0
            
        h_tempo = (geschwindigkeit_mph / 6.0) + 3.0
        for h in hindernisse[:]:
            h.sety(h.ycor() - h_tempo)
            
            # Kollision
            dx = abs(h.xcor() - spieler.xcor())
            dy = abs(h.ycor() - spieler.ycor())
            if dx < 35 and dy < 50 and status == "LÄUFT":
                status = "CRASH"
                sfx_travel_stoppen()         # Zeitreise-Geräusch sofort aus: nach einem Crash gibt es keine Zeitreise
                musik_stoppen(FADE_CRASH)
                
            if h.ycor() < -350:
                h.hideturtle()
                hindernisse.remove(h)
                
        # ⚡ GEWONNEN BEI EXAKT 88 MPH
        if geschwindigkeit_mph >= ziel_geschwindigkeit and status == "LÄUFT":   # nicht, wenn im selben Bild gecrasht
            status = "SIEG"
            sieg_zeit = time.time()
            audio_meldung("SIEG")
            musik_stoppen(FADE_SIEG)
            
            delorean_x = spieler.xcor()
            delorean_y = spieler.ycor()
            spieler.hideturtle()
            
            # Blitz-Effekt
            fenster.bgcolor("white")
            fenster.update()
            time.sleep(0.08)
            fenster.bgcolor(FARBE_NEON_BLAU)
            fenster.update()
            time.sleep(0.08)
            fenster.bgcolor(FARBE_RASEN)
            
            feuer_spuren_zeichnen(delorean_x, delorean_y)
            
        ui_aktualisieren()

    elif status == "SIEG":
        # Den Zeitsprung-Sound kurz vor seinem Ende stumm schließen.
        # (Der Windows-MP3-Player kann ganz am Ende oder beim Schließen kurz "nachknacksen".)
        if sfx_travel_offen:
            position = mci_zahl('status sfxtravel position')
            fast_fertig = sfx_travel_laenge > 0 and position >= sfx_travel_laenge - TRAVEL_ENDE_MS
            if fast_fertig or mci_modus("sfxtravel") in ("stopped", ""):
                sfx_travel_stoppen()

    # Musik ausblenden (nach Crash, Sieg oder Taste M)
    musik_fade_aktualisieren()

    fenster.update()
    fenster.ontimer(spiel_schleife, FPS_TAKT)


def neustart_oder_menue():
    global status
    if status in ["CRASH", "SIEG"]:
        status = "MENÜ"
        
        # Stoppt und schließt den Zeitsprung-Sound, um MCI-Freezes zu verhindern
        sfx_travel_stoppen()

        if musik_aktiv:
            sfx_time_circuits_starten()
            musik_starten()
        menue_anzeigen()
    elif status == "MENÜ":
        spiel_starten()

def taste_d_gedrueckt():
    """Verarbeitet die D-Taste je nach Spielzustand (Lenken oder Menü)."""
    if status == "MENÜ":
        schwierigkeit_wechseln()
    elif status == "LÄUFT":
        tasten_druck("rechts")

# ---------- Key bindings ----------
fenster.onkeypress(lambda: tasten_druck("links"), "a")
fenster.onkeypress(lambda: tasten_druck("links"), "A")
fenster.onkeypress(lambda: tasten_druck("links"), "Left")
fenster.onkeyrelease(lambda: tasten_freigabe("links"), "a")
fenster.onkeyrelease(lambda: tasten_freigabe("links"), "A")
fenster.onkeyrelease(lambda: tasten_freigabe("links"), "Left")

# Tastenbindungen für D / Rechts
fenster.onkeypress(taste_d_gedrueckt, "d")
fenster.onkeypress(taste_d_gedrueckt, "D")
fenster.onkeyrelease(lambda: tasten_freigabe("rechts"), "d")
fenster.onkeyrelease(lambda: tasten_freigabe("rechts"), "D")

fenster.onkeypress(lambda: tasten_druck("rechts"), "Right")
fenster.onkeyrelease(lambda: tasten_freigabe("rechts"), "Right")

# (D ist schon oben gebunden: taste_d_gedrueckt() wechselt im Menü die Schwierigkeit
#  und lenkt im Spiel nach rechts. Ein zweites onkeypress auf "d" würde das ersetzen.)
fenster.onkeypress(musik_togglen, "m")
fenster.onkeypress(musik_togglen, "M")

fenster.onkeypress(neustart_oder_menue, "r")
fenster.onkeypress(neustart_oder_menue, "R")
fenster.onkeypress(neustart_oder_menue, "Return")

fenster.onscreenclick(tastenklick_klick)

fenster.listen()

# Start
if musik_aktiv:
    sfx_time_circuits_starten()  # Start-Sound beim Öffnen
    musik_starten()              # Musik starten

menue_anzeigen()
spiel_schleife()
turtle.done()
