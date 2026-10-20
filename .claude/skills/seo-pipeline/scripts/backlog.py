#!/usr/bin/env python3
"""Gemeinsamer Merkzettel der Agenten (statt langer Berichte): daten/backlog.md

  python3 backlog.py add <nebenartikel|beleg|praxis|regel> <slug> "<Text>"     hängt eine Zeile an (Dubletten werden übersprungen)
  python3 backlog.py list [typ]                                                zeigt den Stand, gruppiert nach Typ
  python3 backlog.py schliessen "<Suchtext>" "<Ergebnis>" [belegt|offen|alexander]
                                                                               verschiebt passende offene Zeilen nach "## Erledigt" (Standard: belegt);
                                                                               offen = recherchiert, kein Beleg gefunden; alexander = nur Praxiswissen

Typen: nebenartikel (Vorschlag für eigenen Artikel, speist die nächste Keyword-Auswahl), beleg (Beleg-Lücke),
praxis (Frage an Alexander), regel (Skript-/Regelkonflikt, der Arbeit gekostet hat).
"""
import re
import sys
from datetime import date
from pathlib import Path

PFAD = Path(__file__).resolve().parents[4] / "daten" / "backlog.md"
TYPEN = ("nebenartikel", "beleg", "praxis", "regel")


def lesen():
    return PFAD.read_text(encoding="utf-8").split("\n") if PFAD.exists() else ["# Backlog der Agenten", ""]


def add(typ, slug, text):
    zeilen = lesen()
    norm = lambda x: re.sub(r"\W+", " ", x.lower()).strip()
    if any(norm(text) in norm(z) and f"[{typ}]" in z for z in zeilen):
        print("schon vorhanden"); return
    zeilen.append(f"- [{typ}] {slug}: {text.strip()} ({date.today().isoformat()})")
    PFAD.parent.mkdir(exist_ok=True)
    PFAD.write_text("\n".join(zeilen).rstrip() + "\n", encoding="utf-8")
    print("eingetragen")


def liste(typ=None):
    for t in TYPEN:
        if typ and t != typ:
            continue
        z = [x for x in lesen() if x.startswith(f"- [{t}]") and " → [" not in x]
        print(f"## {t} ({len(z)})")
        print("\n".join(z))


def schliessen(suche, ergebnis, status="belegt"):
    zeilen = lesen()
    norm = lambda x: re.sub(r"\W+", " ", x.lower()).strip()
    treffer = [z for z in zeilen if z.startswith("- [") and norm(suche) in norm(z)]
    if not treffer:
        print("keine offene Zeile gefunden"); return
    rest = [z for z in zeilen if z not in treffer]
    while rest and rest[-1] == "":
        rest.pop()
    if "## Erledigt" not in rest:
        rest += ["", "## Erledigt", ""]
    for z in treffer:
        rest.append(f"{z} → [{status} {date.today().isoformat()}] {ergebnis.strip()}")
    PFAD.write_text("\n".join(rest).rstrip() + "\n", encoding="utf-8")
    print(f"{len(treffer)} Zeile(n) nach Erledigt verschoben")


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 4 and a[0] == "add" and a[1] in TYPEN:
        add(a[1], a[2], a[3])
    elif len(a) in (3, 4) and a[0] == "schliessen":
        schliessen(a[1], a[2], a[3] if len(a) == 4 else "belegt")
    elif a and a[0] == "list":
        liste(a[1] if len(a) > 1 else None)
    else:
        sys.exit(__doc__)
