---
name: seo-pipeline
description: Erzeugt SEO-Wissensartikel in Menge aus daten/artikel-queue.csv – Entwurf, Compliance-Prüfung, WordPress-Entwurf. Nutzen, wenn Alexander Artikel erstellen, einen Batch starten oder den Stand der Warteschlange sehen will.
---
# seo-pipeline

Ziel: Warteschlange abarbeiten. Der Agent legt nur **Entwürfe** an, Alexander veröffentlicht in WordPress.

## Ablauf
1. `python3 .claude/skills/seo-pipeline/scripts/queue.py next --n <N>` (Standard 5) zeigt die nächsten Zeilen mit `status=offen`, sortiert nach Priorität. Ohne `daten/artikel-queue.csv` erst `keyword-research` ausführen.
2. Pro Zeile einen `article-writer` starten (parallel). Voraussetzung: `material/fakten.md` ist nicht leer. Ist sie leer, Alexander darauf hinweisen und nur Artikel ohne Fallbezug schreiben.
3. Jeden Entwurf an `compliance-reviewer` geben. Rot → Writer überarbeitet (max. 2 Runden), danach `status=blockiert` mit Grund. Gelb/grün → weiter.
4. `python3 .claude/skills/seo-pipeline/scripts/queue.py set <slug> <status>` setzt den Status (`entwurf`, `geprueft`, `blockiert`, `wp_entwurf`).
5. WordPress-Entwurf anlegen nur, wenn `WP_URL`, `WP_USER`, `WP_APP_PASSWORD` gesetzt sind (Schnittstelle: `POST /wp-json/wp/v2/posts` mit `status=draft`). Sonst Entwürfe in `daten/entwuerfe/` lassen und das melden.
6. Bericht an Alexander: Anzahl je Ampel, offene `[FAKT FEHLT]`-Stellen, was in WordPress wartet.

## Regeln
- Nie `status=publish`. Veröffentlichen gibt nur Alexander frei.
- Doppelungen: `queue.py check` meldet Keywords, die zu nah beieinander liegen (gleicher Cluster und gleicher Wortstamm) – zusammenlegen statt zwei Artikel.
- Skalierung: Batchgröße steigern erst, wenn die letzten 10 Entwürfe ohne rot durchliefen.
- Ergebnisse (Indexierung, Rankings) später in `experiment-log.md`.

## Testfälle
Siehe `tests/faelle.md`.
