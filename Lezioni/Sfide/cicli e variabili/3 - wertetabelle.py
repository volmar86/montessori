# ============================================================
#  WERTETABELLE — suche das x für die Gleichung
#
#  Der Computer rechnet für jedes x die linke Seite aus.
#  Du suchst die Zeile, in der das Ergebnis "ziel" ist.
# ============================================================

# ============================================================
#  HIER WIRD ALLES EINGESTELLT
# ============================================================

faktor = 3        # <-- die Gleichung ist: faktor * x + zusatz = ziel
zusatz = 5        # <-- hier: 3 * x + 5 = 29
ziel = 29         # <-- das Ergebnis, das du suchst
x_von = 0         # <-- die Tabelle beginnt bei diesem x
x_bis = 10        # <-- die Tabelle endet bei diesem x

# ============================================================

print("Gleichung:", faktor, "* x +", zusatz, "=", ziel)
print()
print("x     Ergebnis")

for x in range(x_von, x_bis + 1):
    ergebnis = faktor * x + zusatz
    print(x, "    ", ergebnis)

# ============================================================
#  MISSIONEN FÜR DICH
#  1. In welcher Zeile steht das Ziel? Das ist dein x.
#  2. Rechne die Gleichung auch von Hand und vergleiche.
#  3. Ändere die Zahlen und suche ein neues x.
# ============================================================
