# Quellenspeicher (klinische Grundlagen pro Thema)

Allgemeine klinische Aussagen (Rückfall, Risiken, Tragezeiten, Kassenleistung, Marktpreise) stehen **nicht** frei in Artikeln. Sie kommen aus diesem Ordner, eine Datei pro Cluster (`rueckfall.md`, `aligner-risiken.md`, `kosten.md`, weitere nach Bedarf). So sagen alle Artikel zum selben Thema dasselbe, und jede Aussage hat eine prüfbare Quelle.

## Eintragsformat
```
### Q<Nr> Kurztitel
- Aussage (1 bis 2 Sätze, so, wie sie im Artikel stehen darf, mit Einschränkungen der Studie)
- Quelle: Autoren, Titel, Journal, Jahr, DOI oder URL
- Abgerufen: Datum
- Prüfstatus: am Original geprüft | nur Sekundärangabe | übernommen, nicht geprüft
- Grenzen: Population, Studientyp, was nicht daraus folgt
```

## Regeln
- Bevorzugt: Leitlinien (DGKFO, DGZMK/AWMF, BOS, AAO), Cochrane- und andere systematische Übersichten, Verbraucherzentrale und Stiftung Warentest für Preise und Kosten. Anbieter- und Herstellerseiten nur als Beleg für das, was der Anbieter selbst sagt.
- Der Speicher wird in der Hauptsession gepflegt, nicht von Writer oder Reviewer. Technik: `curl` auf `eutils.ncbi.nlm.nih.gov` (esearch/efetch/esummary), `api.crossref.org` und Leitlinien-PDFs, dazu `pdftotext`. Das WebFetch-Werkzeug geht in der Cloud-Umgebung nicht (Hostauflösung am Proxy vorbei). Der Writer markiert Lücken mit `[QUELLE FEHLT: Aussage]`, die Pipeline sammelt sie und die Recherche füllt sie.
- „Nicht am Original geprüft“ heißt: Aussage nur vorsichtig und mit Hinweis auf die Quelle verwenden, im Zweifel als Lücke behandeln.
- Persönliche Haltung und Praxiszahlen von Alexander gehören in `material/fakten.md`, nicht hierher.
