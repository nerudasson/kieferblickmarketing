---
name: keyword-research
description: Wählt die nächsten Artikelthemen aus der Keyword-Auswertung (Excel) und schreibt sie mit Kategorie, Thema und Praxis-Flag in die Artikel-Warteschlange; erweitert die Liste bei Bedarf über DataForSEO. Nutzen am Anfang jedes Batches, bei Themenlücken oder wenn die Queue leer ist.
---
# keyword-research

Ziel: die Queue `daten/artikel-queue.csv` füllen. Danach übernimmt `seo-pipeline` (Brief → Plan → Belege → Schreiben).

## Ablauf
1. **Auswahl (Standard):** `python3 .claude/skills/keyword-research/scripts/waehle_keywords.py --top 10 [--thema retainer|aligner|bleaching|…] [--min-vol 50] [--dry-run]`
   - Quelle: `daten/Kieferblick_Keyword-Auswertung_v1.xlsx` (Sheet Keywords_Funnel). Ohne `--dry-run` werden die Zeilen in die Queue geschrieben (Status `offen`).
   - Filter: nur Keywords, die zu einem Thema in `seo-pipeline/references/themen.json` passen; Fremdes (Holz, Möbel, Auslandspreise, Fremdsprachiges) und Markenbegriffe (ohne `--mit-marken`) fallen raus; ähnliche Keywords werden zu **einem** Artikel zusammengelegt (die anderen werden im Brief Nebenkeywords); schon in der Queue vorhandene Themen werden übersprungen.
   - Priorität = Volumen / (1 + Schwierigkeit/10). Excel-Volumen stammen von 2025; der SEO-Brief holt frische DataForSEO-Zahlen.
   - Neue Themen (z. B. Schnarchen, Knirschen): Muster in `themen.json` ergänzen, dann erneut auswählen.
2. **Erweitern (optional):** Neue Seeds in `daten/seeds.txt`, dann `python3 .claude/skills/keyword-research/scripts/dataforseo.py daten/seeds.txt --out daten/keywords-aktuell.csv [--dry-run]` (Google-Ads-Volumen, kostet Guthaben) und `build_queue.py daten/keywords-aktuell.csv`. Zugang über den Proxy der Umgebung oder `DATAFORSEO_LOGIN`/`DATAFORSEO_PASSWORD`; bei mehr als 1.000 Keywords vorher die Menge nennen.
3. Kurzbericht: gewählte Themen mit Kategorie/Thema, Lücken (Volumen 0 oft „keine Daten“, nicht „keine Suchen“), Themen ohne Beleg-Datei.

## Regeln
- Regionalzahlen nie hochrechnen ohne „Annahme“.
- Markenbegriffe („invisalign“) bleiben vorerst draußen; mit `--mit-marken` tragen sie `notiz=marke`.
- Praxis-Flag der Queue (`pflicht`/`optional`): Standard `optional`. `pflicht` nur für Kernthemen, zu denen Alexander seine Einschätzung in `material/fakten.md` hinterlegt hat.

## Testfälle
`tests/faelle.md`
