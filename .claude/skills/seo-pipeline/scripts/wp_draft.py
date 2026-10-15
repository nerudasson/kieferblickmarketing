#!/usr/bin/env python3
"""Legt einen WordPress-ENTWURF an. Veröffentlichen ist bewusst nicht möglich.

Aufruf: wp_draft.py --title "Titel" --content-file entwurf.html [--slug x] [--excerpt "..."]
Login: kommt über die Proxy-Injektion der Umgebung für kieferblick.de.
Nur wenn WP_USER und WP_APP_PASSWORD gesetzt sind, wird Basic Auth selbst gesendet.
"""
import argparse, base64, json, os, sys, urllib.request

URL = os.environ.get("WP_URL", "https://kieferblick.de").rstrip("/") + "/wp-json/wp/v2/posts"

p = argparse.ArgumentParser()
p.add_argument("--title", required=True)
p.add_argument("--content-file", required=True)
p.add_argument("--slug")
p.add_argument("--excerpt")
a = p.parse_args()

body = {"title": a.title, "content": open(a.content_file, encoding="utf-8").read(), "status": "draft"}
if a.slug:
    body["slug"] = a.slug
if a.excerpt:
    body["excerpt"] = a.excerpt

headers = {"Content-Type": "application/json"}
user, pw = os.environ.get("WP_USER"), os.environ.get("WP_APP_PASSWORD")
if user and pw:
    headers["Authorization"] = "Basic " + base64.b64encode(f"{user}:{pw}".encode()).decode()

req = urllib.request.Request(URL, json.dumps(body).encode(), headers, method="POST")
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.load(r)
except urllib.error.HTTPError as e:
    sys.exit(f"WordPress-Fehler {e.code}: {e.read().decode()[:300]}")
if d.get("status") != "draft":
    sys.exit(f"Unerwarteter Status {d.get('status')} bei ID {d.get('id')} – bitte prüfen.")
print(json.dumps({"id": d["id"], "status": d["status"], "link": d.get("link")}))
