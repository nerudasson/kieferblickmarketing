#!/usr/bin/env python3
"""Artikel-Warteschlange: next | set | check. CSV: daten/artikel-queue.csv"""
import argparse, csv, sys
from pathlib import Path

Q = Path("daten/artikel-queue.csv")
FIELDS = ["slug", "keyword", "cluster", "intent", "volumen", "schwierigkeit", "prioritaet", "status", "notiz"]
STATI = {"offen", "entwurf", "geprueft", "blockiert", "wp_entwurf"}


def load():
    if not Q.exists():
        sys.exit("daten/artikel-queue.csv fehlt: erst keyword-research ausfuehren.")
    with Q.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def save(rows):
    with Q.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def stem(word):
    return word.lower()[:5]


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("next"); n.add_argument("--n", type=int, default=5)
    s = sub.add_parser("set"); s.add_argument("slug"); s.add_argument("status")
    sub.add_parser("check")
    a = ap.parse_args()
    rows = load()
    if a.cmd == "next":
        offen = [r for r in rows if r["status"] == "offen"]
        offen.sort(key=lambda r: float(r.get("prioritaet") or 0), reverse=True)
        for r in offen[: a.n]:
            print(f'{r["slug"]}\t{r["keyword"]}\t{r["cluster"]}\t{r["intent"]}')
    elif a.cmd == "set":
        if a.status not in STATI:
            sys.exit(f"status muss einer von {sorted(STATI)} sein")
        hit = [r for r in rows if r["slug"] == a.slug]
        if not hit:
            sys.exit("slug nicht gefunden")
        hit[0]["status"] = a.status
        save(rows)
    elif a.cmd == "check":
        seen = {}
        for r in rows:
            key = (r["cluster"], frozenset(stem(w) for w in r["keyword"].split() if len(w) > 3))
            seen.setdefault(key[0], []).append((r["keyword"], key[1]))
        found = False
        for cl, items in seen.items():
            for i, (k1, s1) in enumerate(items):
                for k2, s2 in items[i + 1:]:
                    if s1 and s2 and (s1 <= s2 or s2 <= s1):
                        print(f"[{cl}] Ueberschneidung: '{k1}' <-> '{k2}'"); found = True
        if not found:
            print("keine Ueberschneidungen")


if __name__ == "__main__":
    main()
