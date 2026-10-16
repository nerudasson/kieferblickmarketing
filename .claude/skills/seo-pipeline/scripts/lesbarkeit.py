#!/usr/bin/env python3
"""Prüft einen Artikel-Entwurf (Markdown) auf Lesbarkeit und Formatmix.

Aufruf: python3 lesbarkeit.py daten/entwuerfe/<slug>.md [weitere.md ...]
Exit-Code 1, wenn eine Hürde gerissen wird (Schleife im Writer: überarbeiten).

Lesbarkeit: Flesch-Index nach Amstad (deutsch) = 180 - ASL - 58,5 * ASW
ASL = Wörter pro Satz, ASW = Silben pro Wort. Silben werden über Vokalgruppen
geschätzt, Abweichung etwa +-3 Punkte. Gezählt wird nur Fließtext, Listen und
Fragen/Antworten. Frontmatter, Tabellen, Quellen und Platzhalter zählen nicht.
"""
import re
import sys

MIN_FLESCH = 60
MAX_SATZ_WOERTER = 25        # einzelner Satz
MAX_ASL = 14                 # Durchschnitt
MAX_ABSATZ_SAETZE = 3
MAX_FLIESS_ABSCHNITT = 2     # aufeinanderfolgende Absätze ohne Liste/Tabelle/Box
MAX_FLIESS_ANTEIL = 0.5      # Anteil der Wörter in reinen Fließtext-Absätzen
MAX_QUELLEN = 6
MAX_KLAMMERN_ABSATZ = 1      # Quellenklammern [n] (Gruppen wie [7][8] zählen einmal) pro Absatz
ERLAUBTE_PREISE = {19, 149, 299, 300, 399, 799, 3900}   # Einstiegsleiter, Intro-Offers, Aligner-ab-Preis
STUDIENSPRACHE = r"meta-?analyse|cochrane|übersichtsarbeit|verzerrungsrisiko|randomisiert|stichprobe|lebensjahrzehnt|je nach studie|studienlage|evidenz|signifikant|systematische[nr]? übersicht|kohortenstudie"
MIN_H2 = 4
MAX_BOXEN = 2                # Merksaetze/Hinweise pro Artikel
RICHTWERT_WOERTER = {"info": 1000, "kosten": 1400, "vergleich": 1400, "transaktional": 1400}


def silben(wort):
    return max(1, len(re.findall(r"[aeiouyäöü]+", wort.lower())))


def zerlegen(md):
    md = re.sub(r"^---\n.*?\n---\n", "", md, flags=re.S)
    md = re.split(r"^##\s+Quellen\b", md, flags=re.M)[0]
    md = re.sub(r"\[FAKT FEHLT:[^\]]*\]", "", md)
    return md


def pruefe(pfad):
    roh = open(pfad, encoding="utf-8").read()
    fm = re.match(r"^---\n(.*?)\n---\n", roh, flags=re.S)
    fm = fm.group(1) if fm else ""
    md = zerlegen(roh)
    roh_body = re.split(r"^##\s+Quellen\b", re.sub(r"^---\n.*?\n---\n", "", roh, flags=re.S), flags=re.M)[0]
    zeilen = md.split("\n")

    bloecke = []   # (typ, text)
    puffer = []

    faq_zustand = {"faq": False}

    def flush():
        if puffer:
            bloecke.append(("f" if faq_zustand["faq"] else "p", " ".join(puffer).strip()))
            puffer.clear()

    for z in zeilen:
        s = z.strip()
        if not s:
            flush()
        elif s.startswith("#"):
            flush()
            if s.startswith("## "):
                faq_zustand["faq"] = bool(re.match(r"##\s+(Häufige Fragen|FAQ)", s))
            bloecke.append(("h", s))
        elif s.startswith("|"):
            flush()
            if not bloecke or bloecke[-1][0] != "t":
                bloecke.append(("t", s))
        elif re.match(r"^([-*]|\d+\.)\s", s):
            flush()
            bloecke.append(("l", re.sub(r"^([-*]|\d+\.)\s+", "", s)))
        elif s.startswith(">"):
            flush()
            bloecke.append(("b", s.lstrip("> ").strip()))
        else:
            puffer.append(s)
    flush()

    def sauber(t):
        t = re.sub(r"\[\d+(?:[,–-]\s*\d+)*\]", "", t)       # Fußnoten [1]
        t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)         # Links
        t = re.sub(r"[*_`]", "", t)
        t = re.sub(r"^(Merksatz|CTA|Tipp):\s*", "", t)
        return t.strip()

    saetze = []
    for typ, t in bloecke:
        if typ in ("p", "l", "b", "f"):
            t = sauber(t)
            for s in re.split(r"(?<=[.!?])\s+", t):
                if len(re.findall(r"[A-Za-zÄÖÜäöüß]+", s)) >= 1:
                    saetze.append(s)
        elif typ == "h" and re.match(r"^###\s", t):
            pass  # Fragen in der FAQ sind Überschriften, zählen nicht

    woerter = [w for s in saetze for w in re.findall(r"[A-Za-zÄÖÜäöüß]+", s)]
    if not saetze or not woerter:
        print(f"{pfad}: kein Text gefunden")
        return False
    asl = len(woerter) / len(saetze)
    asw = sum(silben(w) for w in woerter) / len(woerter)
    fre = 180 - asl - 58.5 * asw
    lang = [s for s in saetze if len(s.split()) > MAX_SATZ_WOERTER]

    absaetze = [(sauber(t)) for typ, t in bloecke if typ in ("p", "f")]
    lange_abs = [a for a in absaetze
                 if len([x for x in re.split(r"(?<=[.!?])\s+", a) if x]) > MAX_ABSATZ_SAETZE]

    # Fließtext-Wüsten: viele Absätze in Folge ohne Liste, Tabelle, Box oder Überschrift
    lauf = maxlauf = 0
    for typ, _ in bloecke:
        if typ == "p":
            lauf += 1
            maxlauf = max(maxlauf, lauf)
        else:
            lauf = 0

    h2 = sum(1 for typ, t in bloecke if typ == "h" and re.match(r"^##\s", t))
    hat = {
        "kurz": "kurz:" in fm,
        "merksatz": any(typ == "b" and t.lower().startswith("merksatz") for typ, t in bloecke),
        "liste": any(typ == "l" for typ, _ in bloecke),
        "tabelle": any(typ == "t" for typ, _ in bloecke),
        "faq": any(typ == "h" and re.match(r"^###\s", t) for typ, t in bloecke),
        "cta": any(typ == "b" and t.lower().startswith("cta") for typ, t in bloecke),
    }
    hat["praxis"] = bool(re.search(r"^>\s*Praxis:", roh_body, flags=re.M))
    hat["zusage"] = bool(re.search(r"^>\s*Zusage:", roh_body, flags=re.M))
    hat["weiterlesen"] = bool(re.search(r"^##\s+Weiterlesen", roh_body, flags=re.M))
    boxen = sum(1 for typ, t in bloecke if typ == "b" and t.lower().startswith(("merksatz", "tipp", "hinweis")))
    # Pflichtbausteine: Kurzfassung, Merksatz, Liste, FAQ, CTA. Tabelle nur bei Vergleich/Kosten.
    fehlt = [k for k in ("kurz", "merksatz", "liste", "faq", "cta", "praxis", "zusage", "weiterlesen") if not hat[k]]
    intent = re.search(r"^intent:\s*(\S+)", fm, flags=re.M)
    intent = intent.group(1).lower() if intent else ""
    if intent in ("kosten", "vergleich", "transaktional") and not hat["tabelle"]:
        fehlt.append("tabelle")

    # Quellen, Klammern, Studiensprache, Fließtext-Anteil, Preise
    quellen_teil = re.split(r"^##\s+Quellen\b", re.sub(r"^---\n.*?\n---\n", "", roh, flags=re.S), flags=re.M)
    n_quellen = len(re.findall(r"^\d+\.\s", quellen_teil[1], flags=re.M)) if len(quellen_teil) > 1 else 0
    viele_klammern = [t for typ, t in bloecke if typ == "p" and len(re.findall(r"(?:\[\d+\])+", t)) > MAX_KLAMMERN_ABSATZ]
    text_ohne_quellen = " ".join(sauber(t) for typ, t in bloecke if typ in ("p", "l", "b", "f"))
    studien = sorted(set(m.group(0).lower() for m in re.finditer(STUDIENSPRACHE, text_ohne_quellen, flags=re.I)))
    n_leitl = len(re.findall(r"leitlinie", text_ohne_quellen, flags=re.I))
    def anzahl(typen):
        return sum(len(re.findall(r"[A-Za-zÄÖÜäöüß]+", sauber(t))) for typ, t in bloecke if typ in typen)
    w_fliess, w_alle = anzahl(("p",)), max(1, anzahl(("p", "l", "b", "f")))
    anteil = w_fliess / w_alle
    preis_probleme = []
    for sa in re.split(r"(?<=[.!?])\s+", " ".join(t for typ, t in bloecke if typ in ("p", "l", "b", "f"))):
        if re.search(r"\[\d+\]", sa):
            continue  # Preise mit Quellenangabe (Marktpreise) sind erlaubt
        for m in re.finditer(r"(\d{1,3}(?:\.\d{3})*|\d+)\s?€", sa):
            wert = int(m.group(1).replace(".", ""))
            if wert not in ERLAUBTE_PREISE:
                preis_probleme.append(m.group(0))

    n_datenlage = len(re.findall(r"datenlage|studienlage|beweislage", text_ohne_quellen, flags=re.I))
    absolut = sorted(set(m.group(0).lower() for m in re.finditer(r"\b(immer|nie|niemals|garantiert|sicher|ein leben lang|bei jedem|jeder)\b", text_ohne_quellen, flags=re.I)))
    n_luecken = len(re.findall(r"FAKT FEHLT", roh_body))

    fk = re.search(r"^fokus_keyword:\s*\"?([^\"\n]+)", fm, flags=re.M)
    seo_probleme = []
    if fk:
        fkw = fk.group(1).strip().lower()
        stamm = [w[:6] for w in fkw.split() if len(w) > 3]
        def hat_phrase(t):
            t = t.lower()
            return fkw in t or all(x in t for x in stamm)
        titel = re.search(r"^title:\s*\"?([^\"\n]+)", fm, flags=re.M)
        seo_t = re.search(r"^seo_titel:\s*\"?([^\"\n]+)", fm, flags=re.M)
        meta = re.search(r"^meta_description:\s*\"?([^\"\n]+)", fm, flags=re.M)
        h2s = [t for typ, t in bloecke if typ == "h" and t.startswith("## ")]
        erste100 = " ".join(" ".join(sauber(t) for typ, t in bloecke if typ in ("p", "l", "f")).split()[:100])
        if titel and not hat_phrase(titel.group(1)): seo_probleme.append("Hauptphrase fehlt im Titel")
        if seo_t and (len(seo_t.group(1)) > 60 or not hat_phrase(seo_t.group(1))): seo_probleme.append("seo_titel: über 60 Zeichen oder ohne Hauptphrase")
        if not seo_t: seo_probleme.append("seo_titel fehlt")
        if meta and not (110 <= len(meta.group(1)) <= 160 and hat_phrase(meta.group(1))): seo_probleme.append("meta_description: Länge 120–155 oder Hauptphrase fehlt")
        if not meta: seo_probleme.append("meta_description fehlt")
        if not hat_phrase(erste100): seo_probleme.append("Hauptphrase fehlt in den ersten 100 Wörtern")
        if not any(hat_phrase(h) for h in h2s): seo_probleme.append("Hauptphrase in keiner H2")
    else:
        seo_probleme.append("fokus_keyword fehlt im Frontmatter")
    if not re.search(r"^kategorie:\s*\S+", fm, flags=re.M): seo_probleme.append("kategorie fehlt im Frontmatter")

    probleme = []
    probleme += ["SEO: " + x for x in seo_probleme]
    if n_datenlage > 1:
        probleme.append(f"„Datenlage/Studienlage“ {n_datenlage}x: höchstens einmal, sonst „das weiß man noch nicht sicher“ oder weglassen")
    if n_quellen > MAX_QUELLEN:
        probleme.append(f"{n_quellen} Quellen (max. {MAX_QUELLEN}): nur die stärkste je Aussage")
    if viele_klammern:
        probleme.append(f"{len(viele_klammern)} Absatz/Absätze mit mehr als {MAX_KLAMMERN_ABSATZ} Quellenklammer")
    if studien or n_leitl > 1:
        probleme.append("Studiensprache im Text: " + ", ".join(studien + (["leitlinie x%d" % n_leitl] if n_leitl > 1 else [])))
    if anteil > MAX_FLIESS_ANTEIL:
        probleme.append(f"Fließtext-Anteil {anteil:.0%} (max. {MAX_FLIESS_ANTEIL:.0%}): mehr Liste, Tabelle, Merksatz")
    if preis_probleme:
        probleme.append("Preis nicht erlaubt (nur Intro-Offers, Aligner-ab-Preis, Einstiegsleiter): " + ", ".join(sorted(set(preis_probleme))))
    if fre < MIN_FLESCH:
        probleme.append(f"Lesbarkeit {fre:.0f} < {MIN_FLESCH}")
    if asl > MAX_ASL:
        probleme.append(f"Ø Satzlänge {asl:.1f} > {MAX_ASL} Wörter")
    if lang:
        probleme.append(f"{len(lang)} Satz/Sätze über {MAX_SATZ_WOERTER} Wörter, z. B. „{' '.join(lang[0].split()[:8])} …“")
    if lange_abs:
        probleme.append(f"{len(lange_abs)} Absatz/Absätze mit mehr als {MAX_ABSATZ_SAETZE} Sätzen")
    if maxlauf > MAX_FLIESS_ABSCHNITT:
        probleme.append(f"{maxlauf} Absätze in Folge ohne Liste, Tabelle oder Merksatz")
    if boxen > MAX_BOXEN:
        probleme.append(f"{boxen} Merksaetze/Hinweise (max. {MAX_BOXEN})")
    if re.search(r"^##\s+Fazit\b", roh_body, flags=re.M):
        probleme.append("Schlussueberschrift „Fazit“ statt „Was heißt das für Sie?“")
    if h2 < MIN_H2:
        probleme.append(f"nur {h2} H2-Abschnitte (min. {MIN_H2})")
    if fehlt:
        probleme.append("Bausteine fehlen: " + ", ".join(fehlt))

    hinweise = []
    grenze = RICHTWERT_WOERTER.get(intent, RICHTWERT_WOERTER["info"])
    if len(woerter) > grenze * 1.15:
        hinweise.append(f"{len(woerter)} Woerter, Richtwert {grenze}: Nebenfragen als eigenen Artikel auslagern?")
    print(f"{pfad}")
    print(f"  Wörter {len(woerter)} · Sätze {len(saetze)} · Ø {asl:.1f} Wörter/Satz · "
          f"{asw:.2f} Silben/Wort · Lesbarkeit {fre:.0f}")
    print("  Bausteine: " + " ".join(f"{k}={'ja' if v else 'nein'}" for k, v in hat.items())
          + f" · H2={h2}")
    if absolut:
        hinweise.append("Absolutwörter prüfen, ob die Quelle sie trägt: " + ", ".join(absolut))
    if n_luecken:
        hinweise.append(f"{n_luecken} [FAKT FEHLT]-Stelle(n): Entwurf ist nicht veröffentlichungsfähig, nicht nach WordPress")
    for h in hinweise:
        print("  HINWEIS (kein Fehler): " + h)
    if probleme:
        print("  PRÜFEN:")
        for p in probleme:
            print("   - " + p)
    else:
        print("  OK")
    return not probleme


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    ok = all([pruefe(p) for p in sys.argv[1:]])
    sys.exit(0 if ok else 1)
