#!/usr/bin/env python3
"""Orchestrierung der Artikel-Pipeline (deterministische Stufen); die Agent-Aufgaben werden als Arbeitsliste ausgegeben.

  python3 pipeline.py status
  python3 pipeline.py prepare [--n 5] [--slug <slug>] [--no-brief] [--dry-run]   führt die nächste Stufe aus (Brief, Skelett) und gibt die Agent-Arbeitsliste: Planer -> Researcher -> Writer
  python3 pipeline.py live <slug> [slug ...]                     nach der Veröffentlichung: Linkplan auf live setzen (Voraussetzung für Weiterlesen-Links)
  python3 pipeline.py weiterlesen <thema>                        Weiterlesen-Abschnitt der Entwürfe eines Themas mit den live-Geschwistern neu setzen
  python3 pipeline.py gates [slug ...]                           beide Prüfskripte über Entwürfe (Standard: alle mit Status skelett/entwurf)
  python3 pipeline.py check <slug>                               lesbarkeit.py + belege_check.py + hwg_check.py in einem Aufruf (kompakt)
  python3 pipeline.py schlank <slug> [slug ...] [--fakten <datei-thema>]   schlanker Ablauf: Skelett aus dem Brief (ohne Einzelplan) und kompaktes Schreibpaket; Faktenblatt = daten/belege/<thema>-web.md
  python3 pipeline.py paket <slug>                               Schreibpaket daten/pakete/<slug>.md (Plan, Beleg-Aussagen mit Formulierung, Fakten, Preise, Regeln): der Autor liest eine Datei statt sieben
  python3 pipeline.py belegreview-ok <thema>                     nach Korrektur der Beleg-Datei: markiert den Beleg-Review als aktuell (sonst bleibt die Stufe 2b offen)
  python3 pipeline.py patch <slug>                               wendet die PATCHES aus daten/reviews/<slug>.md exakt an (alt -> neu) und führt danach abschluss aus; meldet, was nicht passte
  python3 pipeline.py abschluss <slug>                           Endstand nach Schreiben oder Korrektur: check -> finalize (falls nötig) -> check; danach nichts mehr editieren
  python3 pipeline.py fragen                                     offene [FAKT FEHLT] je Thema, gebündelt für Alexander
  python3 pipeline.py review [slug ...]                          welche Entwürfe der compliance-reviewer prüfen muss (Stichprobenregel), je Artikel ein Reviewer parallel
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


def stempel(slug):
    """Kennung der Belegfragen des Plans: ändert sich der Plan, gelten die Belege als nicht mehr abgedeckt."""
    import hashlib
    sys.path.insert(0, str(HERE))
    import skelett
    pl = skelett.plan_lesen(slug)
    fragen = sorted(a["beleg"].strip() for a in (pl["abschnitte"] if pl else []) if a["beleg"].strip() not in ("–", "-", ""))
    return f"{slug}:{hashlib.md5('|'.join(fragen).encode('utf-8')).hexdigest()[:8]}"


def abgedeckt(thema):
    p = ROOT / "daten" / "belege" / f"{thema}.md"
    if not p.exists():
        return set()
    m = re.search(r"^abgedeckt:\s*(.+)$", p.read_text(encoding="utf-8"), flags=re.M)
    return {x.strip() for x in m.group(1).split(",")} if m else set()


def cluster_datei(thema):
    return ROOT / "daten" / "plaene" / f"_cluster-{thema}.md"


def belegreview_datei(thema):
    return ROOT / "daten" / "reviews" / f"_belege-{thema}.md"


def thema_zeilen(thema):
    return [x for x in laden() if x["thema"] == thema and x["status"] in ("offen", "skelett", "entwurf")]


def stufe(r):
    """Nächste Aufgabe für eine Queue-Zeile."""
    slug = r["slug"]
    if not (ROOT / "daten" / "briefs" / f"{slug}.md").exists():
        return "brief"
    if not (ROOT / "daten" / "plaene" / f"{slug}.md").exists():
        zeilen = thema_zeilen(r["thema"])
        if len(zeilen) >= 2 and not cluster_datei(r["thema"]).exists() and all((ROOT / "daten" / "briefs" / f"{x['slug']}.md").exists() for x in zeilen):
            return "cluster"
        if len(zeilen) >= 2 and not cluster_datei(r["thema"]).exists():
            return "brief"  # Cluster-Plan braucht alle Briefs des Themas
        return "plan"
    ok = lauf(HERE / "skelett.py", "plan-check", slug)
    if ok.returncode != 0:
        return "plan-fix"
    _, s = belege_stand(r["thema"])
    if s != "ok" or stempel(slug) not in abgedeckt(r["thema"]):
        return "belege"
    br, bp = belegreview_datei(r["thema"]), ROOT / "daten" / "belege" / f"{r['thema']}.md"
    if len(thema_zeilen(r["thema"])) >= 3 and (not br.exists() or br.stat().st_mtime < bp.stat().st_mtime):
        return "belegreview"
    d = ROOT / "daten" / "entwuerfe" / f"{slug}.md"
    if not d.exists():
        return "skelett"
    return "schreiben" if "<!-- SCHREIBEN" in d.read_text(encoding="utf-8") else "fertig"


def prepare(a):
    rows = laden()
    offen = sorted((r for r in rows if r["status"] in ("offen", "skelett") and (not a.slug or r["slug"] in a.slug)), key=lambda r: float(r.get("prioritaet") or 0), reverse=True)[: a.n]
    if not offen:
        print("Keine offenen Zeilen."); return
    liste = {"cluster": [], "plan": [], "plan-fix": [], "belege": {}, "belegreview": [], "schreiben": [], "fertig": []}
    for r in offen:  # Briefe zuerst für alle (der Cluster-Plan braucht alle Briefe des Themas)
        if (r["kategorie"] and r["thema"]) and not (ROOT / "daten" / "briefs" / f"{r['slug']}.md").exists():
            if a.no_brief:
                print(f"{r['slug']}: Brief fehlt (--no-brief)"); continue
            res = lauf(HERE / "seo_brief.py", r["keyword"], "--slug", r["slug"], *(["--dry-run"] if a.dry_run else []))
            print((res.stdout or res.stderr).strip())
    for r in offen:
        if not (r["kategorie"] and r["thema"]):
            print(f"! {r['slug']}: Kategorie/Thema fehlt in der Queue (themen.json ergänzen)"); continue
        st = stufe(r)
        if st == "brief":
            continue
        if st == "skelett" and not a.dry_run:
            res = lauf(HERE / "skelett.py", r["slug"], "--kategorie", r["kategorie"], "--thema", r["thema"], "--cluster", r["cluster"], "--intent", r["intent"] or "info", "--praxis", r["praxis"] or "optional")
            print((res.stdout or res.stderr).strip())
            if res.returncode == 0:
                r["status"] = "skelett"; st = "schreiben"
        if st == "cluster":
            if r["thema"] not in liste["cluster"]: liste["cluster"].append(r["thema"])
        elif st == "belegreview":
            if r["thema"] not in liste["belegreview"]: liste["belegreview"].append(r["thema"])
        elif st in ("plan", "plan-fix", "schreiben", "fertig"):
            liste[st].append(r["slug"])
        elif st == "belege":
            liste["belege"].setdefault(r["thema"], []).append(r["slug"])
        elif st == "skelett":
            print(f"DRY-RUN Skelett: {r['slug']}")
    if not a.dry_run:
        speichern(rows)
        geplant_eintragen(rows)
    print("\nARBEITSLISTE (Reihenfolge einhalten)")
    for t in liste["cluster"]:
        sl = [x["slug"] for x in thema_zeilen(t)]
        print(f"  0. article-planner im CLUSTER-MODUS: Thema '{t}' für {', '.join(sl)}  (einmal vor den Einzelplänen; legt daten/plaene/_cluster-{t}.md an)")
    if liste["plan"] or liste["plan-fix"]:
        print(f"  1. article-planner: {', '.join(liste['plan'] + liste['plan-fix'])}  (parallel, je Artikel; liest den Cluster-Plan, falls vorhanden)")
    for t, sl in liste["belege"].items():
        print(f"  2. evidence-researcher: Thema '{t}' für {', '.join(sl)}  (nach den Plänen, vorhandene Belege werden wiederverwendet)")
    for t in liste["belegreview"]:
        print(f"  2b. compliance-reviewer im BELEG-MODUS: Thema '{t}' (einmal; schreibt daten/reviews/_belege-{t}.md; ein falscher Beleg steckt sonst in allen Artikeln)")
    if liste["schreiben"]:
        print(f"  3. article-writer: {', '.join(liste['schreiben'])}  (parallel, je Artikel)")
    if liste["fertig"]:
        print(f"  4. fertig geschrieben: {', '.join(liste['fertig'])} -> pipeline.py gates · review · wp_publish.py")
    print("  Hinweis: nicht auf alle warten. Jeder Artikel geht einzeln in die nächste Stufe, sobald seine eigene fertig ist (Plan -> Belege des Themas -> Skelett -> Schreiben -> abschluss -> Review -> Fix -> abschluss).")
    print("  Vor dem Schreiben: pipeline.py fragen (Praxisfragen an Alexander; nicht blockierend, Artikel ohne Antwort erscheinen ohne Praxis-Block).")
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
        h = lauf(HERE / "hwg_check.py", pfad)
        wert = re.search(r"Lesbarkeit (\d+)", l.stdout)
        luecken = len(re.findall(r"FAKT FEHLT", t))
        nf = nicht_final(pfad)
        ok = l.returncode == 0 and b.returncode == 0 and h.returncode == 0 and not nf
        ok_all &= ok
        if nf: print(f"{s}: NICHT FINAL – " + "; ".join(nf))
        print(f"{s}: Lesbarkeit {wert.group(1) if wert else '?'} · Skript {'OK' if l.returncode == 0 else 'PRÜFEN'} · Belege {'OK' if b.returncode == 0 else 'PRÜFEN'} · HWG-Muster {'OK' if h.returncode == 0 else 'PRÜFEN'} · Lücken {luecken}")
        if not ok:
            for x in (l.stdout + b.stdout + h.stdout).split("\n"):
                if x.startswith("   -") or x.startswith("  - "):
                    print("    " + x.strip())
    sys.exit(0 if ok_all else 1)


def check(a):
    """Beide Prüfskripte in einem Aufruf, kompakte Ausgabe (spart Runden im Agent)."""
    pfad = ROOT / "daten" / "entwuerfe" / f"{a.slug}.md"
    l = lauf(HERE / "lesbarkeit.py", pfad)
    b = lauf(HERE / "belege_check.py", "check", pfad, "--abgleich")
    h = lauf(HERE / "hwg_check.py", pfad)
    ok = l.returncode == 0 and b.returncode == 0 and h.returncode == 0
    print(f"{a.slug}: {'ALLES OK' if ok else 'PRÜFEN'}")
    for ausgabe in (l.stdout, b.stdout, h.stdout):
        for x in ausgabe.split("\n"):
            if x.strip() and not x.startswith(str(pfad)) and not x.strip().startswith("Bausteine"):
                print(x)
    sys.exit(0 if ok else 1)


def geplant_eintragen(rows):
    """Cluster-Slugs als 'geplant' in den Linkplan (Weiterlesen nutzt nur 'live')."""
    lp = ROOT / "daten" / "linkplan.csv"
    if not lp.exists():
        return
    vorh = list(csv.DictReader(lp.open(encoding="utf-8", newline="")))
    kopf = ["slug", "url", "typ", "kategorie", "cluster", "status", "anker"]
    have = {r["slug"] for r in vorh}
    neu = [r for r in rows if r["status"] in ("offen", "skelett") and r["slug"] not in have]
    if not neu:
        return
    for r in neu:
        vorh.append({"slug": r["slug"], "url": f"/{r['kategorie']}/{r['slug']}/", "typ": "artikel", "kategorie": r["kategorie"], "cluster": r["cluster"], "status": "geplant", "anker": r["keyword"].capitalize()})
    w = csv.DictWriter(lp.open("w", encoding="utf-8", newline=""), fieldnames=kopf, extrasaction="ignore")
    w.writeheader(); w.writerows(vorh)


def live(a):
    """Veröffentlichte Artikel im Linkplan auf live setzen (Anker = Titel aus dem Entwurf)."""
    lp = ROOT / "daten" / "linkplan.csv"
    vorh = list(csv.DictReader(lp.open(encoding="utf-8", newline="")))
    kopf = ["slug", "url", "typ", "kategorie", "cluster", "status", "anker"]
    for s_ in a.slugs:
        z = next((r for r in vorh if r["slug"] == s_), None)
        d = ROOT / "daten" / "entwuerfe" / f"{s_}.md"
        titel = re.search(r"^title:\s*(.+)$", d.read_text(encoding="utf-8"), flags=re.M) if d.exists() else None
        if z is None:
            q = next((r for r in laden() if r["slug"] == s_), None)
            if not q: print(f"{s_}: nicht in Queue"); continue
            z = {"slug": s_, "url": f"/{q['kategorie']}/{s_}/", "typ": "artikel", "kategorie": q["kategorie"], "cluster": q["cluster"], "status": "", "anker": ""}
            vorh.append(z)
        z["status"] = "live"
        if titel: z["anker"] = titel.group(1).strip().strip('"')
        print(f"{s_}: live")
    w = csv.DictWriter(lp.open("w", encoding="utf-8", newline=""), fieldnames=kopf, extrasaction="ignore")
    w.writeheader(); w.writerows(vorh)


def weiterlesen(a):
    """Setzt den Abschnitt 'Weiterlesen' der Entwürfe eines Themas neu: live-Geschwister (Cluster) plus Leistungsseite. Danach wp_publish.py --update."""
    lp = ROOT / "daten" / "linkplan.csv"
    plan = list(csv.DictReader(lp.open(encoding="utf-8", newline="")))
    sys.path.insert(0, str(HERE))
    bs = __import__("json").loads((ROOT / ".claude" / "skills" / "seo-pipeline" / "references" / "bausteine.json").read_text(encoding="utf-8"))
    for r in [x for x in laden() if x["thema"] == a.thema]:
        d = ROOT / "daten" / "entwuerfe" / f"{r['slug']}.md"
        if not d.exists(): continue
        geschwister = [f"- [{p['anker']}]({p['url']})" for p in plan if p["typ"] == "artikel" and p["status"] == "live" and p["slug"] != r["slug"] and p["cluster"] == r["cluster"]][:3]
        leist = bs["leistung"].get(r["kategorie"])
        if leist: geschwister.append(f"- [{leist[1]}]({leist[0]})")
        t = d.read_text(encoding="utf-8")
        neu = re.sub(r"(^## Weiterlesen\n\n)(.*?)(?=^## |\Z)", lambda m: m.group(1) + "\n".join(geschwister) + "\n\n", t, flags=re.M | re.S)
        if neu != t:
            d.write_text(neu, encoding="utf-8"); print(f"{r['slug']}: Weiterlesen neu ({len(geschwister)} Links)")


def schlank(a):
    """Schlanker Ablauf: pro Artikel Skelett aus dem Brief (ohne Plan) und ein kompaktes Paket."""
    rows = {r["slug"]: r for r in laden()}
    sys.path.insert(0, str(HERE))
    import belege_check as bc
    for slug in a.slugs:
        q = rows.get(slug)
        if not q:
            print(f"{slug}: nicht in der Queue"); continue
        fakten = a.fakten or f"{q['thema']}-web"
        d = ROOT / "daten" / "entwuerfe" / f"{slug}.md"
        if not d.exists():
            res = lauf(HERE / "skelett.py", slug, "--kategorie", q["kategorie"], "--thema", fakten, "--cluster", q["cluster"], "--intent", q["intent"] or "info", "--praxis", q["praxis"] or "optional")
            print((res.stdout or res.stderr).strip())
        def lies(pfad):
            p = ROOT / pfad
            return p.read_text(encoding="utf-8") if p.exists() else ""
        teile = [f"# Schreibpaket (schlank): {slug}\n\nDas Skelett `daten/entwuerfe/{slug}.md` füllst du aus. Weitere Dateien brauchst du nicht."]
        teile.append(lies(".claude/skills/seo-pipeline/references/regeln-kompakt.md"))
        cl = lies(f"daten/plaene/_cluster-{q['thema']}.md")
        zeile = [z for z in cl.split("\n") if z.startswith("|") and slug in z.split("|")[1]]
        kopf = [z for z in cl.split("\n") if z.startswith("| slug")]
        if zeile:
            teile.append("## Cluster-Zeile (Rolle, Blickwinkel, zugewiesene Nebenkeywords, interne Links)\n\n" + "\n".join(kopf[:1] + ["|---|---|---|---|---|---|"] + zeile[:1]))
            zl = [z for z in cl.split("\n") if "→" in z and slug in z]
            if zl: teile.append("Zusammengelegt in diesen Artikel: " + "; ".join(zl))
        teile.append("## SEO-Brief\n\n" + lies(f"daten/briefs/{slug}.md"))
        bpfad = ROOT / "daten" / "belege" / f"{fakten}.md"
        if bpfad.exists():
            _, quellen, aussagen, _ = bc.belege_lesen(bpfad)
            zeilen = ["| ID | Aussage | Zahlen | Einschränkung | Formulierung |", "|---|---|---|---|---|"]
            for r in aussagen:
                zeilen.append("| " + " | ".join([r[0], r[1], r[2], r[4], (r[6] if len(r) > 6 else "")]) + " |")
            luecken = re.search(r"^##\s+Lücken.*?\n(.*?)(?=^##\s|\Z)", bpfad.read_text(encoding="utf-8"), flags=re.M | re.S)
            teile.append("## Beleg-Aussagen (zitieren mit [B..])\n\n" + "\n".join(zeilen) + ("\n\n### Lücken (Orientierung ohne Zahl)\n" + luecken.group(1).strip() if luecken else ""))
        else:
            teile.append(f"## Beleg-Aussagen\n\n(Faktenblatt daten/belege/{fakten}.md fehlt)")
        teile.append("## Praxisfakten (material/fakten.md)\n\n" + lies("material/fakten.md"))
        out = ROOT / "daten" / "pakete" / f"{slug}.md"
        out.parent.mkdir(exist_ok=True)
        out.write_text("\n\n".join(teile) + "\n", encoding="utf-8")
        print(f"{slug}: Paket {len(' '.join(teile).split())} Wörter")


def belegreview_ok(a):
    r = belegreview_datei(a.thema)
    if not r.exists():
        sys.exit(f"{r.name} fehlt: erst Beleg-Review")
    r.touch()
    print(f"{r.name}: als aktuell markiert")


def normalisieren(pfad):
    """Wiederkehrende Formfehler deterministisch beheben (spart Agentenschritte): Merksatz-Format."""
    t = pfad.read_text(encoding="utf-8")
    neu = re.sub(r"<!--\s*(?:NEBENKEYWORDS|HINWEIS|CLUSTER:).*?-->[ \t]*\n?", "", t, flags=re.S)   # Skelett-Kommentare würden im Beitrag als Text erscheinen
    neu = re.sub(r"^\*\*Merksatz:\*\*\s*", "> Merksatz: ", neu, flags=re.M)
    neu = re.sub(r"^>\s*(?:\*\*)?(?:Merke|Merk dir|Tipp zum Merken)(?:\*\*)?:\s*", "> Merksatz: ", neu, flags=re.M)
    if neu != t:
        pfad.write_text(neu, encoding="utf-8")


def nicht_final(pfad):
    t = pfad.read_text(encoding="utf-8")
    haupt = re.split(r"^##\s+Quellen\b", t, flags=re.M)
    probleme = []
    if re.search(r"<!-- SCHREIBEN", t): probleme.append("Skelett nicht ausgefüllt (<!-- SCHREIBEN)")
    if re.search(r"\[[SB]\d+\]", haupt[0]): probleme.append("Zitate nicht nummeriert ([B..] im Text)")
    if len(haupt) > 1 and "wird von belege_check.py finalize erzeugt" in haupt[1]: probleme.append("Quellenbox leer")
    return probleme


def abschluss_lauf(slug):
    """normalisieren -> check -> finalize (immer, wenn neue [S..]/[B..]-Zitate stehen) -> check -> Finalprüfung. Gibt (ok, Ausgabe) zurück."""
    pfad = ROOT / "daten" / "entwuerfe" / f"{slug}.md"
    if not pfad.exists():
        return False, f"{slug}: kein Entwurf"
    normalisieren(pfad)
    def pruef():
        l = lauf(HERE / "lesbarkeit.py", pfad)
        b = lauf(HERE / "belege_check.py", "check", pfad)
        h = lauf(HERE / "hwg_check.py", pfad)
        return l.returncode == 0 and b.returncode == 0 and h.returncode == 0, l.stdout + b.stdout + h.stdout
    ok, ausgabe = pruef()
    t = pfad.read_text(encoding="utf-8")
    if re.search(r"\[[SB]\d+\]", re.split(r"^##\s+Quellen\b", t, flags=re.M)[0]):
        # auch bei offenen Hinweisen finalisieren, damit nie ein Entwurf mit rohen IDs liegen bleibt
        res = lauf(HERE / "belege_check.py", "finalize", pfad)
        print((res.stdout or res.stderr).strip())
        ok, ausgabe = pruef()
    for pr in nicht_final(pfad):
        ok = False
        ausgabe += f"\n  - NICHT FINAL: {pr}"
    return ok, ausgabe


def abschluss(a):
    """Endstand eines Artikels: check -> finalize (nur bei neuen [S..]/[B..]-Zitaten) -> check. Danach nicht mehr editieren."""
    ok, ausgabe = abschluss_lauf(a.slug)
    print(f"{a.slug}: {'ABSCHLUSS OK (Endstand geprüft)' if ok else 'PRÜFEN'}")
    if not ok:
        pfad = str(ROOT / "daten" / "entwuerfe" / f"{a.slug}.md")
        for x in ausgabe.split("\n"):
            if x.strip() and not x.startswith(pfad):
                print(x)
    sys.exit(0 if ok else 1)


def patch(a):
    """Wendet die PATCHES des Reviews exakt an. Format in daten/reviews/<slug>.md:
       PATCHES:
       - ALT: <exakter Text aus dem Entwurf (eine Zeile)>
         NEU: <Ersatz>
    Jeder ALT-Text muss genau einmal vorkommen. Danach abschluss. Exit 0 nur, wenn alles angewendet wurde und der Endstand OK ist."""
    rv = ROOT / "daten" / "reviews" / f"{a.slug}.md"
    d = ROOT / "daten" / "entwuerfe" / f"{a.slug}.md"
    if not rv.exists() or not d.exists():
        sys.exit(f"{a.slug}: Review oder Entwurf fehlt")
    block = re.search(r"^PATCHES:\s*\n(.*?)(?=^[A-ZÄÖÜ ]+:\s*$|\Z)", rv.read_text(encoding="utf-8"), flags=re.M | re.S)
    paare = re.findall(r"^-\s*ALT:\s*(.+?)\s*\n\s+NEU:\s*(.*?)\s*$", block.group(1), flags=re.M) if block else []
    text = d.read_text(encoding="utf-8")
    angewendet, offen = 0, []
    for alt, neu in paare:
        n = text.count(alt)
        if n == 1:
            text = text.replace(alt, neu); angewendet += 1
        else:
            offen.append(f"{'kommt ' + str(n) + 'x vor' if n else 'nicht gefunden'}: {alt[:70]}")
    if angewendet:
        d.write_text(text, encoding="utf-8")
    ok, ausgabe = abschluss_lauf(a.slug)
    print(f"{a.slug}: {angewendet} von {len(paare)} Patches angewendet · Endstand {'OK' if ok else 'PRÜFEN'}")
    for o in offen:
        print("  offen – " + o)
    if not ok:
        pfad = str(d)
        for x in ausgabe.split("\n"):
            if x.strip() and not x.startswith(pfad):
                print(x)
    sys.exit(0 if (ok and not offen) else 1)


def paket(a):
    """Schreibpaket: alles, was der Autor liest, in einer Datei (spart Lese-Schritte, nichts Neues)."""
    slug = a.slug
    q = next((r for r in laden() if r["slug"] == slug), None)
    if not q:
        sys.exit(f"{slug}: nicht in der Queue")
    def lies(pfad, fallback=""):
        p = ROOT / pfad
        return p.read_text(encoding="utf-8") if p.exists() else fallback
    teile = [f"# Schreibpaket: {slug}\n\nEnthält Regeln, Plan, Cluster-Zeile, Beleg-Aussagen, Praxisfakten und Preise. Das Skelett `daten/entwuerfe/{slug}.md` füllst du aus; weitere Dateien brauchst du nicht zu lesen."]
    teile.append("## Regeln\n\n" + re.sub(r"^# .*\n", "", lies(".claude/skills/seo-pipeline/references/regeln.md")))
    teile.append("## Artikelplan\n\n" + lies(f"daten/plaene/{slug}.md", "(kein Plan)"))
    cl = lies(f"daten/plaene/_cluster-{q['thema']}.md")
    zeile = [z for z in cl.split("\n") if z.startswith("|") and slug in z.split("|")[1]]
    if zeile:
        teile.append("## Cluster-Zeile (Rolle, Blickwinkel, Nebenkeywords, interne Links)\n\n" + zeile[0])
    sys.path.insert(0, str(HERE))
    import belege_check as bc
    bpfad = ROOT / "daten" / "belege" / f"{q['thema']}.md"
    if bpfad.exists():
        _, quellen, aussagen, _ = bc.belege_lesen(bpfad)
        zeilen = ["| ID | Aussage | Zahlen | Quelle | Einschränkung | Formulierung |", "|---|---|---|---|---|---|"]
        for r in aussagen:
            zeilen.append("| " + " | ".join([r[0], r[1], r[2], r[3], r[4], (r[6] if len(r) > 6 else "")]) + " |")
        luecken = re.search(r"^##\s+Lücken.*?\n(.*?)(?=^##\s|\Z)", bpfad.read_text(encoding="utf-8"), flags=re.M | re.S)
        teile.append(f"## Beleg-Aussagen ({q['thema']}; zitieren mit [B..], Quellenbox baut `abschluss`)\n\n" + "\n".join(zeilen) + ("\n\n### Lücken\n" + luecken.group(1).strip() if luecken else ""))
    teile.append("## Praxisfakten (material/fakten.md)\n\n" + lies("material/fakten.md", "(leer)"))
    pr = re.search(r"^##\s+Preise in Wissensartikeln.*?(?=^##\s|\Z)", lies("kontext/angebot-und-preise.md"), flags=re.M | re.S)
    teile.append("## Preise in Wissensartikeln\n\n" + (pr.group(0) if pr else "Nur Intro-Offers und Aligner „ab ca. 3.900 €“ (siehe Regeln)."))
    stil = lies(".claude/skills/seo-pipeline/references/stil-und-format.md")
    if stil:
        teile.append("## Stil und Format\n\n" + stil)
    out = ROOT / "daten" / "pakete" / f"{slug}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n\n".join(teile) + "\n", encoding="utf-8")
    print(f"{out.relative_to(ROOT)} · {len(' '.join(teile).split())} Wörter")


def fragen(_):
    rows = laden()
    bythema = {}
    for r in rows:
        p = ROOT / "daten" / "entwuerfe" / f"{r['slug']}.md"
        if p.exists():
            for m in re.finditer(r"\[FAKT FEHLT:([^\]]*)\]", p.read_text(encoding="utf-8")):
                bythema.setdefault(r["thema"] or "?", []).append((r["slug"], m.group(1).strip()))
    fakten = (ROOT / "material" / "fakten.md").read_text(encoding="utf-8") if (ROOT / "material" / "fakten.md").exists() else ""
    for r in rows:
        pp = ROOT / "daten" / "plaene" / f"{r['slug']}.md"
        if pp.exists() and not re.search(rf"^- {re.escape(r['slug'])}:", fakten, flags=re.M):
            m = re.search(r"^- Praxisfragen:\s*(.+)$", pp.read_text(encoding="utf-8"), flags=re.M)
            if m and "<Frage" not in m.group(1):
                for q in m.group(1).split(";"):
                    if q.strip(): bythema.setdefault(r["thema"] or "?", []).append((r["slug"], "Frage an Alexander: " + q.strip()))
    if not bythema:
        print("Keine offenen [FAKT FEHLT]-Stellen oder Praxisfragen."); return
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
    themen = {r["thema"] for r in rows if r["slug"] in (a.slugs or [x["slug"] for x in rows if x["status"] in ("entwurf", "skelett")])}
    # Rückfallregel je Thema: ein Rot oder viele Befunde in einem Thema zwingt nur dieses Thema zur Vollprüfung
    def modus(thema):
        lg = [r for r in log if r["thema"] == thema]
        rot_ = any(r["ampel"] == "rot" for r in lg[-FENSTER:])
        schnitt_ = (sum(int(r["inhaltlich"]) for r in lg[-5:]) / max(1, len(lg[-5:]))) if lg else 0
        return rot_, schnitt_, (rot_ or schnitt_ >= MAX_INHALT)
    rot, schnitt, voll_modus = (False, 0, False)
    slugs = a.slugs or [r["slug"] for r in rows if r["status"] == "entwurf"]
    geprueft_je_thema = {}
    for r in log:
        geprueft_je_thema[r["thema"]] = geprueft_je_thema.get(r["thema"], 0) + 1
    for t in sorted(themen):
        rot, schnitt, vm = modus(t)
        print(f"Thema {t}: {'VOLLE PRÜFUNG' if vm else 'Stichprobe'} (rot in den letzten {FENSTER}: {'ja' if rot else 'nein'}, Ø wichtige Befunde der letzten 5: {schnitt:.1f}, Grenze {MAX_INHALT})")
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
        if modus(r["thema"])[2]: gruende.append("Rückfallregel (im Thema zuletzt rot oder viele inhaltliche Befunde)")
        if n < VOLL_BIS: gruende.append(f"erst {n} geprüfte Artikel im Thema {r['thema']}")
        if (r["intent"] or "") in ("kosten", "vergleich"): gruende.append("Kosten/Vergleich")
        if re.search(r"^> Praxis:", t, flags=re.M) and "FAKT FEHLT" not in t: gruende.append("Praxis-Block mit Alexanders Aussagen")
        if re.search(r"Krankenkasse|Kasse|§|SGB", t): gruende.append("Kasse/Recht")
        if (len(re.findall(r"\[\d+\]", t)) > 18): gruende.append("viele Zitate")
        if not gruende and (len([x for x in log if x["thema"] == r["thema"]]) + 1) % STICHPROBE == 0:
            gruende.append(f"Stichprobe (jeder {STICHPROBE}.)")
        print(f"{s}: {'PRÜFEN – ' + '; '.join(gruende) if gruende else 'ohne Review (nur Skript-Gates)'}")
        if gruende: muss.append(s)
    print(f"\n{len(muss)} von {len(slugs)} brauchen den Reviewer. Je Artikel EIN compliance-reviewer, alle parallel in einer Runde; Befunde schreibt er nach daten/reviews/<slug>.md, der Autor liest sie dort.")
    for s in muss:
        print(f"  compliance-reviewer: {s}  (Eingabe: pipeline.py check {s}; Ausgabe: daten/reviews/{s}.md)")


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
    st = sub.add_parser("stempel"); st.add_argument("slug")
    ck = sub.add_parser("check"); ck.add_argument("slug")
    ab = sub.add_parser("abschluss"); ab.add_argument("slug")
    sl = sub.add_parser("schlank"); sl.add_argument("slugs", nargs="+"); sl.add_argument("--fakten")
    bo = sub.add_parser("belegreview-ok"); bo.add_argument("thema")
    pk = sub.add_parser("paket"); pk.add_argument("slug")
    pt = sub.add_parser("patch"); pt.add_argument("slug")
    lv = sub.add_parser("live"); lv.add_argument("slugs", nargs="+")
    wl = sub.add_parser("weiterlesen"); wl.add_argument("thema")
    rv = sub.add_parser("review"); rv.add_argument("slugs", nargs="*")
    lg = sub.add_parser("logreview"); lg.add_argument("slug"); lg.add_argument("ampel", choices=["rot", "gelb", "gruen"]); lg.add_argument("n", type=int)
    a = ap.parse_args()
    {"status": status, "prepare": prepare, "gates": gates, "fragen": fragen, "stempel": lambda a: print(stempel(a.slug)), "check": check, "abschluss": abschluss, "paket": paket, "schlank": schlank, "belegreview-ok": belegreview_ok, "patch": patch, "live": live, "weiterlesen": weiterlesen, "review": review, "logreview": logreview}[a.cmd](a)
