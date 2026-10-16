#!/usr/bin/env python3
"""Literaturrecherche für den Quellenspeicher: PubMed (eutils) und Crossref. Nur Standardbibliothek.

  quellen.py search "<suchbegriff>" [--n 5]   PubMed-Treffer mit Titel, Journal, Jahr, DOI
  quellen.py abstract <pmid>                   Abstract und Metadaten (Text)
  quellen.py doi <doi>                         Crossref-Metadaten und Abstract
  quellen.py openalex "<suchbegriff>" [--n 5]  OpenAlex (Zitierzahlen, Open Access; braucht OPENALEX_API_KEY)
Der Aufruf läuft über den Proxy der Umgebung (HTTPS_PROXY). Das WebFetch-Werkzeug nicht verwenden.
"""
import argparse, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

E = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def get(url, as_json=False):
    # NCBI erlaubt ohne Schlüssel ca. 3 Anfragen pro Sekunde: kurze Pause, bei 429 Wiederholung
    req = urllib.request.Request(url, headers={"User-Agent": "kieferblick-quellen/1.0"})
    for versuch in range(4):
        time.sleep(0.5)
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                data = r.read().decode("utf-8", "replace")
            return json.loads(data) if as_json else data
        except urllib.error.HTTPError as e:
            if e.code != 429 or versuch == 3:
                raise
            time.sleep(2 * (versuch + 1))


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


def openalex(term, n, sort):
    """OpenAlex (kostenlos, Schlüssel in OPENALEX_API_KEY nötig; ohne Schlüssel teilt sich das Tageslimit das ganze Netz)."""
    key = os.environ.get("OPENALEX_API_KEY")
    if not key:
        sys.exit("OPENALEX_API_KEY fehlt (kostenloser Schlüssel: https://help.openalex.org/api/authentication/, als Umgebungs-Secret setzen).")
    flt = "type:article"
    q = {"search": term, "per-page": n, "sort": sort, "filter": flt,
         "select": "doi,title,publication_year,cited_by_count,primary_location,open_access,type,authorships",
         "api_key": key}
    res = get("https://api.openalex.org/works?" + urllib.parse.urlencode(q), True)["results"]
    for w in res:
        src = ((w.get("primary_location") or {}).get("source") or {}).get("display_name", "")
        au = ", ".join(a["author"]["display_name"] for a in w.get("authorships", [])[:3])
        print(f'{w["publication_year"]} | zitiert {w["cited_by_count"]} | {src} | {au} | {w["title"]} | {w.get("doi")} | OA: {(w.get("open_access") or {}).get("oa_status")}')


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
    o = sub.add_parser("openalex"); o.add_argument("term"); o.add_argument("--n", type=int, default=5); o.add_argument("--sort", default="relevance_score:desc", help="relevance_score:desc (Standard) oder cited_by_count:desc")
    args = ap.parse_args()
    try:
        {"search": lambda: search(args.term, args.n), "abstract": lambda: abstract(args.pmid), "doi": lambda: doi(args.doi),
         "openalex": lambda: openalex(args.term, args.n, args.sort)}[args.cmd]()
    except Exception as e:
        sys.exit(f"Abruf fehlgeschlagen: {e}")
