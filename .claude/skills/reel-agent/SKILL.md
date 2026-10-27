---
name: reel-agent
description: B2B-Social-Agent für BiteCentric (Zahnärzte in US, UK, CA, AU, NZ, IE), Kanäle Reels und LinkedIn. Erfasst Benchmark-Beiträge, findet Gewinner (Faktor über eigenem Median), remixt deren Struktur auf funktionelle Aligner-Planung und liefert wöchentlich 10 Hooks, 3 Reel-Skripte und LinkedIn-Post-Entwürfe auf Englisch zur Freigabe. Nutzen für die Montags-Wochenliste, nach einem Scout-Lauf oder LinkedIn-Export, bei neuen Reel- oder Post-Ideen und wenn Alexander eigene Zahlen einträgt.
---
# reel-agent

Dritter Hauptagent neben seo-pipeline und ad-writing, aber für den **B2B-Zweig** (BiteCentric), nicht für Kieferblick. **Kanäle:** Reels (Instagram, Hauptteil unten) und LinkedIn als zweites Modul (`references/linkedin.md`, Daten `daten/linkedin/`, Importskript `scripts/li_import.py`). Er **liest und bereitet vor**: nichts posten, kommentieren, folgen oder senden. Alexander gibt frei und filmt.

**Sprache:** mit Alexander Deutsch, alle Reel-Inhalte (Hooks, Skripte, Captions) Englisch. Kontext, Marke, Angebot: `kontext/b2b-bitecentric.md` (zuerst lesen); englische Begriffe, Einstiege und Lücken für US/UK u. a.: `kontext/b2b-bitecentric-en.md`. Daten: `daten/reels/` (`raw/`, `frames/`, `library/`, `output/`).

## Sechs Bausteine
1. **Scout** (läuft lokal im eingeloggten Browser, Details `references/scout-browser.md`): Grid-Views, Caption, Likes, Kommentare, Datum, Frames der ersten Sekunden. Ergebnis als CSV in `daten/reels/raw/<Datum>_<handle>.csv` (Spalten wie `2026-10-27_top.csv`). Keine Videos herunterladen.
2. **Analyse:** `python3 .claude/skills/reel-agent/scripts/reels.py winners` rechnet Faktor über Median und markiert wahrscheinlich beworbene Reels. Danach zerlegt der Agent jeden übertragbaren Gewinner in `account | views | Faktor | Datum | hook_text | hook_type | format | topic | trigger | cta | likely_boosted`. Gewinner = Faktor ≥ 3 über dem Median des eigenen Accounts. Ausreißer und Fremdthemen (privat, Lifestyle, Kurswerbung) nennen, nicht übernehmen. Neue Muster in `library/hooks.csv` (Art „muster“).
3. **Remix:** Struktur übernehmen (Hook-Typ, Format, Ablauf), **nie Inhalt oder Wortlaut**. Jeder Remix nennt sein Vorbild (Account, Reel, Views, Faktor). Thema: funktionelle Aligner-Planung in zentrischer Kieferrelation für Allgemeinzahnärzte.
4. **Generator:** je Woche 10 Hooks und 3 Skripte, Regeln in `references/generator.md`.
5. **Marken- und Rechtsfilter:** erst `reels.py check <Wochenliste>`, dann Agent `reel-reviewer`. Ergebnis je Idee ✅ / ⚠️ / ❌ mit Grund. Regeln in `references/filter.md`, Muster in `references/filter.json`.
6. **Lernschleife:** Alexander trägt Zahlen eigener Reels in `library/own_performance.csv` ein. `reels.py own` vergleicht Hook-Typ, Format, Trigger. Unter 6 Reels (oder 3 je Gruppe) nur Hinweis, nicht gewichten.

## Wochenablauf (Montag)
1. `reels.py status`, neue Rohdaten in `raw/` prüfen. Fehlt ein frischer Scout-Lauf, mit den vorhandenen Daten arbeiten und die Lücke benennen.
2. `reels.py winners`, `reels.py own`.
3. Hooks und Reel-Skripte schreiben (`references/generator.md`), dazu 1–3 LinkedIn-Posts (`references/linkedin.md`). Wochenliste `daten/reels/output/<Datum>_weekly.md` mit den sechs Abschnitten aus `references/wochenliste.md`.
4. `reels.py check <Datei>` bis ohne FEHLER, dann `reel-reviewer` auf die Datei, Befunde einarbeiten.
5. Neue Hooks (Status „entwurf“) und Muster in `library/hooks.csv`. Freigegebene Hooks setzt Alexander auf „freigegeben“.
6. Nach dem ersten Lauf 3–5 weitere Benchmark-Accounts vorschlagen (Okklusion, Kiefergelenk, Funktion; CA/AU), als Vorschlag in Abschnitt 6, nicht eigenmächtig in `benchmarks.csv`.

## Regeln
- Annahmen immer als „Annahme“ kennzeichnen. Fehlende Daten als Lücke benennen, keine Zahlen erfinden. Fehlende Hook-Texte: „spoken hook: unknown“.
- Preise stehen nicht in Reels. Kommentar-Stichworte nur COURSE, CASE, BOOK (`references/filter.json`). Einstiege englisch: Free Online Course, Free Case Review (`kontext/b2b-bitecentric-en.md`, Abschnitt 5); URLs offen, bis dahin Platzhalter „[Einstieg EN]“.
- Alles, was Alexander persönlich erlebt haben müsste, bleibt mit [ ] offen. Klinische Aussagen mit [CHECK].
- Rückgängig nicht machbares (Zugriff auf Konten, Kosten, Posten) nur nach Rückfrage. Dieser Agent braucht keine Schreibrechte auf Instagram.

## Testfälle
`tests/faelle.md`.
