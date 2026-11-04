#!/usr/bin/env python3
"""Konkurrenz-Monitor BiteCentric: Meta Ad Library API (ads_archive), nur Standardbibliothek.

  adlib.py seiten    [--dry-run]   Seiten-IDs der Wettbewerber suchen -> seiten-vorschlag.md (trägt NICHTS ein)
  adlib.py snapshot  [--dry-run]   Anzeigen abfragen (DE, AT, GB), Rohdaten und Anzeigen-Log fortschreiben
  adlib.py report                  Wochenbericht aus Rohdaten und Log (höchstens eine Seite)

--dry-run: kein Netzwerk, kein Token nötig; zeigt Abfrageplan und Obergrenzen.
Echtlauf nur, wenn config/meta.json adlib.echtlauf_freigegeben = true UND META_ADLIB_ACCESS_TOKEN gesetzt ist.
Der Token steht nie in Dateien oder Ausgaben; ad_snapshot_url enthält ihn laut Doku und wird vor dem Speichern bereinigt.
Test-Optionen: --fixture <datei.json> (Antworten aus Datei statt Netzwerk), Umgebungsvariable META_WETTBEWERB_DIR (anderer Ausgabeordner).
"""
import argparse
import collections
import csv
import datetime
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SKILL = Path(__file__).resolve().parents[1]
CONFIG = Path(os.environ.get("META_CONFIG") or ROOT / "config/meta.json")
OUT = Path(os.environ.get("META_WETTBEWERB_DIR") or ROOT / "daten/meta/wettbewerb")
LOG = OUT / "anzeigen-log.csv"

SPALTEN = ["bibliotheks_id", "werbetreibender", "land", "start", "ende", "varianten", "angebot", "aufruf", "format",
           "aufhaenger", "ton", "eu_zielgruppe", "eu_reichweite", "link", "zuerst_gesehen",
           "stufe", "b2b", "reichweite_hinweis", "textauszug", "quelle", "zuletzt_gesehen"]
# Spalten, die der Agent beim Bericht ausfüllt und die das Skript nie überschreibt
MANUELL = ("angebot", "aufruf", "aufhaenger", "ton")

FELDER_BASIS = ("id,page_id,page_name,ad_creation_time,ad_delivery_start_time,ad_delivery_stop_time,ad_creative_bodies,"
                "ad_creative_link_titles,ad_creative_link_captions,ad_creative_link_descriptions,ad_snapshot_url,"
                "languages,publisher_platforms,total_reach_by_location")
FELDER_ERWEITERT = FELDER_BASIS + ",eu_total_reach,target_ages,target_gender,target_locations,beneficiary_payers"

B2B = re.compile(r"zahnärzte\b|zahnärztinnen|kolleg|fortbildung|\bkurs|curriculum|webinar|seminar|praxisinhaber|praxisübernahme|zertifi|\bcme\b|\bcpd\b|"
                 r"dentists\b|course|mentoring|diploma|masterclass|clinician|practice owner|\bgdp\b|hands-on|fallplanung|clincheck|workshop|"
                 r"referent|dozent|anwender|aligner-rechner|rendite", re.I)
B2B_SEITENNAME = re.compile(r"akademie|academy|training|fortbildung|institute|seminar|cephtactics", re.I)
PATIENT = re.compile(r"ihr lächeln|ihre zähne|schönes lächeln|lächeln verdien|termin (?:vereinbaren|buchen)|kostenlose beratung|zahnreinigung|bleaching|"
                     r"your smile|straighter teeth|book (?:a|your) (?:free )?(?:consultation|appointment)|teeth whitening|smile makeover|"
                     r"unsichtbare zahnspange für|zahnspange für sie", re.I)


# ---------------------------------------------------------------- Konfiguration
def laden(pfad):
    try:
        return json.loads(Path(pfad).read_text(encoding="utf-8"))
    except Exception as e:
        sys.exit(f"Datei nicht lesbar: {pfad}: {e}")


def konfig():
    cfg = laden(CONFIG)
    return cfg, laden(SKILL / "references/wettbewerber.json"), laden(SKILL / "references/suchbegriffe.json")


def heute():
    return os.environ.get("META_HEUTE") or datetime.date.today().isoformat()  # META_HEUTE nur für Tests


# ---------------------------------------------------------------- Plan
def chunks(liste, n):
    for i in range(0, len(liste), n):
        yield liste[i:i + n]


def plan_snapshot(cfg, wb, sb):
    calls = []
    for land in cfg["adlib"]["laender"]:
        ids = sorted({str(i) for w in wb["wettbewerber"] if land in w["laender"] and w.get("seiten_ids_bestaetigt") for i in w["seiten_ids"]})
        for blk in chunks(ids, 10):
            calls.append({"art": "seiten", "land": land, "ids": blk})
        for t in sb[sb["gruppe_je_land"][land]]:
            calls.append({"art": "suche", "land": land, "begriff": t})
    return calls


def plan_seiten(wb):
    return [w for w in wb["wettbewerber"] if not w.get("seiten_ids_bestaetigt")]


def plan_ausgeben(titel, anzahl, cfg, extra=""):
    a = cfg["adlib"]
    print(f"{titel}: {anzahl} Abfragen{extra}. Obergrenze max_aufrufe {a['max_aufrufe']}, bis zu {a['max_seiten_je_abfrage']} Seiten je Abfrage.")


# ---------------------------------------------------------------- API
class ApiStopp(Exception):
    pass


def bereinige_url(u):
    """Entfernt access_token aus URLs (ad_snapshot_url enthält ihn laut Doku)."""
    if not u:
        return u
    p = urllib.parse.urlsplit(u)
    q = [(k, v) for k, v in urllib.parse.parse_qsl(p.query) if k.lower() != "access_token"]
    return urllib.parse.urlunsplit((p.scheme, p.netloc, p.path, urllib.parse.urlencode(q), ""))


class Client:
    def __init__(self, cfg, token, fixture=None):
        self.cfg, self.token, self.fixture = cfg, token, fixture
        self.n = 0
        self.erweitert = True
        self.max = cfg["adlib"]["max_aufrufe"]

    def abfrage(self, land, extra, video=False, nach=None):
        a = self.cfg["adlib"]
        if self.fixture is not None:
            antwort = self.fixture.get(f"{land}|video" if video else land, {"data": []})
            self.n += 1
            return antwort
        if self.n >= self.max:
            raise ApiStopp(f"max_aufrufe ({self.max}) erreicht")
        params = {"ad_reached_countries": json.dumps([land]), "ad_type": "ALL", "ad_active_status": "ALL",
                  "ad_delivery_date_min": (datetime.date.fromisoformat(heute()) - datetime.timedelta(days=a["zeitraum_tage"])).isoformat(),
                  "fields": FELDER_ERWEITERT if self.erweitert else FELDER_BASIS, "limit": a["limit"], "access_token": self.token}
        params.update(extra)
        if video:
            params["media_type"] = "VIDEO"
        if nach:
            params["after"] = nach
        url = f"https://graph.facebook.com/{self.cfg.get('graph_version', 'v26.0')}/ads_archive?" + urllib.parse.urlencode(params)
        time.sleep(a["pause_sekunden"])
        self.n += 1
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            try:
                f = json.load(e).get("error", {})
            except Exception:
                raise ApiStopp(f"HTTP {e.code} ohne JSON-Antwort: vermutlich blockiert der Proxy der Umgebung graph.facebook.com (Netzwerkfreigabe/Allowed domains prüfen)")
            code, msg = f.get("code"), str(f.get("message", "")).replace(self.token, "***")
            if code == 100 and "field" in msg.lower() and self.erweitert:
                self.erweitert = False
                print("Hinweis: erweiterte Felder (EU-Reichweite/Zielgruppe) nicht abrufbar, weiter mit Basisfeldern.")
                return self.abfrage(land, extra, video, nach)
            if code == 190:
                raise ApiStopp("Token ungültig oder abgelaufen (Code 190). Langlebigen Token neu erzeugen (Lebensdauer ca. 60 Tage).")
            if code in (4, 17, 32, 613):
                raise ApiStopp(f"Rate-Limit erreicht (Code {code}). Teilergebnis wird gespeichert, später wiederholen.")
            if code == 10:
                raise ApiStopp("Keine Berechtigung (Code 10): meist fehlt die Identitäts-/Standortbestätigung für die Ad Library API oder die Nutzungsbedingungen sind nicht akzeptiert.")
            raise ApiStopp(f"Meta-API-Fehler Code {code}: {msg}")
        except urllib.error.URLError as e:
            raise ApiStopp(f"Netzwerkfehler: {e.reason} (Netzwerkfreigabe für graph.facebook.com prüfen)")

    def alle(self, land, extra, video=False):
        nach, seiten = None, 0
        while True:
            antwort = self.abfrage(land, extra, video, nach)
            for ad in antwort.get("data", []):
                yield ad
            seiten += 1
            nach = (antwort.get("paging") or {}).get("cursors", {}).get("after")
            if not antwort.get("data") or not (antwort.get("paging") or {}).get("next") or seiten >= self.cfg["adlib"]["max_seiten_je_abfrage"]:
                return


def token_holen(cfg):
    name = cfg["umgebungsvariablen"]["adlib_token"]
    t = os.environ.get(name, "")
    if not t:
        sys.exit(f"Kein Token: Umgebungsvariable {name} ist nicht gesetzt.\n"
                 "Ohne Token läuft nur der Trockenlauf (--dry-run). So kommt man an den Token: siehe To-do-Liste "
                 "(Meta-App, Identitätsbestätigung, langlebiger Token als Umgebungsvariable der Cloud-Umgebung).")
    return t


def echtlauf_pruefen(cfg):
    if not cfg["adlib"].get("echtlauf_freigegeben"):
        sys.exit("Echtlauf gesperrt: config/meta.json adlib.echtlauf_freigegeben ist false.\n"
                 "Erst Token und Trockenlauf (--dry-run) von Alexander bestätigen lassen, dann den Schalter setzen.")


# ---------------------------------------------------------------- Normalisierung
def text_von(ad):
    teile = []
    for f in ("ad_creative_bodies", "ad_creative_link_titles", "ad_creative_link_descriptions", "ad_creative_link_captions"):
        v = ad.get(f) or []
        teile += v if isinstance(v, list) else [str(v)]
    return teile


def zielgruppe(ad):
    try:
        teile = []
        ages = ad.get("target_ages")
        if ages:
            teile.append("Alter " + (f"{ages[0]}–{ages[-1]}" if isinstance(ages, list) and len(ages) > 1 else str(ages)))
        if ad.get("target_gender"):
            teile.append(f"Geschlecht {ad['target_gender']}")
        orte = ad.get("target_locations")
        if orte:
            namen = [o.get("name", "") if isinstance(o, dict) else str(o) for o in orte]
            teile.append("Orte " + ", ".join(n for n in namen if n)[:80])
        return "; ".join(teile)
    except Exception:
        return ""


def reichweite(ad):
    if ad.get("eu_total_reach") not in (None, ""):
        return str(ad["eu_total_reach"]), "eu_total_reach"
    if ad.get("total_reach_by_location"):
        return "", "total_reach_by_location (Rohwert): " + json.dumps(ad["total_reach_by_location"], ensure_ascii=False)[:100]
    return "", ""


def stufe_von(ad, wb):
    pid = str(ad.get("page_id", ""))
    name = (ad.get("page_name") or "").lower()
    for w in wb["wettbewerber"]:
        if pid and w.get("seiten_ids_bestaetigt") and pid in {str(i) for i in w["seiten_ids"]}:
            return w["stufe"]
    beste, laenge = "", 0
    for w in wb["wettbewerber"]:
        for kern in [w["suchname"].lower()] + [a.lower() for a in w.get("alias", [])]:
            if kern and name and (kern in name or (len(name) >= 5 and name in kern)) and len(kern) > laenge:
                beste, laenge = w["stufe"], len(kern)
    return beste


def einstufen(text, seitenname=""):
    b, p = bool(B2B.search(text) or B2B_SEITENNAME.search(seitenname)), bool(PATIENT.search(text))
    if b and p:
        return "prüfen"
    if b:
        return "ja"
    if p:
        return "nein"
    return "prüfen"


def normalisieren(ad, land, video_ids, wb):
    start = (ad.get("ad_delivery_start_time") or ad.get("ad_creation_time") or "")[:10]
    stop = (ad.get("ad_delivery_stop_time") or "")[:10]
    texte = text_von(ad)
    gesamt = " ".join(texte)
    reich, hinweis = reichweite(ad)
    n_titel = len(ad.get("ad_creative_link_titles") or [])
    n_body = len(ad.get("ad_creative_bodies") or [])
    fmt = "video" if ad["id"] in video_ids else ("mehrere Texte/Karussell (prüfen)" if max(n_titel, n_body) > 1 else "bild")
    return {
        "bibliotheks_id": str(ad["id"]), "page_id": str(ad.get("page_id", "")), "werbetreibender": ad.get("page_name", ""),
        "laender": [land], "start": start, "ende": stop or "aktiv", "format": fmt,
        "texte": {"bodies": ad.get("ad_creative_bodies") or [], "titel": ad.get("ad_creative_link_titles") or [],
                  "beschreibungen": ad.get("ad_creative_link_descriptions") or [], "captions": ad.get("ad_creative_link_captions") or []},
        "plattformen": ad.get("publisher_platforms") or [], "sprachen": ad.get("languages") or [],
        "eu_zielgruppe": zielgruppe(ad), "eu_reichweite": reich, "reichweite_hinweis": hinweis,
        "link": f"https://www.facebook.com/ads/library/?id={ad['id']}",
        "snapshot": bereinige_url(ad.get("ad_snapshot_url")),
        "gruppe": hashlib.md5("|".join([str(ad.get("page_id", ""))] + texte).encode()).hexdigest()[:10],
        "stufe": stufe_von(ad, wb), "b2b": einstufen(gesamt, ad.get("page_name", "")), "textauszug": re.sub(r"\s+", " ", (texte[0] if texte else ""))[:140],
    }


# ---------------------------------------------------------------- Log
def log_lesen():
    if not LOG.exists():
        return collections.OrderedDict()
    with LOG.open(encoding="utf-8", newline="") as f:
        return collections.OrderedDict((r["bibliotheks_id"], r) for r in csv.DictReader(f))


def log_text(zeilen):
    import io
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=SPALTEN, extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    for r in zeilen.values():
        w.writerow({k: r.get(k, "") for k in SPALTEN})
    return buf.getvalue()


def leck(text, token):
    """True, wenn der Text einen Zugriffstoken enthalten könnte."""
    return "access_token" in text.lower() or (token not in ("", "FIXTURE") and token in text)


def snapshot(dry, fixture_pfad=None):
    cfg, wb, sb = konfig()
    calls = plan_snapshot(cfg, wb, sb)
    n_video = len(calls) if cfg["adlib"]["format_video_pass"] else 0
    plan_ausgeben("Plan snapshot", len(calls) + n_video, cfg, f" (davon {n_video} für die Formaterkennung Video), mindestens {len(calls) + n_video} Aufrufe")
    ohne = [w["name"] for w in wb["wettbewerber"] if not w.get("seiten_ids_bestaetigt")]
    if ohne:
        print(f"Hinweis: {len(ohne)} Wettbewerber ohne bestätigte Seiten-ID (nur über Suchbegriffe auffindbar). Erst `adlib.py seiten`, dann von Alexander bestätigen lassen.")
    if len(calls) + n_video > cfg["adlib"]["max_aufrufe"]:
        sys.exit("Abbruch: Plan überschreitet max_aufrufe in config/meta.json.")
    for c in calls[:8]:
        print("  ", c["art"], c["land"], c.get("begriff") or f"{len(c['ids'])} Seiten-IDs")
    if len(calls) > 8:
        print(f"   … und {len(calls) - 8} weitere")
    if dry:
        if not os.environ.get(cfg["umgebungsvariablen"]["adlib_token"]):
            print(f"Hinweis: Token fehlt ({cfg['umgebungsvariablen']['adlib_token']}). Für den Echtlauf nötig, für den Trockenlauf nicht.")
        if not cfg["adlib"].get("echtlauf_freigegeben"):
            print("Hinweis: Echtlauf ist noch gesperrt (adlib.echtlauf_freigegeben false).")
        print("TROCKENLAUF: kein Netzwerkzugriff, nichts geschrieben.")
        return
    fixture = laden(fixture_pfad) if fixture_pfad else None
    token = "FIXTURE"
    if fixture is None:
        echtlauf_pruefen(cfg)
        token = token_holen(cfg)
    client = Client(cfg, token, fixture)
    gesehen, video_ids, fehler = {}, set(), None
    try:
        for c in calls:
            extra = {"search_page_ids": ",".join(c["ids"])} if c["art"] == "seiten" else {"search_terms": c["begriff"], "search_type": "KEYWORD_UNORDERED"}
            if cfg["adlib"]["format_video_pass"]:
                video_ids |= {str(a["id"]) for a in client.alle(c["land"], extra, video=True)}
            for ad in client.alle(c["land"], extra):
                n = normalisieren(ad, c["land"], video_ids, wb)
                if n["bibliotheks_id"] in gesehen:
                    g = gesehen[n["bibliotheks_id"]]
                    g["laender"] = sorted(set(g["laender"]) | set(n["laender"]))
                    g["quellen"].add(c["art"])
                else:
                    n["quellen"] = {c["art"]}
                    gesehen[n["bibliotheks_id"]] = n
    except ApiStopp as e:
        fehler = str(e)
        print("STOPP:", e)
    # Format nachtragen (Video-Pass läuft je Abfrage vor dem Hauptpass; IDs sind ggf. erst später bekannt)
    for n in gesehen.values():
        if n["bibliotheks_id"] in video_ids:
            n["format"] = "video"
    gruppen = collections.Counter(n["gruppe"] for n in gesehen.values())
    behalten, verworfen = [], []
    for n in gesehen.values():
        n["varianten"] = gruppen[n["gruppe"]]
        (verworfen if n["b2b"] == "nein" else behalten).append(n)
    ausgabe = {"datum": heute(), "aufrufe": client.n, "abbruch": fehler, "ads": [dict(n, quellen=sorted(n["quellen"])) for n in behalten],
               "verworfen": [{"id": n["bibliotheks_id"], "werbetreibender": n["werbetreibender"], "grund": "Patientenwerbung (Textmuster)"} for n in verworfen]}
    roh_text = json.dumps(ausgabe, ensure_ascii=False, indent=1)
    # Log im Speicher fortschreiben
    zeilen = log_lesen()
    neu = 0
    for n in behalten:
        r = zeilen.get(n["bibliotheks_id"])
        if r is None:
            neu += 1
            r = {k: "" for k in SPALTEN}
            r.update(bibliotheks_id=n["bibliotheks_id"], zuerst_gesehen=heute(), quelle=("seite" if "seiten" in n["quellen"] else "suchbegriff"), b2b=n["b2b"])
            zeilen[n["bibliotheks_id"]] = r
        alt_laender = set(filter(None, r.get("land", "").split(";")))
        r.update(werbetreibender=n["werbetreibender"], land=";".join(sorted(alt_laender | set(n["laender"]))), start=n["start"], ende=n["ende"],
                 varianten=n["varianten"], format=n["format"], eu_zielgruppe=n["eu_zielgruppe"], eu_reichweite=n["eu_reichweite"],
                 reichweite_hinweis=n["reichweite_hinweis"], link=n["link"], stufe=n["stufe"] or r.get("stufe", ""),
                 textauszug=n["textauszug"], zuletzt_gesehen=heute())
    csv_text = log_text(zeilen)
    # Sicherheitsprüfung VOR dem Schreiben: kein Token in den Ausgaben, sonst wird nichts gespeichert
    if leck(roh_text, token) or leck(csv_text, token):
        sys.exit("STOPP: Zugriffstoken (oder „access_token“) in den Ergebnissen gefunden. Es wurde NICHTS gespeichert. Bitte Skript prüfen.")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "rohdaten").mkdir(exist_ok=True)
    datei = OUT / "rohdaten" / f"{heute()}.json"
    datei.write_text(roh_text, encoding="utf-8")
    LOG.write_text(csv_text, encoding="utf-8")
    print(f"{client.n} Aufrufe, {len(gesehen)} Anzeigen ({neu} neu im Log, {len(verworfen)} als Patientenwerbung verworfen) -> {datei}")
    if fehler:
        sys.exit(3)


def seiten(dry, fixture_pfad=None):
    cfg, wb, sb = konfig()
    offen = plan_seiten(wb)
    plan_ausgeben("Plan seiten", len(offen), cfg, f" (ein Aufruf je Wettbewerber ohne bestätigte ID, je eine Seite à {cfg['adlib']['limit']} Treffer)")
    if len(offen) > cfg["adlib"]["max_aufrufe"]:
        sys.exit("Abbruch: Plan überschreitet max_aufrufe.")
    if dry:
        if not os.environ.get(cfg["umgebungsvariablen"]["adlib_token"]):
            print(f"Hinweis: Token fehlt ({cfg['umgebungsvariablen']['adlib_token']}).")
        print("TROCKENLAUF: kein Netzwerkzugriff, nichts geschrieben.")
        return
    fixture = laden(fixture_pfad) if fixture_pfad else None
    token = "FIXTURE"
    if fixture is None:
        echtlauf_pruefen(cfg)
        token = token_holen(cfg)
    client = Client(cfg, token, fixture)
    zeilen = ["# Vorschlag Seiten-IDs (automatisch, NICHT eingetragen)", "",
              f"Stand {heute()}. Treffer der Ad Library für den Namen des Wettbewerbers. **Alexander bestätigt**, welche Seite die richtige ist; erst dann trägt der Agent die ID in `references/wettbewerber.json` ein (`seiten_ids_bestaetigt` true).",
              "Die Seiten-ID lässt sich gegenprüfen: Facebook-Seite öffnen → „Transparenz der Seite“ → Seiten-ID.", ""]
    try:
        for w in offen:
            land = "GB" if "GB" in w["laender"] and "DE" not in w["laender"] else "DE"
            zaehler, namen = collections.Counter(), {}
            for i, ad in enumerate(client.abfrage(land, {"search_terms": w["suchname"], "search_type": "KEYWORD_UNORDERED", "fields": "page_id,page_name"}).get("data", [])):
                zaehler[str(ad.get("page_id"))] += 1
                namen[str(ad.get("page_id"))] = ad.get("page_name", "")
            tokens = set(re.findall(r"\w+", w["suchname"].lower()))
            def aehnlich(pid):
                t = set(re.findall(r"\w+", namen[pid].lower()))
                return len(tokens & t) / max(len(tokens), 1)
            ranking = sorted(zaehler, key=lambda p: (-aehnlich(p), -zaehler[p]))[:5]
            zeilen.append(f"## {w['name']} (Stufe {w['stufe']}, Suche „{w['suchname']}“ in {land})")
            if not ranking:
                zeilen += ["- keine Treffer", ""]
                continue
            zeilen += ["| Seiten-ID | Seitenname | Treffer | Namensähnlichkeit |", "|---|---|---|---|"]
            zeilen += [f"| {p} | {namen[p]} | {zaehler[p]} | {aehnlich(p):.0%} |" for p in ranking]
            zeilen.append("")
    except ApiStopp as e:
        print("STOPP:", e)
        zeilen += ["", f"**Abbruch:** {e}"]
    OUT.mkdir(parents=True, exist_ok=True)
    ziel = OUT / "seiten-vorschlag.md"
    text = "\n".join(zeilen) + "\n"
    if leck(text, token):
        sys.exit("STOPP: Token in der Ausgabe gefunden. Es wurde NICHTS gespeichert.")
    ziel.write_text(text, encoding="utf-8")
    print(f"{client.n} Aufrufe -> {ziel}")


# ---------------------------------------------------------------- Bericht
def tage(a, b):
    try:
        return (datetime.date.fromisoformat(b) - datetime.date.fromisoformat(a)).days
    except Exception:
        return None


def wellen(zeilen):
    """Anzahl Kampagnenwellen: neue Welle, wenn eine Anzeige mehr als 21 Tage nach dem Ende der vorigen beginnt."""
    iv = []
    for r in zeilen:
        s = r["start"][:10]
        e = heute() if r["ende"] == "aktiv" else r["ende"][:10]
        if len(s) == 10 and len(e) == 10:
            iv.append((s, e))
    iv.sort()
    n, ende = 0, None
    for s, e in iv:
        if ende is None or tage(ende, s) is None or tage(ende, s) > 21:
            n += 1
        ende = e if ende is None or e > ende else ende
    return n


def report():
    cfg, wb, sb = konfig()
    rd = sorted((OUT / "rohdaten").glob("2*.json"))
    if not rd:
        sys.exit("Keine Rohdaten vorhanden (erst `adlib.py snapshot` ausführen).")
    letzte = json.loads(rd[-1].read_text(encoding="utf-8"))
    vor = json.loads(rd[-2].read_text(encoding="utf-8")) if len(rd) > 1 else None
    zeilen = list(log_lesen().values())
    echt = [r for r in zeilen if not r["bibliotheks_id"].startswith("bestand-")]
    stand = letzte["datum"]
    grenze = vor["datum"] if vor else None
    neu = [r for r in echt if r["zuerst_gesehen"] == stand] if vor else []
    neu_b2b = [r for r in neu if r["b2b"] in ("ja", "prüfen")]
    L = [f"# Konkurrenz-Monitor Meta, Woche bis {stand} (automatisch, Agent ergänzt Abschnitt 5)", ""]
    if letzte.get("abbruch"):
        L += [f"> **Lauf unvollständig:** {letzte['abbruch']}", ""]
    if not vor:
        L += [f"> Erster Lauf: Basislinie ({len(letzte['ads'])} Anzeigen). Neues und Veränderungen gibt es ab dem zweiten Lauf.", ""]
    L += ["## 1. Neue B2B-Anzeigen", f"{len(neu_b2b)} neu seit {grenze or '–'}."]
    if neu_b2b:
        L += ["| Werbetreibender | Land | Start | Format | Angebot / Aufhänger | Link |", "|---|---|---|---|---|---|"]
        for r in neu_b2b[:12]:
            L.append(f"| {r['werbetreibender']} | {r['land']} | {r['start']} | {r['format']} | {(r['angebot'] + ' / ' + r['aufhaenger']).strip(' /') or 'offen'} | {r['link']} |")
        if len(neu_b2b) > 12:
            L.append(f"… {len(neu_b2b) - 12} weitere im Log.")
    pruef = [r for r in zeilen if r["b2b"] == "prüfen" and not r["bibliotheks_id"].startswith("bestand-")]
    L += ["", "## 2. Neue Aufhänger"]
    bekannt = {r["aufhaenger"] for r in echt if r["zuerst_gesehen"] != stand and r["aufhaenger"]}
    neue_ah = sorted({r["aufhaenger"] for r in neu_b2b if r["aufhaenger"]} - bekannt)
    ohne = [r for r in neu_b2b if not r["aufhaenger"]]
    L += [("- " + ", ".join(neue_ah)) if neue_ah else "- keine eingestuften neuen Aufhänger"]
    if ohne:
        L.append(f"- {len(ohne)} neue Anzeige(n) noch ohne Aufhänger/Ton/Angebot: Agent stuft beim Bericht ein.")
    L += ["", "## 3. Veränderungen bei Stufe-1-Anbietern"]
    if vor:
        a_neu = {x["bibliotheks_id"]: x for x in letzte["ads"] if x["stufe"].startswith("1")}
        a_alt = {x["bibliotheks_id"]: x for x in vor["ads"] if x["stufe"].startswith("1")}
        neu_ids = [a_neu[i] for i in a_neu if i not in a_alt]
        beendet = [a_neu[i] for i in a_neu if i in a_alt and a_alt[i]["ende"] == "aktiv" and a_neu[i]["ende"] != "aktiv"]
        L += [f"- neu: {', '.join(sorted({x['werbetreibender'] for x in neu_ids})) or 'keine'}",
              f"- beendet: {', '.join(sorted({x['werbetreibender'] for x in beendet})) or 'keine'}"]
    else:
        L.append("- noch nicht berechenbar (Basislinie).")
    L += ["", "## 4. Erfolgshinweise", "**UK (Laufzeit und Varianten):**"]
    uk = sorted((r for r in echt if "GB" in r["land"]), key=lambda r: -(tage(r["start"], heute() if r["ende"] == "aktiv" else r["ende"]) or 0))[:5]
    for r in uk:
        d = tage(r["start"], heute() if r["ende"] == "aktiv" else r["ende"])
        L.append(f"- {r['werbetreibender']}: {d if d is not None else '?'} Tage, {r['varianten'] or '?'} Variante(n)")
    if not uk:
        L.append("- keine UK-Anzeigen im Log")
    L.append("**DACH (Häufigkeit eines Themas über mehrere Wellen):**")
    je = collections.defaultdict(list)
    for r in echt:
        if set(r["land"].split(";")) & {"DE", "AT"}:
            je[r["werbetreibender"]].append(r)
    mehrfach = [(n, wellen(rs), sorted({r["aufhaenger"] for r in rs if r["aufhaenger"]})) for n, rs in je.items() if wellen(rs) >= 2]
    for n, w, ah in sorted(mehrfach, key=lambda x: -x[1])[:6]:
        L.append(f"- {n}: {w} Wellen" + (f", Aufhänger: {', '.join(ah)}" if ah else ""))
    if not mehrfach:
        L.append("- noch keine Wiederholung über mehrere Wellen erkennbar")
    L += ["", "## 5. Anregungen für eigene Anzeigen", "_Agent ergänzt: höchstens drei, je Anregung Aufruf nach Aufrufregel angeben und vorher mit "
          "`anzeigen_check_meta.py --text \"…\"` prüfen. Muster übernehmen, nie Wortlaut._", "",
          "## Hinweise"]
    L.append(f"- {len(pruef)} Anzeige(n) mit B2B-Einstufung „prüfen“ im Log.")
    L.append(f"- {len(letzte.get('verworfen', []))} Treffer als Patientenwerbung verworfen (Stichprobe der Liste in den Rohdaten prüfen).")
    n_offen = sum(1 for w in wb["wettbewerber"] if not w.get("seiten_ids_bestaetigt"))
    if n_offen:
        L.append(f"- {n_offen} Wettbewerber ohne bestätigte Seiten-ID (nur über Suchbegriffe erfasst).")
    L.append("- Grenzen: Stichwortsuche erfasst nicht alles; CH nicht abgedeckt; Reichweite nur für EU-Anzeigen als eu_total_reach.")
    (OUT / "berichte").mkdir(parents=True, exist_ok=True)
    ziel = OUT / "berichte" / f"{stand}.md"
    ziel.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"Bericht: {ziel} ({len(L)} Zeilen)" + ("  ACHTUNG: länger als eine Seite, kürzen" if len(L) > 70 else ""))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("modus", choices=["seiten", "snapshot", "report"])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--fixture")
    a = ap.parse_args()
    if a.modus == "snapshot":
        snapshot(a.dry_run, a.fixture)
    elif a.modus == "seiten":
        seiten(a.dry_run, a.fixture)
    else:
        report()
