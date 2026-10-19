#!/usr/bin/env python3
"""Markdown-Entwurf -> WordPress-Entwurf (status=draft, nie publish).

  python3 wp_publish.py daten/entwuerfe/<slug>.md --dry-run [--out datei.html]
  python3 wp_publish.py daten/entwuerfe/<slug>.md            legt den Entwurf an (POST)
  python3 wp_publish.py daten/entwuerfe/<slug>.md --update <post-id>

Blöcke wie in den bestehenden Entwürfen (Gutenberg + Klassen kb-merksatz, kb-hinweis, kb-cta, kb-faq, kb-quellen,
kb-vergleich). Setzt Kategorie, Auszug, Theme-Felder (kb_kurz, kb_ursache, kb_behandlung, kb_dauer, kb_kosten, kb_ablauf)
und Yoast (_yoast_wpseo_title, _yoast_wpseo_metadesc, _yoast_wpseo_focuskw).
Verweigert: [FAKT FEHLT], nicht ausgefüllte <!-- SCHREIBEN -->, nicht bestandene Prüfskripte. Zugang: Proxy der Umgebung
(WP_URL/WP_USER/WP_APP_PASSWORD optional als Umgebungsvariablen).
"""
import argparse
import base64
import datetime
import html
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
WP = os.environ.get("WP_URL", "https://kieferblick.de").rstrip("/")


def api(pfad, daten=None, methode=None):
    h = {"Content-Type": "application/json"}
    u, p = os.environ.get("WP_USER"), os.environ.get("WP_APP_PASSWORD")
    if u and p:
        h["Authorization"] = "Basic " + base64.b64encode(f"{u}:{p}".encode()).decode()
    req = urllib.request.Request(WP + "/wp-json/wp/v2/" + pfad, data=json.dumps(daten).encode() if daten is not None else None,
                                 headers=h, method=methode or ("POST" if daten is not None else "GET"))
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def link_ziele():
    """Pfade aller Seiten/Beiträge auf der Website: veröffentlicht oder (nur Beiträge) als Entwurf mit erwartetem Pfad."""
    ok, entwurf = set(), set()
    for typ in ("pages", "posts"):
        for st in ("publish", "draft"):
            try:
                for x in api(f"{typ}?per_page=100&status={st}&context=edit&_fields=id,slug,link,categories"):
                    if st == "publish":
                        ok.add(re.sub(r"^https?://[^/]+", "", x["link"]))
                    elif typ == "posts":
                        entwurf.add(x["slug"])
            except Exception:
                return None, None
    return ok, entwurf


def links_pruefen(body):
    ok, entwurf = link_ziele()
    if ok is None:
        return ["Link-Prüfung nicht möglich (Website nicht erreichbar)"], []
    fehler, warnungen = [], []
    for ziel in sorted(set(re.findall(r"\]\((/[^)#?]*)\)", body))):
        if ziel in ok: continue
        slug = ziel.rstrip("/").split("/")[-1]
        (warnungen if slug in entwurf else fehler).append(
            f"Link {ziel}: " + ("Zielartikel ist noch Entwurf (gilt erst nach Veröffentlichung)" if slug in entwurf else "Seite existiert nicht auf kieferblick.de"))
    return fehler, warnungen


def frontmatter(t):
    m = re.match(r"^---\n(.*?)\n---\n", t, flags=re.S)
    fm, key = {}, None
    for z in m.group(1).split("\n"):
        mm = re.match(r"^(\w+):\s*(.*)$", z)
        if mm and not z.startswith(" "):
            key = mm.group(1); v = mm.group(2).strip()
            fm[key] = "" if v == "|" else v.strip('"')
        elif key and z.startswith("  "):
            fm[key] = (fm[key] + "\n" + z.strip()).strip("\n")
    return fm, t[m.end():]


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\s?(?:\[\d+\])+(?!\()", lambda m: "<sup>" + ", ".join(re.findall(r"\d+", m.group(0))) + "</sup>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    return s


def p(text, cls=None, pre=""):
    a = f' {{"className":"{cls}"}}' if cls else ""
    c = f' class="{cls}"' if cls else ""
    return f"<!-- wp:paragraph{a} -->\n<p{c}>{pre}{inline(text)}</p>\n<!-- /wp:paragraph -->"


def liste(items, geordnet=False, cls=None):
    tag = "ol" if geordnet else "ul"
    attrs = {}
    if geordnet: attrs["ordered"] = True
    if cls: attrs["className"] = cls
    a = " " + json.dumps(attrs) if attrs else ""
    c = f' class="{cls}"' if cls else (' class="wp-block-list"' if not geordnet else "")
    li = "".join(f"<!-- wp:list-item --><li>{inline(i)}</li><!-- /wp:list-item -->" for i in items)
    return f"<!-- wp:list{a} -->\n<{tag}{c}>{li}</{tag}>\n<!-- /wp:list -->"


def tabelle(zeilen):
    z = [[c.strip() for c in r.strip().strip("|").split("|")] for r in zeilen if not re.match(r"^\|(?:[\s:-]+\|)+$", r.strip())]
    kopf, rest = z[0], z[1:]
    th = "".join(f"<th>{inline(c)}</th>" for c in kopf)
    tr = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rest)
    return f'<!-- wp:table {{"className":"kb-vergleich"}} -->\n<figure class="wp-block-table kb-vergleich"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></figure>\n<!-- /wp:table -->'


def details(frage, inner, cls, offen=False):
    attr = ',"showContent":true' if offen else ""
    op = " open" if offen else ""
    return f'<!-- wp:details {{"className":"{cls}"{attr}}} -->\n<details class="wp-block-details {cls}"{op}><summary>{inline(frage)}</summary>{inner}</details>\n<!-- /wp:details -->'


def parse_blocks(body):
    """Liefert Liste (typ, daten) in Reihenfolge."""
    bl, puffer, i = [], [], 0
    zeilen = body.split("\n")

    def flush():
        if puffer:
            bl.append(("p", " ".join(puffer))); puffer.clear()
    while i < len(zeilen):
        s = zeilen[i].strip()
        if not s:
            flush()
        elif s.startswith("###"):
            flush(); bl.append(("h3", s[3:].strip()))
        elif s.startswith("##"):
            flush(); bl.append(("h2", s[2:].strip()))
        elif s.startswith("|"):
            flush(); t = []
            while i < len(zeilen) and zeilen[i].strip().startswith("|"):
                t.append(zeilen[i]); i += 1
            bl.append(("table", t)); continue
        elif re.match(r"^(-|\*)\s", s):
            flush(); it = []
            while i < len(zeilen) and re.match(r"^(-|\*)\s", zeilen[i].strip()):
                it.append(re.sub(r"^(-|\*)\s+", "", zeilen[i].strip())); i += 1
            bl.append(("ul", it)); continue
        elif re.match(r"^\d+\.\s", s):
            flush(); it = []
            while i < len(zeilen) and re.match(r"^\d+\.\s", zeilen[i].strip()):
                it.append(re.sub(r"^\d+\.\s+", "", zeilen[i].strip())); i += 1
            bl.append(("ol", it)); continue
        elif s.startswith(">"):
            flush(); q = []
            while i < len(zeilen) and zeilen[i].strip().startswith(">"):
                q.append(zeilen[i].strip().lstrip(">").strip()); i += 1
            bl.append(("quote", " ".join(x for x in q if x))); continue
        else:
            puffer.append(s)
        i += 1
    flush()
    return bl


def render(body):
    out, i, bl = [], 0, parse_blocks(body)
    sektion = ""
    while i < len(bl):
        typ, d = bl[i]
        if typ == "h2":
            sektion = d
            if d != "Quellen":  # die Quellenbox trägt ihre eigene Überschrift (Summary), kein zusätzliches H2
                out.append(f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{inline(d)}</h2>\n<!-- /wp:heading -->')
            i += 1; continue
        if sektion == "Quellen" and typ == "ol":
            li = "".join(f"<!-- wp:list-item --><li>{inline(x)}</li><!-- /wp:list-item -->" for x in d)
            out.append(details("Quellen", f'<!-- wp:list {{"ordered":true}} -->\n<ol>{li}</ol>\n<!-- /wp:list -->', "kb-quellen", offen=True)); i += 1; continue
        if sektion.startswith("Häufige Fragen") and typ == "h3":
            frage, inner = d, []
            i += 1
            while i < len(bl) and bl[i][0] not in ("h2", "h3"):
                t2, d2 = bl[i]
                inner.append(p(d2) if t2 == "p" else liste(d2, t2 == "ol") if t2 in ("ul", "ol") else "")
                i += 1
            out.append(details(frage, "".join(inner), "kb-faq")); continue
        if typ == "p": out.append(p(d))
        elif typ == "h3": out.append(f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{inline(d)}</h3>\n<!-- /wp:heading -->')
        elif typ == "ul": out.append(liste(d))
        elif typ == "ol": out.append(liste(d, True))
        elif typ == "table": out.append(tabelle(d))
        elif typ == "quote":
            m = re.match(r"^(Merksatz|CTA|Praxis|Zusage):\s*(.*)$", d)
            if not m: out.append(p(d, "kb-hinweis"))
            elif m.group(1) == "Merksatz": out.append(p(m.group(2), "kb-merksatz"))
            elif m.group(1) == "CTA": out.append(p(m.group(2), "kb-cta"))
            elif m.group(1) == "Praxis": out.append(p(m.group(2), "kb-hinweis", "<strong>Aus der Praxis:</strong> "))
            else: out.append(p(m.group(2), "kb-hinweis", "<strong>So arbeiten wir:</strong> "))
        i += 1
    return "\n\n".join(x for x in out if x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("datei")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--update", type=int)
    a = ap.parse_args()
    pfad = Path(a.datei)
    t = pfad.read_text(encoding="utf-8")
    fm, body = frontmatter(t)
    fehler = []
    if "FAKT FEHLT" in t: fehler.append("[FAKT FEHLT] offen: Entwurf ist nicht veröffentlichungsfähig")
    if "<!-- SCHREIBEN" in t: fehler.append("Skelett nicht ausgefüllt")
    elif re.search(r"<!--(?!\s*/?wp:)", body): fehler.append("HTML-Kommentar im Text (würde als sichtbarer Text erscheinen): pipeline.py abschluss <slug> entfernt ihn")
    for k in ("title", "slug", "kategorie", "seo_titel", "meta_description", "fokus_keyword"):
        if not fm.get(k): fehler.append(f"Frontmatter {k} leer")
    if not a.dry_run:
        for name, cmd in (("lesbarkeit.py", [HERE / "lesbarkeit.py", pfad]), ("belege_check.py check", [HERE / "belege_check.py", "check", pfad]), ("hwg_check.py", [HERE / "hwg_check.py", pfad])):
            r = subprocess.run([sys.executable, *map(str, cmd)], capture_output=True, text=True)
            if r.returncode != 0: fehler.append(f"{name} meldet PRÜFEN")
    lf, lw = links_pruefen(body)
    fehler += lf
    for w in lw: print("Hinweis: " + w)
    if fehler and not a.dry_run:
        sys.exit("Abbruch:\n- " + "\n- ".join(fehler))
    inhalt = render(body)
    sichtbar = re.sub(r"<[^>]+>", " ", re.sub(r"<!--.*?-->", "", inhalt, flags=re.S))
    for m in sorted(set(re.findall(r"\[[^\]]{1,60}\]", sichtbar)))[:5]:
        print(f"Hinweis: eckige Klammern im Text ({m}): das Theme färbt sie als Platzhalter gelb, bitte umformulieren")
    if a.dry_run:
        for f in fehler: print("Hinweis (würde echten Lauf stoppen): " + f)
        if a.out: Path(a.out).write_text(inhalt, encoding="utf-8")
        print(f"Dry-Run: {len(inhalt)} Zeichen HTML, {inhalt.count('<!-- wp:')} Blöcke" + (f" -> {a.out}" if a.out else ""))
        return
    kat = {c["slug"]: c["id"] for c in api("categories?per_page=100&_fields=id,slug")}
    if fm["kategorie"] not in kat: sys.exit(f"Kategorie {fm['kategorie']} existiert nicht in WordPress")
    meta = {"kb_kurz": fm.get("kurz", ""), "kb_ursache": fm.get("ursache", ""), "kb_behandlung": fm.get("behandlung", ""),
            "kb_geprueft": datetime.date.today().isoformat(), "kb_dauer": fm.get("dauer", ""), "kb_kosten": fm.get("kosten", ""), "kb_ablauf": fm.get("ablauf", ""),
            "_yoast_wpseo_title": fm["seo_titel"], "_yoast_wpseo_metadesc": fm["meta_description"], "_yoast_wpseo_focuskw": fm["fokus_keyword"]}
    import infoboxen  # feste Infobox je Produktgruppe überschreibt die Artikelfelder (material/infoboxen.md)
    for f, v in infoboxen.lade(fm["kategorie"], fm.get("cluster")).items():
        meta["kb_" + f] = v
    daten = {"title": fm["title"], "slug": fm["slug"], "status": "draft", "content": inhalt, "excerpt": fm["meta_description"],
             "categories": [kat[fm["kategorie"]]], "meta": meta}
    bild = json.loads((HERE.parent / "references" / "bausteine.json").read_text(encoding="utf-8")).get("beitragsbild", {}).get(fm["kategorie"])
    if bild: daten["featured_media"] = bild
    r = api(f"posts/{a.update}" if a.update else "posts", daten, "POST")
    print(f"WordPress-Entwurf: ID {r['id']} · Status {r['status']} · {r.get('link')}")


if __name__ == "__main__":
    main()
