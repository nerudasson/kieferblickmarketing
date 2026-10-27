# LinkedIn-Modul (zweiter Kanal des Reel-Agenten)

Gleiches Gerüst wie bei Reels (Benchmarks → Gewinner → Remix → Generator → Filter → Lernschleife), eigene Daten unter `daten/linkedin/`. Hook-Bibliothek gemeinsam (`daten/reels/library/hooks.csv`, Spalte `kanal`). Wochenliste gemeinsam, LinkedIn als Abschnitte „### Post n“.

## Daten
- `daten/linkedin/raw/<Datum>_eigene-posts.csv`: Texte der eigenen Beiträge, erzeugt mit `python3 .claude/skills/reel-agent/scripts/li_import.py posts <Rich_Media.csv> --out ...` aus dem **Basis-Export** (Profil → Einstellungen → Datenschutz → Kopie Ihrer Daten). Der Basis-Export enthält nur Beiträge mit Bild oder Video (Textbeiträge ohne Medien fehlen) und **keine Reichweite**. Nachrichten, Kontakte, Einladungen werden nie gelesen oder ins Repo kopiert.
- `daten/linkedin/library/own_performance.csv`: Zahlen je eigener Beitrag (Spalten: datum, post_url, impressionen, reaktionen, kommentare, geteilt, klicks, hook_id, hook_type, format, trigger, stichwort, notiz). Quelle: Statistik-Export der Beiträge (Creator-Analytics, Excel) oder von Hand. Auswertung: `reels.py own --kanal linkedin`.
- `daten/linkedin/library/benchmarks.csv`: Vergleichsprofile mit Median. **Kein Browser-Scout**: LinkedIn geht gegen automatisches Auslesen strenger vor. Quelle sind Webquellen und Posts, die Alexander einfügt (Text, Impressionen sichtbar nur bei Reaktionen/Kommentaren, daher Faktor nur grob).
- `daten/linkedin/library/stil-eigene-posts.md`: Auswertung der eigenen Beiträge (Stil, Themen, Lücken).

## Format und Regeln
- Sprache: Phase 1 Posts auf Deutsch (Ihre bisherigen Posts sind englisch/gemischt, das Publikum ist dadurch eventuell international; Annahme: für DACH-Ziel auf Deutsch umstellen, Zahlen zeigen, ob Reichweite sinkt). Stichworte KURS / FALL / BUCH.
- Postlänge: Ihr Median liegt bei ca. 2.200 Zeichen. Annahme: das bleibt, bis Zahlen etwas anderes zeigen. Erste zwei Zeilen = Hook (vor „mehr anzeigen“), max. ca. 12 Wörter pro Zeile.
- Hashtags: höchstens 5 (Skript-Hinweis darüber). Ihr bisheriger Schnitt liegt deutlich höher; ob weniger besser läuft, zeigt erst die Lernschleife.
- Ende: Kommentar-Stichwort COURSE / CASE / BOOK oder eine Frage an die Kollegen. Keine Preise, keine Rabatte.
- Fachliche Aussagen [CHECK], persönliche Erlebnisse [ ], Herstellernamen ⚠️ legal review, kein Angriff auf Kollegen, Kieferorthopäden, Hersteller oder Kursanbieter (gilt auch für „Most orthodontists …“-Vergleiche).
- Kommentare und Vernetzungsanfragen (Skills `comment-draft`, `connection-request-draft`) kommen später; bis dahin nur Posts.
- Der Agent postet nichts. Posten auf dem persönlichen Profil bleibt Alexanders Handlung.

## Entwurfsformat in der Wochenliste
```
### Post <n> · <Titel> (<Mix>)
Vorbild: <Quelle, Muster> (oder eigener Post, Datum)
Hook: <zwei erste Zeilen>
Text: <Beats / Fließtext>
Ende: <Stichwort oder Frage>
Caption/Hashtags: <höchstens 5>
Filter: ✅ / ⚠️ / ❌
```
`reels.py check` prüft Marker, Verbotswörter, Stichwort, Preise und Hashtag-Zahl der Posts.
