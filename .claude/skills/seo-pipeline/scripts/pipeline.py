#!/usr/bin/env python3
"""Orchestrierung der Artikel-Pipeline (deterministische Stufen); die Agent-Aufgaben werden als Arbeitsliste ausgegeben.

  python3 pipeline.py status
  python3 pipeline.py prepare [--n 5] [--slug <slug>] [--no-brief] [--dry-run]   führt die nächste Stufe aus (Brief, Skelett) und gibt die Agent-Arbeitsliste: Planer -> Researcher -> Writer
  python3 pipeline.py gates [slug ...]                           beide Prüfskripte über Entwürfe (Standard: alle mit Status skelett/entwurf)
  python3 pipeline.py check <slug>                               lesbarkeit.py + belege_check.py in einem Aufruf (kompakt)
  python3 pipeline.py fragen                                     offene [FAKT FEHLT] je Thema, gebündelt für Alexander
  python3 pipeline.py review [slug ...]                          welche Entwürfe der compliance-reviewer prüfen muss (Stichprobenregel)
  python3 pipeline.py logreview <slug> <rot|gelb|gruen> <n>      Ergebnis eintragen (n = Zahl inhaltlicher Befunde, ohne Platzhalter)
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

REVIEWLOG = ROOT / "daten" / "review-log.csv"
VOLL_BIS = 3          # die ersten N Artikel je Thema immer prüfen
STICHPROBE = 5        # danach jeder fünfte
FENSTER = 10          # Rückfallregel: letzte N Prüfungen
MAX_INHALT = 3        # >= so viele inhaltliche Befunde im Schnitt der letzten 5 -> wieder alles prüfen


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


def status_zeile(r):
    try:
        return stufe(r)
    except Exception:
        return "?"


def status(_):
    rows = laden()
    print(f"Queue: {len(rows)} Zeilen")
    stat = {}
    for r in rows:
        stat[r["status"]] = stat.get(r["status"], 0) + 1
    print("  " + ", ".join(f"{k}: {v}" for k, v in sorted(stat.items())))
    themen = sorted({r["thema"] for r in rows if r["thema"]})
    print("Nächste Stufe je Artikel:")
    for r in rows:
        if r["status"] in ("offen", "skelett", "entwurf"):
            print(f"  {r['slug']:28} {r['status']:9} -> {status_zeile(r)}")
    print("Themen:")
    for t in themen:
        tage, s = belege_stand(t)
        n = sum(1 for r in rows if r["thema"] == t)
        print(f"  {t:12} {n} Artikel · Belege: {s}" + (f" ({tage} Tage alt)" if tage is not None else ""))


def abgedeckt(thema):
    p = ROOT / "daten" / "belege" / f"{thema}.md"
    if not p.exists():
        return set()
    m = re.search(r"^abgedeckt:\s*(.+)$", p.read_text(encoding="utf-8"), flags=re.M)
    return {x.strip() for x in m.group(1).split(",")} if m else set()


def stufe(r):
    """Nächste Aufgabe für eine Queue-Zeile."""
    slug = r["slug"]
    if not (ROOT / "daten" / "briefs" / f"{slug}.md").exists():
        return "brief"
    if not (ROOT / "daten" / "plaene" / f"{slug}.md").exists():
        return "plan"
    ok = lauf(HERE / "skelett.py", "plan-check", slug)
    if ok.returncode != 0:
        return "plan-fix"
    _, s = belege_stand(r["thema"])
    if s != "ok" or slug not in abgedeckt(r["thema"]):
        return "belege"
    d = ROOT / "daten" / "entwuerfe" / f"{slug}.md"
    if not d.exists():
        return "skelett"
    return "schreiben" if "<!-- SCHREIBEN" in d.read_text(encoding="utf-8") else "fertig"


def prepare(a):
    rows = laden()
    offen = sorted((r for r in rows if r["status"] in ("offen", "skelett") and (not a.slug or r["slug"] in a.slug)), key=lambda r: float(r.get("prioritaet") or 0), reverse=True)[: a.n]
    if not offen:
        print("Keine offenen Zeilen."); return
    liste = {"plan": [], "plan-fix": [], "belege": {}, "schreiben": [], "fertig": []}
    for r in offen:
        if not (r["kategorie"] and r["thema"]):
            print(f"! {r['slug']}: Kategorie/Thema fehlt in der Queue (themen.json ergänzen)"); continue
        st = stufe(r)
        if st == "brief":
            if a.no_brief:
                print(f"{r['slug']}: Brief fehlt (--no-brief)"); continue
            res = lauf(HERE / "seo_brief.py", r["keyword"], "--slug", r["slug"], *(["--dry-run"] if a.dry_run else []))
            print((res.stdout or res.stderr).strip())
            if a.dry_run:
                continue
            st = stufe(r)
        if st == "skelett" and not a.dry_run:
            res = lauf(HERE / "skelett.py", r["slug"], "--kategorie", r["kategorie"], "--thema", r["thema"], "--cluster", r["cluster"], "--intent", r["intent"] or "info", "--praxis", r["praxis"] or "optional")
            print((res.stdout or res.stderr).strip())
            if res.returncode == 0:
                r["status"] = "skelett"; st = "schreiben"
        if st in ("plan", "plan-fix", "schreiben", "fertig"):
            liste[st].append(r["slug"])
        elif st == "belege":
            liste["belege"].setdefault(r["thema"], []).append(r["slug"])
        elif st == "skelett":
            print(f"DRY-RUN Skelett: {r['slug']}")
    if not a.dry_run:
        speichern(rows)
    print("\nARBEITSLISTE (Reihenfolge einhalten)")
    if liste["plan"] or liste["plan-fix"]:
        print(f"  1. article-planner: {', '.join(liste['plan'] + liste['plan-fix'])}  (parallel, je Artikel)")
    for t, sl in liste["belege"].items():
        print(f"  2. evidence-researcher: Thema '{t}' für {', '.join(sl)}  (nach den Plänen, vorhandene Belege werden wiederverwendet)")
    if liste["schreiben"]:
        print(f"  3. article-writer: {', '.join(liste['schreiben'])}  (parallel, je Artikel)")
    if liste["fertig"]:
        print(f"  4. fertig geschrieben: {', '.join(liste['fertig'])} -> pipeline.py gates · review · wp_publish.py")
    print("  Danach erneut: pipeline.py prepare (legt Skelette an, sobald Plan und Belege da sind)")


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


def check(a):
    """Beide Prüfskripte in einem Aufruf, kompakte Ausgabe (spart Runden im Agent)."""
    pfad = ROOT / "daten" / "entwuerfe" / f"{a.slug}.md"
    l = lauf(HERE / "lesbarkeit.py", pfad)
    b = lauf(HERE / "belege_check.py", "check", pfad, "--abgleich")
    ok = l.returncode == 0 and b.returncode == 0
    print(f"{a.slug}: {'ALLES OK' if ok else 'PRÜFEN'}")
    for ausgabe in (l.stdout, b.stdout):
        for x in ausgabe.split("\n"):
            if x.strip() and not x.startswith(str(pfad)) and not x.strip().startswith("Bausteine"):
                print(x)
    sys.exit(0 if ok else 1)


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


def reviewlog():
    if not REVIEWLOG.exists():
        return []
    return list(csv.DictReader(REVIEWLOG.open(encoding="utf-8", newline="")))


def review(a):
    rows = laden()
    log = reviewlog()
    letzte = log[-FENSTER:]
    rot = any(r["ampel"] == "rot" for r in letzte)
    schnitt = (sum(int(r["inhaltlich"]) for r in log[-5:]) / max(1, len(log[-5:]))) if log else 99
    voll_modus = rot or schnitt >= MAX_INHALT
    slugs = a.slugs or [r["slug"] for r in rows if r["status"] == "entwurf"]
    geprueft_je_thema = {}
    for r in log:
        geprueft_je_thema[r["thema"]] = geprueft_je_thema.get(r["thema"], 0) + 1
    print(f"Modus: {'VOLLE PRÜFUNG' if voll_modus else 'Stichprobe'} (rot in den letzten {FENSTER}: {'ja' if rot else 'nein'}, Ø inhaltliche Befunde der letzten 5: {schnitt:.1f}, Grenze {MAX_INHALT})")
    bytes_ = {r["slug"]: r for r in rows}
    muss = []
    for s in slugs:
        r = bytes_.get(s)
        pfad = ROOT / "daten" / "entwuerfe" / f"{s}.md"
        if not r or not pfad.exists():
            continue
        t = pfad.read_text(encoding="utf-8")
        gruende = []
        n = geprueft_je_thema.get(r["thema"], 0)
        if voll_modus: gruende.append("Rückfallregel (zuletzt rot oder viele inhaltliche Befunde)")
        if n < VOLL_BIS: gruende.append(f"erst {n} geprüfte Artikel im Thema {r['thema']}")
        if (r["intent"] or "") in ("kosten", "vergleich"): gruende.append("Kosten/Vergleich")
        if re.search(r"^> Praxis:", t, flags=re.M) and "FAKT FEHLT" not in t: gruende.append("Praxis-Block mit Alexanders Aussagen")
        if re.search(r"Krankenkasse|Kasse|§|SGB", t): gruende.append("Kasse/Recht")
        if (len(re.findall(r"\[\d+\]", t)) > 18): gruende.append("viele Zitate")
        if not gruende and (len([x for x in log if x["thema"] == r["thema"]]) + 1) % STICHPROBE == 0:
            gruende.append(f"Stichprobe (jeder {STICHPROBE}.)")
        print(f"{s}: {'PRÜFEN – ' + '; '.join(gruende) if gruende else 'ohne Review (nur Skript-Gates)'}")
        if gruende: muss.append(s)
    print(f"\n{len(muss)} von {len(slugs)} brauchen den Reviewer. Mehrere in EINEM Aufruf prüfen lassen (Regeln werden einmal gelesen).")


def logreview(a):
    rows = {r["slug"]: r for r in laden()}
    r = rows.get(a.slug)
    neu = not REVIEWLOG.exists()
    with REVIEWLOG.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if neu: w.writerow(["datum", "slug", "thema", "ampel", "inhaltlich"])
        w.writerow([date.today().isoformat(), a.slug, r["thema"] if r else "", a.ampel, a.n])
    print("eingetragen")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    p = sub.add_parser("prepare"); p.add_argument("--n", type=int, default=5); p.add_argument("--slug", action="append"); p.add_argument("--no-brief", action="store_true"); p.add_argument("--dry-run", action="store_true")
    g = sub.add_parser("gates"); g.add_argument("slugs", nargs="*")
    sub.add_parser("fragen")
    ck = sub.add_parser("check"); ck.add_argument("slug")
    rv = sub.add_parser("review"); rv.add_argument("slugs", nargs="*")
    lg = sub.add_parser("logreview"); lg.add_argument("slug"); lg.add_argument("ampel", choices=["rot", "gelb", "gruen"]); lg.add_argument("n", type=int)
    a = ap.parse_args()
    {"status": status, "prepare": prepare, "gates": gates, "fragen": fragen, "check": check, "review": review, "logreview": logreview}[a.cmd](a)
