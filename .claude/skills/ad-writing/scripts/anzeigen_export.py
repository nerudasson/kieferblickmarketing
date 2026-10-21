#!/usr/bin/env python3
"""Exportiert eine geprüfte Kampagnendatei für den Google Ads Editor.

  anzeigen_export.py <datei.json> [--force]

Schreibt <datei>.csv (Kampagne PAUSIERT), <datei>-einstellungen.md (Einstellungen, die von Hand gesetzt werden) und
<datei>-vorschau.md (lesbare Fassung aller Gruppen, Keywords und Anzeigen zur Freigabe).
Bricht ab, solange anzeigen_check.py HART-Treffer meldet (außer --force, nur für Tests).
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anzeigen_check import pruefen  # noqa: E402

UEB, BES = 15, 4


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    pfad = Path(args[0])
    k = json.loads(pfad.read_text(encoding="utf-8"))
    hart, weich = pruefen(k)
    if hart and "--force" not in sys.argv:
        sys.exit(f"Export abgebrochen: {len(hart)} HART-Treffer (erst anzeigen_check.py).")
    kopf = (["Campaign", "Campaign Status", "Budget", "Budget type", "Bid Strategy Type", "Networks", "Languages",
             "Ad Group", "Ad Group Status", "Max CPC", "Keyword", "Criterion Type", "Ad type"]
            + [f"Headline {i}" for i in range(1, UEB + 1)] + ["Headline 1 position"]
            + [f"Description {i}" for i in range(1, BES + 1)] + ["Path 1", "Path 2", "Final URL"])
    zeilen = []

    def z(**kw): zeilen.append({c: kw.get(c, "") for c in kopf})

    c = k["kampagne"]
    z(**{"Campaign": c, "Campaign Status": "Paused", "Budget": k["tagesbudget_eur"], "Budget type": "Daily",
         "Bid Strategy Type": "Maximize clicks", "Networks": "Google search", "Languages": "de"})
    for n in k.get("negativ", []):
        z(**{"Campaign": c, "Keyword": n, "Criterion Type": "Campaign Negative Phrase"})
    for g in k["gruppen"]:
        z(**{"Campaign": c, "Ad Group": g["name"], "Ad Group Status": "Enabled", "Max CPC": k["max_cpc_eur"]})
        for kw in g["keywords"]:
            z(**{"Campaign": c, "Ad Group": g["name"], "Keyword": kw["text"], "Criterion Type": kw["match"].capitalize()})
        for a in g["anzeigen"]:
            row = {"Campaign": c, "Ad Group": g["name"], "Ad type": "Responsive search ad", "Headline 1 position": "1",
                   "Path 1": a.get("pfad1", ""), "Path 2": a.get("pfad2", ""), "Final URL": g["landingpage"]}
            for i, t in enumerate(a["ueberschriften"], 1): row[f"Headline {i}"] = t
            for i, t in enumerate(a["beschreibungen"], 1): row[f"Description {i}"] = t
            z(**row)
    csv_pfad = pfad.with_suffix(".csv")
    with open(csv_pfad, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=kopf, delimiter=","); w.writeheader(); w.writerows(zeilen)
    md = [f"# Einstellungen von Hand: {c}", "",
          "Diese Punkte setzt Alexander im Konto, sie stehen nicht im Import. Kampagne ist im Import **pausiert**.", "",
          f"- Standorte (Einstellung „Präsenz“): {', '.join(k.get('standorte', [])) or 'siehe Zonenplan'}",
          f"- Gebotsstrategie: {k.get('gebotsstrategie')}, Obergrenze {k.get('max_cpc_eur')} € je Klick; Tagesbudget {k.get('tagesbudget_eur')} €",
          "- Netzwerke: nur Suche; Suchpartner und Display aus",
          "- Automatisch erzeugte Assets, Seitenerweiterung (AI Max) und automatisch angewendete Empfehlungen aus",
          "- Erweiterungen: Sitelinks (Ablauf, Preise, Über Alexander), Anruf, Standort",
          "- Conversion-Ziele: laut Tracking-Plan (Anfrage gesendet, Anruf)", "", "## Offene Entscheidungen / WEICH-Treffer"]
    md += [f"- {x}" for x in weich] or ["- keine"]
    pfad.with_name(pfad.stem + "-einstellungen.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    v = [f"# Vorschau: {c}", "",
         f"Tagesbudget {k['tagesbudget_eur']} €, max. {k['max_cpc_eur']} € je Klick, {k.get('zone', '')}. Entwurf, nichts davon ist live.", ""]
    for g in k["gruppen"]:
        kws = list(dict.fromkeys(x["text"] for x in g["keywords"]))
        v += [f"## Gruppe: {g['name']}", f"- Winkel: {g['winkel']}", f"- CTA: {g['cta']}", f"- Seite: {g['landingpage']}",
              f"- Keywords (je exakt und als Wortgruppe): {', '.join(kws)}", ""]
        for a in g["anzeigen"]:
            v += [f"### Anzeige {a.get('variante', '')}: {a.get('kontrast', '')}", ""]
            v += [f"{i}. {t}" for i, t in enumerate(a["ueberschriften"], 1)]
            v += [""] + [f"- {t}" for t in a["beschreibungen"]]
            v += ["", f"Pfad: kieferblick.de/{a.get('pfad1', '')}/{a.get('pfad2', '')}"]
            if a.get("entscheidung"): v += [f"Offen: {a['entscheidung']}"]
            v += [""]
    v += ["## Negativbegriffe (Wortgruppe, Kampagne)", ", ".join(k.get("negativ", [])), ""]
    if k.get("entscheidungen"): v += ["## Offene Entscheidungen"] + [f"- {e}" for e in k["entscheidungen"]]
    pfad.with_name(pfad.stem + "-vorschau.md").write_text("\n".join(v) + "\n", encoding="utf-8")
    print(f"{len(zeilen)} Zeilen -> {csv_pfad.name}; Einstellungen -> {pfad.stem}-einstellungen.md ({len(weich)} weich)")


if __name__ == "__main__":
    main()
