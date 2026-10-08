#!/usr/bin/env python3
"""Suchvolumen via DataForSEO (Google Ads Search Volume, live). Nur Standardbibliothek."""
import argparse, base64, csv, json, os, sys, time, urllib.request

ENDPOINT = "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"
# 2276 = Deutschland. Mülheim an der Ruhr fehlt in der Google-Ads-Standortliste (geprüft 08.10.2026),
# daher Umkreis um die Praxis (Leineweberstr. 72, ca. 51.4272,6.8826): "lat,lon,radius_km".
# Der Radius-Code "ruhr" wird von der API ignoriert (liefert bundesweite Werte) und bleibt nur zur Doku.
# Stattdessen Staedte im Umkreis ca. 40 km (Entfernung grob von Muelheim). Einzelabruf: --location <stadt>,
# alle zusammen: --region (Summe pro Keyword = Annahme, Einzugsgebiet ohne Ueberlappung).
STAEDTE = {
    "essen": 1004625, "duisburg": 1004612, "oberhausen": 1004710, "duesseldorf": 1004615,
    "ratingen": 1004719, "bottrop": 1004601, "gelsenkirchen": 1004631, "bochum": 1004596,
    "velbert": 1004747, "heiligenhaus": 1004645, "mettmann": 1004700, "herne": 1004651,
    "gladbeck": 9048374, "moers": 1004702, "krefeld": 1004675, "neuss": 1004708,
    "dortmund": 1004611, "wuppertal": 1004769, "dinslaken": 9048281, "hattingen": 1004643,
    "witten": 1004768, "herten": 1004652, "recklinghausen": 1004721, "hilden": 1004655,
}
LOCATION_CODES = {"bund": 2276, "ruhr": "51.4272,6.8826,40", **STAEDTE}
BATCH = 1000


def read_seeds(path):
    with open(path, encoding="utf-8") as f:
        return sorted({l.strip().lower() for l in f if l.strip()})


def request(auth, keywords, location):
    key = "location_coordinate" if isinstance(location, str) else "location_code"
    body = [{"keywords": keywords, "language_code": "de", key: location}]
    req = urllib.request.Request(
        ENDPOINT, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", **({"Authorization": "Basic " + auth} if auth else {})})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def region(a, kws):
    n = -(-len(kws) // BATCH) * len(STAEDTE)
    if a.dry_run:
        print(f"DRY-RUN: {len(kws)} Keywords x {len(STAEDTE)} Staedte = {n} Anfrage(n)")
        return
    login, pw = os.environ.get("DATAFORSEO_LOGIN"), os.environ.get("DATAFORSEO_PASSWORD")
    auth = base64.b64encode(f"{login}:{pw}".encode()).decode() if login and pw else None
    tab = {k: {} for k in kws}
    for stadt, code in STAEDTE.items():
        for i in range(0, len(kws), BATCH):
            for versuch in range(4):  # Limit 12 Anfragen/Minute (40202), 50301 = zu viele Anfragen
                time.sleep(5.5)
                resp = request(auth, kws[i:i + BATCH], code)
                if all(t.get("status_code") not in (40202, 50301) for t in resp.get("tasks", [])):
                    break
                time.sleep(30)
            for task in resp.get("tasks", []):
                if task.get("status_code") != 20000:
                    sys.exit(f"DataForSEO-Fehler: {task.get('status_code')} {task.get('status_message')}")
                for item in task.get("result") or []:
                    tab.setdefault(item["keyword"], {})[stadt] = item.get("search_volume")
    with open(a.out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["keyword", "volumen_region_summe", "staedte_mit_daten"] + list(STAEDTE))
        for k in kws:
            v = tab[k]
            w.writerow([k, sum(x or 0 for x in v.values()), sum(1 for x in v.values() if x)] + [v.get(s) for s in STAEDTE])
    print(f"{len(kws)} Keywords x {len(STAEDTE)} Staedte -> {a.out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("seeds")
    ap.add_argument("--out", required=True)
    ap.add_argument("--location", choices=LOCATION_CODES, default="bund")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--region", action="store_true", help="alle Staedte aus STAEDTE abrufen, Summe je Keyword")
    a = ap.parse_args()
    kws = read_seeds(a.seeds)
    if a.region:
        return region(a, kws)
    loc = LOCATION_CODES[a.location]
    if loc is None:
        sys.exit(f"Standort-Code fuer '{a.location}' ist noch nicht gesetzt (LOCATION_CODES).")
    if a.dry_run:
        print(f"DRY-RUN: {len(kws)} Keywords, Standort {loc}, {-(-len(kws)//BATCH)} Anfrage(n) an {ENDPOINT}")
        return
    # Ohne Variablen traegt der Umgebungs-Proxy die Zugangsdaten fuer api.dataforseo.com ein.
    login, pw = os.environ.get("DATAFORSEO_LOGIN"), os.environ.get("DATAFORSEO_PASSWORD")
    auth = base64.b64encode(f"{login}:{pw}".encode()).decode() if login and pw else None
    rows = []
    for i in range(0, len(kws), BATCH):
        resp = request(auth, kws[i:i + BATCH], loc)
        for task in resp.get("tasks", []):
            if task.get("status_code") != 20000:
                sys.exit(f"DataForSEO-Fehler: {task.get('status_code')} {task.get('status_message')}")
            for item in task.get("result") or []:
                rows.append({
                    "keyword": item.get("keyword"), "volumen": item.get("search_volume"),
                    "cpc": item.get("cpc"), "wettbewerb": item.get("competition"),
                    "standort": a.location})
    with open(a.out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["keyword", "volumen", "cpc", "wettbewerb", "standort"])
        w.writeheader(); w.writerows(rows)
    print(f"{len(rows)} Zeilen -> {a.out}")


if __name__ == "__main__":
    main()
