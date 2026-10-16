# Artikelstruktur

Vorbild: `daten/entwuerfe/aligner-kosten.md`. WordPress-Vorlage „Wissen“ (Beitrag mit Kategorie, Metafeldern und Block-Klassen).

## Frontmatter
title, slug, keyword, cluster, intent, autor (Alexander Andreev), kategorie (aligner · bleaching-zahnreinigung · funktionsschiene · schnarchschiene · veneers), meta_description (max. 155 Zeichen), status (entwurf) und die Metafelder:
- `kb_kurz`: drei Zeilen (Block mit `|`), je ein kurzer Satz, Hero-Bullets
- `kb_ursache`, `kb_behandlung`, `kb_dauer`, `kb_kosten`, `kb_ablauf`: **je genau ein Satz**, höchstens ca. 20 Wörter, allgemein zum Thema
- `kb_geprueft` bleibt leer (Alexander setzt das Datum bei der Freigabe)

## Aufbau des Textes
1. Antwort in den ersten zwei Sätzen
2. H2-Gliederung passend zur Suchabsicht (Fragen als H2 wo sinnvoll)
3. Nachteile und Grenzen ehrlich
4. Kosten oder Ablauf konkret, wenn das Keyword danach fragt
5. Optional ein kurzer Abschnitt „Wie machen wir das bei Kieferblick“ (nur Fakten aus den Kontextdateien)
6. FAQ (3 bis 5 Fragen, kurz)
7. „Was heißt das für Sie?“, danach CTA und Quellen

Länge: Info 800 bis 1.200 Wörter, Kosten/Vergleich 1.200 bis 1.800. Interne Links: 2 bis 4 auf Artikel desselben Clusters, 1 auf die Leistungsseite, nur wenn das Ziel existiert.

## Direktiven im Markdown (werden zu WordPress-Blöcken)
- `## Überschrift` · normale Absätze · `- ` Aufzählung · `1. ` Nummerierung
- `!merksatz Text` (ein Merksatz je Artikel) · `!hinweis Text` · `!cta Text`
- `!schritte` gefolgt von `1. **Titel:** Text`-Zeilen
- `!tabelle` oder `!vergleich` gefolgt von Zeilen mit `|` (erste Zeile = Kopf)
- `?? Frage` und direkt darunter `!! Antwort` (FAQ)
- `!quellen` gefolgt von nummerierten Quellen

Umwandlung und Anlegen als Entwurf: `python3 .claude/skills/seo-pipeline/scripts/md2wp.py <datei.md> <kategorie-id>` schreibt das JSON für `POST /wp-json/wp/v2/posts` (Status immer `draft`). Kategorie-IDs: aligner 3, bleaching-zahnreinigung 4, schnarchschiene 5, veneers 6, funktionsschiene 7.
