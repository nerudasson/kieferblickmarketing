#!/usr/bin/env python3
"""Reel-Agent: feste Abläufe (nur Standardbibliothek).

  reels.py status                   Stand der Dateien
  reels.py winners [--min 3]        Gewinner je Account (Faktor über Median) aus daten/reels/raw/*.csv
  reels.py check <weekly.md>        Vorprüfung der Wochenliste (Hooks, Skripte, Filter-Muster)
  reels.py own                      Auswertung der eigenen Reels nach Hook-Typ, Format, Trigger

Der Skript-Check ersetzt die Prüfung durch den reel-reviewer nicht, er spart ihm die Mustersuche.
"""
import csv
import json
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DATA = ROOT / "daten" / "reels"
REFS = Path(__file__).resolve().parents[1] / "references"
MIN_FAKTOR = 3.0
BOOST_QUOTE = 0.005  # Likes/Views darunter: wahrscheinlich beworben (Annahme)
MIN_SCAN_FUER_MEDIAN = 30


def parse_views(s):
    s = str(s).strip().lower().replace("\xa0", " ")
    if not s:
        return None
    m = re.match(r"^([\d.,]+)\s*(mio|m|tsd|k)?\.?$", s)
    if not m:
        return None
    num, unit = m.groups()
    if unit in ("mio", "m", "tsd", "k"):
        v = float(num.replace(",", "."))
        return int(v * {"mio": 1e6, "m": 1e6, "tsd": 1e3, "k": 1e3}[unit])
    return int(re.sub(r"[.,]", "", num))


def de(n):
    return f"{int(n):,}".replace(",", ".")


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def benchmarks():
    return {r["handle"]: r for r in read_csv(DATA / "library" / "benchmarks.csv")}


def latest_raw_per_account():
    """Je Account die Zeilen aus der Datei mit dem jüngsten Datum im Namen."""
    best = {}
    for p in sorted((DATA / "raw").glob("*.csv")):
        rows = read_csv(p)
        for acc in {r["account"] for r in rows}:
            best[acc] = (p.name, [r for r in rows if r["account"] == acc])
    return best


def cmd_winners(min_faktor):
    bm = benchmarks()
    print("| Account | Code | Views | Faktor | Likes/Views | Hinweis | Thema |")
    print("|---|---|---|---|---|---|---|")
    keine = []
    for acc, (fname, rows) in sorted(latest_raw_per_account().items()):
        vals = [parse_views(r["views"]) for r in rows]
        vals = [v for v in vals if v]
        if len(vals) >= MIN_SCAN_FUER_MEDIAN:
            median = statistics.median(vals)
        else:
            median = float(bm.get(acc, {}).get("median_views") or 0)
        if not median:
            keine.append(acc)
            continue
        treffer = []
        for r in rows:
            v = parse_views(r["views"])
            if not v:
                continue
            f = v / median
            if f < min_faktor:
                continue
            likes = parse_views(r.get("likes", ""))
            hint = r.get("hinweis", "")
            boosted = (likes is not None and likes / v < BOOST_QUOTE) or bool(
                re.search(r"bezahlt|beworben|paid", hint, re.I))
            quote = f"{likes / v:.1%}" if likes else "n/a"
            if boosted and not re.search(r"beworben|bezahlt|paid", hint, re.I):
                hint = ("wahrscheinlich beworben; " + hint).strip("; ")
            treffer.append((f, r, v, quote, hint))
        for f, r, v, quote, hint in sorted(treffer, key=lambda t: -t[0]):
            print(f"| {acc} | {r['code']} | {de(v)} | {f:.1f}x | {quote} | {hint} | {r.get('thema', '')} |")
        if not treffer:
            print(f"| {acc} | – | – | kein Reel ≥ {min_faktor}x (Median {de(median)}) | | | |")
    if keine:
        print(f"\nOhne Median (Lücke, Scout-Lauf fehlt): {', '.join(keine)}")
    print(f"\nMedian: aus der Rohdatei, wenn ≥ {MIN_SCAN_FUER_MEDIAN} Reels vorliegen, sonst aus library/benchmarks.csv. "
          f"„Wahrscheinlich beworben“ ist eine Annahme (Likes/Views < {BOOST_QUOTE:.1%} oder Hinweis).")


# --- Check der Wochenliste -------------------------------------------------

def load_filter():
    return json.loads((REFS / "filter.json").read_text(encoding="utf-8"))


def words(text):
    return re.findall(r"[A-Za-z0-9’'$€%.,-]+", re.sub(r"\[[^\]]*\]", "", text))


def cmd_check(path):
    flt = load_filter()
    text = Path(path).read_text(encoding="utf-8")
    hard, soft = [], []

    # Hook-Tabelle: | Nr | Hook | Trigger | Vorbild | Filter |
    hooks = []
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 5 and cells[0].isdigit():
            hooks.append(cells)
    if len(hooks) != 10:
        hard.append(f"Hook-Tabelle: {len(hooks)} Zeilen statt 10")
    for nr, hook, trigger, vorbild, status in [h[:5] for h in hooks]:
        n = len(words(hook))
        if n > flt["max_hook_woerter"]:
            hard.append(f"Hook {nr}: {n} Wörter (max {flt['max_hook_woerter']})")
        if trigger.lower() not in flt["trigger"]:
            hard.append(f"Hook {nr}: Trigger „{trigger}“ nicht in {flt['trigger']}")
        if not vorbild:
            hard.append(f"Hook {nr}: Vorbild fehlt")
        if not status or not re.search(r"✅|⚠️|❌", status):
            hard.append(f"Hook {nr}: Filter-Status fehlt")
        if "!" in hook:
            hard.append(f"Hook {nr}: Ausrufezeichen")
        low = hook.lower()
        for w in flt["verboten"]:
            if re.search(rf"\b{re.escape(w)}", low):
                hard.append(f"Hook {nr}: verbotenes Wort/Muster „{w}“")
        for w in flt["kollegen_angriff"]:
            if re.search(rf"\b{re.escape(w)}", low):
                hard.append(f"Hook {nr}: möglicher Angriff auf Kollegen („{w}“)")
        for w in flt["legal_review"]:
            if re.search(rf"\b{re.escape(w)}", low) and "⚠️" not in status:
                hard.append(f"Hook {nr}: nennt „{w}“, braucht ⚠️ legal review")

    # Skripte: Abschnitte ab „### Skript“
    parts = re.split(r"(?m)^### Skript", text)[1:]
    if len(parts) != 3:
        hard.append(f"Skripte: {len(parts)} statt 3")
    stichworte = flt["stichworte"]
    for i, part in enumerate(parts, 1):
        for marker in flt["skript_marker"]:
            if marker not in part:
                hard.append(f"Skript {i}: Abschnitt „{marker}“ fehlt")
        m = re.search(r"Comment\s+([A-Z]{3,12})", part)
        if not m:
            hard.append(f"Skript {i}: Kommentar-Stichwort fehlt")
        elif m.group(1) not in stichworte:
            hard.append(f"Skript {i}: Stichwort {m.group(1)} nicht in {list(stichworte)}")
        low = part.lower()
        for w in flt["verboten"]:
            if re.search(rf"\b{re.escape(w)}", low):
                hard.append(f"Skript {i}: verbotenes Wort/Muster „{w}“")
        if re.search(r"\d[\d.,]*\s?(€|\$|£|eur|usd)", low) or re.search(r"[€$£]\s?\d", low):
            soft.append(f"Skript {i}: nennt einen Preis (Preise stehen nicht in Reels)")
        if "!" in part.split("Caption")[-1]:
            soft.append(f"Skript {i}: Ausrufezeichen in der Caption")
        if not ("[CHECK]" in part or "[ ]" in part):
            soft.append(f"Skript {i}: weder [CHECK] noch [ ] gesetzt (prüfen, ob nichts zu prüfen ist)")
    n_check = text.count("[CHECK]")
    n_gap = len(re.findall(r"\[ \]", text))
    print(f"{path}: Hooks {len(hooks)}, Skripte {len(parts)}, [CHECK] {n_check}, [ ] {n_gap}")
    for h in hard:
        print("FEHLER:", h)
    for s in soft:
        print("HINWEIS:", s)
    if not hard and not soft:
        print("Keine Treffer.")
    sys.exit(1 if hard else 0)


# --- Lernschleife ------------------------------------------------------------

def cmd_own():
    rows = read_csv(DATA / "library" / "own_performance.csv")
    rows = [r for r in rows if parse_views(r.get("views", ""))]
    print(f"Eigene Reels mit Zahlen: {len(rows)}")
    if len(rows) < 6:
        print("Lücke: unter 6 Reels ist keine Aussage belastbar. Weiter nach den Benchmarks gewichten.")
    for key in ("hook_type", "format", "trigger"):
        groups = defaultdict(list)
        for r in rows:
            groups[r.get(key) or "?"].append(parse_views(r["views"]))
        print(f"\n| {key} | Reels | Median Views |\n|---|---|---|")
        for k, v in sorted(groups.items(), key=lambda kv: -statistics.median(kv[1])):
            flag = "" if len(v) >= 3 else " (< 3 Reels, nur Hinweis)"
            print(f"| {k} | {len(v)} | {int(statistics.median(v))}{flag} |")
    if rows:
        print(f"\nMedian aller eigenen Reels: {int(statistics.median(parse_views(r['views']) for r in rows))}")


def cmd_status():
    for sub in ("raw", "frames", "library", "output"):
        files = [p.name for p in (DATA / sub).glob("*") if p.name != ".gitkeep"]
        print(f"{sub}: {len(files)} Dateien" + (f" (zuletzt {sorted(files)[-1]})" if files else ""))
    hooks = read_csv(DATA / "library" / "hooks.csv")
    print(f"hooks.csv: {len(hooks)} Einträge; own_performance.csv: {len(read_csv(DATA / 'library' / 'own_performance.csv'))} Reels")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "status":
        cmd_status()
    elif a[0] == "winners":
        cmd_winners(float(a[a.index("--min") + 1]) if "--min" in a else MIN_FAKTOR)
    elif a[0] == "check" and len(a) > 1:
        cmd_check(a[1])
    elif a[0] == "own":
        cmd_own()
    else:
        print(__doc__)
        sys.exit(2)
