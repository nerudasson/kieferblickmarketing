---
name: keyword-research
description: Holt Suchvolumen und Wettbewerb über DataForSEO (Standort Mülheim/Ruhr und bundesweit), clustert Keywords nach Suchabsicht und schreibt die Artikel-Warteschlange. Nutzen bei neuen Keyword-Daten, Themenlücken oder wenn die Queue leer ist.
---
# keyword-research

## Ablauf
1. Seed-Liste: Keywords aus `daten/Kieferblick_Keyword-Auswertung_v1.xlsx` (Sheet Keywords_Funnel) plus Lücken aus `kontext/keyword-daten.md` (Schnarchen, Knirschen, Prophylaxe, „Zahnarzt Mülheim“). Als Textdatei, ein Keyword pro Zeile, in `daten/seeds.txt`.
2. Abrufen: `python3 .claude/skills/keyword-research/scripts/dataforseo.py daten/seeds.txt --out daten/keywords-aktuell.csv [--location bund|ruhr] [--dry-run]`
   - Zugang über `DATAFORSEO_LOGIN` und `DATAFORSEO_PASSWORD` (Umgebungs-Secrets). Ohne `--dry-run` entstehen Kosten bei DataForSEO: vorher Menge nennen, bei mehr als 1.000 Keywords Alexander fragen.
3. Queue bauen: `python3 .claude/skills/keyword-research/scripts/build_queue.py daten/keywords-aktuell.csv` schreibt `daten/artikel-queue.csv` (bestehende Zeilen und ihre Status bleiben).
4. Kurzbericht: Top-Cluster, Lücken, fehlende Daten (Volumen 0 oft „keine Daten“, nicht „keine Suchen“).

## Regeln
- Regionalzahlen nie hochrechnen ohne „Annahme“. Echte Standortdaten bevorzugen.
- Das Skript nutzt Standort-Code als Konfiguration (`LOCATION_CODES` im Skript). Mülheim-Code vor erstem Lauf über den DataForSEO-Locations-Endpunkt prüfen, bis dahin gilt Deutschland.
- Markenbegriffe („invisalign“) werden in der Queue mit `notiz=marke` markiert; der compliance-reviewer entscheidet über Verwendung.

## Testfälle
`tests/faelle.md`
