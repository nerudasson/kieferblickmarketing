#!/usr/bin/env python3
"""Keyword-Auswahl: waehlt aus der Keyword-Auswertung (Excel) die naechsten Artikelthemen und schreibt sie in die Queue.

  python3 waehle_keywords.py --xlsx daten/Kieferblick_Keyword-Auswertung_v1.xlsx --top 10 [--thema retainer] [--min-vol 100] [--dry-run] [--mit-marken]

Regeln: nur Keywords, die zu einem Thema in seo-pipeline/references/themen.json passen; Fremdsprachiges, Holz/Möbel,
Auslandspreise und Markenbegriffe (ohne --mit-marken) fallen raus; ähnliche Keywords (gleicher Wortstamm-Satz) werden
zu EINEM Artikel zusammengelegt, das volumenstärkste ist der Artikel, die anderen werden im SEO-Brief Nebenkeywords.
Bereits in der Queue vorhandene Themen werden übersprungen. Die Volumen hier sind Excel-Werte (Juni/August 2025);
der SEO-Brief holt später frische DataForSEO-Zahlen und ersetzt sie.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
Q = ROOT / "daten" / "artikel-queue.csv"
FIELDS = ["slug", "keyword", "cluster", "intent", "volumen", "schwierigkeit", "prioritaet", "status", "notiz", "kategorie", "thema", "praxis"]
AUS = re.compile(r"wood|oak|holz|plywood|mdf|furnier|möbel|moebel|sheet|indien|india|mumbai|türkei|tuerkei|ungarn|polen|schweiz|österreich|oesterreich|wien|zürich|thailand|\bmm\b|\d+/\d+|kosmetik|haar|nagel|3m |\bcheap\b|\bcost\b|\bbest\b|\bnear\b|\bdental\b", re.I)
MARKEN = re.compile(r"invisalign|dr\.? ?smile|drsmile|angel ?aligner|clearcorrect|spark|plusdental|zenyum|smile club|impress", re.I)
INTENT = [("kosten", r"kosten|preis|teuer|ratenzahlung|krankenkasse"), ("erfahrung", r"erfahrung|test|bewertung"),
          ("anbieter", r"zahnarzt|praxis|n[aä]he|in [a-zäöü]+$"), ("rueckfall", r"retainer|verschieb|wandern"),
          ("ausloeser", r"richten|begradig|schief|l[uü]cke|engstand")]


def slugify(k):
    s = k.lower().translate(str.maketrans("äöüß", "aous"))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def stamm(k):
    return frozenset(w[:5] for w in re.findall(r"[a-zäöüß]+", k.lower()) if len(w) > 3)


def intent(k):
    for name, pat in INTENT:
        if re.search(pat, k):
            return name
    return "info"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xlsx", default=str(ROOT / "daten" / "Kieferblick_Keyword-Auswertung_v1.xlsx"))
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--thema")
    ap.add_argument("--min-vol", type=int, default=50)
    ap.add_argument("--mit-marken", action="store_true")
    ap.add_argument("--max-pro-thema", type=int, default=3, help="höchstens N neue Artikel je Thema (Cluster), damit nicht drei Varianten desselben Themas parallel entstehen")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    import openpyxl
    cfg = json.loads((ROOT / ".claude" / "skills" / "seo-pipeline" / "references" / "themen.json").read_text(encoding="utf-8"))["regeln"]
    vorhanden = []
    if Q.exists():
        vorhanden = list(csv.DictReader(Q.open(encoding="utf-8", newline="")))
    belegt = [stamm(r["keyword"]) for r in vorhanden]
    ws = openpyxl.load_workbook(a.xlsx, read_only=True, data_only=True)["Keywords_Funnel"]
    rows = list(ws.iter_rows(values_only=True))[1:]
    kandidaten = {}
    for r in rows:
        k, vol, diff = (r[1] or "").strip().lower(), int(r[2] or 0), r[3]
        if not k or vol < a.min_vol or AUS.search(k):
            continue
        if MARKEN.search(k) and not a.mit_marken:
            continue
        regel = next((x for x in cfg if re.search(x["muster"], k)), None)
        if not regel or (a.thema and regel["thema"] != a.thema):
            continue
        st = stamm(k)
        if not st or any(st <= b or b <= st for b in belegt):
            continue
        # gleiche Absicht: Wortstamm-Teilmenge -> zusammenlegen (volumenstärkstes behalten)
        for alt in list(kandidaten):
            if st <= alt or alt <= st:
                if vol > kandidaten[alt]["volumen"]:
                    del kandidaten[alt]
                    break
                else:
                    st = None
                    break
        if st is None:
            continue
        try:
            d = float(diff) if diff not in (None, "") else 30.0
        except (TypeError, ValueError):
            d = 30.0
        kandidaten[st] = dict(keyword=k, volumen=vol, schwierigkeit=d, regel=regel)
    sortiert = sorted(kandidaten.values(), key=lambda c: c["volumen"] / (1 + c["schwierigkeit"] / 10), reverse=True)
    auswahl, je_thema = [], {}
    for c in sortiert:
        t = c["regel"]["thema"]
        if je_thema.get(t, 0) >= a.max_pro_thema:
            continue
        je_thema[t] = je_thema.get(t, 0) + 1
        auswahl.append(c)
        if len(auswahl) >= a.top:
            break
    neu = []
    for c in auswahl:
        k = c["keyword"]
        neu.append(dict(slug=slugify(k), keyword=k, cluster=c["regel"]["cluster"], intent=intent(k), volumen=c["volumen"],
                        schwierigkeit=int(c["schwierigkeit"]), prioritaet=round(c["volumen"] / (1 + c["schwierigkeit"] / 10), 1),
                        status="offen", notiz="marke" if MARKEN.search(k) else "", kategorie=c["regel"]["kategorie"],
                        thema=c["regel"]["thema"], praxis=c["regel"]["praxis"]))
    print(f"{len(neu)} neue Artikelthemen aus {len(kandidaten)} Kandidaten:")
    for n in neu:
        print(f"  {n['volumen']:>6}  {n['keyword']:<40} {n['kategorie']}/{n['thema']} · {n['intent']}")
    if a.dry_run or not neu:
        return
    gesamt = vorhanden + neu
    with Q.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader(); w.writerows(gesamt)
    print(f"-> {Q} ({len(gesamt)} Zeilen)")


if __name__ == "__main__":
    main()
