---
name: seo-pipeline
description: Erzeugt SEO-Wissensartikel in Menge aus daten/artikel-queue.csv – Entwurf, Compliance-Prüfung, WordPress-Entwurf. Nutzen, wenn Alexander Artikel erstellen, einen Batch starten oder den Stand der Warteschlange sehen will.
---
# seo-pipeline

Ziel: Warteschlange abarbeiten. Der Agent legt nur **Entwürfe** an, Alexander veröffentlicht in WordPress.

## Ablauf
1. `python3 .claude/skills/seo-pipeline/scripts/queue.py next --n <N>` zeigt die nächsten Zeilen mit `status=offen`. Ohne `daten/artikel-queue.csv` erst `keyword-research` ausführen.
2. **SEO-Brief** je Zeile: `python3 .claude/skills/seo-pipeline/scripts/seo_brief.py "<keyword>" --slug <slug>` (DataForSEO, ca. 0,02–0,03 USD je Brief; bei mehr als 20 am Stück vorher die Summe nennen).
3. **Belege je Thema (einmal, nicht je Artikel):** Existiert `daten/belege/<thema>.md` nicht oder ist der Stand älter als 12 Monate, den `evidence-researcher` starten (er deckt alle Briefe des Themas ab). `belege_check.py validate` muss OK melden. Thema = Kategorie-Cluster, z. B. `retainer`.
4. **Skelett je Artikel:** `python3 .claude/skills/seo-pipeline/scripts/skelett.py <slug> --kategorie <kat> --thema <thema> --cluster <cluster>` (Kategorien: `references/kategorien.md`).
5. **Writer** je Artikel parallel (`article-writer`). Er füllt das Skelett aus den Belegen und prüft sich mit `lesbarkeit.py` und `belege_check.py check`, dann `finalize`.
6. **Gate durch dich:** beide Skripte nochmals über `daten/entwuerfe/*.md`. Nicht „OK“ → höchstens 2 Rückläufe an den Writer, danach `status=blockiert` mit Grund.
7. **compliance-reviewer** je Entwurf (HWG, Ton, Fakten gegen die Beleg-Tabelle). Rot → Writer, max. 2 Runden, danach `blockiert`. Gelb/grün → weiter.
8. `python3 .claude/skills/seo-pipeline/scripts/queue.py set <slug> <status>` (`entwurf`, `geprueft`, `blockiert`, `wp_entwurf`).
9. **Fragenliste:** alle `[FAKT FEHLT]` je Thema bündeln und Alexander einmal vorlegen (Antworten in `material/fakten.md` unter „Persönliche Einschätzung“ als Zeile `- <slug>: …`). Danach Skelett mit `--force` neu oder den Praxis-Block ersetzen.
10. WordPress-Entwurf (`status=draft`) nur, wenn keine `[FAKT FEHLT]`-Stelle mehr offen ist und `WP_URL`, `WP_USER`, `WP_APP_PASSWORD` gesetzt sind. Konverter Markdown → Blöcke steht noch aus; bis dahin bleiben Entwürfe in `daten/entwuerfe/`.
11. Bericht an Alexander: Anzahl je Ampel, Lesbarkeit, offene Fragen je Thema, was wartet.

## Regeln
- Nie `status=publish`. Veröffentlichen gibt nur Alexander frei.
- Doppelungen: `queue.py check` meldet Keywords, die zu nah beieinander liegen (gleicher Cluster und gleicher Wortstamm) – zusammenlegen statt zwei Artikel.
- Skalierung: Batchgröße steigern erst, wenn die letzten 10 Entwürfe ohne rot durchliefen.
- Ergebnisse (Indexierung, Rankings) später in `experiment-log.md`.

## Testfälle
Siehe `tests/faelle.md`.
