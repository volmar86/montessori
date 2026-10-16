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
#    - R oder ENTER nach Spielende für Neustart / Menü
# ============================================================

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

pygame.init()
pygame.mixer.init()

fenster = pygame.display.set_mode((BREITE, HOEHE))
pygame.display.set_caption("DeLorean 88 mph Challenge ⚡ (Pygame Edition)")
uhr = pygame.time.Clock()


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
        sound_travel.play()

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

def schmaler_machen(surf):
    """Macht ein Auto-Bild schmaler (Höhe bleibt gleich)."""
    neue_breite = round(surf.get_width() * AUTO_BREITE_FAKTOR)
    return pygame.transform.smoothscale(surf, (neue_breite, surf.get_height()))

delorean_img = schmaler_machen(erstelle_delorean_surface())
auto_rot_img = schmaler_machen(erstelle_auto_rot_surface())

AUTO_HALB = delorean_img.get_width() // 2              # halbe Bildbreite (zum Zentrieren)
TREFFER_BREITE = round(36 * AUTO_BREITE_FAKTOR)        # Breite der Kollisionsbox
RAND = 30                                              # Abstand Auto-Mitte zum Straßenrand


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

# Schriftarten
font_titel = pygame.font.SysFont("Courier", 36, bold=True)
font_ui = pygame.font.SysFont("Courier", 22, bold=True)
font_sub = pygame.font.SysFont("Courier", 16, bold=True)


def hole_schwierigkeits_parameter():
    if schwierigkeitsgrade[schwierigkeit_index] == "Anfänger":
        return 15.0, 0.03, 1.4, 65.0
    elif schwierigkeitsgrade[schwierigkeit_index] == "Mittel":
        return 25.0, 0.05, 1.0, 70.0
    else:  # Experte
        return 40.0, 0.08, 0.6, 75.0


def spiel_starten():
    global status, geschwindigkeit_mph, hindernisse, partikel_liste, hindernis_timer, sfx_travel_gestartet, spieler_x
    status = "LÄUFT"
    sfx_travel_gestartet = False
    
    start_spd, _, _, _ = hole_schwierigkeits_parameter()
    geschwindigkeit_mph = start_spd
    hindernis_timer = 0
    spieler_x = 400.0
    
    hindernisse.clear()
    partikel_liste.clear()
    
    if sound_tc:
        sound_tc.stop()


def text_mit_glanz_zeichnen(text, font, farbe, x, y):
    """Zeichnet einen retro Neon-Text mit Schatten-Effekt."""
    schatten = font.render(text, True, (0, 0, 0))
    vordergrund = font.render(text, True, farbe)
    
    rect_s = schatten.get_rect(center=(x + 2, y + 2))
    rect_v = vordergrund.get_rect(center=(x, y))
    
    fenster.blit(schatten, rect_s)
    fenster.blit(vordergrund, rect_v)


# ---------- Hauptschleife ----------
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
                    status = "MENÜ"
                    if sound_travel:
                        sound_travel.stop()
                    if musik_aktiv:
                        sfx_time_circuits_starten()
                        musik_starten()
                        
            elif event.key == pygame.K_d:
                if status == "MENÜ":
                    schwierigkeit_index = (schwierigkeit_index + 1) % len(schwierigkeitsgrade)
                    
            elif event.key == pygame.K_m:
                musik_aktiv = not musik_aktiv
                if musik_aktiv:
                    sfx_time_circuits_starten()
                    musik_starten()
                else:
                    musik_stoppen(FADE_TASTE_M)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if status == "MENÜ":
                if 200 < mx < 600 and 200 < my < 260:
                    spiel_starten()
                elif 200 < mx < 600 and 270 < my < 330:
                    schwierigkeit_index = (schwierigkeit_index + 1) % len(schwierigkeitsgrade)
                elif 200 < mx < 600 and 340 < my < 400:
                    musik_aktiv = not musik_aktiv
                    if musik_aktiv:
                        sfx_time_circuits_starten()
                        musik_starten()
                    else:
                        musik_stoppen(FADE_TASTE_M)

    # 2. GAME LOGIC
    if status == "LÄUFT":
        _, beschleunigung, spawn_faktor, trigger_speed = hole_schwierigkeits_parameter()
        
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
        scrolling_tempo = geschwindigkeit_mph / 3.0
        for i in range(len(streifen_y)):
            streifen_y[i] += scrolling_tempo
            if streifen_y[i] > HOEHE:
                streifen_y[i] -= HOEHE
                
        # Hindernisse erzeugen
        hindernis_timer += 1
        spawn_intervall = max(12, int((60 - int(geschwindigkeit_mph / 2)) * spawn_faktor))
        if hindernis_timer >= spawn_intervall:
            x_pos = random.randint(STRASSE_LINKS + RAND + 5, STRASSE_RECHTS - RAND - 5)
            hindernisse.append([x_pos, -80])
            hindernis_timer = 0
            
        # Hindernisse bewegen & Kollisionsprüfung
        h_tempo = (geschwindigkeit_mph / 6.0) + 3.0
        spieler_rect = pygame.Rect(spieler_x - TREFFER_BREITE / 2, spieler_y - 35, TREFFER_BREITE, 70)

        for h in hindernisse[:]:
            h[1] += h_tempo
            h_rect = pygame.Rect(h[0] - TREFFER_BREITE / 2, h[1] - 35, TREFFER_BREITE, 70)
            
            if spieler_rect.colliderect(h_rect) and status == "LÄUFT":
                status = "CRASH"
                if sound_travel:
                    sound_travel.stop()          # Zeitreise-Geräusch sofort aus: nach einem Crash gibt es keine Zeitreise
                musik_stoppen(FADE_CRASH)
                
            if h[1] > HOEHE + 100:
                hindernisse.remove(h)
                
        # ⚡ Sieg bei 88 MPH
        if geschwindigkeit_mph >= ziel_geschwindigkeit and status == "LÄUFT":   # nicht, wenn im selben Bild gecrasht
            status = "SIEG"
            sieg_zeit = time.time()
            musik_stoppen(FADE_SIEG)

            # Feuer-Partikel erzeugen
            for y_p in range(int(spieler_y), HOEHE, 12):
                for offset in [-15, 15]:
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
        fenster.blit(auto_rot_img, (h[0] - AUTO_HALB, h[1] - 40))
        
    # Feuer-Spuren bei Sieg
    if status == "SIEG":
        for p in partikel_liste:
            pygame.draw.circle(fenster, p[2], (int(p[0]), int(p[1])), random.randint(4, 7))
            
    # DeLorean zeichnen (nur wenn nicht im SIEG Zustand verschwunden)
    if status != "SIEG":
        fenster.blit(delorean_img, (spieler_x - AUTO_HALB, spieler_y - 40))
        
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
        text_mit_glanz_zeichnen("[ ENTER / KLICK ] SPIEL STARTEN", font_ui, FARBE_WEISS, 400, 230)
        
        diff_str = f"[ D ] SCHWIERIGKEIT: < {schwierigkeitsgrade[schwierigkeit_index]} >"
        text_mit_glanz_zeichnen(diff_str, font_ui, FARBE_NEON_BLAU, 400, 290)
        
        m_color = (144, 238, 144) if musik_aktiv else (220, 20, 60)
        m_str = f"[ M ] MUSIK: < {'AN' if musik_aktiv else 'AUS'} >"
        text_mit_glanz_zeichnen(m_str, font_ui, m_color, 400, 350)
        
        txt_sub = font_sub.render("Steuerung: A/D oder Pfeiltasten zum Lenken", True, (180, 180, 180))
        fenster.blit(txt_sub, txt_sub.get_rect(center=(400, 430)))
        
    # Crash Screen
    elif status == "CRASH":
        text_mit_glanz_zeichnen("CRASH! 💥", font_titel, FARBE_FEUER_ORANGE, 400, 250)
        text_mit_glanz_zeichnen("Drücke 'R' oder ENTER für Menü", font_ui, FARBE_WEISS, 400, 320)
        
    # Sieg Screen
    elif status == "SIEG":
        text_mit_glanz_zeichnen("88 MPH! ZEITREISE IN DIE 50er! ⚡", font_titel, FARBE_GOLD, 400, 240)
        text_mit_glanz_zeichnen("Drücke 'R' oder ENTER für Menü", font_ui, FARBE_WEISS, 400, 310)

    pygame.display.flip()

pygame.quit()
sys.exit()
