#!/usr/bin/env python3
"""Belegprüfung und Quellenbox.

  python3 belege_check.py validate daten/belege/<thema>.md
  python3 belege_check.py check daten/entwuerfe/<slug>.md           (Beleg-Datei aus Frontmatter thema_belege)
  python3 belege_check.py finalize daten/entwuerfe/<slug>.md        ([S3] -> [1], baut ## Quellen)

Beleg-Datei (Markdown, siehe .claude/agents/evidence-researcher.md):
  ## Quellen   Tabelle: | ID | Kurzname | Zitat | Kennung | Typ | Qualität |
  ## Aussagen  Tabelle: | ID | Aussage | Zahlen | Quelle | Einschränkung | Geprüft über |
check meldet: unbekannte Quell-IDs, mehr als 6 Quellen, Zahlen (%, Jahre, Monate, Studien, Teilnehmer) in Sätzen
mit Beleg-Zitat, die in den Zahlen/Aussagen der Beleg-Datei nicht vorkommen, Zahlen ohne Beleg im Fließtext
(außer in Zusage, CTA, Praxis), und veraltete Belege (Stand älter als 12 Monate).
"""
import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MAX_QUELLEN = 6
ZAHL = re.compile(r"(\d+(?:[.,]\d+)?)\s?(%|Prozent|Jahre[n]?|Monate[n]?|Studien|Teilnehmer\w*)")


def tabelle(text, ueberschrift):
    m = re.search(rf"^##\s+{ueberschrift}\b.*?\n(.*?)(?=^##\s|\Z)", text, flags=re.M | re.S)
    rows = []
    if m:
        for z in m.group(1).split("\n"):
            if z.startswith("|") and not re.match(r"^\|[\s:-]+\|", z):
                rows.append([c.strip() for c in z.strip().strip("|").split("|")])
    return rows[1:] if rows else []


def belege_lesen(pfad):
    t = Path(pfad).read_text(encoding="utf-8")
    fm = re.match(r"^---\n(.*?)\n---", t, flags=re.S)
    stand = re.search(r"^stand:\s*(\S+)", fm.group(1), flags=re.M) if fm else None
    return t, tabelle(t, "Quellen"), tabelle(t, "Aussagen"), (stand.group(1) if stand else None)


def validate(pfad):
    t, q, a, stand = belege_lesen(pfad)
    fehler = []
    ids = {r[0] for r in q}
    if not q: fehler.append("Tabelle ‚Quellen‘ fehlt oder leer")
    if not a: fehler.append("Tabelle ‚Aussagen‘ fehlt oder leer")
    for r in q:
        if len(r) < 6 or not r[3]: fehler.append(f"Quelle {r[0]}: Kennung (PMID/DOI/URL) fehlt")
    for r in a:
        if len(r) < 6: fehler.append(f"Aussage {r[0]}: Spalten fehlen"); continue
        for sid in re.findall(r"S\d+", r[3]):
            if sid not in ids: fehler.append(f"Aussage {r[0]}: Quelle {sid} unbekannt")
        if not r[5]: fehler.append(f"Aussage {r[0]}: ‚Geprüft über‘ fehlt")
        if not r[4]: fehler.append(f"Aussage {r[0]}: Einschränkung fehlt (auch ‚keine‘ nennen)")
    if not stand: fehler.append("stand: fehlt im Frontmatter")
    elif (date.today() - datetime.strptime(stand, "%Y-%m-%d").date()).days > 365:
        fehler.append(f"Belege älter als 12 Monate (Stand {stand}): neu prüfen")
    print(f"{pfad}: {len(q)} Quellen, {len(a)} Aussagen" + (", FEHLER:" if fehler else ", OK"))
    for f in fehler: print("  - " + f)
    return not fehler


def artikel(pfad):
    t = Path(pfad).read_text(encoding="utf-8")
    fm = re.match(r"^---\n(.*?)\n---\n", t, flags=re.S)
    thema = re.search(r"^thema_belege:\s*(\S+)", fm.group(1), flags=re.M).group(1) if fm else None
    body = t[fm.end():] if fm else t
    return t, body, thema


def check(pfad):
    t, body, thema = artikel(pfad)
    if not thema:
        print("thema_belege fehlt im Frontmatter"); return False
    bpfad = ROOT / "daten" / "belege" / f"{thema}.md"
    if not bpfad.exists():
        print(f"Beleg-Datei {bpfad} fehlt: erst evidence-researcher"); return False
    _, q, a, stand = belege_lesen(bpfad)
    ids = {r[0] for r in q}
    bmap = {r[0]: r for r in a if len(r) >= 6}
    erlaubt = " ".join(" ".join(r) for r in a)
    erlaubt_zahlen = {(m.group(1).replace(",", "."), m.group(2)[0]) for m in ZAHL.finditer(erlaubt)}
    erlaubt_nums = {m.group(1).replace(",", ".") for m in ZAHL.finditer(erlaubt)} | set(re.findall(r"\d+(?:[.,]\d+)?", " ".join(r[2] for r in a)))
    haupt = re.split(r"^##\s+Quellen\b", body, flags=re.M)[0]
    fehler = []
    benutzt = []
    benutzt_b = []
    if not re.search(r"\[[SB]\d+\]", haupt):  # bereits finalisiert: [n] über die Kennungen der Quellenbox zurückübersetzen
        qbox = re.split(r"^##\s+Quellen\b", body, flags=re.M)
        eintraege = re.findall(r"^(\d+)\.\s+(.+)$", qbox[1], flags=re.M) if len(qbox) > 1 else []
        zuordnung = {}
        for n, txt in eintraege:
            for r in q:
                if r[3] and r[3].split("·")[0].strip() and r[3].split("·")[0].strip() in txt:
                    zuordnung[n] = r[0]
        haupt = re.sub(r"\[(\d+)\]", lambda m: f"[{zuordnung.get(m.group(1), 'S0')}]", haupt)
    for kid in re.findall(r"\[([SB]\d+)\]", haupt):
        if kid.startswith("B"):
            if kid not in bmap:
                fehler.append(f"Aussage {kid} nicht in der Beleg-Datei"); continue
            if kid not in benutzt_b: benutzt_b.append(kid)
            sid = (re.findall(r"S\d+", bmap[kid][3]) or ["S0"])[0]
        else:
            sid = kid
        if sid not in ids: fehler.append(f"Quelle {sid} nicht in der Beleg-Datei")
        elif sid not in benutzt: benutzt.append(sid)
    if len(benutzt) > MAX_QUELLEN: fehler.append(f"{len(benutzt)} Quellen im Text (max. {MAX_QUELLEN})")
    for zeile in haupt.split("\n"):
        if zeile.lstrip().startswith(("> Zusage", "> CTA", "> Praxis", "<!--", "title:", "kosten:")): continue
        zb = re.findall(r"\[(B\d+)\]", zeile)
        lokal = set(re.findall(r"\d+(?:[.,]\d+)?", " ".join(bmap[k][2] for k in zb if k in bmap)))
        lokal = {x.replace(",", ".") for x in lokal}
        for m in ZAHL.finditer(zeile):
            num = m.group(1).replace(",", ".")
            if zb and num not in lokal:
                fehler.append(f"Zahl „{m.group(0)}“ steht nicht in der zitierten Aussage ({', '.join(zb)}): {zeile.strip()[:70]}")
            elif num not in erlaubt_nums:
                zitiert = bool(re.search(r"\[S\d+\]|\[\d+\]", zeile))
                fehler.append(f"Zahl „{m.group(0)}“ {'nicht in den Belegen' if zitiert else 'ohne Beleg'}: {zeile.strip()[:70]}")
    if stand and (date.today() - datetime.strptime(stand, "%Y-%m-%d").date()).days > 365:
        fehler.append(f"Belege veraltet (Stand {stand})")
    print(f"{pfad}: {len(benutzt)} Quellen genutzt ({', '.join(benutzt)})" + (" · PRÜFEN:" if fehler else " · OK"))
    for f in fehler: print("  - " + f)
    if "--abgleich" in sys.argv:
        print("  ABGLEICH Satz <-> Beleg (prüfe: sagt der Satz mehr, anderes oder für andere Personen als die Aussage?)")
        for zeile in haupt.split("\n"):
            for k in dict.fromkeys(re.findall(r"\[(B\d+)\]", zeile)):
                if k in bmap:
                    print(f"   - Satz: {re.sub(chr(91) + 'B' + chr(92) + 'd+' + chr(93), '', zeile).strip()[:110]}")
                    print(f"     {k}: {bmap[k][1][:110]} | Einschr.: {bmap[k][4][:110]}")
    else:
        for k in benutzt_b:
            print(f"  {k} Einschränkung (im Satz kurz mitnehmen): {bmap[k][4][:160]}")
    return not fehler


def finalize(pfad):
    t, body, thema = artikel(pfad)
    bpfad = ROOT / "daten" / "belege" / f"{thema}.md"
    _, q, _, _ = belege_lesen(bpfad)
    info = {r[0]: r for r in q}
    haupt = re.split(r"^##\s+Quellen\b", t, flags=re.M)[0]
    _, _, a, _ = belege_lesen(bpfad)
    bmap = {r[0]: r for r in a if len(r) >= 6}

    def zu_s(k):
        return k if k.startswith("S") else (re.findall(r"S\d+", bmap[k][3]) or ["S0"])[0]
    reihenfolge = []
    for k in re.findall(r"\[([SB]\d+)\]", haupt):
        if zu_s(k) not in reihenfolge: reihenfolge.append(zu_s(k))
    neu = {sid: i + 1 for i, sid in enumerate(reihenfolge)}
    haupt = re.sub(r"\[([SB]\d+)\]", lambda m: f"[{neu[zu_s(m.group(1))]}]", haupt)
    liste = []
    for sid in reihenfolge:
        r = info.get(sid)
        if not r: sys.exit(f"{sid} unbekannt")
        liste.append(f"{neu[sid]}. {r[2]} {r[3]}")
    Path(pfad).write_text(haupt.rstrip() + "\n\n## Quellen\n\n" + "\n".join(liste) + "\n", encoding="utf-8")
    print(f"{pfad}: {len(reihenfolge)} Quellen nummeriert und eingetragen")


if __name__ == "__main__":
    args = [x for x in sys.argv if not x.startswith("--")]
    sys.argv = args + [x for x in sys.argv if x.startswith("--")]
    if len(args) != 3 or args[1] not in ("validate", "check", "finalize"):
        sys.exit(__doc__)
    ok = {"validate": validate, "check": check, "finalize": lambda p: finalize(p) or True}[args[1]](args[2])
    sys.exit(0 if ok else 1)
