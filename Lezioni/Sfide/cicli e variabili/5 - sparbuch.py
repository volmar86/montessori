# ============================================================
#  MEIN SPARBUCH — wie wächst das Geld?
#
#  Jedes Jahr gibt die Bank Zinsen auf das, was schon da ist.
#  Vergleiche mit "jedes Jahr gleich viel dazu".
# ============================================================

# ============================================================
#  HIER WIRD ALLES EINGESTELLT
# ============================================================

start = 100       # <-- so viel Euro legst du an
zins = 5          # <-- Zinsen pro Jahr in Prozent
jahre = 20        # <-- wie viele Jahre du wartest

# ============================================================

betrag = start               # Geld mit Zinseszins
einfach = start              # Geld, zu dem jedes Jahr gleich viel kommt
zuwachs = start * zins / 100 # so viel kommt im ersten Jahr dazu

print("Jahr | mit Zinseszins | immer gleich viel dazu")

for jahr in range(1, jahre + 1):
    # Zinsen auf das ganze Geld, das jetzt da ist.
    betrag = betrag + betrag * zins / 100
    # Immer wieder derselbe Betrag.
    einfach = einfach + zuwachs
    print(jahr, "|", round(betrag, 2), "|", round(einfach, 2))

# ============================================================
#  MISSIONEN FÜR DICH
#  1. Nach wie vielen Jahren ist das Geld doppelt so viel?
#  2. Ändere zins auf 10. Wann verdoppelt es sich jetzt?
#  3. Was ist größer: Zinseszins oder "gleich viel dazu"?
# ============================================================
