# Übergabe Keyword-Abruf und Ads-Datenbasis (Stand 08.10.2026)

## Stand
- DataForSEO läuft über den Proxy (keine Umgebungsvariablen nötig). Guthaben ca. 47 $. **Keine Abrufe ohne Rückfrage bei Alexander** (Kosten höher als gedacht, ca. 0,09 $ pro Anfrage, 24 Städte x 1.000 Keywords nicht getestet).
- Radius-Abruf (`ruhr`) wird von der API ignoriert und liefert bundesweite Werte. Städte einzeln über `--location <stadt>` oder `--region` (24 Städte, Limit 12 Anfragen/Minute). Städtesummen sind bei kleinen Werten unzuverlässig (Rundung auf 10, Doppelzählung).
- Mülheim an der Ruhr fehlt in der Google-Ads-Standortliste.
- Google Ads liefert für viele Gesundheits-Keywords keine Daten (z. B. „invisalign kosten“).

## Daten im Repo
- `daten/cpc-tendenzen.csv`: CPC und Volumen aus SE Ranking (08.10.2026), Semrush 2025 und DataForSEO-Test, alles bundesweit.
- `daten/seoranking-export-2026-10-08.csv`: Rohexport SE Ranking (996 Keywords).
- `daten/seeds-test1000.txt`, `seoranking-keywords-1000.csv`, `keyword-planner-1000.csv`: dieselben 1.000 Keywords für Abrufe/Uploads.

## Offene Punkte
- CPC-Widerspruch: SE Ranking/Semrush 0,5–1,5 € gegen DataForSEO (Google Ads) 2,5–8 €. Planungsannahme 1–3 €, klärt der Keyword-Planner (Gebotsspanne) oder der erste Testmonat.
- Regionalzahlen: Keyword-Planner mit 40 km um Mülheim exportieren (Keyword-Ideen mit Zeilen pro Keyword). Der bisherige Forecast-Export enthält nur Kampagnensummen und keinen Standort.
- Cluster `sonstiges` in `cpc-tendenzen.csv` durchsehen.
- Nächster Schritt: Agent-Konzept für Google Ads. Vorschlag: zuerst nur lesen und vorschlagen, Schreibzugriff erst nach Testphase (Frage an Alexander offen).
