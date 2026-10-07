# ============================================================
#  BUCHSTABEN — jeder Buchstabe als eigener Befehl
#
#  Die Regel, die alles zusammenhält:
#  Jeder Buchstabe FÄNGT unten links an und HÖRT unten links
#  beim nächsten Buchstaben auf — Stift oben, Blickrichtung
#  rechts. Darum kann man sie beliebig hintereinander schreiben.
#
#  So benutzt man es:
#     stift = Buchstaben(hoehe=100)
#     stift.schreibe("HALLO WELT")
#     stift.fertig()
#
#  Oder ein Buchstabe allein:
#     stift.D()
#
#  ECKIG ODER RUND?
#  B C D G J O P Q R S U gibt es zweimal: rund (mit circle)
#  und eckig (nur mit geraden Linien). Eckig geht ohne circle,
#  also mit dem, was ihr schon könnt.
#     stift.S_eckig()                      ein Buchstabe
#     Buchstaben(eckig=True).schreibe("SOFIA")   das ganze Wort
# ============================================================

import turtle

# Jeder Buchstabe ist in einem Kästchen gezeichnet:
# links unten ist (0, 0), oben ist 100. Die Breite steht bei
# jedem Buchstaben dabei.
HOCH = 100


class Buchstaben:

    def __init__(self, hoehe=100, abstand=20, dicke=4, farbe="black",
                 start_x=-300, start_y=0, eckig=False, rand_rechts=None):
        self.massstab = hoehe / HOCH
        self.eckig = eckig
        self.rand_rechts = rand_rechts    # None = bis zum Fensterrand
        self.abstand = abstand
        self.start_x = start_x
        self.start_y = start_y
        self.x = start_x                  # linke untere Ecke des nächsten Buchstabens
        self.y = start_y
        self.t = turtle.Turtle()
        self.t.speed(0)
        self.t.pensize(dicke)
        self.t.color(farbe)
        self.t.hideturtle()
        self.t.penup()
        self.t.goto(self.x, self.y)
        self.t.setheading(0)

    # ---------- Werkzeuge ----------

    def _punkt(self, x, y):
        """Rechnet eine Stelle im Kästchen in eine Stelle auf dem Bildschirm um."""
        return self.x + x * self.massstab, self.y + y * self.massstab

    def _linie(self, punkte):
        """Zeichnet einen Linienzug durch alle Punkte."""
        self.t.penup()
        self.t.goto(self._punkt(*punkte[0]))
        self.t.pendown()
        for p in punkte[1:]:
            self.t.goto(self._punkt(*p))
        self.t.penup()

    def _bogen(self, start, richtung, radius, winkel):
        """Zeichnet einen Bogen: wo anfangen, wohin schauen, wie rund, wie weit.
        Radius positiv = Mittelpunkt links, gegen den Uhrzeigersinn.
        Radius negativ = Mittelpunkt rechts, mit dem Uhrzeigersinn."""
        self.t.penup()
        self.t.goto(self._punkt(*start))
        self.t.setheading(richtung)
        self.t.pendown()
        self.t.circle(radius * self.massstab, winkel)
        self.t.penup()

    def _punkte_oben(self, breite):
        """Die zwei Punkte für Ä, Ö, Ü."""
        for x in [breite * 0.3, breite * 0.7]:
            self.t.penup()
            self.t.goto(self._punkt(x, 120))
            self.t.dot(self.t.pensize() * 2)

    def _weiter(self, breite):
        """Fertig: ab zur linken unteren Ecke des nächsten Buchstabens."""
        self.x = self.x + (breite + self.abstand) * self.massstab
        self.t.penup()
        self.t.goto(self.x, self.y)
        self.t.setheading(0)

    # ---------- Buchstaben aus geraden Linien ----------

    def A(self):
        self._linie([(0, 0), (35, 100), (70, 0)])
        self._linie([(14, 40), (56, 40)])
        self._weiter(70)

    def E(self):
        self._linie([(60, 100), (0, 100), (0, 0), (60, 0)])
        self._linie([(0, 50), (45, 50)])
        self._weiter(60)

    def F(self):
        self._linie([(60, 100), (0, 100), (0, 0)])
        self._linie([(0, 50), (45, 50)])
        self._weiter(60)

    def H(self):
        self._linie([(0, 0), (0, 100)])
        self._linie([(60, 0), (60, 100)])
        self._linie([(0, 50), (60, 50)])
        self._weiter(60)

    def I(self):
        self._linie([(0, 100), (40, 100)])
        self._linie([(20, 100), (20, 0)])
        self._linie([(0, 0), (40, 0)])
        self._weiter(40)

    def K(self):
        self._linie([(0, 0), (0, 100)])
        self._linie([(60, 100), (0, 50), (60, 0)])
        self._weiter(60)

    def L(self):
        self._linie([(0, 100), (0, 0), (55, 0)])
        self._weiter(55)

    def M(self):
        self._linie([(0, 0), (0, 100), (40, 40), (80, 100), (80, 0)])
        self._weiter(80)

    def N(self):
        self._linie([(0, 0), (0, 100), (65, 0), (65, 100)])
        self._weiter(65)

    def T(self):
        self._linie([(0, 100), (60, 100)])
        self._linie([(30, 100), (30, 0)])
        self._weiter(60)

    def V(self):
        self._linie([(0, 100), (32, 0), (65, 100)])
        self._weiter(65)

    def W(self):
        self._linie([(0, 100), (22, 0), (45, 70), (68, 0), (90, 100)])
        self._weiter(90)

    def X(self):
        self._linie([(0, 100), (60, 0)])
        self._linie([(0, 0), (60, 100)])
        self._weiter(60)

    def Y(self):
        self._linie([(0, 100), (30, 50), (60, 100)])
        self._linie([(30, 50), (30, 0)])
        self._weiter(60)

    def Z(self):
        self._linie([(0, 100), (60, 100), (0, 0), (60, 0)])
        self._weiter(60)

    # ---------- Buchstaben mit Bögen ----------

    def B(self):
        self._linie([(0, 0), (0, 100)])
        self._linie([(0, 100), (30, 100)])
        self._bogen((30, 100), 0, -25, 180)
        self._linie([(30, 50), (0, 50)])
        self._linie([(0, 50), (30, 50)])
        self._bogen((30, 50), 0, -25, 180)
        self._linie([(30, 0), (0, 0)])
        self._weiter(55)

    def C(self):
        self._bogen((70, 65), 90, 35, 180)
        self._linie([(0, 65), (0, 35)])
        self._bogen((0, 35), 270, 35, 180)
        self._weiter(70)

    def D(self):
        self._linie([(0, 0), (0, 100)])
        self._linie([(0, 100), (10, 100)])
        self._bogen((10, 100), 0, -50, 180)
        self._linie([(10, 0), (0, 0)])
        self._weiter(60)

    def G(self):
        self._bogen((70, 65), 90, 35, 180)
        self._linie([(0, 65), (0, 35)])
        self._bogen((0, 35), 270, 35, 180)
        self._linie([(70, 35), (70, 50), (40, 50)])
        self._weiter(70)

    def J(self):
        self._linie([(50, 100), (50, 25)])
        self._bogen((50, 25), 270, -25, 180)
        self._weiter(50)

    def O(self):
        self._linie([(0, 35), (0, 65)])
        self._bogen((0, 65), 90, -35, 180)
        self._linie([(70, 65), (70, 35)])
        self._bogen((70, 35), 270, -35, 180)
        self._weiter(70)

    def P(self):
        self._linie([(0, 0), (0, 100)])
        self._linie([(0, 100), (30, 100)])
        self._bogen((30, 100), 0, -25, 180)
        self._linie([(30, 50), (0, 50)])
        self._weiter(55)

    def Q(self):
        self._linie([(0, 35), (0, 65)])
        self._bogen((0, 65), 90, -35, 180)
        self._linie([(70, 65), (70, 35)])
        self._bogen((70, 35), 270, -35, 180)
        self._linie([(45, 25), (75, -5)])
        self._weiter(75)

    def R(self):
        self._linie([(0, 0), (0, 100)])
        self._linie([(0, 100), (30, 100)])
        self._bogen((30, 100), 0, -25, 180)
        self._linie([(30, 50), (0, 50)])
        self._linie([(0, 50), (55, 0)])
        self._weiter(55)

    def S(self):
        self._bogen((50, 75), 90, 25, 270)
        self._bogen((25, 50), 0, -25, 270)
        self._weiter(50)

    def U(self):
        self._linie([(0, 100), (0, 30)])
        self._bogen((0, 30), 270, 30, 180)
        self._linie([(60, 30), (60, 100)])
        self._weiter(60)

    # ---------- Die gleichen Buchstaben, aber eckig ----------
    # Nur gerade Linien: kein circle nötig.

    def B_eckig(self):
        self._linie([(0, 0), (0, 100)])
        self._linie([(0, 100), (35, 100), (55, 80), (55, 70), (35, 50), (0, 50)])
        self._linie([(0, 50), (35, 50), (55, 30), (55, 20), (35, 0), (0, 0)])
        self._weiter(55)

    def C_eckig(self):
        self._linie([(60, 85), (40, 100), (15, 100), (0, 85),
                     (0, 15), (15, 0), (40, 0), (60, 15)])
        self._weiter(60)

    def D_eckig(self):
        self._linie([(0, 0), (0, 100), (40, 100), (60, 70),
                     (60, 30), (40, 0), (0, 0)])
        self._weiter(60)

    def G_eckig(self):
        self._linie([(60, 85), (40, 100), (15, 100), (0, 85),
                     (0, 15), (15, 0), (40, 0), (60, 15), (60, 45), (35, 45)])
        self._weiter(60)

    def J_eckig(self):
        self._linie([(50, 100), (50, 25), (35, 0), (15, 0), (0, 20)])
        self._weiter(50)

    def O_eckig(self):
        self._linie([(20, 0), (0, 25), (0, 75), (20, 100), (50, 100),
                     (70, 75), (70, 25), (50, 0), (20, 0)])
        self._weiter(70)

    def P_eckig(self):
        self._linie([(0, 0), (0, 100), (35, 100), (55, 80),
                     (55, 70), (35, 50), (0, 50)])
        self._weiter(55)

    def Q_eckig(self):
        self._linie([(20, 0), (0, 25), (0, 75), (20, 100), (50, 100),
                     (70, 75), (70, 25), (50, 0), (20, 0)])
        self._linie([(45, 25), (75, -5)])
        self._weiter(75)

    def R_eckig(self):
        self._linie([(0, 0), (0, 100), (35, 100), (55, 80),
                     (55, 70), (35, 50), (0, 50)])
        self._linie([(0, 50), (55, 0)])
        self._weiter(55)

    def S_eckig(self):
        self._linie([(60, 85), (40, 100), (15, 100), (0, 85), (0, 65),
                     (15, 50), (45, 50), (60, 35), (60, 15), (45, 0),
                     (15, 0), (0, 15)])
        self._weiter(60)

    def U_eckig(self):
        self._linie([(0, 100), (0, 25), (20, 0), (40, 0), (60, 25), (60, 100)])
        self._weiter(60)

    # ---------- Umlaute ----------

    def Ae(self):
        self._punkte_oben(70)
        self.A()

    def Oe(self):
        self._punkte_oben(70)
        self.O_eckig() if self.eckig else self.O()

    def Ue(self):
        self._punkte_oben(60)
        self.U_eckig() if self.eckig else self.U()

    # ---------- Wörter ----------

    NAMEN = {"Ä": "Ae", "Ö": "Oe", "Ü": "Ue"}

    # ---------- Wie breit ist ein Buchstabe? ----------
    # Das braucht man, um VORHER zu wissen, ob ein Wort noch in
    # die Zeile passt.

    BREITEN = {"A": 70, "B": 55, "C": 70, "D": 60, "E": 60, "F": 60, "G": 70,
               "H": 60, "I": 40, "J": 50, "K": 60, "L": 55, "M": 80, "N": 65,
               "O": 70, "P": 55, "Q": 75, "R": 55, "S": 50, "T": 60, "U": 60,
               "V": 65, "W": 90, "X": 60, "Y": 60, "Z": 60,
               "Ä": 70, "Ö": 70, "Ü": 60, " ": 40}

    BREITEN_ECKIG = {"B": 55, "C": 60, "D": 60, "G": 60, "J": 50, "O": 70,
                     "P": 55, "Q": 75, "R": 55, "S": 60, "U": 60, "Ö": 70,
                     "Ü": 60}

    def buchstabenbreite(self, zeichen):
        """Wie breit ist dieser Buchstabe, mit dem Abstand dahinter?"""
        zeichen = zeichen.upper()
        if self.eckig and zeichen in self.BREITEN_ECKIG:
            breite = self.BREITEN_ECKIG[zeichen]
        else:
            breite = self.BREITEN.get(zeichen, 0)
        return (breite + self.abstand) * self.massstab

    def wortbreite(self, wort):
        """Wie breit ist ein ganzes Wort?"""
        return sum(self.buchstabenbreite(z) for z in wort)

    def _rechter_rand(self):
        if self.rand_rechts is not None:
            return self.rand_rechts
        return turtle.Screen().window_width() / 2 - 20

    def _passt_noch(self, breite):
        return self.x + breite <= self._rechter_rand()

    def leerzeichen(self):
        self._weiter(40)

    def zeilenumbruch(self):
        self.x = self.start_x
        self.y = self.y - 160 * self.massstab
        self.t.penup()
        self.t.goto(self.x, self.y)
        self.t.setheading(0)

    def _ein_zeichen(self, zeichen):
        """Zeichnet genau einen Buchstaben. Unbekanntes wird übersprungen."""
        name = self.NAMEN.get(zeichen, zeichen)
        if self.eckig and hasattr(self, name + "_eckig"):
            name = name + "_eckig"
        if hasattr(self, name):
            getattr(self, name)()

    def schreibe(self, text, umbruch=True):
        """Schreibt einen Text. Mit umbruch=True fängt ein Wort, das nicht
        mehr in die Zeile passt, automatisch auf der nächsten Zeile an."""
        for zeile, absatz in enumerate(text.upper().split("\n")):
            if zeile > 0:
                self.zeilenumbruch()
            for nummer, wort in enumerate(absatz.split(" ")):
                if nummer > 0:                       # das Leerzeichen davor
                    if umbruch and not self._passt_noch(self.buchstabenbreite(" ")):
                        self.zeilenumbruch()
                    else:
                        self.leerzeichen()
                if umbruch and self.x > self.start_x and \
                        not self._passt_noch(self.wortbreite(wort)):
                    self.zeilenumbruch()
                for zeichen in wort:
                    if umbruch and not self._passt_noch(self.buchstabenbreite(zeichen)):
                        self.zeilenumbruch()         # ein Wort, das allein zu lang ist
                    self._ein_zeichen(zeichen)

    def fertig(self):
        turtle.done()


if __name__ == "__main__":
    fenster = turtle.Screen()
    fenster.setup(1000, 400)
    fenster.title("Buchstaben")

    stift = Buchstaben(hoehe=90, start_x=-420, start_y=-40, eckig=True)
    stift.schreibe("WILLKOMMEN AN ALLEN")
    stift.fertig()