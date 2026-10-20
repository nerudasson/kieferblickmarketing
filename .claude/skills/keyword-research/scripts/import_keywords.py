#!/usr/bin/env python3
"""Keyword-Exporte (Semrush-Format) in die Datenbasis `daten/keywords-export.csv` einpflegen.

  python3 import_keywords.py <export.csv> [<export.csv> ...] [--stand 2026-10] [--dry-run]

Erwartete Spalten: Keyword, Difficulty, "Search vol.", "Search intent", CPC, Competition (weitere werden ignoriert).
Die Datei ist die fortlaufende Datenbasis neben der Excel (Stand 2025): Je Keyword steht eine Zeile (klein geschrieben),
bei Dubletten gewinnt der neuere Stand, bei gleichem Stand der höhere Wert. `waehle_keywords.py` liest Excel und diese Datei,
die Export-Werte ersetzen die Excel-Werte. Die Quelle (Dateiname ohne Hash) bleibt je Zeile erhalten.
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ZIEL = ROOT / "daten" / "keywords-export.csv"
FELDER = ["keyword", "volumen", "schwierigkeit", "intention", "cpc", "wettbewerb", "quelle", "stand"]


def zahl(x, typ=float):
    try:
        return typ(float(str(x).replace(",", ".")))
    except (TypeError, ValueError):
        return None


def quelle(pfad):
    n = Path(pfad).stem
    n = re.sub(r"^[0-9a-f]{8}-", "", n)
    n = re.sub(r"^export_research_de_suggestion_keywords_history_related_eur_", "", n)
    return "Semrush-Export " + n


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    stand = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--stand"), "2026-10")
    args = [a for a in args if a != stand]
    if not args:
        sys.exit(__doc__)
    db = {}
    if ZIEL.exists():
        for r in csv.DictReader(ZIEL.open(encoding="utf-8", newline="")):
            db[r["keyword"]] = r
    neu = dup = 0
    for pfad in args:
        n_neu = n_dup = n_alle = 0
        for r in csv.DictReader(open(pfad, encoding="utf-8-sig", newline="")):
            k = (r.get("Keyword") or "").strip().lower()
            if not k:
                continue
            n_alle += 1
            zeile = {"keyword": k, "volumen": zahl(r.get("Search vol."), int) or 0, "schwierigkeit": zahl(r.get("Difficulty"), int),
                     "intention": (r.get("Search intent") or "").strip(), "cpc": zahl(r.get("CPC")) or 0,
                     "wettbewerb": zahl(r.get("Competition")) or 0, "quelle": quelle(pfad), "stand": stand}
            alt = db.get(k)
            if alt is None:
                n_neu += 1
            else:
                n_dup += 1
                if (alt["stand"], int(alt["volumen"] or 0)) > (stand, zeile["volumen"]):
                    continue
            db[k] = zeile
        print(f"{Path(pfad).name[:60]}: {n_alle} Zeilen, {n_neu} neu, {n_dup} schon vorhanden")
        neu += n_neu
        dup += n_dup
    print(f"Datenbasis: {len(db)} Keywords ({neu} neu, {dup} Dubletten aufgelöst)")
    if "--dry-run" in sys.argv:
        return
    zeilen = sorted(db.values(), key=lambda z: -int(z["volumen"] or 0))
    with ZIEL.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FELDER)
        w.writeheader()
        w.writerows(zeilen)
    print(f"-> {ZIEL}")


if __name__ == "__main__":
    main()
