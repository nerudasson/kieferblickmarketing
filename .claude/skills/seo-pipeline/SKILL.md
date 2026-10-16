---
name: seo-pipeline
description: Erzeugt SEO-Wissensartikel in Menge aus daten/artikel-queue.csv – Entwurf, WordPress-Entwurf (Compliance prüft Alexander selbst). Nutzen, wenn Alexander Artikel erstellen, einen Batch starten oder den Stand der Warteschlange sehen will.
---
# seo-pipeline

Ziel: Warteschlange abarbeiten. Der Agent legt nur **Entwürfe** an, Alexander veröffentlicht in WordPress.

## Ablauf
1. `python3 .claude/skills/seo-pipeline/scripts/queue.py next --n <N>` (Standard 5) zeigt die nächsten Zeilen mit `status=offen`, sortiert nach Priorität. Ohne `daten/artikel-queue.csv` erst `keyword-research` ausführen.
2. Pro Zeile einen `article-writer` starten (parallel). Voraussetzung: `material/fakten.md` ist nicht leer. Ist sie leer, Alexander darauf hinweisen und nur Artikel ohne Fallbezug schreiben.
3. Kein automatischer Compliance-Check. Alexander prüft die Entwürfe selbst in WordPress (Entscheidung 16.10.2026). Der `compliance-reviewer` läuft nur, wenn Alexander ihn ausdrücklich anfordert.
4. `python3 .claude/skills/seo-pipeline/scripts/queue.py set <slug> <status>` setzt den Status (`entwurf`, `blockiert`, `wp_entwurf`).
5. WordPress-Entwurf anlegen (`POST /wp-json/wp/v2/posts` auf kieferblick.de mit `status=draft`; die Zugangsdaten setzt der Proxy der Umgebung). Aufbau wie die Artikelvorlage des Plugins: Blöcke mit den Klassen `kb-merksatz`, `kb-hinweis`, `kb-schritte`, `kb-vergleich`, `kb-faq`, `kb-cta`, `kb-quellen` und den Feldern `kb_kurz`, `kb_ursache`, `kb_behandlung`, `kb_dauer`, `kb_kosten`; kein eigenes CSS, keine eigenen Module.
6. Wissenschaftliche Fakten recherchiert der `article-writer` selbst und nennt die Quellen im Artikel (Block `kb-quellen`) und in `material/quellen.md`.
7. Bericht an Alexander: offene `[FAKT FEHLT]`-Stellen (nur Praxis-Fakten), verwendete Quellen, was in WordPress wartet.

## Regeln
- Nie `status=publish`. Veröffentlichen gibt nur Alexander frei.
- Doppelungen: `queue.py check` meldet Keywords, die zu nah beieinander liegen (gleicher Cluster und gleicher Wortstamm) – zusammenlegen statt zwei Artikel.
- Skalierung: Batchgröße steigern erst, wenn Alexander die letzten Entwürfe ohne größere Korrekturen übernommen hat.
- Ergebnisse (Indexierung, Rankings) später in `experiment-log.md`.

## Testfälle
Siehe `tests/faelle.md`.
