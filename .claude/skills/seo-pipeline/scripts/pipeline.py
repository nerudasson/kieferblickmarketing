#!/usr/bin/env python3
"""Orchestrierung der Artikel-Pipeline (deterministische Stufen); die Agent-Aufgaben werden als Arbeitsliste ausgegeben.

  python3 pipeline.py status
  python3 pipeline.py prepare [--n 5] [--no-brief] [--dry-run]   Briefs + Skelette für die nächsten offenen Zeilen
  python3 pipeline.py gates [slug ...]                           beide Prüfskripte über Entwürfe (Standard: alle mit Status skelett/entwurf)
  python3 pipeline.py fragen                                     offene [FAKT FEHLT] je Thema, gebündelt für Alexander
"""
import argparse
import csv
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
Q = ROOT / "daten" / "artikel-queue.csv"
FIELDS = ["slug", "keyword", "cluster", "intent", "volumen", "schwierigkeit", "prioritaet", "status", "notiz", "kategorie", "thema", "praxis"]


def laden():
    if not Q.exists():
        sys.exit("daten/artikel-queue.csv fehlt: erst keyword-research ausführen.")
    return list(csv.DictReader(Q.open(encoding="utf-8", newline="")))


def speichern(rows):
    w = csv.DictWriter(Q.open("w", encoding="utf-8", newline=""), fieldnames=FIELDS, extrasaction="ignore")
    w.writeheader(); w.writerows(rows)


def lauf(*args):
    return subprocess.run([sys.executable, *map(str, args)], cwd=ROOT, capture_output=True, text=True)


def belege_stand(thema):
    p = ROOT / "daten" / "belege" / f"{thema}.md"
    if not p.exists():
        return None, "fehlt"
    m = re.search(r"^stand:\s*(\S+)", p.read_text(encoding="utf-8"), flags=re.M)
    if not m:
        return None, "ohne Stand"
    tage = (date.today() - datetime.strptime(m.group(1), "%Y-%m-%d").date()).days
    return tage, ("veraltet" if tage > 365 else "ok")


def status(_):
    rows = laden()
    print(f"Queue: {len(rows)} Zeilen")
    stat = {}
    for r in rows:
        stat[r["status"]] = stat.get(r["status"], 0) + 1
    print("  " + ", ".join(f"{k}: {v}" for k, v in sorted(stat.items())))
    themen = sorted({r["thema"] for r in rows if r["thema"]})
    print("Themen:")
    for t in themen:
        tage, s = belege_stand(t)
        n = sum(1 for r in rows if r["thema"] == t)
        print(f"  {t:12} {n} Artikel · Belege: {s}" + (f" ({tage} Tage alt)" if tage is not None else ""))


def prepare(a):
    rows = laden()
    offen = sorted((r for r in rows if r["status"] == "offen"), key=lambda r: float(r.get("prioritaet") or 0), reverse=True)[: a.n]
    if not offen:
        print("Keine offenen Zeilen."); return
    arbeit_forscher, arbeit_writer = set(), []
    for r in offen:
        if not (r["kategorie"] and r["thema"]):
            print(f"! {r['slug']}: Kategorie/Thema fehlt in der Queue (themen.json ergänzen)"); continue
        brief = ROOT / "daten" / "briefs" / f"{r['slug']}.md"
        if not brief.exists() and not a.no_brief:
            cmd = [HERE / "seo_brief.py", r["keyword"], "--slug", r["slug"]] + (["--dry-run"] if a.dry_run else [])
            res = lauf(*cmd)
            print(res.stdout.strip() or res.stderr.strip())
        _, s = belege_stand(r["thema"])
        if s != "ok":
            arbeit_forscher.add(r["thema"])
        if a.dry_run:
            print(f"DRY-RUN Skelett: {r['slug']} ({r['kategorie']}/{r['thema']}, Praxis {r['praxis'] or 'optional'})"); continue
        res = lauf(HERE / "skelett.py", r["slug"], "--kategorie", r["kategorie"], "--thema", r["thema"], "--cluster", r["cluster"], "--intent", r["intent"] or "info", "--praxis", r["praxis"] or "optional")
        print((res.stdout or res.stderr).strip())
        if res.returncode == 0:
            r["status"] = "skelett"; arbeit_writer.append(r["slug"])
    if not a.dry_run:
        speichern(rows)
    print("\nARBEITSLISTE")
    for t in sorted(arbeit_forscher):
        print(f"  1. evidence-researcher: Thema '{t}' (Belege {belege_stand(t)[1]}) – vor den Writern")
    for s in arbeit_writer:
        print(f"  2. article-writer: {s}")
    if arbeit_writer:
        print("  3. danach: pipeline.py gates · compliance-reviewer · wp_publish.py")


def gates(a):
    rows = laden()
    slugs = a.slugs or [r["slug"] for r in rows if r["status"] in ("skelett", "entwurf")]
    ok_all = True
    for s in slugs:
        pfad = ROOT / "daten" / "entwuerfe" / f"{s}.md"
        if not pfad.exists():
            print(f"{s}: kein Entwurf"); continue
        t = pfad.read_text(encoding="utf-8")
        if "<!-- SCHREIBEN" in t:
            print(f"{s}: Skelett noch nicht ausgefüllt"); ok_all = False; continue
        l = lauf(HERE / "lesbarkeit.py", pfad)
        b = lauf(HERE / "belege_check.py", "check", pfad)
        wert = re.search(r"Lesbarkeit (\d+)", l.stdout)
        luecken = len(re.findall(r"FAKT FEHLT", t))
        ok = l.returncode == 0 and b.returncode == 0
        ok_all &= ok
        print(f"{s}: Lesbarkeit {wert.group(1) if wert else '?'} · Skript {'OK' if l.returncode == 0 else 'PRÜFEN'} · Belege {'OK' if b.returncode == 0 else 'PRÜFEN'} · Lücken {luecken}")
        if not ok:
            for x in (l.stdout + b.stdout).split("\n"):
                if x.startswith("   -") or x.startswith("  - "):
                    print("    " + x.strip())
    sys.exit(0 if ok_all else 1)


def fragen(_):
    rows = laden()
    bythema = {}
    for r in rows:
        p = ROOT / "daten" / "entwuerfe" / f"{r['slug']}.md"
        if p.exists():
            for m in re.finditer(r"\[FAKT FEHLT:([^\]]*)\]", p.read_text(encoding="utf-8")):
                bythema.setdefault(r["thema"] or "?", []).append((r["slug"], m.group(1).strip()))
    if not bythema:
        print("Keine offenen [FAKT FEHLT]-Stellen."); return
    for t, items in bythema.items():
        print(f"## Thema {t}")
        for s, f in items:
            print(f"- {s}: {f}")
    print("\nAntworten: material/fakten.md, Abschnitt ‚Persönliche Einschätzung‘, je Zeile '- <slug>: …' (1–3 Sätze genügen).")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    p = sub.add_parser("prepare"); p.add_argument("--n", type=int, default=5); p.add_argument("--no-brief", action="store_true"); p.add_argument("--dry-run", action="store_true")
    g = sub.add_parser("gates"); g.add_argument("slugs", nargs="*")
    sub.add_parser("fragen")
    a = ap.parse_args()
    {"status": status, "prepare": prepare, "gates": gates, "fragen": fragen}[a.cmd](a)
