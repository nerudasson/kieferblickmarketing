#!/usr/bin/env python3
"""Legt das Artikel-Skelett an: Frontmatter, Überschriften aus dem SEO-Brief, Zusage, CTA, Weiterlesen.

Aufruf: python3 skelett.py <slug> --kategorie <kat> --thema <belege-thema> [--intent info] [--brief daten/briefs/<x>.md] [--force]
        python3 skelett.py plan-check <slug>          prüft daten/plaene/<slug>.md auf Format und Vollständigkeit
Mit Plan (daten/plaene/<slug>.md, Agent article-planner): Abschnitte, Elemente (Tabelle/Liste/Schritte/Fließtext),
Belegfragen und Ziel-Länge kommen aus dem Plan. Ohne Plan: Überschriften aus dem Brief (Fallback).
Der Writer ersetzt nur die Stellen <!-- SCHREIBEN: ... -->. Zusage und CTA kommen aus references/bausteine.json
(3 Varianten je Kategorie, Auswahl nach Hash des Slugs). Weiterlesen aus daten/linkplan.csv.
"""
import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[2]


def variante(slug, liste, salz=""):
    h = int(hashlib.sha1((slug + salz).encode()).hexdigest(), 16)
    return liste[h % len(liste)]


def brief_lesen(pfad):
    t = Path(pfad).read_text(encoding="utf-8") if Path(pfad).exists() else ""
    haupt = re.search(r"\*\*(.+?)\*\* · Volumen", t)
    neben = re.findall(r"^\| ([^|]+?) \| (\d+) \|", t, flags=re.M)
    fragen = []
    m = re.search(r"## Fragen der Suchenden.*?\n(.*?)\n\n", t, flags=re.S)
    if m:
        fragen = [x[2:].strip() for x in m.group(1).split("\n") if x.startswith("- ")]
    return (haupt.group(1) if haupt else ""), [(a.strip(), int(b)) for a, b in neben if a.strip() not in ("Phrase", "Rang")], fragen


def plan_lesen(slug):
    pf = ROOT / "daten" / "plaene" / f"{slug}.md"
    if not pf.exists():
        return None
    t = pf.read_text(encoding="utf-8")
    fm = dict(re.findall(r"^(\w+):\s*(.+)$", re.match(r"^---\n(.*?)\n---", t, flags=re.S).group(1), flags=re.M)) if t.startswith("---") else {}
    abschnitte = []
    m = re.search(r"^## Abschnitte\n(.*?)(?=^## |\Z)", t, flags=re.M | re.S)
    if m:
        for z in m.group(1).split("\n"):
            if z.startswith("|") and not re.match(r"^\|(?:[\s:-]+\|)+$", z.strip()):
                c = [x.strip() for x in z.strip().strip("|").split("|")]
                if len(c) >= 6 and c[0].isdigit():
                    abschnitte.append(dict(nr=c[0], h2=c[1], cluster=c[2], argument=c[3], element=c[4], beleg=c[5], woerter=(c[6] if len(c) > 6 else '')))
    bs = re.search(r"^## Bausteine\n(.*?)(?=^## |\Z)", t, flags=re.M | re.S)
    faq = []
    if bs:
        f = re.search(r"^- FAQ:\s*(.+)$", bs.group(1), flags=re.M)
        if f:
            faq = [x.strip().rstrip("?") + "?" for x in f.group(1).split(";") if x.strip()]
    return dict(fm=fm, abschnitte=abschnitte, faq=faq, text=t)


FEST_WOERTER = 400  # Einstieg, Was Sie jetzt tun können, Nachteile, FAQ, Was heißt das für Sie


def plan_check(slug):
    pl = plan_lesen(slug)
    if not pl:
        sys.exit(f"daten/plaene/{slug}.md fehlt")
    fehler = []
    ab = pl["abschnitte"]
    if len(ab) < 3: fehler.append(f"nur {len(ab)} Abschnitte (mind. 3, meist 4–7)")
    if len(ab) > 10: fehler.append(f"{len(ab)} Abschnitte: zu viel für einen Artikel, Nebenfragen auslagern")
    gueltig = {"fließtext", "liste", "tabelle", "schritte"}
    for a in ab:
        if a["element"].lower().split()[0] not in gueltig: fehler.append(f"Abschnitt {a['nr']}: Element '{a['element']}' unbekannt")
        if not a["argument"]: fehler.append(f"Abschnitt {a['nr']}: Argument fehlt")
        if not a["beleg"]: fehler.append(f"Abschnitt {a['nr']}: Belegfrage leer (– eintragen, wenn keine nötig)")
    nb = sum(1 for a in ab if a["beleg"] not in ("–", "-", ""))
    if nb > 5: fehler.append(f"{nb} Belegfragen: höchstens 5 (nur die wichtigen)")
    if nb < 2: fehler.append(f"nur {nb} Belegfragen: mindestens 2")
    intent = pl["fm"].get("intent", "info")
    if intent in ("kosten", "vergleich") and not any(a["element"].lower().startswith("tabelle") for a in ab):
        fehler.append("Intent Kosten/Vergleich ohne Tabelle")
    run = 0
    for a in ab:
        run = run + 1 if a["element"].lower().startswith("fließtext") else 0
        if run > 2: fehler.append("mehr als 2 Fließtext-Abschnitte hintereinander"); break
    zw = re.match(r"\s*(\d+)\s*[-–]\s*(\d+)", pl["fm"].get("ziel_woerter", ""))
    if not zw:
        fehler.append("ziel_woerter fehlt (Format 1000-1400)")
    else:
        lo, hi = int(zw.group(1)), int(zw.group(2))
        bf = ROOT / "daten" / "briefs" / f"{slug}.md"
        m = bf.exists() and re.search(r"Empfohlene Ziel-Länge: (\d+)[-–](\d+)", bf.read_text(encoding="utf-8"))
        if m and lo < int(m.group(1)) * 0.9:
            fehler.append(f"ziel_woerter {lo}-{hi} liegt unter der SEO-Empfehlung {m.group(1)}–{m.group(2)} aus dem Brief: Empfehlung übernehmen und die Abschnitte darauf auslegen")
        summe = sum(int(re.findall(r"\d+", a["woerter"])[-1]) for a in ab if re.findall(r"\d+", a["woerter"]))
        if summe + FEST_WOERTER < lo * 0.9:
            fehler.append(f"Plan zu kurz: Abschnitte {summe} + feste Teile {FEST_WOERTER} = {summe + FEST_WOERTER} Wörter, Ziel {lo}–{hi}. Abschnitte ergänzen (Pflichtthemen der Wettbewerber, Fragen, Verwandte Suchen, Ablauf, Alltag, Nachteile) oder Budgets je Element anheben (Tabelle 150–250, Liste 120–200, Schritte 150–250, Fließtext 150–300)")
        elif summe + FEST_WOERTER > hi * 1.15:
            fehler.append(f"Plan zu lang: {summe + FEST_WOERTER} Wörter, Ziel {lo}–{hi}: Budgets senken oder Nebenfragen auslagern")
    kw = pl["fm"].get("keyword", "").strip().lower()
    if kw and not any(all(w[:5] in a["h2"].lower() for w in kw.split() if len(w) > 3) for a in ab):
        fehler.append("Hauptphrase steht in keiner Abschnitts-Überschrift")
    print(f"Plan {slug}: {len(ab)} Abschnitte, {nb} Belegfragen, ziel_woerter {pl['fm'].get('ziel_woerter')}" + (" · FEHLER:" if fehler else " · OK"))
    for f in fehler: print("  - " + f)
    sys.exit(1 if fehler else 0)


def praxis_text(slug):
    f = ROOT / "material" / "fakten.md"
    if f.exists():
        m = re.search(rf"^- {re.escape(slug)}:\s*(.+)$", f.read_text(encoding="utf-8"), flags=re.M)
        if m:
            return m.group(1).strip()
    return None


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "plan-check":
        plan_check(sys.argv[2])
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--kategorie", required=True)
    ap.add_argument("--thema", required=True, help="Name der Beleg-Datei in daten/belege/")
    ap.add_argument("--intent", default="info")
    ap.add_argument("--cluster", default="")
    ap.add_argument("--brief")
    ap.add_argument("--out")
    ap.add_argument("--praxis", choices=["pflicht", "optional"], default="optional")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    bs = json.loads((BASE / "references" / "bausteine.json").read_text(encoding="utf-8"))
    kat = a.kategorie
    brief = a.brief or f"daten/briefs/{a.slug}.md"
    haupt, neben, fragen = brief_lesen(ROOT / brief)
    out = Path(a.out) if a.out else ROOT / "daten" / "entwuerfe" / f"{a.slug}.md"
    if out.exists() and not a.force:
        sys.exit(f"{out} existiert. Mit --force überschreiben.")
    zus = variante(a.slug, bs["zusage"].get(kat) or bs["zusage"]["aligner"])
    ersttermin = bs["erstterminseite"].get(kat, "/erstermin/")
    cta = variante(a.slug, bs["cta"]["default"], "cta").replace("{ersttermin}", ersttermin)
    # Weiterlesen
    links = []
    lp = ROOT / "daten" / "linkplan.csv"
    if lp.exists():
        for r in csv.DictReader(lp.open(encoding="utf-8")):
            if r["typ"] == "artikel" and r["slug"] != a.slug and r["kategorie"] == kat:
                links.append(f"- [{r['anker']}]({r['url']})")
    leist = bs["leistung"].get(kat)
    if leist:
        links.append(f"- [{leist[1]}]({leist[0]})")
    links = links[:4]
    plan = plan_lesen(a.slug)
    h2 = [q for q in fragen][:4] or ["<!-- SCHREIBEN: Frage aus dem Brief -->"]
    faq = [q for q in fragen[4:]][:3] + [n for n, _ in neben if n.endswith("?") or n.startswith(("wie", "was", "warum", "kann", "können", "muss"))][:2]
    hinweise = {"tabelle": "TABELLE (2–4 Spalten, 5–10 Zeilen, nur eine Zahlenreihe) mit 2–3 Sätzen Einordnung davor oder danach",
                "liste": "LISTE (5–8 Punkte, je 1–3 Zeilen, Fettanfang möglich) mit 1–2 Einordnungssätzen",
                "schritte": "SCHRITTE (nummerierte Liste, je Schritt 1–2 Sätze, dazu Hinweis, was dabei schiefgehen kann)",
                "fließtext": "FLIESSTEXT (2–4 kurze Absätze, je 1–3 Sätze, mit einer Alltagssituation von Julia)"}
    if plan and plan["abschnitte"]:
        abschn = []
        for ab in plan["abschnitte"]:
            el = ab["element"].lower().split()[0]
            beleg = f" Belegfrage: {ab['beleg']}" if ab["beleg"] not in ("–", "-", "") else " Kein Beleg nötig (Orientierung/Erklärung)."
            abschn.append(f"## {ab['h2']}\n\n<!-- CLUSTER: {ab['cluster']} -->\n<!-- SCHREIBEN: {hinweise.get(el, el.upper())}, BUDGET {ab['woerter'] or '150'} Wörter (mindestens 80 % davon schreiben). Argument: {ab['argument']}.{beleg} Belege zitieren mit [B…]; fehlt ein Beleg, als Orientierung ohne Zahl schreiben, Abschnitt nie streichen. -->\n\n")
        faq = plan["faq"] or faq
        ziel = plan["fm"].get("ziel_woerter", "")
    else:
        abschn = [f"## {q}\n\n<!-- SCHREIBEN: 1–2 kurze Absätze, dann Liste, Tabelle oder Merksatz; nur Belege, zitiert mit [B…] -->\n\n" for q in h2]
        ziel = ""
    px = praxis_text(a.slug)
    omit_praxis = a.praxis == "optional" and not px
    praxis = f"> Praxis: {px}" if px else "> Praxis: [FAKT FEHLT: Alexanders Einschätzung zu diesem Thema in 3–5 Sätzen: Was er in der Praxis sieht, woran Patienten es zuerst bemerken, wann er zum Termin rät. In material/fakten.md unter „Persönliche Einschätzung“ als Zeile „- " + a.slug + ": …“ eintragen.]"
    doc = f"""---
title: ""
slug: {a.slug}
kategorie: {kat}
keyword: {haupt}
fokus_keyword: {haupt}
cluster: {a.cluster}
intent: {a.intent}
thema_belege: {a.thema}
ziel_woerter: {ziel}
plan: {"ja" if plan else "nein"}
praxis: {a.praxis}
autor: Alexander Andreev
seo_titel: ""
meta_description: ""
status: entwurf
kurz: |
  <!-- SCHREIBEN: drei Sätze, je eine Aussage -->
ursache:
behandlung:
dauer:
kosten:
ablauf:
---

<!-- NEBENKEYWORDS aus dem Brief (nur nutzen, wo die Belege es hergeben): {", ".join(f"{n} ({v})" for n, v in neben[:12])} -->

<!-- HINWEIS: Die Überschriften stammen aus dem Plan und bleiben. Fehlt für einen Abschnitt der Beleg, wird er als Orientierung ohne Zahl geschrieben, nicht gestrichen und nicht gekürzt. Preisfragen nach der Preisregel beantworten. Die Wortbudgets der Abschnitte sind Teil des Plans. -->

<!-- SCHREIBEN: Einstieg, 2–3 Sätze, direkte Antwort mit der Hauptphrase "{haupt}" in den ersten 100 Wörtern -->

## Was Sie jetzt tun können

<!-- SCHREIBEN: Liste mit 3–5 Punkten: Orientierung ist ohne Quelle erlaubt (anrufen, Foto, notieren, Unterlagen), keine Entwarnung/Dringlichkeit/Fristen ohne Beleg oder Praxis-Eintrag; letzter Punkt: wann ein Termin sinnvoll ist -->

""" + "".join(abschn) + f"""{"" if omit_praxis else "## Aus der Praxis" + chr(10) + chr(10) + praxis + chr(10)}
## Das spricht dagegen: Grenzen und Nachteile

<!-- SCHREIBEN: Liste mit 3–5 Punkten, je 1–2 Sätze, ehrlich; belegte Nachteile mit [B…], übrige als Orientierung ohne Zahl -->

## Häufige Fragen

""" + ("".join(f"### {q if q.endswith('?') else q.capitalize() + '?'}\n\n<!-- SCHREIBEN: Antwort 2–3 Sätze; ohne Beleg als Orientierung formulieren, Frage nicht streichen -->\n\n" for q in faq[:6]) or "<!-- SCHREIBEN: 3–5 FAQ-Fragen als ### Frage? mit Antwort, Fragen aus Brief und Nebenkeywords -->\n\n") + f"""## Was heißt das für Sie?

<!-- SCHREIBEN: 3–4 Stichpunkte mit der Einordnung für Julia -->

> Zusage: {zus}

> CTA: {cta}

## Weiterlesen

{chr(10).join(links)}

## Quellen

<!-- wird von belege_check.py finalize erzeugt -->
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    print(f"Skelett: {out} · {len(abschn)} H2 · {len(faq[:4])} FAQ · Zusage/CTA-Variante nach Hash · Praxis: {'vorhanden' if px else ('weggelassen (optional)' if omit_praxis else 'FAKT FEHLT')}")


if __name__ == "__main__":
    main()
