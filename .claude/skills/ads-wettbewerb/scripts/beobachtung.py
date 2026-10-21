#!/usr/bin/env python3
"""Wöchentliche Beobachtung der Google-Anzeigen von Wettbewerbern (DataForSEO SERP, nur Standardbibliothek).

  beobachtung.py snapshot [--dry-run]   Abfragen laufen lassen, daten/ads/beobachtung/<Datum>.json schreiben
  beobachtung.py report                 alle Momentaufnahmen vergleichen, daten/ads/beobachtung/auswertung.md schreiben
Zugang: Proxy der Umgebung oder DATAFORSEO_LOGIN/DATAFORSEO_PASSWORD.
"""
import argparse, base64, collections, datetime, hashlib, json, os, pathlib, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = pathlib.Path(__file__).resolve().parents[4]
CONFIG = ROOT / ".claude/skills/ads-wettbewerb/references/beobachtung.json"
OUT = ROOT / "daten/ads/beobachtung"
ENDPOINT = "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"
KOSTEN_PRO_ABFRAGE = 0.002


def jobs(cfg):
    return [(thema, kw, ort, code) for thema, kws in cfg["keywords"].items()
            for kw in kws for ort, code in cfg["standorte"].items()]


def abfrage(job, cfg, headers):
    thema, kw, ort, code = job
    body = [{"keyword": kw, "language_code": "de", "location_code": code,
             "device": cfg["geraet"], "os": "android", "depth": 10}]
    req = urllib.request.Request(ENDPOINT, data=json.dumps(body).encode(), headers=headers)
    for versuch in range(4):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                task = json.load(r)["tasks"][0]
            res = (task.get("result") or [{}])[0]
            ads, pack = [], []
            for i in res.get("items") or []:
                if i.get("type") == "paid":
                    ads.append({k: i.get(k) for k in ("domain", "title", "description", "rank_absolute", "url")})
                elif i.get("type") == "local_pack":
                    pack.append({"titel": i.get("title"), "bewertung": (i.get("rating") or {}).get("value"),
                                 "anzahl": (i.get("rating") or {}).get("votes_count")})
            return {"thema": thema, "keyword": kw, "ort": ort, "anzeigen": ads, "local_pack": pack, "fehler": None}
        except Exception as e:
            fehler = str(e)
            time.sleep(3 * (versuch + 1))
    return {"thema": thema, "keyword": kw, "ort": ort, "anzeigen": [], "local_pack": [], "fehler": fehler}


def snapshot(dry):
    cfg = json.load(open(CONFIG, encoding="utf-8"))
    liste = jobs(cfg)
    kosten = len(liste) * KOSTEN_PRO_ABFRAGE
    print(f"{len(liste)} Abfragen, ca. {kosten:.2f} USD (Obergrenze {cfg['max_abfragen']})")
    if len(liste) > cfg["max_abfragen"]:
        sys.exit("Abbruch: mehr Abfragen als max_abfragen in beobachtung.json.")
    if dry:
        return
    headers = {"Content-Type": "application/json"}
    login, pw = os.environ.get("DATAFORSEO_LOGIN"), os.environ.get("DATAFORSEO_PASSWORD")
    if login and pw:
        headers["Authorization"] = "Basic " + base64.b64encode(f"{login}:{pw}".encode()).decode()
    with ThreadPoolExecutor(4) as ex:
        ergebnis = list(ex.map(lambda j: abfrage(j, cfg, headers), liste))
    fehler = sum(1 for e in ergebnis if e["fehler"])
    OUT.mkdir(parents=True, exist_ok=True)
    datei = OUT / f"{datetime.date.today().isoformat()}.json"
    json.dump({"datum": datetime.date.today().isoformat(), "geraet": cfg["geraet"], "ergebnisse": ergebnis},
              open(datei, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(ergebnis)} Ergebnisse ({fehler} Fehler) -> {datei.relative_to(ROOT)}")


def anzeigen_id(a):
    return hashlib.md5(f"{a['domain']}|{a['title']}|{a['description']}".encode()).hexdigest()[:10]


def report():
    dateien = sorted(p for p in OUT.glob("2*.json"))
    if not dateien:
        sys.exit("Keine Momentaufnahmen vorhanden (erst snapshot ausführen).")
    snaps = [json.load(open(p, encoding="utf-8")) for p in dateien]
    gesehen = {}  # id -> {texte, wochen, domains}
    sichtbar = collections.defaultdict(lambda: collections.defaultdict(int))
    abfragen = collections.defaultdict(int)
    for s in snaps:
        for e in s["ergebnisse"]:
            if e["fehler"]:
                continue
            abfragen[s["datum"]] += 1
            for a in e["anzeigen"]:
                i = anzeigen_id(a)
                g = gesehen.setdefault(i, {"domain": a["domain"], "title": a["title"], "desc": a["description"],
                                           "tage": set(), "themen": set()})
                g["tage"].add(s["datum"]); g["themen"].add(e["thema"])
                sichtbar[s["datum"]][a["domain"]] += 1
    letzte, vorletzte = snaps[-1]["datum"], snaps[-2]["datum"] if len(snaps) > 1 else None
    zeilen = [f"# Anzeigen-Beobachtung Wettbewerber (automatisch, Stand {letzte})",
              f"Momentaufnahmen: {len(snaps)} ({', '.join(s['datum'] for s in snaps)}). Gerät {snaps[-1]['geraet']}. "
              "Eine Anzeige zählt als gleich, wenn Domain, Überschriften und Beschreibung gleich sind. "
              "Laufzeit ist ein Indiz für Wirtschaftlichkeit (Annahme), kein Beleg für Leistung.", ""]
    n = abfragen[letzte]
    top = sorted(sichtbar[letzte].items(), key=lambda x: -x[1])[:15]
    zeilen += [f"## Sichtbarkeit in der letzten Woche ({n} gültige Abfragen)", "| Werbetreibender | Anzeigen-Einblendungen | je Abfrage |", "|---|---|---|"]
    zeilen += [f"| {d} | {c} | {c / n:.2f} |" for d, c in top]
    lang = sorted((g for g in gesehen.values() if len(g["tage"]) >= 3), key=lambda g: -len(g["tage"]))[:15]
    zeilen += ["", "## Langläufer (in mindestens 3 Momentaufnahmen)"]
    zeilen += [f"- **{g['domain']}** ({len(g['tage'])} Wochen, {', '.join(sorted(g['themen']))}): {g['title']} | {g['desc']}" for g in lang] or ["- noch keine (erst ab der dritten Woche)"]
    if vorletzte:
        neu = [g for g in gesehen.values() if min(g["tage"]) == letzte]
        zeilen += ["", f"## Neu seit {vorletzte}"]
        zeilen += [f"- **{g['domain']}** ({', '.join(sorted(g['themen']))}): {g['title']} | {g['desc']}" for g in neu[:25]] or ["- nichts Neues"]
        weg = [g for g in gesehen.values() if vorletzte in g["tage"] and letzte not in g["tage"]]
        zeilen += ["", f"## Seit {vorletzte} nicht mehr gesehen"]
        zeilen += [f"- {g['domain']}: {g['title']}" for g in weg[:25]] or ["- nichts"]
    (OUT / "auswertung.md").write_text("\n".join(zeilen) + "\n", encoding="utf-8")
    print(f"auswertung.md geschrieben ({len(gesehen)} verschiedene Anzeigen)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("modus", choices=["snapshot", "report"])
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    snapshot(a.dry_run) if a.modus == "snapshot" else report()
