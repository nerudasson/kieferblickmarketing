#!/usr/bin/env python3
"""PubMed-Recherche fuer den article-writer (NCBI E-utilities, nur Standardbibliothek, lesend, kostenlos).

  python3 pubmed.py suche "<englische Suchanfrage>" [--n 8] [--typ leitlinie|review|studie] [--ab 2015]
  python3 pubmed.py abstract <PMID> [<PMID> ...]

Gibt je Treffer PMID, Jahr, Journal, Publikationstyp, DOI, Titel und (bei `abstract`) den Abstract aus.
Regeln: Aussagen nur aus dem Abstract oder Volltext uebernehmen, nie aus dem Gedaechtnis.
Ohne API-Key sind 3 Anfragen pro Sekunde erlaubt; das Skript wartet entsprechend.
"""
import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
TYPEN = {
    "leitlinie": '("Practice Guideline"[pt] OR "Guideline"[pt] OR guideline[ti] OR consensus[ti])',
    "review": '("Systematic Review"[pt] OR "Meta-Analysis"[pt] OR "Cochrane Database Syst Rev"[ta])',
    "studie": '("Randomized Controlled Trial"[pt] OR "Clinical Trial"[pt] OR "Cohort Studies"[mh])',
}


def get(path, **params):
    time.sleep(0.4)
    url = BASE + path + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read().decode("utf-8")


def suche(q, n, typ, ab):
    term = q
    if typ:
        term += " AND " + TYPEN[typ]
    if ab:
        term += f' AND ("{ab}"[dp] : "3000"[dp])'
    ids = json.loads(get("esearch.fcgi", db="pubmed", retmode="json", retmax=n, sort="relevance", term=term))["esearchresult"]["idlist"]
    if not ids:
        print("Keine Treffer. Anfrage breiter fassen (englische Fachbegriffe, weniger AND).")
        return
    zeigen(ids, mit_abstract=False)


def zeigen(ids, mit_abstract):
    xml = get("efetch.fcgi", db="pubmed", retmode="xml", id=",".join(ids))
    root = ET.fromstring(xml)
    for art in root.findall(".//PubmedArticle"):
        pmid = art.findtext(".//PMID")
        titel = "".join(art.find(".//ArticleTitle").itertext()) if art.find(".//ArticleTitle") is not None else ""
        jahr = art.findtext(".//PubDate/Year") or (art.findtext(".//PubDate/MedlineDate") or "")[:4]
        journal = art.findtext(".//Journal/ISOAbbreviation") or art.findtext(".//Journal/Title") or ""
        typen = ", ".join(t.text for t in art.findall(".//PublicationType"))
        doi = next((e.text for e in art.findall(".//ArticleId") if e.get("IdType") == "doi"), "")
        print(f"PMID {pmid} · {jahr} · {journal} · {typen}\n  DOI {doi}\n  {titel}")
        if mit_abstract:
            teile = []
            for a in art.findall(".//Abstract/AbstractText"):
                lab = a.get("Label")
                txt = "".join(a.itertext())
                teile.append(f"{lab}: {txt}" if lab else txt)
            print("  ABSTRACT: " + (" ".join(teile) if teile else "(keiner vorhanden, nicht verwenden)"))
        print()


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("suche"); s.add_argument("anfrage"); s.add_argument("--n", type=int, default=8)
    s.add_argument("--typ", choices=TYPEN); s.add_argument("--ab", type=int)
    a = sub.add_parser("abstract"); a.add_argument("pmid", nargs="+")
    x = ap.parse_args()
    if x.cmd == "suche":
        suche(x.anfrage, x.n, x.typ, x.ab)
    else:
        zeigen([re.sub(r"\D", "", p) for p in x.pmid], mit_abstract=True)


if __name__ == "__main__":
    main()
