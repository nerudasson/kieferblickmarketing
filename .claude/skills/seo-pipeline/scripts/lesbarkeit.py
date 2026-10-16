#!/usr/bin/env python3
"""Prüft einen Artikel-Entwurf (Markdown) auf Lesbarkeit und Formatmix.

Aufruf: python3 lesbarkeit.py daten/entwuerfe/<slug>.md [weitere.md ...]
Exit-Code 1, wenn eine Hürde gerissen wird (Schleife im Writer: überarbeiten).

Lesbarkeit: Flesch-Index nach Amstad (deutsch) = 180 - ASL - 58,5 * ASW
ASL = Wörter pro Satz, ASW = Silben pro Wort. Silben werden über Vokalgruppen
geschätzt, Abweichung etwa +-3 Punkte. Gezählt wird nur Fließtext, Listen und
Fragen/Antworten. Frontmatter, Tabellen, Quellen und Platzhalter zählen nicht.
"""
import re
import sys

MIN_FLESCH = 60
MAX_SATZ_WOERTER = 25        # einzelner Satz
MAX_ASL = 14                 # Durchschnitt
MAX_ABSATZ_SAETZE = 3
MAX_FLIESS_ABSCHNITT = 4     # aufeinanderfolgende Absätze ohne Liste/Tabelle/Box
MIN_H2 = 4


def silben(wort):
    return max(1, len(re.findall(r"[aeiouyäöü]+", wort.lower())))


def zerlegen(md):
    md = re.sub(r"^---\n.*?\n---\n", "", md, flags=re.S)
    md = re.split(r"^##\s+Quellen\b", md, flags=re.M)[0]
    md = re.sub(r"\[FAKT FEHLT:[^\]]*\]", "", md)
    return md


def pruefe(pfad):
    roh = open(pfad, encoding="utf-8").read()
    fm = re.match(r"^---\n(.*?)\n---\n", roh, flags=re.S)
    fm = fm.group(1) if fm else ""
    md = zerlegen(roh)
    zeilen = md.split("\n")

    bloecke = []   # (typ, text)
    puffer = []

    def flush():
        if puffer:
            bloecke.append(("p", " ".join(puffer).strip()))
            puffer.clear()

    for z in zeilen:
        s = z.strip()
        if not s:
            flush()
        elif s.startswith("#"):
            flush()
            bloecke.append(("h", s))
        elif s.startswith("|"):
            flush()
            if not bloecke or bloecke[-1][0] != "t":
                bloecke.append(("t", s))
        elif re.match(r"^([-*]|\d+\.)\s", s):
            flush()
            bloecke.append(("l", re.sub(r"^([-*]|\d+\.)\s+", "", s)))
        elif s.startswith(">"):
            flush()
            bloecke.append(("b", s.lstrip("> ").strip()))
        else:
            puffer.append(s)
    flush()

    def sauber(t):
        t = re.sub(r"\[\d+(?:[,–-]\s*\d+)*\]", "", t)       # Fußnoten [1]
        t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)         # Links
        t = re.sub(r"[*_`]", "", t)
        t = re.sub(r"^(Merksatz|CTA|Tipp):\s*", "", t)
        return t.strip()

    saetze = []
    for typ, t in bloecke:
        if typ in ("p", "l", "b"):
            t = sauber(t)
            for s in re.split(r"(?<=[.!?])\s+", t):
                if len(re.findall(r"[A-Za-zÄÖÜäöüß]+", s)) >= 1:
                    saetze.append(s)
        elif typ == "h" and re.match(r"^###\s", t):
            pass  # Fragen in der FAQ sind Überschriften, zählen nicht

    woerter = [w for s in saetze for w in re.findall(r"[A-Za-zÄÖÜäöüß]+", s)]
    if not saetze or not woerter:
        print(f"{pfad}: kein Text gefunden")
        return False
    asl = len(woerter) / len(saetze)
    asw = sum(silben(w) for w in woerter) / len(woerter)
    fre = 180 - asl - 58.5 * asw
    lang = [s for s in saetze if len(s.split()) > MAX_SATZ_WOERTER]

    absaetze = [(sauber(t)) for typ, t in bloecke if typ == "p"]
    lange_abs = [a for a in absaetze
                 if len([x for x in re.split(r"(?<=[.!?])\s+", a) if x]) > MAX_ABSATZ_SAETZE]

    # Fließtext-Wüsten: viele Absätze in Folge ohne Liste, Tabelle, Box oder Überschrift
    lauf = maxlauf = 0
    for typ, _ in bloecke:
        if typ == "p":
            lauf += 1
            maxlauf = max(maxlauf, lauf)
        else:
            lauf = 0

    h2 = sum(1 for typ, t in bloecke if typ == "h" and re.match(r"^##\s", t))
    hat = {
        "kurz": "kurz:" in fm,
        "merksatz": any(typ == "b" and t.lower().startswith("merksatz") for typ, t in bloecke),
        "liste": any(typ == "l" for typ, _ in bloecke),
        "tabelle": any(typ == "t" for typ, _ in bloecke),
        "faq": any(typ == "h" and re.match(r"^###\s", t) for typ, t in bloecke),
        "cta": any(typ == "b" and t.lower().startswith("cta") for typ, t in bloecke),
    }
    # Pflichtbausteine: Kurzfassung, Merksatz, Liste, FAQ, CTA. Tabelle nur bei Vergleich/Kosten.
    fehlt = [k for k in ("kurz", "merksatz", "liste", "faq", "cta") if not hat[k]]
    intent = re.search(r"^intent:\s*(\S+)", fm, flags=re.M)
    intent = intent.group(1).lower() if intent else ""
    if intent in ("kosten", "vergleich", "transaktional") and not hat["tabelle"]:
        fehlt.append("tabelle")

    probleme = []
    if fre < MIN_FLESCH:
        probleme.append(f"Lesbarkeit {fre:.0f} < {MIN_FLESCH}")
    if asl > MAX_ASL:
        probleme.append(f"Ø Satzlänge {asl:.1f} > {MAX_ASL} Wörter")
    if lang:
        probleme.append(f"{len(lang)} Satz/Sätze über {MAX_SATZ_WOERTER} Wörter, z. B. „{' '.join(lang[0].split()[:8])} …“")
    if lange_abs:
        probleme.append(f"{len(lange_abs)} Absatz/Absätze mit mehr als {MAX_ABSATZ_SAETZE} Sätzen")
    if maxlauf > MAX_FLIESS_ABSCHNITT:
        probleme.append(f"{maxlauf} Absätze in Folge ohne Liste, Tabelle oder Merksatz")
    if h2 < MIN_H2:
        probleme.append(f"nur {h2} H2-Abschnitte (min. {MIN_H2})")
    if fehlt:
        probleme.append("Bausteine fehlen: " + ", ".join(fehlt))

    print(f"{pfad}")
    print(f"  Wörter {len(woerter)} · Sätze {len(saetze)} · Ø {asl:.1f} Wörter/Satz · "
          f"{asw:.2f} Silben/Wort · Lesbarkeit {fre:.0f}")
    print("  Bausteine: " + " ".join(f"{k}={'ja' if v else 'nein'}" for k, v in hat.items())
          + f" · H2={h2}")
    if probleme:
        print("  PRÜFEN:")
        for p in probleme:
            print("   - " + p)
    else:
        print("  OK")
    return not probleme


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    ok = all([pruefe(p) for p in sys.argv[1:]])
    sys.exit(0 if ok else 1)
