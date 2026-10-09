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

# ====== EINSTELLUNGEN ======
BREITE = 800
HOEHE = 600
FPS = 60

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
    global musik_laeuft
    if not musik_aktiv:
        return
    try:
        if not musik_laeuft and os.path.exists(hole_audio_pfad(AUDIO_MUSIK)):
            pygame.mixer.music.set_volume(0.35)  # 35% Lautstärke
            pygame.mixer.music.play(-1)  # Endlosschleife
            musik_laeuft = True
        else:
            pygame.mixer.music.set_volume(0.35)
    except Exception as e:
        print(f"[AUDIO] Fehler beim Starten der Musik: {e}")

def musik_stoppen():
    global musik_laeuft
    pygame.mixer.music.stop()
    pygame.mixer.stop()
    musik_laeuft = False


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

delorean_img = erstelle_delorean_surface()
auto_rot_img = erstelle_auto_rot_surface()


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
                    musik_stoppen()

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
                        musik_stoppen()

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
        spieler_x = max(230.0, min(570.0, spieler_x))
        
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
            x_pos = random.randint(235, 565)
            hindernisse.append([x_pos, -80])
            hindernis_timer = 0
            
        # Hindernisse bewegen & Kollisionsprüfung
        h_tempo = (geschwindigkeit_mph / 6.0) + 3.0
        spieler_rect = pygame.Rect(spieler_x - 18, spieler_y - 35, 36, 70)
        
        for h in hindernisse[:]:
            h[1] += h_tempo
            h_rect = pygame.Rect(h[0] - 18, h[1] - 35, 36, 70)
            
            if spieler_rect.colliderect(h_rect):
                status = "CRASH"
                musik_stoppen()
                
            if h[1] > HOEHE + 100:
                hindernisse.remove(h)
                
        # ⚡ Sieg bei 88 MPH
        if geschwindigkeit_mph >= ziel_geschwindigkeit:
            status = "SIEG"
            sieg_zeit = time.time()
            
            # Feuer-Partikel erzeugen
            for y_p in range(int(spieler_y), HOEHE, 12):
                for offset in [-16, 16]:
                    partikel_liste.append([spieler_x + offset + random.randint(-4, 4), y_p, random.choice([(255, 69, 0), (255, 140, 0), (255, 215, 0)])])

    elif status == "SIEG":
        # 10 Sekunden Fade-Out der Musik
        verstrichen = time.time() - sieg_zeit
        fade_dauer = 10.0
        if verstrichen < fade_dauer and musik_aktiv:
            vol = max(0.0, 0.35 * (1.0 - verstrichen / fade_dauer))
            pygame.mixer.music.set_volume(vol)
        elif verstrichen >= fade_dauer:
            pygame.mixer.music.stop()

    # 3. ZEICHNEN / RENDERN
    # Rasen Hintergrund
    fenster.fill(FARBE_RASEN)
    
    # Asphaltierte Straße (400px breit in der Mitte)
    pygame.draw.rect(fenster, FARBE_STRASSE, (200, 0, 400, HOEHE))
    pygame.draw.line(fenster, FARBE_WEISS, (205, 0), (205, HOEHE), 5)
    pygame.draw.line(fenster, FARBE_WEISS, (595, 0), (595, HOEHE), 5)
    
    # Mittellinien der Straße
    for y_pos in streifen_y:
        pygame.draw.rect(fenster, FARBE_WEISS, (396, y_pos, 8, 40), border_radius=2)
        
    # Hindernisse zeichnen
    for h in hindernisse:
        fenster.blit(auto_rot_img, (h[0] - 22, h[1] - 40))
        
    # Feuer-Spuren bei Sieg
    if status == "SIEG":
        for p in partikel_liste:
            pygame.draw.circle(fenster, p[2], (int(p[0]), int(p[1])), random.randint(4, 7))
            
    # DeLorean zeichnen (nur wenn nicht im SIEG Zustand verschwunden)
    if status != "SIEG":
        fenster.blit(delorean_img, (spieler_x - 22, spieler_y - 40))
        
    # UI Overhead Display (während des Spiels)
    if status == "LÄUFT":
        spd_val = min(geschwindigkeit_mph, ziel_geschwindigkeit)
        txt_spd = font_ui.render(f"SPEED: {spd_val:.1f} MPH", True, FARBE_NEON_BLAU)
        txt_diff = font_ui.render(f"MODUS: {schwierigkeitsgrade[schwierigkeit_index]}", True, FARBE_WEISS)
        fenster.blit(txt_spd, (20, 20))
        fenster.blit(txt_diff, (BREITE - txt_diff.get_width() - 20, 20))
        
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