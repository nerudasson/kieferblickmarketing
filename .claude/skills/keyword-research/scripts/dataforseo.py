#!/usr/bin/env python3
"""Suchvolumen via DataForSEO (Google Ads Search Volume, live). Nur Standardbibliothek."""
import argparse, base64, csv, json, os, sys, urllib.request

ENDPOINT = "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"
# 2276 = Deutschland. Mülheim an der Ruhr fehlt in der Google-Ads-Standortliste (geprüft 08.10.2026),
# daher Umkreis um die Praxis (Leineweberstr. 72, ca. 51.4272,6.8826): "lat,lon,radius_km".
LOCATION_CODES = {"bund": 2276, "ruhr": "51.4272,6.8826,40", "essen": 1004625}
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("seeds")
    ap.add_argument("--out", required=True)
    ap.add_argument("--location", choices=LOCATION_CODES, default="bund")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    kws = read_seeds(a.seeds)
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
