#!/usr/bin/env python3
"""Legt das Artikel-Skelett an: Frontmatter, Überschriften aus dem SEO-Brief, Zusage, CTA, Weiterlesen.

Aufruf: python3 skelett.py <slug> --kategorie <kat> --thema <belege-thema> [--intent info] [--brief daten/briefs/<x>.md] [--force]
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


def praxis_text(slug):
    f = ROOT / "material" / "fakten.md"
    if f.exists():
        m = re.search(rf"^- {re.escape(slug)}:\s*(.+)$", f.read_text(encoding="utf-8"), flags=re.M)
        if m:
            return m.group(1).strip()
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--kategorie", required=True)
    ap.add_argument("--thema", required=True, help="Name der Beleg-Datei in daten/belege/")
    ap.add_argument("--intent", default="info")
    ap.add_argument("--cluster", default="")
    ap.add_argument("--brief")
    ap.add_argument("--out")
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
    px = praxis_text(a.slug)
    praxis = f"> Praxis: {px}" if px else "> Praxis: [FAKT FEHLT: Alexanders Einschätzung zu diesem Thema in 3–5 Sätzen: Was er in der Praxis sieht, woran Patienten es zuerst bemerken, wann er zum Termin rät. In material/fakten.md unter „Persönliche Einschätzung“ als Zeile „- " + a.slug + ": …“ eintragen.]"
    h2 = [q for q in fragen][:4] or ["<!-- SCHREIBEN: Frage aus dem Brief -->"]
    faq = [q for q in fragen[4:]][:3] + [n for n, _ in neben if n.endswith("?") or n.startswith(("wie", "was", "warum", "kann", "können", "muss"))][:2]
    doc = f"""---
title: ""
slug: {a.slug}
kategorie: {kat}
keyword: {haupt}
fokus_keyword: {haupt}
cluster: {a.cluster}
intent: {a.intent}
thema_belege: {a.thema}
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

<!-- HINWEIS: Die Überschriften unten stammen aus dem SEO-Brief und sind Vorschläge. Streiche oder ersetze sie, wenn die Belege nichts hergeben oder die Frage eine Preisfrage ist (Preisregel). Mindestens 3 H2, die Hauptphrase in 1–2 H2. -->

<!-- SCHREIBEN: Einstieg, 2–3 Sätze, direkte Antwort mit der Hauptphrase "{haupt}" in den ersten 100 Wörtern -->

## Was Sie jetzt tun können

<!-- SCHREIBEN: Liste mit 3–5 Punkten, ohne Druck, ohne Diagnose; letzter Punkt: wann ein Termin sinnvoll ist -->

""" + "".join(f"## {q}\n\n<!-- SCHREIBEN: 1–2 kurze Absätze, dann Liste, Tabelle oder Merksatz; nur Belege B… mit [S…] -->\n\n" for q in h2) + f"""## Aus der Praxis

{praxis}

## Das spricht dagegen: Grenzen und Nachteile

<!-- SCHREIBEN: Liste, ehrlich, nur belegte oder praxisbekannte Punkte -->

## Häufige Fragen

""" + ("".join(f"### {q if q.endswith('?') else q.capitalize() + '?'}\n\n<!-- SCHREIBEN: Antwort höchstens 3 Sätze oder Frage streichen, wenn nicht belegbar -->\n\n" for q in faq[:4]) or "<!-- SCHREIBEN: 3–5 FAQ-Fragen als ### Frage? mit Antwort, Fragen aus Brief und Nebenkeywords -->\n\n") + f"""## Was heißt das für Sie?

<!-- SCHREIBEN: 2–3 Stichpunkte -->

> Zusage: {zus}

> CTA: {cta}

## Weiterlesen

{chr(10).join(links)}

## Quellen

<!-- wird von belege_check.py finalize erzeugt -->
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    print(f"Skelett: {out} · {len(h2)} H2 · {len(faq[:4])} FAQ · Zusage/CTA-Variante nach Hash · Praxis: {'vorhanden' if px else 'FAKT FEHLT'}")


if __name__ == "__main__":
    main()
