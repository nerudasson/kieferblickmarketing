#!/usr/bin/env python3
"""LinkedIn-Export einlesen (nur eigene Beitragstexte, nichts Privates).

  li_import.py posts <Rich_Media.csv> [--out daten/linkedin/raw/<Datum>_eigene-posts.csv]

Liest aus dem Basis-Export von LinkedIn die Zeilen „You uploaded a feed photo/video“ (Beitragstext
steht in „Media Description“). Nachrichten, Kontakte und Einladungen werden nie gelesen. Der Basis-Export
enthält KEINE Reichweite oder Reaktionen; diese kommen aus dem Statistik-Export (Creator-Analytics) und
werden in daten/linkedin/library/own_performance.csv eingetragen.
Hinweis: Der Export ersetzt Nicht-Lateinisches durch „?“; die Zahl steht in nichtlatein_anteil.
"""
import csv
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def main(src, out):
    rows = list(csv.reader(open(src, encoding="utf-8")))[1:]
    res = []
    for r in rows:
        m = re.match(r"You uploaded a (feed photo|video|photo) on (.+?) at", r[0])
        if not m:
            continue
        d = datetime.strptime(m.group(2), "%B %d, %Y").date().isoformat()
        text = r[1].strip()
        if len(text) < 20:
            continue
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        eng = [l for l in lines if re.search(r"[A-Za-z]{4}", l)]
        res.append({
            "datum": d,
            "art": m.group(1),
            "zeichen": len(text),
            "hook_zeile": (eng[0] if eng else lines[0])[:160],
            "hashtags": len(re.findall(r"#\w+", text)),
            "nichtlatein_anteil": f"{text.count('?') / len(text):.1%}",
            "text": text,
        })
    res.sort(key=lambda x: x["datum"], reverse=True)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(res[0]))
        w.writeheader()
        w.writerows(res)
    print(f"{len(res)} Beiträge nach {out}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2 or a[0] != "posts":
        print(__doc__)
        sys.exit(2)
    out = a[a.index("--out") + 1] if "--out" in a else str(ROOT / "daten/linkedin/raw/eigene-posts.csv")
    main(a[1], out)
