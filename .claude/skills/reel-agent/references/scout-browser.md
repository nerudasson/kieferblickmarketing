# Scout im eingeloggten Browser (Claude in Chrome)

Läuft **lokal** auf Alexanders Rechner (in dieser Cloud-Sitzung gibt es keinen eingeloggten Browser). Der Scout liest nur: nicht liken, folgen, kommentieren oder nachrichten. Keine Videos herunterladen (Nutzungsbedingungen von Instagram).

## Bewährtes Vorgehen (Erst-Analyse 27.10.2026)
- `instagram.com/<handle>/reels/` öffnen. Grid-Kacheln `a[href*="/reel/"]` zeigen die Views. Zahlenformat deutsch: „601.000“, „2,4 Mio.“ (`reels.py` parst das).
- Per JavaScript schrittweise scrollen und sammeln. JS-Aufrufe brechen nach ca. 45 s ab: höchstens ca. 22 Scroll-Runden à 1,1 s je Aufruf. Das Grid wird virtualisiert, deshalb **oben anfangen** (angepinnte Reels sonst verpasst), Ergebnisse je Aufruf in einer Variable sammeln und zusammenführen.
- Caption, Likes, Kommentare, Datum: same-origin `fetch('/reel/<code>/')` und `og:description`-Meta-Tag.
- Tool-Ausgaben werden ab ca. 1.000 Zeichen abgeschnitten und bei URL-artigem Text blockiert: Ausgaben kurz halten, Captions kürzen, Sonderzeichen filtern, Daten in Dateien schreiben statt ausgeben.
- **Hook-Erfassung** für die Top 10 je Account: Reel öffnen, `video.muted = true; video.pause(); video.currentTime = 0.3 / 1.5 / 3.0`, jeweils Screenshot nach `daten/reels/frames/<code>_0.3.png` usw. Daraus Text-Einblendung, Setting, Format ablesen. Gesprochenes ohne Einblendung: „spoken hook: unknown“.
- Je Account festhalten: Zahl gescannter Reels, Median-Views, Top 10. Likes/Views deutlich unter 0,5 % → „wahrscheinlich beworben“ (Annahme).

## Ausgabeformat
CSV `daten/reels/raw/<YYYY-MM-DD>_<handle>.csv` mit den Spalten
`account,code,views,likes,comments,date,pinned,hinweis,thema`.
Ab 30 Reels je Account berechnet `reels.py winners` den Median selbst, darunter nutzt es `library/benchmarks.csv`. Nach einem vollen Scan `median_views`, `scan_n`, `stand` in `benchmarks.csv` nachziehen.

## Offen
Ob ein Anbieter-Dienst (z. B. Apify, DataForSEO) die Daten statt des Browsers liefern kann, ist nicht geprüft; das hängt an den Nutzungsbedingungen von Instagram und an Kosten und braucht Alexanders Entscheidung.
