#!/usr/bin/env python3
"""Themenplan aus der gesamten Keyword-Basis (Excel + daten/keywords-export.csv) -> daten/themenplan.csv

  python3 themenplan.py [--dry-run]

Schritte: relevante Keywords (gleiche Filter wie waehle_keywords.py) -> Zusammenlegen gleicher Suchabsicht über Wortstämme
(Näherung, ohne SERP-Daten) -> Score = Kopf-Volumen / (1 + Schwierigkeit/10) x Produktgewicht x Intentgewicht -> Wellen und Batches.
Produkt- und Intentgewichte sind Annahmen (siehe GEWICHT/INTENT_GEWICHT), Alexander kann sie ändern.
Welle 1 = beste 100 von Stufe A (Kopf-Volumen >= 200, KD <= 40), Welle 2 = Rest von A, Welle 3 = Stufe B (100-199, KD <= 40),
Welle 0 = schwere Kopfbegriffe (KD > 40, Volumen >= 200) als Hauptartikel, Welle 9 = zurückgestellt (Volumen < 100).
"""
import csv
import json
import re
import sys
from pathlib import Path

import openpyxl

sys.path.insert(0, str(Path(__file__).resolve().parent))
import waehle_keywords as w

ROOT = w.ROOT
GEWICHT = {"aligner/aligner": 1.0, "aligner/biss": 0.8, "retainer/retainer": 0.9, "schnarchen/schnarchen": 0.9,
           "bleaching/bleaching": 0.8, "bleaching/pzr": 0.8, "veneers/veneers": 0.4}   # Annahme; Veneers: Seite erst mit Labor live
INTENT_GEWICHT = {"kosten": 1.3, "erfahrung": 1.3, "ausloeser": 1.2, "rueckfall": 1.2, "anbieter": 1.0, "info": 1.0}
PRODUKT_REIHENFOLGE = ["retainer/retainer", "bleaching/bleaching", "aligner/aligner", "aligner/biss", "schnarchen/schnarchen", "bleaching/pzr", "veneers/veneers"]
STOP = set("wie viel was kostet kosten eine einen einer einem ein der die das den dem für bei beim mit ohne und oder von vom zum zur ist sind gibt man kann ich mein meine nach vor auf in im am an".split())


def stems(k):
    return frozenset(t[:5] for t in re.findall(r"[a-zäöüß]+", k) if t not in STOP and len(t) > 2)


def main():
    regeln = json.loads((ROOT / ".claude/skills/seo-pipeline/references/themen.json").read_text(encoding="utf-8"))["regeln"]
    rows = {}
    for r in list(openpyxl.load_workbook(ROOT / "daten/Kieferblick_Keyword-Auswertung_v1.xlsx", read_only=True, data_only=True)["Keywords_Funnel"].iter_rows(values_only=True))[1:]:
        k = (r[1] or "").strip().lower()
        if k:
            rows[k] = (int(r[2] or 0), float(r[3]) if r[3] not in (None, "") else 30.0)
    exp = ROOT / "daten" / "keywords-export.csv"
    if exp.exists():
        for z in csv.DictReader(exp.open(encoding="utf-8")):
            rows[z["keyword"]] = (int(z["volumen"]), float(z["schwierigkeit"] or 30))
    kept = []
    for k, (v, d) in rows.items():
        if w.AUS.search(k) or w.MARKEN.search(k):
            continue
        reg = next((x for x in regeln if re.search(x["muster"], k)), None)
        if not reg or reg.get("geparkt"):
            continue
        kept.append((v, d, k, reg["thema"] + "/" + reg["cluster"], reg["kategorie"]))
    kept.sort(reverse=True)
    cl = []
    for v, d, k, t, kat in kept:
        s = stems(k)
        if not s:
            continue
        for c in cl:
            if c["t"] != t:
                continue
            j = len(s & c["s"]) / len(s | c["s"])
            if s == c["s"] or j >= 0.6 or (len(c["s"]) >= 2 and (s <= c["s"] or c["s"] <= s) and j >= 0.5):
                c["m"].append((k, v))
                break
        else:
            cl.append(dict(v=v, d=d, k=k, t=t, kat=kat, s=s, m=[]))
    qrows = list(csv.DictReader((ROOT / "daten/artikel-queue.csv").open(encoding="utf-8")))
    queue = [stems(r["keyword"]) for r in qrows]
    for r in qrows:   # Nebenkeywords schon geschriebener Artikel (Briefe) gelten als abgedeckt
        bj = ROOT / "daten" / "briefs" / f"{r['slug']}.json"
        if r["status"] != "offen" and bj.exists():
            queue += [stems(v["keyword"]) for v in json.loads(bj.read_text(encoding="utf-8")).get("vorschlaege", [])]
    out = []
    for c in cl:
        if any(c["s"] and x and len(c["s"] & x) / len(c["s"] | x) >= 0.6 for x in queue):
            continue
        it = w.intent(c["k"])
        score = c["v"] / (1 + c["d"] / 10) * GEWICHT.get(c["t"], 0.5) * INTENT_GEWICHT.get(it, 1.0)
        if c["v"] >= 200 and c["d"] > 40:
            welle = 0
        elif c["v"] >= 200:
            welle = 2
        elif c["v"] >= 100:
            welle = 3
        else:
            welle = 9
        out.append(dict(c=c, intent=it, score=round(score, 1), welle=welle))
    a = sorted([o for o in out if o["welle"] == 2], key=lambda o: -o["score"])
    for o in a[:100]:
        o["welle"] = 1
    order = {t: i for i, t in enumerate(PRODUKT_REIHENFOLGE)}
    out.sort(key=lambda o: (o["welle"], order.get(o["c"]["t"], 99), -o["score"]))
    batch, n_in_batch, last = 0, 0, None
    for o in out:
        key = (o["welle"], o["c"]["t"])
        if o["welle"] == 9:
            o["batch"] = ""
            continue
        if key != last or n_in_batch >= 10:
            batch += 1
            n_in_batch = 0
            last = key
        n_in_batch += 1
        o["batch"] = batch
    if "--dry-run" in sys.argv:
        import collections
        print(collections.Counter(o["welle"] for o in out))
        return
    with (ROOT / "daten/themenplan.csv").open("w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["welle", "batch", "produkt", "kategorie", "hauptkeyword", "volumen", "schwierigkeit", "intent", "score", "nebenkeywords (Volumen)", "status"])
        for o in out:
            c = o["c"]
            neben = " · ".join(f"{k} ({v})" for k, v in sorted(c["m"], key=lambda x: -x[1])[:6])
            wr.writerow([o["welle"], o["batch"], c["t"], c["kat"], c["k"], c["v"], int(c["d"]), o["intent"], o["score"], neben, "offen"])
    print(f"{len(out)} Themen -> daten/themenplan.csv")


if __name__ == "__main__":
    main()
