---
name: seo-pipeline
description: Erzeugt SEO-Wissensartikel in Menge aus daten/artikel-queue.csv – Evidenz je Cluster, SEO-Brief, Entwurf in einfacher Sprache, WordPress-Entwurf (Compliance prüft Alexander selbst). Nutzen, wenn Alexander Artikel erstellen, einen Batch starten oder den Stand der Warteschlange sehen will.
---
# seo-pipeline

Ziel: Warteschlange abarbeiten. Der Agent legt nur **Entwürfe** an, Alexander veröffentlicht in WordPress.

## Ablauf (Cluster zuerst, dann Artikel)
Die Fakten kommen aus recherchierter Evidenz, nicht aus der Praxis. Darum wird einmal pro Cluster recherchiert und viele Artikel schreiben daraus. Das hält die Kosten niedrig und die Aussagen einheitlich.

1. `python3 .claude/skills/seo-pipeline/scripts/queue.py next --n <N>` (Standard 5) zeigt die nächsten Zeilen mit `status=offen`, sortiert nach Priorität. Ohne `daten/artikel-queue.csv` erst `keyword-research` ausführen.
2. **Evidenz je Cluster:** Gibt es für das Cluster noch kein `daten/evidenz/<cluster-slug>.md`, starte den `evidence-researcher` (einmal pro Cluster). Prüfstatus der Quellen im Blatt beachten.
3. **SEO-Brief je Artikel:** `python3 .claude/skills/seo-pipeline/scripts/seo_brief.py "<keyword>" --out daten/briefs/<slug>.json` (kostet etwa 0,02 US-Dollar).
4. **Entwurf:** Pro Zeile ein `article-writer` (parallel). Er schreibt aus Evidenzblatt, Brief, `fakten.md` und `standpunkte.md`, ohne eigene Recherche, und prüft Lesbarkeit (Flesch ≥ 65, WSTF ≤ 6). Ohne Evidenzblatt schreibt er nicht.
5. **WordPress-Entwurf:** `python3 .claude/skills/seo-pipeline/scripts/md_to_wp.py daten/entwuerfe/<slug>.md --post` (setzt in die Blöcke der Plugin-Vorlage um, immer `status=draft`). Danach `queue.py set <slug> wp_entwurf`.
6. Kein automatischer Compliance-Check. Alexander prüft die Entwürfe selbst in WordPress. Der `compliance-reviewer` läuft nur auf Anforderung.
7. Bericht an Alexander: Anzahl Entwürfe, Artikel mit `quellenstatus: offen`, offene `[FAKT FEHLT]` (Ausnahme), Lesbarkeit, Kosten (Tokens, DataForSEO).

## Qualitätsschranken bei großer Menge
- **Stichprobe:** Von jedem neuen Cluster prüft Alexander die ersten 3 Entwürfe, bevor mehr entstehen. Danach alle 20 Artikel eine Stichprobe von 2.
- **Quellenstatus:** Ein Cluster geht erst in die Breite, wenn die Kernquellen Status A haben (Netzwerkfreigabe für PubMed, PMC, DOI, Cochrane nötig). Artikel mit `quellenstatus: offen` bleiben Entwurf.
- **Eigener Wert je Artikel:** Jeder Artikel beantwortet eine echte Suchfrage anders oder besser als die Top-3 (Brief). Kein Artikel, der nur ein Keyword umformuliert. `queue.py check` meldet Doppelungen.
- **Tempo beim Veröffentlichen:** Alexander veröffentlicht gestaffelt (z. B. 5 bis 10 pro Woche), nicht tausende am Stück. Suchmaschinen bewerten massenhaft erzeugte Inhalte kritisch (Richtlinie gegen „Scaled Content Abuse“). Medizinische Seiten werden besonders streng geprüft.
- **Kostendeckel:** Pro Artikel höchstens etwa 40.000 Tokens und 0,05 US-Dollar DataForSEO. Für ein Cluster mit Recherche zusätzlich etwa 100.000 bis 200.000 Tokens, einmalig.

## Regeln
- Nie `status=publish`. Veröffentlichen gibt nur Alexander frei.
- Doppelungen: `queue.py check` meldet Keywords, die zu nah beieinander liegen (gleicher Cluster und gleicher Wortstamm) – zusammenlegen statt zwei Artikel.
- Skalierung: Batchgröße steigern erst, wenn Alexander die letzten Entwürfe ohne größere Korrekturen übernommen hat.
- Fälle, Patientengeschichten und erfundene Praxiserfahrung gibt es nicht. Persönliche Aussagen nur aus `material/standpunkte.md`.
- Ergebnisse (Indexierung, Rankings) später in `experiment-log.md`.

## Testfälle
Siehe `tests/faelle.md`.
