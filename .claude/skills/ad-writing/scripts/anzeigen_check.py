#!/usr/bin/env python3
"""Prüft eine Kampagnendatei (daten/ads/kampagnen/<kampagne>.json) vor dem Compliance-Review.

  anzeigen_check.py <datei.json>

HART = muss behoben werden (Exit-Code 1). WEICH = prüfen und begründen. Nur Standardbibliothek.
Regeln: references/google.md, references/hwg-anzeigen.md, kontext/google-ads-strategie.md.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OBERGRENZEN = Path(__file__).resolve().parents[1] / "references/obergrenzen.json"
BUDGET = ROOT / "config/budget.json"

MAX_UEB, MAX_BES, MAX_PFAD = 30, 90, 15
HART_TEXT = [
    (r"garantier|\bgarantie", "Statt Garantie „Zusage“."),
    (r"\brabatt|\baktion\b|\bschnäppchen|\bgratis-?angebot", "Rabatt/Aktion ist ausgeschlossen."),
    (r"nur noch heute|\bjetzt sofort|\bletzte[nr]? plätze|nur für kurze zeit|\bbegrenzt(?:e|es)? angebot|\bsolange der vorrat", "Dringlichkeit ist ausgeschlossen (Knappheit nur als echte Terminplätze, ohne Druck)."),
    (r"\b(?:der|die|das|den|dem) beste[nrms]?\b|\bbeste[nrms]?\b|\bperfekt|\bluxus|\bschmerzfrei|\bohne risiko\b|\bunschlagbar|\bnummer 1\b|\bnr\. ?1\b|\btestsieger|\bbestpreis|\bführend", "Superlativ/Werbeversprechen: sachlich beschreiben."),
    (r"\bheilt\b|\bbeseitigt\b|\bstoppt\b|\bverhindert garantiert|\bnie wieder\b|\bfür immer\b", "Heil-/Ergebnisversprechen."),
    (r"\bunsichtbar", "„unsichtbar“ steht nicht in unserer Wortwelt (nur als Suchbegriff): „diskret“."),
    (r"traumlächeln|hollywood|traumzähne", "Nicht unsere Wortwelt."),
    (r"vorher[- ]?nachher|vorher/nachher", "Vorher-nachher nicht in Anzeigen."),
    (r"kieferorthop[äa]d|fachzahnarzt|\bfachzahnärztin", "Berufsbezeichnung: Alexander ist Zahnarzt, nicht Fachzahnarzt für Kieferorthopädie."),
    (r"invisalign|clearcorrect|smileunion|drsmile|dr\. ?smile|ilovemysmile|smile club", "Fremdmarke nicht im Anzeigentext (nur als Keyword)."),
]
WEICH_TEXT = [
    (r"\bkostenlos|\bgratis\b|kostenfrei", "„kostenlos“: Preisbezug in Anzeigen ist eine offene Entscheidung von Alexander."),
    (r"\d[\d.,]*\s?(?:€|euro)|\bab ca\.", "Preisangabe: nur nach Freigabe (Intro-Offers, Aligner „ab ca. 3.900 €“)."),
    (r"\bexperte|\bexpertin|\bspezialist|\bspezialisiert", "Selbstzuschreibung: nur mit Beleg (Berufsrecht)."),
    (r"★|\bsterne\b|bewertung|note 1|\d,\d\s?(?:von 5|sterne)", "Bewertungsangabe: nur mit echten Zahlen aus dem Google-Profil."),
    (r"termine? (?:innerhalb|in) \d|innerhalb von \d+ (?:stunden|tag)|\bsofort\b", "Fristzusage: nur belegte Zusagen."),
    (r"\bbester? preis|\bgünstig(?:ste[nrms]?)?\b|\bpreiswert", "Preisversprechen: Kieferblick positioniert sich nicht über den Preis."),
]


def lade(pfad):
    try:
        return json.loads(Path(pfad).read_text(encoding="utf-8"))
    except Exception as e:
        sys.exit(f"Datei nicht lesbar: {e}")


def pruefen(k):
    hart, weich = [], []

    def h(ort, text): hart.append(f"{ort}: {text}")
    def w(ort, text): weich.append(f"{ort}: {text}")

    # Kampagne: Budget und Gebot
    budget = json.loads(BUDGET.read_text(encoding="utf-8"))
    grenzen = json.loads(OBERGRENZEN.read_text(encoding="utf-8"))
    key = k.get("budget_key")
    monat = budget.get("google_kampagnen_eur", {}).get(key)
    if monat is None:
        h("Kampagne", f"budget_key „{key}“ fehlt in config/budget.json (google_kampagnen_eur).")
    elif k.get("tagesbudget_eur") is None or k["tagesbudget_eur"] * 30.4 > monat * 1.05:
        h("Kampagne", f"Tagesbudget {k.get('tagesbudget_eur')} € ergibt über {monat} € im Monat (Deckel).")
    grenze = grenzen.get(key, {}).get("max_cpc_eur")
    if grenze is None:
        h("Kampagne", f"Keine Gebotsobergrenze für „{key}“ in references/obergrenzen.json.")
    elif k.get("max_cpc_eur") is None or k["max_cpc_eur"] > grenze:
        h("Kampagne", f"Max. Klickpreis {k.get('max_cpc_eur')} € über Obergrenze {grenze} €.")
    if not k.get("negativ"):
        h("Kampagne", "Negativliste fehlt.")
    if not k.get("standorte"):
        w("Kampagne", "Standorte nicht angegeben (für die Einstellungsdatei).")

    # Gruppen
    if not k.get("gruppen"):
        h("Kampagne", "Keine Anzeigengruppen.")
    for g in k.get("gruppen", []):
        gn = f"Gruppe „{g.get('name')}“"
        kws = g.get("keywords", [])
        if not 4 <= len(kws) <= 20:
            w(gn, f"{len(kws)} Keyword-Zeilen (Richtwert 4–10 Keywords, je Exact und Phrase bis 20 Zeilen).")
        for kw in kws:
            if kw.get("match") not in ("exact", "phrase"):
                h(gn, f"Keyword „{kw.get('text')}“ mit Match-Typ „{kw.get('match')}“ (nur exact/phrase, kein Broad).")
            if re.search(r"kieferorthop", kw.get("text", ""), re.I) and "kfo-test" not in g.get("name", "").lower() and "kfo" not in g.get("name", "").lower():
                w(gn, "Keyword mit „kieferorthop…“ gehört in die KFO-Testgruppe.")
        if not g.get("landingpage", "").startswith("https://kieferblick.de/"):
            h(gn, "Landingpage fehlt oder nicht auf kieferblick.de (https).")
        if not g.get("anzeigen"):
            h(gn, "Keine Anzeige.")
        for a in g.get("anzeigen", []):
            an = f"{gn}, Anzeige {a.get('variante', '?')}"
            ueb, bes = a.get("ueberschriften", []), a.get("beschreibungen", [])
            if not 3 <= len(ueb) <= 15:
                h(an, f"{len(ueb)} Überschriften (3–15).")
            elif len(ueb) < 10:
                w(an, f"{len(ueb)} Überschriften (Ziel 10–15 für die Anzeigenstärke).")
            if not 2 <= len(bes) <= 4:
                h(an, f"{len(bes)} Beschreibungen (2–4).")
            elif len(bes) < 4:
                w(an, f"{len(bes)} Beschreibungen (Ziel 4).")
            for i, t in enumerate(ueb, 1):
                if len(t) > MAX_UEB: h(an, f"Überschrift {i} hat {len(t)} Zeichen (höchstens {MAX_UEB}): „{t}“")
            for i, t in enumerate(bes, 1):
                if len(t) > MAX_BES: h(an, f"Beschreibung {i} hat {len(t)} Zeichen (höchstens {MAX_BES}): „{t[:40]}…“")
            for p in ("pfad1", "pfad2"):
                if len(a.get(p, "") or "") > MAX_PFAD: h(an, f"{p} hat mehr als {MAX_PFAD} Zeichen.")
            alle = ueb + bes
            norm = [re.sub(r"\W+", " ", t.lower()).strip() for t in alle]
            if len(set(norm)) != len(norm):
                h(an, "Doppelte Texte (Überschriften und Beschreibungen müssen verschieden sein).")
            for t in alle:
                if "!" in t: h(an, f"Ausrufezeichen: „{t}“")
                if re.search(r"\b[A-ZÄÖÜ]{4,}\b", t): w(an, f"Großschreibung zur Betonung: „{t}“")
                if re.search(r"\+?\d[\d /-]{7,}\d", t): h(an, f"Telefonnummer im Text (Anruferweiterung nutzen): „{t}“")
                for muster, hinweis in HART_TEXT:
                    if g.get("marke_im_text_ok") and "Fremdmarke" in hinweis: continue
                    for m in re.finditer(muster, t, re.I):
                        h(an, f"„{m.group(0)}“ in „{t}“ – {hinweis}")
                for muster, hinweis in WEICH_TEXT:
                    for m in re.finditer(muster, t, re.I):
                        w(an, f"„{m.group(0)}“ in „{t}“ – {hinweis}")
            begr = [b.lower() for b in g.get("thema_begriffe", [])]
            if ueb and begr and not any(b in ueb[0].lower() for b in begr):
                h(an, f"Überschrift 1 („{ueb[0]}“) enthält keinen Themabegriff {begr} (wird auf Position 1 fixiert).")
            if not begr:
                w(gn, "thema_begriffe fehlen.")
            if a.get("entscheidung"):
                w(an, f"Offene Entscheidung: {a['entscheidung']}")
    return hart, weich


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    k = lade(sys.argv[1])
    hart, weich = pruefen(k)
    print(f"Anzeigen-Check „{k.get('kampagne')}“: {'OK' if not hart else 'PRÜFEN'} ({len(hart)} hart, {len(weich)} weich)")
    for z in hart: print("HART  ", z)
    for z in weich: print("WEICH ", z)
    sys.exit(1 if hart else 0)


if __name__ == "__main__":
    main()
