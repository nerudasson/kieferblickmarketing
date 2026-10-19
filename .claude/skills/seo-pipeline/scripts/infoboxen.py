#!/usr/bin/env python3
"""Feste Infoboxen je Produktgruppe (material/infoboxen.md).

  python3 infoboxen.py anwenden <slug> [<slug> ...]   schreibt die Felder ins Frontmatter von daten/entwuerfe/<slug>.md
  python3 infoboxen.py zeige <kategorie> [<cluster>]

Als Modul: lade(kategorie, cluster=None) -> {feld: text}; leer, wenn die Kategorie nicht hinterlegt ist.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DATEI = ROOT / "material" / "infoboxen.md"
FELDER = ("ursache", "behandlung", "dauer", "kosten", "ablauf")


def _abschnitt(schluessel):
    werte, aktiv = {}, False
    for z in DATEI.read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^##\s+(\S+)\s*$", z)
        if m:
            aktiv = m.group(1) == schluessel
            continue
        m = re.match(r"^-\s+(\w+):\s*(.+?)\s*$", z)
        if aktiv and m and m.group(1) in FELDER and m.group(2) != "offen":
            werte[m.group(1)] = m.group(2)
    return werte


def lade(kategorie, cluster=None):
    """Box je Kategorie; `kategorie/cluster` gewinnt, wenn vorhanden. Felder mit „offen“ bleiben leer."""
    if not DATEI.exists():
        return {}
    return (_abschnitt(f"{kategorie}/{cluster}") if cluster else {}) or _abschnitt(kategorie)


def anwenden(slug):
    pfad = ROOT / "daten" / "entwuerfe" / f"{slug}.md"
    t = pfad.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", t, flags=re.S)
    kat = re.search(r"^kategorie:\s*(\S+)", m.group(1), flags=re.M).group(1)
    cl = re.search(r"^cluster:\s*(\S+)", m.group(1), flags=re.M)
    werte = lade(kat, cl.group(1) if cl else None)
    if not werte:
        return f"{slug}: keine Infobox für Kategorie {kat} hinterlegt"
    zeilen = [z for z in m.group(1).split("\n") if not re.match(r"^(%s):" % "|".join(werte), z)]
    zeilen += [f"{f}: {werte[f]}" for f in FELDER if f in werte]
    pfad.write_text("---\n" + "\n".join(zeilen) + "\n---\n" + t[m.end():], encoding="utf-8")
    return f"{slug}: Infobox {kat} gesetzt"


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "anwenden":
        for s in sys.argv[2:]:
            print(anwenden(s))
    elif len(sys.argv) > 2 and sys.argv[1] == "zeige":
        for k, v in lade(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None).items():
            print(f"{k}: {v}")
    else:
        sys.exit(__doc__)
