---
name: seo-pipeline
description: Erzeugt SEO-Wissensartikel in Menge aus daten/artikel-queue.csv – Entwurf, Compliance-Prüfung, WordPress-Entwurf. Nutzen, wenn Alexander Artikel erstellen, einen Batch starten oder den Stand der Warteschlange sehen will.
---
# seo-pipeline

Ziel: Warteschlange abarbeiten. Der Agent legt nur **Entwürfe** an, Alexander veröffentlicht in WordPress.

## Ablauf
1. `python3 .claude/skills/seo-pipeline/scripts/queue.py next --n <N>` (Standard 5) zeigt die nächsten Zeilen mit `status=offen`, sortiert nach Priorität. Ohne `daten/artikel-queue.csv` erst `keyword-research` ausführen.
1b. **Quellenspeicher prüfen:** Für den Cluster jeder Zeile muss `material/quellen/<cluster>.md` die klinischen Grundlagen des Themas enthalten (am Original geprüft). Fehlen sie, **zuerst recherchieren, selbständig und ohne Rückfrage bei Alexander**: einen `source-researcher` je Cluster starten (parallel), mit der Liste der fehlenden Aussagen. Er arbeitet so: PubMed über `curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=…"` und `efetch` (Abstract), DOI-Metadaten über `https://api.crossref.org/works/<doi>`, Leitlinien-PDFs per `curl` und `pdftotext`. Das WebFetch-Werkzeug löst Hostnamen selbst auf und scheitert hinter dem Proxy, `curl` geht. Bevorzugt Leitlinien (DGKFO, AWMF, BOS, AAO), Cochrane und systematische Übersichten. Einträge nach `material/quellen/README.md` anlegen, mit Abrufdatum und Prüfstatus.
2. Pro Zeile einen `article-writer` starten (parallel). Voraussetzung: `material/fakten.md` ist nicht leer. Ist sie leer, Alexander darauf hinweisen und nur Artikel ohne Fallbezug schreiben.
3. Jeden Entwurf an `compliance-reviewer` geben (ein Durchlauf, parallel zu den anderen). **Rot:** der Writer korrigiert genau die roten Stellen (eine Runde, keine Gesamtüberarbeitung), ich prüfe die korrigierten Stellen selbst per Lesen, keine neue Reviewer-Runde. Bleibt die Stelle rot, `status=blockiert` mit Grund. **Gelb/grün: keine Schleife.** Die Hinweise gehen gesammelt in den Bericht an Alexander, der Entwurf geht weiter. Ein WordPress-Entwurf entsteht erst nach der Prüfung, nie davor. **Quellen-Lücken:** Werden vor dem Schreiben geschlossen (Schritt 1b). Melden Writer oder Reviewer danach noch Lücken, gehen sie gesammelt in den Bericht und in den Quellenspeicher-Backlog (`material/quellen/<cluster>.md`, Abschnitt „Lücken“), der Entwurf wird nicht neu geschrieben. Alexander nur fragen, was keine Quelle beantworten kann (Praxisfakten, Preise, Entscheidungen), gesammelt im Bericht.
4. `python3 .claude/skills/seo-pipeline/scripts/queue.py set <slug> <status>` setzt den Status (`entwurf`, `geprueft`, `blockiert`, `wp_entwurf`).
5. WordPress-Entwurf anlegen: In der Cloud-Umgebung authentifiziert der Proxy Anfragen an `kieferblick.de` selbst, `WP_*`-Variablen sind dort nicht nötig. Erst `python3 .claude/skills/seo-pipeline/scripts/md2wp.py daten/entwuerfe/<slug>.md <kategorie-id>` (Blöcke, Kategorie und `kb_`-Metafelder der Vorlage), dann `POST https://kieferblick.de/wp-json/wp/v2/posts` mit `status=draft` (bei vorhandenem Beitrag `.../posts/<id>`). Lokal ohne Proxy nur mit `WP_URL`, `WP_USER`, `WP_APP_PASSWORD`. Ohne Zugang Entwürfe in `daten/entwuerfe/` lassen und das melden.
6. Bericht an Alexander: Anzahl je Ampel, offene `[FAKT FEHLT]`-Stellen, was in WordPress wartet.

## Regeln
- Nie `status=publish`. Veröffentlichen gibt nur Alexander frei.
- Doppelungen: `queue.py check` meldet Keywords, die zu nah beieinander liegen (gleicher Cluster und gleicher Wortstamm) – zusammenlegen statt zwei Artikel.
- Skalierung: Batchgröße steigern erst, wenn die letzten 10 Entwürfe ohne rot durchliefen.
- Ergebnisse (Indexierung, Rankings) später in `experiment-log.md`.

## Testfälle
Siehe `tests/faelle.md`.
