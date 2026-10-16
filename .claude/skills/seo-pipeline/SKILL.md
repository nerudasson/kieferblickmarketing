---
name: seo-pipeline
description: Erzeugt SEO-Wissensartikel in Menge aus daten/artikel-queue.csv – Entwurf, Compliance-Prüfung, WordPress-Entwurf. Nutzen, wenn Alexander Artikel erstellen, einen Batch starten oder den Stand der Warteschlange sehen will.
---
# seo-pipeline

Ziel: Warteschlange abarbeiten. Der Agent legt nur **Entwürfe** an, Alexander veröffentlicht in WordPress.

## Ablauf
Deterministische Stufen übernimmt `scripts/pipeline.py`, die Agenten bekommen eine Arbeitsliste.
1. `python3 .claude/skills/seo-pipeline/scripts/pipeline.py status` zeigt Queue, Themen und Alter der Belege.
2. `pipeline.py prepare --n 5` nimmt die nächsten offenen Zeilen, holt fehlende SEO-Briefe (`seo_brief.py`, ca. 0,02–0,03 USD je Brief; `--dry-run` zeigt die Abrufe, bei mehr als 20 am Stück vorher die Summe nennen), legt die Skelette an (`skelett.py`, Praxis-Block je nach `praxis` der Queue pflicht oder optional) und gibt die **Arbeitsliste** aus. Kategorie und Thema kommen aus der Queue (Zuordnung `references/themen.json`, Kategorien `references/kategorien.md`).
3. **Belege je Thema, einmal:** Fehlt `daten/belege/<thema>.md` oder ist sie älter als 12 Monate, `evidence-researcher` starten (vor den Writern). `belege_check.py validate` muss OK melden.
4. **`article-writer`** je Skelett parallel. Er füllt es aus den Belegen (Zitate `[B19]`), prüft sich mit `lesbarkeit.py` und `belege_check.py check` und ruft `finalize` auf.
5. `pipeline.py gates` prüft alle Entwürfe nochmals. Nicht OK → höchstens 2 Rückläufe an den Writer, danach `queue.py set <slug> blockiert`.
6. **`compliance-reviewer`** je Entwurf (HWG, Ton, Fakten gegen die Beleg-Tabelle). Rot → Writer, max. 2 Runden. Gelb/grün → `queue.py set <slug> geprueft`.
7. `pipeline.py fragen` bündelt alle offenen `[FAKT FEHLT]` je Thema für Alexander (Antwort 1–3 Sätze je Zeile in `material/fakten.md`, Abschnitt „Persönliche Einschätzung“, Format `- <slug>: …`). Artikel mit `praxis: optional` brauchen das nicht; der Praxis-Block fehlt dann einfach.
8. WordPress-Entwurf: `wp_publish.py <entwurf> --dry-run` zeigt das HTML, ohne `--dry-run` legt es den Entwurf an (Kategorie, Yoast, Theme-Felder, `status=draft`). Verweigert bei `[FAKT FEHLT]`, ausstehenden Prüfungen oder unbekannter Kategorie. Danach `queue.py set <slug> wp_entwurf`.
9. Bericht an Alexander: Anzahl je Ampel, Lesbarkeit, offene Fragen je Thema, was in WordPress wartet.

## Regeln
- Nie `status=publish`. Veröffentlichen gibt nur Alexander frei.
- Doppelungen: `queue.py check` meldet Keywords, die zu nah beieinander liegen (gleicher Cluster und gleicher Wortstamm) – zusammenlegen statt zwei Artikel.
- Skalierung: Batchgröße steigern erst, wenn die letzten 10 Entwürfe ohne rot durchliefen.
- Ergebnisse (Indexierung, Rankings) später in `experiment-log.md`.

## Testfälle
Siehe `tests/faelle.md`.
