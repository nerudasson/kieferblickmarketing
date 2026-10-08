#!/usr/bin/env python3
"""Keywords-CSV -> daten/artikel-queue.csv (clustert nach Wortmuster, behaelt vorhandene Status)."""
import csv, re, sys
from pathlib import Path

Q = Path("daten/artikel-queue.csv")
FIELDS = ["slug", "keyword", "cluster", "intent", "volumen", "schwierigkeit", "prioritaet", "status", "notiz"]
INTENT = [("kosten", r"kosten|preis|teuer|ratenzahlung"), ("erfahrung", r"erfahrung|test|bewertung"),
          ("anbieter", r"zahnarzt|praxis|n[aä]he|in [a-zäöü]+$"), ("rueckfall", r"retainer|verschieb|wandern"),
          ("ausloeser", r"richten|begradig|schief|l[uü]cke|engstand")]
MARKEN = re.compile(r"invisalign|drsmile|dr\.? smile")


def slugify(k):
    s = k.lower().translate(str.maketrans("äöüß", "aous"))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def intent(k):
    for name, pat in INTENT:
        if re.search(pat, k):
            return name
    return "info"


def main(src):
    old = {}
    if Q.exists():
        with Q.open(encoding="utf-8", newline="") as f:
            old = {r["slug"]: r for r in csv.DictReader(f)}
    with open(src, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            k = (r["keyword"] or "").strip().lower()
            slug = slugify(k)
            if not slug or slug in old:
                continue
            vol = int(float(r.get("volumen") or 0))
            diff = r.get("schwierigkeit") or ""
            prio = vol / (1 + float(diff or 30) / 10)
            old[slug] = {"slug": slug, "keyword": k, "cluster": intent(k), "intent": intent(k),
                         "volumen": vol, "schwierigkeit": diff, "prioritaet": round(prio, 1),
                         "status": "offen", "notiz": "marke" if MARKEN.search(k) else ""}
    Q.parent.mkdir(exist_ok=True)
    with Q.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader(); w.writerows(old.values())
    print(f"{len(old)} Zeilen in {Q}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Aufruf: build_queue.py <keywords.csv>")
    main(sys.argv[1])
