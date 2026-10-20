# ============================================================
#  DELOREAN 88 MPH CHALLENGE – PYGAME EDITION (HD GRAPHICS)
#  
#  Menü-Steuerung:
#    - ENTER oder Klick auf START: Spiel beginnen
#    - Taste D oder Klick: Schwierigkeit ändern (Anfänger / Mittel / Experte)
#    - Taste M oder Klick: Musik An/Aus
#  
#  Spiel-Steuerung:
#    - A / D oder Pfeiltasten zum Lenken
#    - Touch / Maus: waagerecht ziehen, das Auto folgt der Bewegung
#    - R oder ENTER (oder Tippen) nach Spielende für Neustart / Menü
# ============================================================

import asyncio     # nötig für die Web-Version (Pygbag); auf PC und Android stört es nicht
import pygame
import random
import time
import os
import sys
import math

# ====== EINSTELLUNGEN ======
BREITE = 800
HOEHE = 600
FPS = 60

STRASSE_BREITE = 440                             # Breite der Straße in Pixeln
STRASSE_LINKS = (BREITE - STRASSE_BREITE) // 2   # linker Straßenrand (180)
STRASSE_RECHTS = STRASSE_LINKS + STRASSE_BREITE  # rechter Straßenrand (620)
AUTO_BREITE_FAKTOR = 0.95                        # 1.0 = Originalbreite der Autos
AUTO_GROESSE = 0.7                               # alle Autos kleiner (Breite UND Höhe): 0.7 = 30 % kleiner
AUTO_LAENGE_FAKTOR = 0.85                        # Autos zusätzlich kürzer (nur die Länge): 0.85 = 15 % kürzer

FARBE_STRASSE = (45, 45, 50)
FARBE_RASEN = (34, 139, 34)
FARBE_RASEN_DUNKEL = (25, 110, 25)
FARBE_NEON_BLAU = (0, 255, 255)
FARBE_FEUER_ORANGE = (255, 69, 0)
FARBE_GOLD = (255, 215, 0)
FARBE_WEISS = (255, 255, 255)

# ---------- Audio-Dateinamen ----------
AUDIO_MUSIK = "bttf midi.mp3"
AUDIO_TIME_CIRCUITS = "time_circuits.mp3"
AUDIO_TRAVEL = "80to88.mp3"

MUSIK_LAUTSTAERKE = 0.35   # normale Lautstärke der Musik (0.0 bis 1.0)
FADE_CRASH = 5.0           # so viele Sekunden wird die Musik nach einem Crash leiser
FADE_SIEG = 10.0           # ... und nach dem Sieg
FADE_TASTE_M = 1.0         # ... und wenn man mit M die Musik ausschaltet
TRAVEL_ENDE_MS = 400       # die letzten Millisekunden von 80to88 abschneiden (gegen das Knacksen am Ende)

TOUCH_EMPFINDLICHKEIT = 1.3   # Lenken mit Finger/Maus: 1.0 = das Auto bewegt sich so weit wie der Finger, höher = empfindlicher
ENDE_SPERRE = 0.8             # Sekunden nach Crash/Sieg, in denen ein Tippen noch ignoriert wird

# Größerer Audio-Puffer (Standard: 512): die Musik gracht nicht mehr, wenn das Spiel kurz beschäftigt ist.
# Preis: etwas mehr Verzögerung (~46 ms), bei Musik und Soundeffekten nicht zu hören.
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()

fenster = pygame.display.set_mode((BREITE, HOEHE), pygame.SCALED)   # SCALED: passt sich dem Handy-Bildschirm an
pygame.display.set_caption("DeLorean 88 mph Challenge ⚡ (Pygame Edition)")
uhr = pygame.time.Clock()


# ---------- Schrift: überall dieselbe (auf Android und im Browser gibt es "Courier"/"Arial" nicht) ----------
SCHRIFT_DATEI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "DejaVuSansMono.ttf")


def hole_schrift(name, groesse, fett=False):
    """Nimmt die mitgelieferte Schrift (gleich auf PC, Android und Web); fehlt die Datei, die Systemschrift."""
    if os.path.exists(SCHRIFT_DATEI):
        schrift = pygame.font.Font(SCHRIFT_DATEI, groesse)
        schrift.set_bold(fett)
        return schrift
    return pygame.font.SysFont(name, groesse, bold=fett)



# ---------- Pfad-Finder für Audio ----------
def hole_audio_pfad(dateiname):
    """Ermittelt den Pfad der Audiodatei im 'Music'-Ordner oder im Hauptordner.
    Eine .ogg-Datei hat Vorrang vor der .mp3 (Android und Web nutzen .ogg; auf dem PC reichen die .mp3)."""
    skript_ordner = os.path.dirname(os.path.abspath(__file__))
    basis = os.path.splitext(dateiname)[0]
    varianten = [basis, basis.replace(" ", "_"), basis.replace("_", "")]
    if "80to88" in basis:
        varianten.append("80_to_88")
    mögliche_namen = [v + endung for endung in (".ogg", ".mp3") for v in varianten]

    for name in mögliche_namen:
        pfad_music = os.path.join(skript_ordner, "Music", name)
        pfad_direkt = os.path.join(skript_ordner, name)
        if os.path.exists(pfad_music):
            return pfad_music
        if os.path.exists(pfad_direkt):
            return pfad_direkt
    return os.path.join(skript_ordner, dateiname)


# ---------- Audio-Manager (Pygame Mixer) ----------
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


# ---------- Prozedurale HD-Grafiken erstellen ----------
def erstelle_delorean_surface():
    """Zeichnet ein hochauflösendes, glattes Vector-Sprite der DeLorean."""
    surf = pygame.Surface((44, 80), pygame.SRCALPHA)
    
    # Schatten
    pygame.draw.ellipse(surf, (0, 0, 0, 100), (2, 5, 40, 72))
    
    # Reifen
    pygame.draw.rect(surf, (20, 20, 20), (2, 10, 8, 16), border_radius=3)
    pygame.draw.rect(surf, (20, 20, 20), (34, 10, 8, 16), border_radius=3)
    pygame.draw.rect(surf, (20, 20, 20), (2, 54, 8, 16), border_radius=3)
    pygame.draw.rect(surf, (20, 20, 20), (34, 54, 8, 16), border_radius=3)
    
    # Karosserie (Silber-Gradient Effekt)
    pygame.draw.rect(surf, (190, 195, 200), (6, 8, 32, 64), border_radius=6)
    pygame.draw.rect(surf, (220, 225, 230), (8, 12, 28, 56), border_radius=4)
    
    # Windschutzscheibe & Dach
    pygame.draw.rect(surf, (30, 40, 50), (10, 24, 24, 16), border_radius=3)
    pygame.draw.rect(surf, (0, 200, 255, 150), (12, 25, 20, 6)) # Blau-Reflektion
    pygame.draw.rect(surf, (160, 165, 170), (11, 40, 22, 18))  # Dach
    
    # Motorhaube & Flux-Kompensator Haken
    pygame.draw.line(surf, (100, 105, 110), (12, 18), (32, 18), 2)
    pygame.draw.circle(surf, (255, 215, 0), (22, 10), 3) # Pol-Stecker
    
    # Scheinwerfer vorne (Cyan Glow)
    pygame.draw.rect(surf, (0, 255, 255), (7, 6, 8, 3), border_radius=1)
    pygame.draw.rect(surf, (0, 255, 255), (29, 6, 8, 3), border_radius=1)
    
    # Rücklichter hinten (Crimson)
    pygame.draw.rect(surf, (220, 20, 60), (8, 70, 10, 3))
    pygame.draw.rect(surf, (220, 20, 60), (26, 70, 10, 3))
    
    return surf

def erstelle_auto_rot_surface():
    """Zeichnet ein HD-Sprite für das rote Hindernis-Auto."""
    surf = pygame.Surface((44, 80), pygame.SRCALPHA)
    
    # Schatten
    pygame.draw.ellipse(surf, (0, 0, 0, 100), (2, 5, 40, 72))
    
    # Reifen
    pygame.draw.rect(surf, (20, 20, 20), (2, 10, 8, 16), border_radius=3)
    pygame.draw.rect(surf, (20, 20, 20), (34, 10, 8, 16), border_radius=3)
    pygame.draw.rect(surf, (20, 20, 20), (2, 54, 8, 16), border_radius=3)
    pygame.draw.rect(surf, (20, 20, 20), (34, 54, 8, 16), border_radius=3)
    
    # Karosserie
    pygame.draw.rect(surf, (180, 0, 0), (6, 8, 32, 64), border_radius=8)
    pygame.draw.rect(surf, (220, 30, 30), (9, 12, 26, 56), border_radius=6)
    
    # Scheiben
    pygame.draw.rect(surf, (40, 50, 60), (10, 26, 24, 14), border_radius=2)
    pygame.draw.rect(surf, (40, 50, 60), (11, 52, 22, 8), border_radius=2)
    
    # Lichter
    pygame.draw.rect(surf, (255, 255, 200), (8, 70, 8, 3)) # Gelbe Lichter oben (fährt nach unten)
    pygame.draw.rect(surf, (255, 255, 200), (28, 70, 8, 3))
    
    return surf

def groesse_anpassen(surf):
    """Macht ein Auto-Bild kleiner: schmaler (AUTO_BREITE_FAKTOR) und insgesamt kleiner (AUTO_GROESSE)."""
    neue_breite = round(surf.get_width() * AUTO_BREITE_FAKTOR * AUTO_GROESSE)
    neue_hoehe = round(surf.get_height() * AUTO_GROESSE * AUTO_LAENGE_FAKTOR)
    return pygame.transform.smoothscale(surf, (neue_breite, neue_hoehe))

delorean_img = groesse_anpassen(erstelle_delorean_surface())
auto_rot_img = groesse_anpassen(erstelle_auto_rot_surface())

AUTO_HALB = delorean_img.get_width() // 2              # halbe Bildbreite (zum Zentrieren)
AUTO_HALB_HOCH = delorean_img.get_height() // 2        # halbe Bildhöhe (zum Zentrieren)
TREFFER_BREITE = round(36 * AUTO_BREITE_FAKTOR * AUTO_GROESSE)   # Breite der Kollisionsbox
TREFFER_HOEHE = round(70 * AUTO_GROESSE * AUTO_LAENGE_FAKTOR)    # Höhe (Länge) der Kollisionsbox
RAND = 30                                              # Abstand Auto-Mitte zum Straßenrand
FEUER_ABSTAND = round(16 * AUTO_BREITE_FAKTOR * AUTO_GROESSE)    # Feuerspuren: so weit links/rechts der Mitte (bei den Reifen)


# ---------- Tachometer (links neben der Straße) ----------
# Nachgebaut nach dem Film-Tacho: weiße mph-Zahlen 15 bis 95 (55 rot, ganz oben),
# innen blaue km/h-Zahlen, unten eine Digitalanzeige.
TACHO_X = STRASSE_LINKS // 2      # Mitte des Tachos: mitten im linken Rasen (90)
TACHO_Y = HOEHE - 95              # ... und unten (505)
TACHO_RADIUS = 80
TACHO_ANFANG = 15                 # kleinste Zahl (unten links)
TACHO_MAX = 95                    # größte Zahl (unten rechts). Im Film: extra gebauter Tacho bis 95 mph
TACHO_OBEN = 55                   # diese Zahl steht ganz oben
TACHO_GRAD_PRO_MPH = 3.05                                   # so viele Grad dreht der Zeiger pro mph
TACHO_ZAHLEN = [15, 25, 35, 45, 55, 65, 75, 85, 95]         # weiße mph-Zahlen
TACHO_ROTE_ZAHLEN = [55]                                    # diese Zahlen sind rot
TACHO_KMH = [40, 60, 80, 100, 120, 140, 160]                # blaue km/h-Zahlen innen
FARBE_KMH = (122, 167, 224)

font_tacho = hole_schrift("Arial", 13, True)
font_kmh = hole_schrift("Arial", 9, True)
font_tacho_klein = hole_schrift("Arial", 9)
font_mph = hole_schrift("Arial", 12, True)
font_digital = hole_schrift("Courier", 22, True)


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


# ---------- Spielzustand & Parameter ----------
schwierigkeitsgrade = ["Anfänger", "Mittel", "Experte"]
schwierigkeit_index = 1

status = "MENÜ"
geschwindigkeit_mph = 30.0
ziel_geschwindigkeit = 88.0

spieler_x = 400.0
spieler_y = 480.0

streifen_y = [i * 100 for i in range(7)]
hindernisse = [] # Liste von [x, y]
partikel_liste = [] # Feuer-Partikel bei 88 MPH

hindernis_timer = 0
sfx_travel_gestartet = False
start_travel_zeit = 0.0
sieg_zeit = 0.0
ende_zeit = 0.0            # Zeitpunkt von Crash oder Sieg (damit ein Tippen nicht sofort das Menü öffnet)

# Schriftarten
font_titel = hole_schrift("Courier", 36, True)
font_ui = hole_schrift("Courier", 22, True)
font_sub = hole_schrift("Courier", 16, True)


def hole_schwierigkeits_parameter():
    """Gibt (Startgeschwindigkeit, Beschleunigung, Spawn-Faktor, Trigger-Geschwindigkeit, Scroll-Faktor) zurück.
    Wie lange das Spiel dauert, bestimmen Start, Beschleunigung und Trigger (Anfänger: kurz, Experte: lang).
    Wie schwer es ist, bestimmen Spawn-Faktor (kleiner = mehr Autos) und Scroll-Faktor
    (1.0 = Straße und Autos so schnell wie ursprünglich, kleiner = langsamer = leichter)."""
    if schwierigkeitsgrade[schwierigkeit_index] == "Anfänger":
        return 40.0, 0.08, 1.4, 75.0, 0.6
    elif schwierigkeitsgrade[schwierigkeit_index] == "Mittel":
        return 25.0, 0.05, 1.0, 70.0, 0.8
    else:  # Experte
        return 15.0, 0.03, 0.6, 65.0, 1.0


def spiel_starten():
    global status, geschwindigkeit_mph, hindernisse, partikel_liste, hindernis_timer, sfx_travel_gestartet, spieler_x
    status = "LÄUFT"
    sfx_travel_gestartet = False
    
    start_spd = hole_schwierigkeits_parameter()[0]
    geschwindigkeit_mph = start_spd
    hindernis_timer = 0
    spieler_x = 400.0
    
    hindernisse.clear()
    partikel_liste.clear()
    
    if sound_tc:
        sound_tc.stop()


def zum_menue():
    """Zurück ins Menü (nach Crash oder Sieg)."""
    global status
    status = "MENÜ"
    if sound_travel:
        sound_travel.stop()
    if musik_aktiv:
        musik_starten()          # Time-Circuits-Sound nur beim allerersten Start, nicht bei jedem Menü


def text_mit_glanz_zeichnen(text, font, farbe, x, y):
    """Zeichnet einen retro Neon-Text mit Schatten-Effekt."""
    schatten = font.render(text, True, (0, 0, 0))
    vordergrund = font.render(text, True, farbe)
    
    rect_s = schatten.get_rect(center=(x + 2, y + 2))
    rect_v = vordergrund.get_rect(center=(x, y))
    
    fenster.blit(schatten, rect_s)
    fenster.blit(vordergrund, rect_v)


# ---------- Hauptschleife ----------
async def main():
    global ende_zeit, geschwindigkeit_mph, hindernis_timer, musik_aktiv, schwierigkeit_index
    global sfx_travel_gestartet, sieg_zeit, spieler_x, start_travel_zeit, status
    laufend = True
    if musik_aktiv:
        sfx_time_circuits_starten()
        musik_starten()

    while laufend:
        dt = uhr.tick(FPS)
    
        # 1. EVENTEINGABE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                laufend = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_r]:
                    if status == "MENÜ":
                        spiel_starten()
                    elif status in ["CRASH", "SIEG"]:
                        zum_menue()

                elif event.key == pygame.K_d:
                    if status == "MENÜ":
                        schwierigkeit_index = (schwierigkeit_index + 1) % len(schwierigkeitsgrade)
                    
                elif event.key == pygame.K_m:
                    musik_aktiv = not musik_aktiv
                    if musik_aktiv:
                        musik_starten()
                    else:
                        musik_stoppen(FADE_TASTE_M)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos           # bei Touch ist das die Stelle, wo der Finger tippt
                if status == "MENÜ":
                    if 200 < mx < 600 and 200 < my < 260:
                        spiel_starten()
                    elif 200 < mx < 600 and 270 < my < 330:
                        schwierigkeit_index = (schwierigkeit_index + 1) % len(schwierigkeitsgrade)
                    elif 200 < mx < 600 and 340 < my < 400:
                        musik_aktiv = not musik_aktiv
                        if musik_aktiv:
                            musik_starten()
                        else:
                            musik_stoppen(FADE_TASTE_M)
                elif status in ["CRASH", "SIEG"] and time.time() - ende_zeit > ENDE_SPERRE:
                    zum_menue()              # Tippen = zurück ins Menü

            # Lenken mit dem Finger: waagerecht ziehen, das Auto bewegt sich mit (relativ, der Finger muss nicht auf dem Auto sein)
            elif event.type == pygame.FINGERMOTION and status == "LÄUFT":
                spieler_x += event.dx * BREITE * TOUCH_EMPFINDLICHKEIT

            # Dasselbe mit der Maus (Ziehen mit gedrückter linker Taste); vom Finger erzeugte Mausereignisse werden übersprungen
            elif event.type == pygame.MOUSEMOTION and status == "LÄUFT":
                if event.buttons[0] and not getattr(event, "touch", False):
                    spieler_x += event.rel[0] * TOUCH_EMPFINDLICHKEIT

        # 2. GAME LOGIC
        if status == "LÄUFT":
            _, beschleunigung, spawn_faktor, trigger_speed, scroll_faktor = hole_schwierigkeits_parameter()
        
            # Geschwindigkeits-Steigerung
            if geschwindigkeit_mph < trigger_speed:
                geschwindigkeit_mph += beschleunigung
                if geschwindigkeit_mph >= trigger_speed:
                    geschwindigkeit_mph = trigger_speed
                    sfx_travel_gestartet = True
                    start_travel_zeit = time.time()
                    sfx_travel_starten()
            else:
                verstrichen = time.time() - start_travel_zeit
                geschwindigkeit_mph = trigger_speed + (verstrichen / 6.5) * (ziel_geschwindigkeit - trigger_speed)
                if geschwindigkeit_mph >= ziel_geschwindigkeit:
                    geschwindigkeit_mph = ziel_geschwindigkeit
                
            # Spieler Lenkung (A/D oder Pfeiltasten)
            tasten = pygame.key.get_pressed()
            if tasten[pygame.K_a] or tasten[pygame.K_LEFT]:
                spieler_x -= 7.0
            if tasten[pygame.K_d] or tasten[pygame.K_RIGHT]:
                spieler_x += 7.0
            
            # Straßengrenzen
            spieler_x = max(STRASSE_LINKS + RAND, min(STRASSE_RECHTS - RAND, spieler_x))
        
            # Straßenstreifen scrollen
            scrolling_tempo = geschwindigkeit_mph / 3.0 * scroll_faktor
            for i in range(len(streifen_y)):
                streifen_y[i] += scrolling_tempo
                if streifen_y[i] > HOEHE:
                    streifen_y[i] -= HOEHE
                
            # Hindernisse erzeugen
            hindernis_timer += 1
            # Geteilt durch scroll_faktor: fahren die Autos langsamer, kommen sie auch seltener,
            # sonst stünden sie enger hintereinander und das Spiel wäre nicht leichter
            spawn_intervall = max(12, int((60 - int(geschwindigkeit_mph / 2)) * spawn_faktor / scroll_faktor))
            if hindernis_timer >= spawn_intervall:
                x_pos = random.randint(STRASSE_LINKS + RAND + 5, STRASSE_RECHTS - RAND - 5)
                hindernisse.append([x_pos, -80])
                hindernis_timer = 0
            
            # Hindernisse bewegen & Kollisionsprüfung
            h_tempo = ((geschwindigkeit_mph / 6.0) + 3.0) * scroll_faktor
            spieler_rect = pygame.Rect(spieler_x - TREFFER_BREITE / 2, spieler_y - TREFFER_HOEHE / 2, TREFFER_BREITE, TREFFER_HOEHE)

            for h in hindernisse[:]:
                h[1] += h_tempo
                h_rect = pygame.Rect(h[0] - TREFFER_BREITE / 2, h[1] - TREFFER_HOEHE / 2, TREFFER_BREITE, TREFFER_HOEHE)
            
                if spieler_rect.colliderect(h_rect) and status == "LÄUFT":
                    status = "CRASH"
                    ende_zeit = time.time()
                    if sound_travel:
                        sound_travel.stop()          # Zeitreise-Geräusch sofort aus: nach einem Crash gibt es keine Zeitreise
                    musik_stoppen(FADE_CRASH)
                
                if h[1] > HOEHE + 100:
                    hindernisse.remove(h)
                
            # ⚡ Sieg bei 88 MPH
            if geschwindigkeit_mph >= ziel_geschwindigkeit and status == "LÄUFT":   # nicht, wenn im selben Bild gecrasht
                status = "SIEG"
                sieg_zeit = time.time()
                ende_zeit = sieg_zeit
                musik_stoppen(FADE_SIEG)

                # Feuer-Partikel erzeugen
                for y_p in range(int(spieler_y), HOEHE, 12):
                    for offset in [-FEUER_ABSTAND, FEUER_ABSTAND]:
                        partikel_liste.append([spieler_x + offset + random.randint(-4, 4), y_p, random.choice([(255, 69, 0), (255, 140, 0), (255, 215, 0)])])

        # Musik ausblenden (nach Crash, Sieg oder Taste M)
        musik_fade_aktualisieren()

        # 3. ZEICHNEN / RENDERN
        # Rasen Hintergrund
        fenster.fill(FARBE_RASEN)
    
        # Asphaltierte Straße (STRASSE_BREITE Pixel breit, in der Mitte)
        pygame.draw.rect(fenster, FARBE_STRASSE, (STRASSE_LINKS, 0, STRASSE_BREITE, HOEHE))
        pygame.draw.line(fenster, FARBE_WEISS, (STRASSE_LINKS + 5, 0), (STRASSE_LINKS + 5, HOEHE), 5)
        pygame.draw.line(fenster, FARBE_WEISS, (STRASSE_RECHTS - 5, 0), (STRASSE_RECHTS - 5, HOEHE), 5)
    
        # Mittellinien der Straße
        for y_pos in streifen_y:
            pygame.draw.rect(fenster, FARBE_WEISS, (396, y_pos, 8, 40), border_radius=2)
        
        # Hindernisse zeichnen
        for h in hindernisse:
            fenster.blit(auto_rot_img, (h[0] - AUTO_HALB, h[1] - AUTO_HALB_HOCH))
        
        # Feuer-Spuren bei Sieg
        if status == "SIEG":
            for p in partikel_liste:
                pygame.draw.circle(fenster, p[2], (int(p[0]), int(p[1])), random.randint(4, 7))
            
        # DeLorean zeichnen (nur wenn nicht im SIEG Zustand verschwunden)
        if status != "SIEG":
            fenster.blit(delorean_img, (spieler_x - AUTO_HALB, spieler_y - AUTO_HALB_HOCH))
        
        # Tacho (im Spiel, nach Crash und nach Sieg – nicht im Menü)
        if status != "MENÜ":
            tacho_zeichnen(min(geschwindigkeit_mph, ziel_geschwindigkeit))

        # UI Overhead Display (während des Spiels)
        if status == "LÄUFT":
            txt_diff = font_ui.render(f"MODUS: {schwierigkeitsgrade[schwierigkeit_index]}", True, FARBE_WEISS)
            pos = (BREITE - txt_diff.get_width() - 20, 20)
            # Halbtransparenter Hintergrund, damit der Text über dem Straßenrand lesbar bleibt
            hintergrund = pygame.Surface((txt_diff.get_width() + 12, txt_diff.get_height() + 6), pygame.SRCALPHA)
            hintergrund.fill((0, 0, 0, 150))
            fenster.blit(hintergrund, (pos[0] - 6, pos[1] - 3))
            fenster.blit(txt_diff, pos)
        
        # Menü Overlay
        elif status == "MENÜ":
            box_surf = pygame.Surface((520, 360), pygame.SRCALPHA)
            box_surf.fill((0, 0, 0, 220)) # Halbtransparentes Schwarz
            fenster.blit(box_surf, (140, 120))
        
            text_mit_glanz_zeichnen("⚡ DELOREAN 88 MPH ⚡", font_titel, FARBE_GOLD, 400, 160)
            text_mit_glanz_zeichnen("[ ENTER / TIPPEN ] SPIEL STARTEN", font_ui, FARBE_WEISS, 400, 230)
        
            diff_str = f"[ D ] SCHWIERIGKEIT: < {schwierigkeitsgrade[schwierigkeit_index]} >"
            text_mit_glanz_zeichnen(diff_str, font_ui, FARBE_NEON_BLAU, 400, 290)
        
            m_color = (144, 238, 144) if musik_aktiv else (220, 20, 60)
            m_str = f"[ M ] MUSIK: < {'AN' if musik_aktiv else 'AUS'} >"
            text_mit_glanz_zeichnen(m_str, font_ui, m_color, 400, 350)
        
            txt_sub = font_sub.render("Steuerung: A/D, Pfeiltasten oder Finger ziehen", True, (180, 180, 180))
            fenster.blit(txt_sub, txt_sub.get_rect(center=(400, 430)))
        
        # Crash Screen
        elif status == "CRASH":
            text_mit_glanz_zeichnen("CRASH!", font_titel, FARBE_FEUER_ORANGE, 400, 250)
            text_mit_glanz_zeichnen("Drücke 'R', ENTER oder tippe für Menü", font_ui, FARBE_WEISS, 400, 320)
        
        # Sieg Screen
        elif status == "SIEG":
            text_mit_glanz_zeichnen("88 MPH! ZEITREISE IN DIE 50er! ⚡", font_titel, FARBE_GOLD, 400, 240)
            text_mit_glanz_zeichnen("Drücke 'R', ENTER oder tippe für Menü", font_ui, FARBE_WEISS, 400, 310)

        pygame.display.flip()
        await asyncio.sleep(0)       # gibt dem Browser Zeit (Pygbag); sonst friert die Web-Version ein

    pygame.quit()


asyncio.run(main())
