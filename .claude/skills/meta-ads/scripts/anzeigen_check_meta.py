#!/usr/bin/env python3
"""Prüft einen Meta-Kampagnenentwurf (daten/meta/kampagnen/<name>.json) vor dem Compliance-Review.

  anzeigen_check_meta.py <datei.json>
  anzeigen_check_meta.py --text "Ein Satz oder Entwurf"   (nur Ton und Verbotswörter, z. B. für Anregungen im Wochenbericht)

HART = muss behoben werden (Exit-Code 1). WEICH = prüfen und begründen. Nur Standardbibliothek.
Regeln: kontext/bitecentric/*.md, references/aufruf-regeln.json, config/meta.json.
"""
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[4]
REGELN = Path(__file__).resolve().parents[1] / "references/aufruf-regeln.json"
CONFIG = Path(os.environ.get("META_CONFIG") or ROOT / "config/meta.json")  # META_CONFIG nur für Tests

HART_TEXT = [
    (r"master ?class", "„Masterclass“ ist ausgeschlossen."),
    (r"webinar", "„Webinar“ fürs Intro nicht verwenden: „Intro“ oder „Live-Einführung“."),
    (r"garantie|garantier", "Statt Garantie „Zusage“; keine Garantien."),
    (r"\bfunctional", "„Functional …“ ist ausgeschlossen (systemgebundener Begriff der Wettbewerber)."),
    (r"\bscheu(?:-dental| academy)?\b", "Scheu wird nicht genannt (Gesamtkonzept 2; Verhältnis offen)."),
    (r"kieferblick", "Kieferblick ist eine andere Marke und steht nicht in BiteCentric-Anzeigen."),
    (r"fall-?triage|fall einreichen|open case night|strategie-?gespräch|erstgespräch|1:1-?coaching|prüfungsgespräch|fall-?gutschein|blueprint|joint-first|aligner-formel", "Name nach Gesamtkonzept 6.1 nicht verwenden (richtig: Fall-Einschätzung, Fallabend online, Vorgespräch, Einzelbegleitung, Zweitmeinung, Erstfall)."),
    (r"online-?kurs", "„kostenloser Online-Kurs“ passt nicht zum Live-Intro (Gesamtkonzept 6.1): „Intro“."),
    (r"lead[- ]?magnet|upsell|downsell|continuity", "Interne Begriffe nicht nach außen (Gesamtkonzept 6.1)."),
    (r"rabatt|frühbucher|aktionspreis|\baktion\b|sparen sie|\d+\s?%\s?(?:rabatt|günstiger|ersparnis)", "Rabatt-Aufmacher sind ausgeschlossen."),
    (r"nur noch|letzte[nr]? plätze|jetzt sichern|nicht verpassen|begrenzte plätze|bis (?:morgen|heute)|heute noch|letzte chance|zeit läuft|nur (?:heute|diese woche)", "Künstliche Dringlichkeit ist ausgeschlossen."),
    (r"umsatz|umsätze|rendite|zusatzgewinn|mehr einnahmen|einnahmen steigern|verdienen sie|durch die decke|garantiert", "Keine Umsatz-, Ergebnis- oder Renditeversprechen."),
    (r"\bbeste[nrms]?\b|\bführend|\beinzigartig|\bunschlagbar|\bnummer 1\b|\bnr\. ?1\b|\bperfekt|\bgrößte[nrms]?\b|\bschnellste", "Superlativ: sachlich beschreiben."),
    (r"!", "Ausrufezeichen: ruhiger Ton, keine Ausrufe."),
    (r"\bdu\b|\bdich\b|\bdein\w*|\bdir\b", "Sie-Form verwenden, nicht duzen."),
    (r"falsch behandelt|bisher\w* (?:\w+ )?falsch|machen sie (?:diesen|den) fehler|fehler,? die sie|zu unrecht behandelt|schlecht behandelt|schlecht geplant", "Nie andeuten, dass bisherige Behandlungen falsch waren."),
    (r"\bkrass|\bmega\b|wahnsinn|revolution|gamechanger|game changer|geheimnis|das müssen sie|unglaublich|schockierend", "Hype-Ton: kollegial, fallbasiert, ruhig."),
    (r"kurs buchen|jetzt buchen|kurs kaufen|jetzt kaufen|warenkorb|\bbestellen\b", "Nie direkt zu einem bezahlten Kurs."),
    (r"[\w.+-]+@[\w-]+\.[\w.-]+|(?:\+\d{2}|\b0\d{2,4})[\s/-]?\d{3,}", "E-Mail-Adresse oder Telefonnummer im Anzeigentext."),
]
WEICH_TEXT = [
    (r"\bfehler|\bfalsch|versag|scheiter|misserfolg|schiefgelaufen", "Fehler-/Misserfolgswort: „Fehlerfall“ als Falltyp ist ok, nie als Vorwurf an bisherige Behandlungen."),
    (r"\bsie (?:haben|leiden|sind|kämpfen|fühlen sich)\b", "Meta „personal attributes“: keine Zuschreibung persönlicher Eigenschaften oder Zustände."),
    (r"invisalign|align technology|clearcorrect|dentsply|sure ?smile|angel aligner|tipton", "Wettbewerber/Marke: nur sachlich, nie wertend; „systemneutral“ genügt meist."),
    (r"zertifi|fortbildungspunkt|\bpunkte\b|\bcme\b|\bcpd\b", "Qualifikationsangabe: nur mit Beleg (creative_typ „qualifikation“ mit Feld beleg)."),
    (r"basiskurs|curriculum|einzelbegleitung|\b2\.?990|\b4\.?990|\b10\.?990", "Kursname oder Kurspreis im Text: Aufruf bleibt trotzdem die Stufe der Aufrufregel."),
    (r"\bsofort\b|\bschnell\b", "Zeitdruck-Nähe: sachlich bleiben."),
    (r"\bgewinn|\blohnt sich|wirtschaftlich", "Wirtschaftlichkeit: nur als ehrliche Rechnung inkl. Zeit und Risiko, ohne Versprechen."),
    (r"vorher[- ]?nachher", "Vorher-nachher: nur echte Fälle aus Fall-Dossiers, ohne Ergebnisversprechen."),
]
WEICH_TEXT_ORIGINAL = [
    (r"\b(?:Frau|Herr|Patient(?:in)?)\s+[A-ZÄÖÜ][a-zäöü]+", "Mögliche Personen- oder Patientenangabe: keine Namen."),
]
CTA_VERBOTEN = {"SHOP_NOW", "BUY_NOW", "ORDER_NOW", "BOOK_NOW", "GET_OFFER", "GET_QUOTE", "APPLY_NOW"}
CTA_ERLAUBT = {"LEARN_MORE", "DOWNLOAD", "SIGN_UP", "SUBSCRIBE", "WATCH_MORE", "SEE_MORE", "LISTEN_NOW", "CONTACT_US", "NO_BUTTON"}
BILDQUELLE_ERLAUBT = {"fall-dossier", "eigene-aufnahme", "dokument"}
BILDQUELLE_VERBOTEN = {"ki", "ai", "stock", "generiert", "generisch"}


def lade_json(pfad):
    try:
        return json.loads(Path(pfad).read_text(encoding="utf-8"))
    except Exception as e:
        sys.exit(f"Datei nicht lesbar: {pfad}: {e}")


def text_treffer(text):
    """Liefert (hart, weich) für einen Text."""
    low = text.lower()
    hart = [m for rx, m in HART_TEXT if re.search(rx, low)]
    weich = [m for rx, m in WEICH_TEXT if re.search(rx, low)]
    weich += [m for rx, m in WEICH_TEXT_ORIGINAL if re.search(rx, text)]
    return hart, weich


def utm_ok(wert):
    return bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", wert or ""))


def pruefen(k):
    hart, weich = [], []

    def h(ort, t): hart.append(f"{ort}: {t}")
    def w(ort, t): weich.append(f"{ort}: {t}")

    regeln = lade_json(REGELN)
    cfg = lade_json(CONFIG)
    ads_cfg = cfg.get("ads", {})

    # Kampagne
    if k.get("status") not in (None, "PAUSED"):
        h("Kampagne", f"status „{k.get('status')}“: Entwürfe sind immer PAUSED.")
    for feld in ("begruendung", "erwartete_wirkung"):
        if not str(k.get(feld, "")).strip():
            h("Kampagne", f"Feld {feld} fehlt (Pflicht für das Änderungsprotokoll).")
    stufe = k.get("stufe_kontakt")
    stufe_regel = regeln["stufen"].get(stufe)
    if not stufe_regel:
        h("Kampagne", f"stufe_kontakt „{stufe}“ unbekannt (erlaubt: {', '.join(regeln['stufen'])}).")
        erlaubt = []
        budget_key = None
    else:
        erlaubt = stufe_regel["aufrufe"]
        budget_key = stufe_regel["budget_key"]
    if budget_key:
        monat = ads_cfg.get("kampagnen_eur", {}).get(budget_key, 0)
        tag = k.get("tagesbudget_eur")
        if not monat:
            h("Kampagne", f"Kein Monatsbudget für „{budget_key}“ in config/meta.json (Lücke, Alexander trägt es ein).")
        elif tag is None or tag * 30.4 > monat * 1.05:
            h("Kampagne", f"Tagesbudget {tag} € ergibt über {monat} € im Monat (Deckel).")
    if "kunden" not in [str(x).lower() for x in k.get("ausschluesse", [])]:
        h("Kampagne", "Kunden müssen immer ausgeschlossen werden (ausschluesse enthält „kunden“).")
    if not k.get("laender"):
        h("Kampagne", "laender fehlt.")
    zg = k.get("zielgruppe", {})
    if stufe in ("warm", "heiss", "heiss_nicht_erschienen") and not zg.get("custom_audiences"):
        h("Zielgruppe", "Warm/Heiß braucht benutzerdefinierte Zielgruppen (custom_audiences).")
    if stufe in ("kalt", "kalt_fall") and not (zg.get("berufe_oder_interessen") or zg.get("lookalike")):
        w("Zielgruppe", "Keine Berufe/Interessen/Lookalike für die kalte Zielgruppe angegeben.")
    if k.get("optimierungsereignis") != "Lead":
        w("Kampagne", "Optimiert wird auf das häufigste Ereignis (Anmeldung Leseprobe/Werkzeug = „Lead“).")
    if k.get("entscheidung"):
        w("Kampagne", f"Offene Entscheidung: {k['entscheidung']}")

    nummern = []
    anzahl = 0
    for g in k.get("anzeigengruppen", []):
        for a in g.get("anzeigen", []):
            anzahl += 1
            nr = a.get("nr")
            ort = f"Anzeige {nr}"
            nummern.append(nr)
            if a.get("entscheidung"):
                w(ort, f"Offene Entscheidung: {a['entscheidung']}")

            # Aufruf
            haupt, neben = a.get("hauptaufruf"), a.get("nebenaufruf")
            verboten = regeln["verboten_als_aufruf"]
            if not haupt:
                h(ort, "hauptaufruf fehlt.")
            elif haupt in verboten:
                h(ort, f"Hauptaufruf „{haupt}“: nie direkt zu einem bezahlten Kurs.")
            elif haupt not in erlaubt:
                h(ort, f"Hauptaufruf „{haupt}“ passt nicht zu Kontaktstufe „{stufe}“ (erlaubt: {', '.join(erlaubt)}).")
            if neben:
                if neben in verboten:
                    h(ort, f"Nebenaufruf „{neben}“: nie direkt zu einem bezahlten Kurs.")
                elif neben not in erlaubt:
                    h(ort, f"Nebenaufruf „{neben}“ passt nicht zu Kontaktstufe „{stufe}“.")
                elif neben == haupt:
                    h(ort, "Nebenaufruf gleich Hauptaufruf.")
            if a.get("weitere_aufrufe"):
                h(ort, "Höchstens ein Haupt- und ein Nebenaufruf je Anzeige.")

            # Creative
            typ = a.get("creative_typ")
            if typ not in regeln["creative_typen"]:
                h(ort, f"creative_typ „{typ}“ unbekannt (erlaubt: {', '.join(regeln['creative_typen'])}).")
            if typ in ("fall-in-bildern", "gruendergeschichte", "entscheidung-am-fall") and not a.get("fall_dossier"):
                h(ort, "Grundlage sind echte Fälle: Feld fall_dossier (Kennung) fehlt.")
            pflicht = regeln["creative_typen_mit_beleg"].get(typ)
            if pflicht and not a.get(pflicht):
                h(ort, f"creative_typ „{typ}“ braucht das Feld {pflicht}.")
            quelle = str(a.get("bild_quelle", "")).lower()
            if not quelle:
                h(ort, "bild_quelle fehlt (fall-dossier, eigene-aufnahme oder dokument).")
            elif quelle in BILDQUELLE_VERBOTEN:
                h(ort, "Keine generischen KI- oder Stock-Bilder von Menschen oder Zähnen.")
            elif quelle not in BILDQUELLE_ERLAUBT:
                w(ort, f"bild_quelle „{quelle}\" unbekannt (erlaubt: {', '.join(sorted(BILDQUELLE_ERLAUBT))}).")

            # Texte
            for feld, grenze in (("primaerer_text", 300), ("titel", 40), ("beschreibung", 30)):
                t = a.get(feld) or ""
                if feld == "primaerer_text" and not t.strip():
                    h(ort, "primaerer_text fehlt.")
                if len(t) > grenze:
                    w(ort, f"{feld} hat {len(t)} Zeichen (Richtwert {grenze}, Meta kürzt in der Anzeige).")
                th, tw = text_treffer(t)
                for m in th: h(f"{ort} {feld}", m)
                for m in tw: w(f"{ort} {feld}", m)
            if typ != "qualifikation" and re.search(r"zertifi|fortbildungspunkt", " ".join(str(a.get(x, "")) for x in ("primaerer_text", "titel", "beschreibung")).lower()):
                w(ort, "Qualifikation im Text, aber creative_typ ist nicht „qualifikation“.")

            # Button
            cta = a.get("cta_button")
            if cta in CTA_VERBOTEN:
                h(ort, f"Button „{cta}“ führt in Richtung Kauf/Buchung.")
            elif cta and cta not in CTA_ERLAUBT:
                w(ort, f"Button „{cta}“ unbekannt (üblich: LEARN_MORE, DOWNLOAD, SIGN_UP).")

            # Link und UTM
            link = a.get("link", "")
            u = urlparse(link)
            if u.scheme != "https":
                h(ort, "Link muss https sein.")
            domains = ads_cfg.get("erlaubte_domains", [])
            host = (u.hostname or "").lower()
            if not any(host == d or host.endswith("." + d) for d in domains):
                h(ort, f"Link-Domain „{host}“ nicht in erlaubte_domains ({', '.join(domains)}).")
            if re.search(r"basiskurs|curriculum|einzelbegleitung|checkout|kaufen|buchen|warenkorb", u.path.lower()):
                h(ort, "Link führt direkt auf einen bezahlten Kurs/Kauf.")
            q = {key: v[0] for key, v in parse_qs(u.query).items()}
            utm = a.get("utm", {})
            for key in ("utm_source", "utm_medium", "utm_campaign", "utm_content"):
                wert = q.get(key)
                if wert is None:
                    h(ort, f"{key} fehlt im Link.")
                    continue
                if utm.get(key) not in (None, wert):
                    h(ort, f"{key} im Link („{wert}“) weicht von utm ab („{utm.get(key)}“).")
                if not utm_ok(wert):
                    h(ort, f"{key} „{wert}“: nur klein, Bindestriche, ohne Umlaute und Sonderzeichen.")
            if q.get("utm_source") not in (None, regeln["utm_source_meta"]):
                h(ort, f"utm_source muss „{regeln['utm_source_meta']}“ sein.")
            if q.get("utm_medium") not in (None, regeln["utm_medium_meta"]):
                h(ort, f"utm_medium muss „{regeln['utm_medium_meta']}“ sein.")
            camp = q.get("utm_campaign")
            if camp is not None:
                if not re.fullmatch(regeln["utm_campaign_erlaubt_regex"], camp):
                    h(ort, f"utm_campaign „{camp}“ nicht in der UTM-Konvention.")
                soll = regeln["utm_campaign_zu_aufruf"].get(haupt, haupt)
                if haupt and camp != soll:
                    h(ort, f"utm_campaign „{camp}“ passt nicht zum Hauptaufruf „{haupt}“ (erwartet „{soll}“).")
            inhalt = q.get("utm_content")
            if inhalt is not None:
                if not re.fullmatch(regeln["utm_content_anzeige_regex"], inhalt):
                    h(ort, f"utm_content „{inhalt}“: für Meta-Anzeigen „anzeige-<nr>“.")
                elif nr is not None and int(inhalt.split("-")[1]) != int(nr):
                    h(ort, f"utm_content „{inhalt}“ passt nicht zur Anzeigennummer {nr}.")
    if anzahl == 0:
        h("Kampagne", "Keine Anzeigen vorhanden.")
    if len(nummern) != len(set(nummern)):
        h("Kampagne", "Anzeigennummern (nr) sind nicht eindeutig.")
    return hart, weich


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--text":
        hart, weich = text_treffer(" ".join(sys.argv[2:]))
        hart = [f"Text: {m}" for m in hart]
        weich = [f"Text: {m}" for m in weich]
    elif len(sys.argv) == 2:
        hart, weich = pruefen(lade_json(sys.argv[1]))
    else:
        sys.exit(__doc__)
    for z in hart:
        print("HART  ", z)
    for z in weich:
        print("WEICH ", z)
    if hart:
        print(f"FEHLER ({len(hart)} hart, {len(weich)} weich)")
        sys.exit(1)
    print(f"OK ({len(hart)} hart, {len(weich)} weich)")


if __name__ == "__main__":
    main()
