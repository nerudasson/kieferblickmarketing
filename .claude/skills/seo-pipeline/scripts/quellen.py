#!/usr/bin/env python3
"""Literaturrecherche für den Quellenspeicher: PubMed (eutils) und Crossref. Nur Standardbibliothek.

  quellen.py search "<suchbegriff>" [--n 5]   PubMed-Treffer mit Titel, Journal, Jahr, DOI
  quellen.py abstract <pmid>                   Abstract und Metadaten (Text)
  quellen.py doi <doi>                         Crossref-Metadaten und Abstract
Der Aufruf läuft über den Proxy der Umgebung (HTTPS_PROXY). Das WebFetch-Werkzeug nicht verwenden.
"""
import argparse, json, re, sys, urllib.parse, urllib.request

E = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def get(url, as_json=False):
    req = urllib.request.Request(url, headers={"User-Agent": "kieferblick-quellen/1.0"})
    with urllib.request.urlopen(req, timeout=40) as r:
        data = r.read().decode("utf-8", "replace")
    return json.loads(data) if as_json else data


def search(term, n):
    q = urllib.parse.urlencode({"db": "pubmed", "term": term, "retmax": n, "retmode": "json", "sort": "relevance"})
    ids = get(f"{E}/esearch.fcgi?{q}", True)["esearchresult"]["idlist"]
    if not ids:
        print("keine Treffer"); return
    s = get(f"{E}/esummary.fcgi?db=pubmed&retmode=json&id={','.join(ids)}", True)["result"]
    for i in ids:
        d = s[i]
        doi = next((x["value"] for x in d.get("articleids", []) if x["idtype"] == "doi"), "")
        au = ", ".join(a["name"] for a in d.get("authors", [])[:3])
        print(f'PMID {i} | {d["pubdate"][:4]} | {d["source"]} | {au} | {d["title"]} | DOI {doi}')


def abstract(pmid):
    print(get(f"{E}/efetch.fcgi?db=pubmed&id={pmid}&rettype=abstract&retmode=text"))


def doi(d):
    m = get("https://api.crossref.org/works/" + urllib.parse.quote(d), True)["message"]
    au = ", ".join(f'{a.get("family", "")} {a.get("given", "")}'.strip() for a in m.get("author", []))
    print(m["title"][0]); print(au)
    print(m.get("container-title", [""])[0], m["issued"]["date-parts"][0], "Bd.", m.get("volume"), "Nr.", m.get("issue"), m.get("page") or m.get("article-number"))
    print(re.sub("<[^>]+>", "", m.get("abstract", "(kein Abstract bei Crossref)")))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search"); s.add_argument("term"); s.add_argument("--n", type=int, default=5)
    a = sub.add_parser("abstract"); a.add_argument("pmid")
    c = sub.add_parser("doi"); c.add_argument("doi")
    args = ap.parse_args()
    try:
        {"search": lambda: search(args.term, args.n), "abstract": lambda: abstract(args.pmid), "doi": lambda: doi(args.doi)}[args.cmd]()
    except Exception as e:
        sys.exit(f"Abruf fehlgeschlagen: {e}")
