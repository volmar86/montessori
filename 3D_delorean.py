# ============================================================
#  DELOREAN 88 MPH CHALLENGE – PSEUDO-3D / MODE 7
#
#  Steuerung:
#    - A / D oder Pfeiltasten zum Lenken
#    - ENTER oder R für Neustart
# ============================================================

import pygame
import random
import math
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

pygame.init()
fenster = pygame.display.set_mode((BREITE, HOEHE))
pygame.display.set_caption("DeLorean 88 mph Challenge – Pseudo-3D")
uhr = pygame.time.Clock()

font_ui = pygame.font.SysFont("Courier", 22, bold=True)
font_titel = pygame.font.SysFont("Courier", 32, bold=True)

# ====== GAME VARIABLES ======
pos_z = 0.0
spieler_x = 0.0
geschwindigkeit_mph = 30.0
ziel_geschwindigkeit = 88.0
status = "LÄUFT"
kurven_neigung = 0.0

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
def zeichne_pseudo_3d_welt():
    zeichne_himmel()

    for y in range(HORIZONT_Y, HOEHE):
        perspektive = (y - HORIZONT_Y) / (HOEHE - HORIZONT_Y)
        streifen_z = pos_z + (1.0 / (perspektive + 0.001)) * 20.0
        abwechseln = int(streifen_z / 15.0) % 2 == 0

        breite = strassen_breite(perspektive)
        mitte = strassen_mitte(perspektive)

        rasen = FARBE_RASEN_1 if abwechseln else FARBE_RASEN_2
        strasse = FARBE_STRASSE_1 if abwechseln else FARBE_STRASSE_2
        bord = FARBE_BORDSTEIN_1 if abwechseln else FARBE_BORDSTEIN_2

        # Dunst: ganz hinten verschwimmen die Farben mit dem Horizont
        dunst = max(0.0, 1.0 - (y - HORIZONT_Y) / 110)
        rasen = mischen(rasen, FARBE_DUNST, dunst)
        strasse = mischen(strasse, FARBE_DUNST, dunst * 0.8)
        bord = mischen(bord, FARBE_DUNST, dunst * 0.6)

        pygame.draw.line(fenster, rasen, (0, y), (BREITE, y))
        pygame.draw.line(fenster, bord, (mitte - breite / 2 - 12, y), (mitte + breite / 2 + 12, y), 2)
        pygame.draw.line(fenster, strasse, (mitte - breite / 2, y), (mitte + breite / 2, y))

        # gestrichelte Mittellinie (wird vorne breiter)
        if abwechseln:
            halb = max(1, perspektive * 5)
            linie = mischen(FARBE_MITTELLINIE, FARBE_DUNST, dunst)
            pygame.draw.line(fenster, linie, (mitte - halb, y), (mitte + halb, y))


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


# ====== HAUPTSCHLEIFE ======
laufend = True
while laufend:
    dt = uhr.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            laufend = False
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RETURN, pygame.K_r] and status in ["CRASH", "SIEG"]:
                status = "LÄUFT"
                geschwindigkeit_mph = 30.0
                pos_z = 0.0
                spieler_x = 0.0
                hindernisse.clear()

    if status == "LÄUFT":
        if geschwindigkeit_mph < ziel_geschwindigkeit:
            geschwindigkeit_mph += 8.0 * dt
        else:
            geschwindigkeit_mph = ziel_geschwindigkeit
            status = "SIEG"

        pos_z += geschwindigkeit_mph * 5.0 * dt

        # Lenkung & F-Zero Neigungseffekt
        tasten = pygame.key.get_pressed()
        lenk_richtung = 0
        if tasten[pygame.K_a] or tasten[pygame.K_LEFT]:
            lenk_richtung = 1
        if tasten[pygame.K_d] or tasten[pygame.K_RIGHT]:
            lenk_richtung = -1

        spieler_x += lenk_richtung * 2.5 * dt
        spieler_x = max(-1.8, min(1.8, spieler_x))
        kurven_neigung = -lenk_richtung * 12.0

        # Spawnen von Hindernissen (spur: wo auf der Straße, -0.75 = links ... +0.75 = rechts)
        if random.random() < 0.03:
            hindernisse.append([pos_z + 400.0, random.uniform(-0.75, 0.75)])

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

    # 4. DeLorean zeichnen
    if status != "SIEG":
        gedrehtes_auto = pygame.transform.rotate(delorean_base, kurven_neigung)
        rect = gedrehtes_auto.get_rect(center=(BREITE // 2, 520))
        fenster.blit(gedrehtes_auto, rect)

    # 5. Tacho und Text
    tacho_zeichnen(min(geschwindigkeit_mph, ziel_geschwindigkeit))

    if status == "CRASH":
        txt_c = font_titel.render("CRASH! [ENTER / R]", True, (255, 69, 0))
        fenster.blit(txt_c, txt_c.get_rect(center=(BREITE // 2, 300)))
    elif status == "SIEG":
        txt_s = font_titel.render("88 MPH! ZEITREISE!", True, FARBE_TEXT)
        fenster.blit(txt_s, txt_s.get_rect(center=(BREITE // 2, 300)))

    pygame.display.flip()

pygame.quit()
sys.exit()