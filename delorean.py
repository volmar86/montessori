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

musik_aktiv = True
musik_laeuft = False  # Boolean-Flag: Läuft die Hintergrundmusik bereits?
letzter_vol_wert = 350  # Lautstärke-Tracker für stufenloses Fade-Out

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
    global letzter_vol_wert, musik_laeuft
    if not musik_aktiv:
        return
    try:
        # Wenn die Musik bereits läuft, nur Lautstärke zurücksetzen (nicht neu starten!)
        if musik_laeuft:
            ctypes.windll.winmm.mciSendStringW('setaudio bgm volume to 350', None, 0, 0)
            letzter_vol_wert = 350
            return

        pfad = hole_audio_pfad(AUDIO_MUSIK)
        if os.path.exists(pfad):
            ctypes.windll.winmm.mciSendStringW('stop bgm', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW('close bgm', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW(f'open "{pfad}" type mpegvideo alias bgm', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW('setaudio bgm volume to 350', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW('play bgm repeat', None, 0, 0)
            letzter_vol_wert = 350  # Lautstärke-Tracker zurücksetzen
            musik_laeuft = True     # Flag auf True setzen
    except Exception as e:
        print(f"[AUDIO BGM] Fehler: {e}")

def sfx_travel_starten():
    """Spielt den Beschleunigungs- & Zeitsprung-Sound ab."""
    if not musik_aktiv:
        return
    try:
        pfad = hole_audio_pfad(AUDIO_TRAVEL)
        if os.path.exists(pfad):
            ctypes.windll.winmm.mciSendStringW('stop sfxtravel', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW('close sfxtravel', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW(f'open "{pfad}" type mpegvideo alias sfxtravel', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW('setaudio sfxtravel volume to 1000', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW('play sfxtravel', None, 0, 0)
    except Exception as e:
        print(f"[AUDIO SFX TRAVEL] Fehler: {e}")

def musik_stoppen():
    """Stoppt alle laufenden Audio-Spuren."""
    global musik_laeuft
    try:
        ctypes.windll.winmm.mciSendStringW('stop bgm', None, 0, 0)
        ctypes.windll.winmm.mciSendStringW('close bgm', None, 0, 0)
        ctypes.windll.winmm.mciSendStringW('stop sfx_tc', None, 0, 0)
        ctypes.windll.winmm.mciSendStringW('close sfx_tc', None, 0, 0)
        ctypes.windll.winmm.mciSendStringW('stop sfxtravel', None, 0, 0)
        ctypes.windll.winmm.mciSendStringW('close sfxtravel', None, 0, 0)
        musik_laeuft = False  # Flag auf False zurücksetzen
    except Exception:
        pass


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
musik_stopp_geplant = False

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
        musik_stoppen()
    if status == "MENÜ":
        menue_anzeigen()


def spiel_starten():
    global status, geschwindigkeit_mph, hindernis_timer, sfx_travel_gestartet, musik_stopp_geplant, letzter_vol_wert
    
    status = "LÄUFT"
    sfx_travel_gestartet = False
    musik_stopp_geplant = False
    letzter_vol_wert = 350
    
    # 1. Menü-Box sofort vom Bildschirm entfernen
    anzeige.clear()
    
    # 2. Menü-Sound stoppen, falls er noch läuft
    try:
        ctypes.windll.winmm.mciSendStringW('stop sfx_tc', None, 0, 0)
        ctypes.windll.winmm.mciSendStringW('close sfx_tc', None, 0, 0)
    except Exception:
        pass

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
    
    if status == "LÄUFT":
        anzeige.color(FARBE_NEON_BLAU)
        anzeige.goto(-360, 250)
        current_spd = min(geschwindigkeit_mph, ziel_geschwindigkeit)
        anzeige.write(f"SPEED: {current_spd:.1f} MPH", align="left", font=("Courier", 22, "bold"))
        
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
    global geschwindigkeit_mph, status, hindernis_timer, sfx_travel_gestartet, start_travel_zeit, sieg_zeit, musik_stopp_geplant, letzter_vol_wert
    
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
            if dx < 35 and dy < 50:
                status = "CRASH"
                musik_stoppen()
                
            if h.ycor() < -350:
                h.hideturtle()
                hindernisse.remove(h)
                
        # ⚡ GEWONNEN BEI EXAKT 88 MPH
        if geschwindigkeit_mph >= ziel_geschwindigkeit:
            status = "SIEG"
            sieg_zeit = time.time()
            
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
        # Stufenloses Ausblenden der Musik über 10 Sekunden (Fade-Out)
        verstrichen = time.time() - sieg_zeit
        fade_dauer = 10.0  # Fade-Out Dauer in Sekunden
        
        if verstrichen < fade_dauer:
            neuer_vol = max(0, int(350 * (1.0 - verstrichen / fade_dauer)))
            if neuer_vol != letzter_vol_wert and musik_aktiv:
                letzter_vol_wert = neuer_vol
                try:
                    ctypes.windll.winmm.mciSendStringW(f'setaudio bgm volume to {neuer_vol}', None, 0, 0)
                except Exception:
                    pass
        elif not musik_stopp_geplant:
            musik_stopp_geplant = True
            musik_stoppen()
        
    fenster.update()
    fenster.ontimer(spiel_schleife, FPS_TAKT)


def neustart_oder_menue():
    global status
    if status in ["CRASH", "SIEG"]:
        status = "MENÜ"
        
        # Stoppt und schließt den Zeitsprung-Sound, um MCI-Freezes zu verhindern
        try:
            ctypes.windll.winmm.mciSendStringW('stop sfxtravel', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW('close sfxtravel', None, 0, 0)
        except Exception:
            pass

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

fenster.onkeypress(schwierigkeit_wechseln, "d")
fenster.onkeypress(schwierigkeit_wechseln, "D")
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
