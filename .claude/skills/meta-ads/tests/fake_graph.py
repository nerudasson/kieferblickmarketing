#!/usr/bin/env python3
"""Lokaler Testserver für meta_push.py (kein Meta-Zugriff). Start: fake_graph.py <port> <logdatei>.
Antwortet auf POST/GET wie die Graph API mit erfundenen IDs und schreibt jede Anfrage (ohne Token) ins Log."""
import json, sys, itertools
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
zaehler = itertools.count(1000)
namen = []
log = open(sys.argv[2], "w")
class H(BaseHTTPRequestHandler):
    def _antwort(self, obj, code=200):
        b = json.dumps(obj).encode(); self.send_response(code); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        log.write(f"GET {urlparse(self.path).path}\n"); log.flush()
        self._antwort({"data": [{"name": n} for n in namen]})
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0)); q = parse_qs(self.rfile.read(n).decode())
        q.pop("access_token", None)
        log.write(f"POST {urlparse(self.path).path} status={q.get('status', ['-'])[0]}\n"); log.flush()
        if urlparse(self.path).path.endswith("adimages"):
            return self._antwort({"images": {"x.png": {"hash": "HASH123"}}})
        if urlparse(self.path).path.endswith("campaigns"): namen.append(q.get("name", [""])[0])
        self._antwort({"id": str(next(zaehler))})
    def log_message(self, *a): pass
HTTPServer(("127.0.0.1", int(sys.argv[1])), H).serve_forever()
