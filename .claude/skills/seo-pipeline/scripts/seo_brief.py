#!/usr/bin/env python3
"""SEO-Brief je Artikel aus DataForSEO (Quelle fuer Volumen und Begriffe).

Aufruf: python3 seo_brief.py "<keyword>" [--slug <slug>] [--out daten/briefs] [--dry-run]
Schreibt <out>/<slug>.json (Rohdaten) und <out>/<slug>.md (Brief fuer den Writer).

Abrufe pro Brief (Kosten zusammen etwa 0,02-0,03 USD):
  1. Labs keyword_suggestions (Deutschland): Nebenkeywords mit Volumen
  2. SERP organic live advanced (Deutschland): Top 10,
     Ähnliche Fragen, Verwandte Suchen, KI-Uebersicht
  3. On-Page instant_pages fuer die Top-5-Seiten: Ueberschriften und Wortzahl (parallel, ca. 0,001 USD)
Zugang: DATAFORSEO_LOGIN und DATAFORSEO_PASSWORD, falls gesetzt. In der
Cloud-Umgebung traegt der Proxy die Zugangsdaten ein, dann sind sie nicht noetig.
Nur Standardbibliothek. Nur lesende Abrufe, nichts wird veroeffentlicht.
"""
import argparse
import concurrent.futures
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HOST = "https://api.dataforseo.com"
LOC_DE = 2276        # Deutschland (Volumen)
LOC_SERP = 2276      # Deutschland: die Artikel sind bundesweit gedacht (Essen nur bei lokalen Keywords)
MARKE = re.compile(r"invisalign|dr\.? ?smile|drsmile|angel ?aligner|spark|clearcorrect|zenyum|plusdental")
FREMD = re.compile(r"schweiz|österreich|oesterreich|wien|türkei|tuerkei|ungarn|polen|zürich|indien|thailand")
SEP = "|"
VERSUCHE = 5
SKIP_DOMAINS = re.compile(r"reddit|youtube|wikipedia|facebook|instagram|amazon")


def roh_html(url):
    import urllib.request
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; Kieferblick-SEO-Brief)"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read(2_500_000).decode("utf-8", "ignore")


def elemente(url):
    """Nur Zählung (Tabellen, FAQ-Fragen), kein Text wird gespeichert."""
    try:
        h = roh_html(url)
        h = re.sub(r"<(nav|footer|aside|header)\b.*?</\1>", "", h, flags=re.S | re.I)
        frag = len(set(re.findall(r"<h[2-6][^>]*>\s*(?:<[^>]+>\s*)*([^<]{8,140}\?)\s*<", h))) + len(re.findall(r"<summary\b", h))
        return len(re.findall(r"<table\b", h)), frag
    except Exception:
        return None, None


def wettbewerb(org):
    """Struktur der Top-Seiten (nur Ueberschriften und Wortzahl, nie der Text): DataForSEO On-Page instant_pages."""
    def holen(o):
        try:
            d, t = post("/v3/on_page/instant_pages", [{"url": o["url"], "load_resources": False, "enable_javascript": False}])
            it = (t.get("result") or [{}])[0]["items"][0]
            m = it.get("meta") or {}
            h = m.get("htags") or {}
            tab, faq = elemente(o["url"])
            return {"rang": o["rang"], "domain": o["domain"], "url": o["url"], "tabellen": tab, "faq": faq,
                    "woerter": (m.get("content") or {}).get("plain_text_word_count"),
                    "h2": h.get("h2") or [], "h3": (h.get("h3") or [])[:12], "kosten": d.get("cost", 0)}
        except Exception as e:  # nicht abrufbar: kein Abbruch
            return {"rang": o["rang"], "domain": o["domain"], "url": o["url"], "woerter": None, "h2": [], "h3": [], "fehler": str(e)[:60], "kosten": 0}
    kandidaten = [o for o in org if not SKIP_DOMAINS.search(o["domain"])][:5]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
        return list(ex.map(holen, kandidaten))


def slugify(k):
    s = k.lower().translate(str.maketrans("äöüß", "aous"))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def post(path, body):
    headers = {"Content-Type": "application/json"}
    login, pw = os.environ.get("DATAFORSEO_LOGIN"), os.environ.get("DATAFORSEO_PASSWORD")
    if login and pw:
        headers["Authorization"] = "Basic " + base64.b64encode(f"{login}:{pw}".encode()).decode()
    req = urllib.request.Request(HOST + path, data=json.dumps(body).encode(), headers=headers)
    d = None
    for versuch in range(1, VERSUCHE + 1):   # Gateway-Fehler (502/503/504), 429 und Zeitüberschreitungen: wiederholen
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                d = json.load(r)
            break
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or versuch == VERSUCHE:
                sys.exit(f"DataForSEO HTTP {e.code} bei {path} nach {versuch} Versuch(en)")
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if versuch == VERSUCHE:
                sys.exit(f"DataForSEO nicht erreichbar bei {path} nach {versuch} Versuch(en): {e}")
        time.sleep(2 ** versuch)             # 2, 4, 8, 16 s
    t = d["tasks"][0]
    if t.get("status_code") != 20000:
        sys.exit(f"DataForSEO-Fehler {t.get('status_code')}: {t.get('status_message')}")
    return d, t


def abrufen(keyword):
    kosten = 0.0
    d, t = post("/v3/dataforseo_labs/google/keyword_suggestions/live", [{
        "keyword": keyword, "language_code": "de", "location_code": LOC_DE, "limit": 80,
        "include_seed_keyword": True,
        "order_by": ["keyword_info.search_volume,desc"],
        "filters": [["keyword_info.search_volume", ">", 0]]}])
    kosten += d.get("cost", 0)
    res = (t.get("result") or [{}])[0]
    seed = res.get("seed_keyword_data") or {}
    sug = [{"keyword": i["keyword"], "volumen": i["keyword_info"]["search_volume"],
            "schwierigkeit": (i.get("keyword_properties") or {}).get("keyword_difficulty"),
            "intent": (i.get("search_intent_info") or {}).get("main_intent")}
           for i in res.get("items") or []]
    d, t = post("/v3/serp/google/organic/live/advanced", [{
        "keyword": keyword, "language_code": "de", "location_code": LOC_SERP, "depth": 10}])
    kosten += d.get("cost", 0)
    res = (t.get("result") or [{}])[0]
    items = res.get("items") or []
    serp = {
        "organisch": [{"rang": i["rank_group"], "domain": i["domain"], "titel": i["title"], "url": i["url"]}
                      for i in items if i["type"] == "organic"][:10],
        "fragen": [q.get("title") for i in items if i["type"] == "people_also_ask" for q in i.get("items") or []],
        "verwandt": [x for i in items if i["type"] == "related_searches" for x in i.get("items") or []],
        "typen": sorted({i["type"] for i in items}),
    }
    seiten = wettbewerb(serp["organisch"])
    kosten += sum(s.get("kosten", 0) for s in seiten)
    seed_info = (seed.get("keyword_info") or {})
    vol = seed_info.get("search_volume")
    if vol is None:  # Seed fehlt in den Vorschlaegen: Volumen gezielt nachholen
        d, t = post("/v3/dataforseo_labs/google/keyword_overview/live", [{
            "keywords": [keyword], "language_code": "de", "location_code": LOC_DE}])
        kosten += d.get("cost", 0)
        for i in ((t.get("result") or [{}])[0].get("items") or []):
            vol = (i.get("keyword_info") or {}).get("search_volume")
    return {"keyword": keyword, "volumen": vol,
            "seed_gefunden": bool(seed), "vorschlaege": sug, "serp": serp, "wettbewerb": seiten, "kosten_usd": round(kosten, 4)}


def brief_md(b, slug):
    sug = [s for s in b["vorschlaege"] if s["keyword"] != b["keyword"] and not FREMD.search(s["keyword"])]
    gesehen, einzig = set(), []
    for s in sug:  # Wortstellungs-Doppelungen ("zaehne im alter" / "im alter zaehne") zusammenfassen
        key = frozenset(re.findall(r"\w+", s["keyword"]))
        if key not in gesehen:
            gesehen.add(key)
            einzig.append(s)
    sug = einzig
    ok = [s for s in sug if not MARKE.search(s["keyword"])]
    marke = [s for s in sug if MARKE.search(s["keyword"])]
    neben = ok[:12]
    serp = b["serp"]
    vol = b["volumen"]
    z = [f"# SEO-Brief: {b['keyword']}", "",
         f"Quelle: DataForSEO (Labs Deutschland, SERP Deutschland, On-Page-Struktur der Top-Seiten), Abruf-Kosten {b['kosten_usd']} USD. "
         "Volumen = Suchen pro Monat laut DataForSEO, bundesweit; gerundet, nicht mit der Excel vergleichbar.", "",
         "## Hauptphrase",
         f"- **{b['keyword']}** · Volumen: {vol if vol is not None else 'keine Daten (kein Hinweis auf null Suchen)'}",
         f"- Slug: `{slug}`", "",
         "## Nebenkeywords (in Überschriften, FAQ und Text einbauen, nie stopfen)",
         "| Phrase | Volumen | Schwierigkeit | Intent |", "|---|---|---|---|"]
    for s in neben:
        z.append(f"| {s['keyword']} | {s['volumen']} | {s['schwierigkeit'] if s['schwierigkeit'] is not None else '–'} | {s['intent'] or '–'} |")
    if marke:
        z += ["", "Markenbegriffe (sachlich nutzbar, wo sie dem Leser helfen; nicht als eigene Leistung ausgeben, nicht wertend vergleichen): "
              + ", ".join(f"{s['keyword']} ({s['volumen']})" for s in marke[:5])]
    z += ["", "## Fragen der Suchenden („Ähnliche Fragen“)"]
    z += [f"- {q}" for q in serp["fragen"]] or ["- keine"]
    z += ["", "Als H2 oder FAQ-Frage beantworten, wenn sie zum Artikel passen. Nur, was mit `material/fakten.md` oder einer Quelle belegbar ist.",
          "", "## Verwandte Suchen"]
    z += [f"- {q}" for q in serp["verwandt"]] or ["- keine"]
    z += ["", "## Wer rankt (bundesweit)", "| Rang | Domain | Titel |", "|---|---|---|"]
    for o in serp["organisch"]:
        z.append(f"| {o['rang']} | {o['domain']} | {o['titel'].replace(SEP, '/')} |")
    wb = b.get("wettbewerb") or []
    langtexte = sorted(s["woerter"] for s in wb if s.get("woerter") and s["woerter"] >= 800)
    tabs = sorted(s["tabellen"] for s in wb if s.get("tabellen") is not None)
    faqs = sorted(s["faq"] for s in wb if s.get("faq") is not None)
    z += ["", "## Wettbewerber-Struktur (Top-Ergebnisse bundesweit; nur Überschriften und Länge, kein Text übernehmen)"]
    if langtexte:
        med = langtexte[len(langtexte) // 2]
        z += [f"Wortzahl der ausführlichen Seiten (ab 800 Wörter): {', '.join(map(str, langtexte))} · Median {med} · **Empfohlene Ziel-Länge: {int(med * 0.8 // 100 * 100)}–{int(med * 1.2 // 100 * 100)} Wörter**", ""]
    if tabs:
        z += [f"Wettbewerber-Elemente (Median der abrufbaren Seiten): Tabellen {tabs[len(tabs) // 2]} · FAQ-Fragen {faqs[len(faqs) // 2] if faqs else 0}", ""]
    z += ["| Rang | Domain | Wörter | Tab | FAQ | Überschriften (H2) |", "|---|---|---|---|---|---|"]
    for s in wb:
        h2 = "; ".join(x.strip().replace(SEP, "/")[:60] for x in s["h2"][:8]) or ("nicht abrufbar" if s.get("fehler") else "–")
        z.append(f"| {s['rang']} | {s['domain']} | {s['woerter'] or '–'} | {s.get('tabellen') if s.get('tabellen') is not None else '–'} | {s.get('faq') if s.get('faq') is not None else '–'} | {h2} |")
    z += ["", "Auswertung durch den Planer: Themen, die mehrere Seiten behandeln (Pflicht-Abschnitte), und Themen, die fehlen (unsere Lücken)."]
    ki = "ja" if "ai_overview" in serp["typen"] else "nein"
    z += ["", f"SERP-Elemente: {', '.join(serp['typen'])}. KI-Übersicht: **{ki}**"
          + (" (Einstieg als kurze, direkte Antwort schreiben)." if ki == "ja" else "."),
          "", "## Vorgaben Yoast und Platzierung",
          f"- Fokus-Keyword (`_yoast_wpseo_focuskw`): **{b['keyword']}**",
          f"- SEO-Titel (`_yoast_wpseo_title`, Frontmatter `seo_titel`): höchstens 60 Zeichen inkl. „| Kieferblick“, Hauptphrase möglichst am Anfang, keine Doppelung mit Wettbewerbertiteln.",
          "- Meta-Beschreibung (`_yoast_wpseo_metadesc`, Frontmatter `meta_description`): 120–155 Zeichen, Hauptphrase enthalten, nennt den Nutzen, endet ohne Druck-CTA.",
          f"- Hauptphrase (oder nächste natürliche Form) in: Titel/H1, Slug, ersten 100 Wörtern, 1–2 H2, einem Bild-Alt-Text, Meta. Dichte etwa 0,5–2,5 % (nicht stopfen), in jedem Drittel des Textes mindestens einmal.",
          "- Mindestens 4 der Nebenkeywords wörtlich oder in natürlicher Beugung, davon 2 als H2 oder FAQ-Frage.",
          "- Interne Links: 2–4 aus `daten/linkplan.csv` (Cluster), 1 Leistungsseite. Nur existierende Seiten."]
    return "\n".join(z) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keyword")
    ap.add_argument("--slug")
    ap.add_argument("--out", default="daten/briefs")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    kw = a.keyword.strip().lower()
    slug = a.slug or slugify(kw)
    if a.dry_run:
        print(f"DRY-RUN: 2 Abrufe (Labs keyword_suggestions DE {LOC_DE}, SERP Deutschland {LOC_SERP}) fuer '{kw}', ca. 0,02 USD, Ziel {a.out}/{slug}.*")
        return
    b = abrufen(kw)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{slug}.json").write_text(json.dumps(b, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / f"{slug}.md").write_text(brief_md(b, slug), encoding="utf-8")
    print(f"{out}/{slug}.md · Volumen {b['volumen']} · {len(b['vorschlaege'])} Nebenkeywords · "
          f"{len(b['serp']['fragen'])} Fragen · {b['kosten_usd']} USD")


if __name__ == "__main__":
    main()
