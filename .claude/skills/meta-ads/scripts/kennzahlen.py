#!/usr/bin/env python3
"""Wochenauswertung Meta-Anzeigen: Kosten je Lead / MQL / SQL / Käufer nach Anzeige (nur Standardbibliothek).

  kennzahlen.py <eingabe.json> [--ausgabe daten/meta/wochen/<woche>.md]

Eingabe (nur Zählwerte, keine Kontaktzeilen, keine Patienten- oder Personendaten):
{
  "woche": "2026-W46",
  "meta":    [{"utm_campaign": "leseprobe", "utm_content": "anzeige-001", "ausgaben_eur": 120.5}],
  "hubspot": [{"utm_source": "meta", "utm_campaign": "leseprobe", "utm_content": "anzeige-001",
               "lead": 40, "mql": 6, "sql": 2, "customer": 0}]
}
„meta“ stammt aus den Werbekonto-Berichten (Ads-MCP oder Insights), „hubspot“ aus Zählabfragen über Kontakte
(Phase erreicht = hs_v2_date_entered_* gesetzt; siehe kontext/bitecentric/hubspot-felder.md). Nur utm_source=meta zählt.
Leitgröße: Gewinnungskosten je Käufer nach Quelle. Richtwerte für die Aussagekraft sind Annahmen (siehe references/auswertung.md).
"""
import collections
import json
import sys
from pathlib import Path

MIN_LEADS_ENTSCHEIDUNG = 30  # Annahme: darunter nur Tendenz


def eur(x):
    return "–" if x is None else f"{x:,.0f} €".replace(",", ".")


def je(ausgaben, n):
    return ausgaben / n if n else None


def auswerten(daten):
    ausg = collections.defaultdict(float)
    for z in daten.get("meta", []):
        ausg[(z["utm_campaign"], z["utm_content"])] += float(z.get("ausgaben_eur", 0))
    zaehl = collections.defaultdict(lambda: dict(lead=0, mql=0, sql=0, customer=0))
    verworfen = 0
    for z in daten.get("hubspot", []):
        if z.get("utm_source") != "meta":
            verworfen += 1
            continue
        k = (z["utm_campaign"], z["utm_content"])
        for f in ("lead", "mql", "sql", "customer"):
            zaehl[k][f] += int(z.get(f, 0))
    zeilen = []
    for k in sorted(set(ausg) | set(zaehl)):
        a, c = ausg.get(k, 0.0), zaehl[k]
        zeilen.append({"campaign": k[0], "content": k[1], "ausgaben": a, **c,
                       "k_lead": je(a, c["lead"]), "k_mql": je(a, c["mql"]), "k_sql": je(a, c["sql"]), "k_kunde": je(a, c["customer"])})
    return zeilen, verworfen


def bericht(daten):
    zeilen, verworfen = auswerten(daten)
    gesamt = {f: sum(z[f] for z in zeilen) for f in ("lead", "mql", "sql", "customer")}
    gesamt_a = sum(z["ausgaben"] for z in zeilen)
    out = [f"# Meta-Auswertung {daten.get('woche', '')} (BiteCentric, Quelle meta)", "",
           "Optimiert wird auf das häufigste Ereignis (Anmeldung Leseprobe/Werkzeug). Qualität kommt aus HubSpot (Lead → MQL → SQL → Customer). Leitgröße: Gewinnungskosten je Käufer.", "",
           "| Kampagne (utm_campaign) | Anzeige | Ausgaben | Lead | MQL | SQL | Käufer | € je Lead | € je MQL | € je SQL | € je Käufer |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for z in zeilen:
        out.append(f"| {z['campaign']} | {z['content']} | {eur(z['ausgaben'])} | {z['lead']} | {z['mql']} | {z['sql']} | {z['customer']} | "
                   f"{eur(z['k_lead'])} | {eur(z['k_mql'])} | {eur(z['k_sql'])} | {eur(z['k_kunde'])} |")
    out.append(f"| **Summe** | | **{eur(gesamt_a)}** | {gesamt['lead']} | {gesamt['mql']} | {gesamt['sql']} | {gesamt['customer']} | "
               f"{eur(je(gesamt_a, gesamt['lead']))} | {eur(je(gesamt_a, gesamt['mql']))} | {eur(je(gesamt_a, gesamt['sql']))} | {eur(je(gesamt_a, gesamt['customer']))} |")
    out += ["", "## Aussagekraft"]
    if gesamt["lead"] < MIN_LEADS_ENTSCHEIDUNG:
        out.append(f"- Nur {gesamt['lead']} Leads: Tendenz, keine Entscheidungsgrundlage (Richtwert ab {MIN_LEADS_ENTSCHEIDUNG}, Annahme). Nichts umstellen.")
    if gesamt["customer"] == 0:
        out.append("- Noch kein Käufer: Qualität über MQL- und SQL-Quote beurteilen, Kosten je Käufer noch nicht berechenbar.")
    if gesamt["lead"]:
        out.append(f"- Quoten: MQL {gesamt['mql'] / gesamt['lead']:.0%} der Leads, SQL {gesamt['sql'] / gesamt['lead']:.0%} der Leads.")
    ohne_ausgaben = [z for z in zeilen if z["ausgaben"] == 0 and z["lead"]]
    if ohne_ausgaben:
        out.append(f"- {len(ohne_ausgaben)} Zeile(n) mit Leads, aber ohne Ausgaben: UTM-Werte in Anzeige und HubSpot prüfen.")
    if verworfen:
        out.append(f"- {verworfen} HubSpot-Zeile(n) mit anderer utm_source ignoriert.")
    out += ["", "## Entscheidungen (höchstens drei, keine täglichen Änderungen wegen der Lernphase)",
            "1. _vom Agenten als Vorschlag ausfüllen, Alexander entscheidet_", "",
            "Neue Anzeigen nur pausiert anlegen; jede Änderung ins Protokoll `daten/meta/protokoll.md`."]
    return "\n".join(out) + "\n"


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    ziel = None
    if "--ausgabe" in args:
        i = args.index("--ausgabe")
        ziel = args[i + 1]
        del args[i:i + 2]
    try:
        daten = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    except Exception as e:
        sys.exit(f"Eingabe nicht lesbar: {e}")
    text = bericht(daten)
    if ziel:
        Path(ziel).parent.mkdir(parents=True, exist_ok=True)
        Path(ziel).write_text(text, encoding="utf-8")
        print(f"geschrieben: {ziel}")
    else:
        print(text)


if __name__ == "__main__":
    main()
