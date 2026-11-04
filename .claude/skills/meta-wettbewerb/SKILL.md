---
name: meta-wettbewerb
description: Beobachtet wöchentlich, wie Wettbewerber von BiteCentric auf Meta (Facebook, Instagram) um Zahnärzte werben. Fragt die Meta Ad Library API für DE, AT und GB ab, führt ein Anzeigen-Log ohne Dubletten und schreibt einen einseitigen Wochenbericht mit Anregungen für eigene Anzeigen. Nutzen für den Konkurrenz-Monitor, vor dem Schreiben neuer BiteCentric-Anzeigen und wenn Wettbewerber-Anzeigen eingeordnet werden sollen. Nicht für die Google-Anzeigen von Kieferblick (dafür ads-wettbewerb).
---
# meta-wettbewerb (BiteCentric)

Ziel: Muster für Aufhänger, Aufruf und Ton aus dem Markt gewinnen. **Beobachtet wird, was geschaltet wird, nicht was performt.** Als Erfolgshinweis gilt in UK die Laufzeit und Variantenzahl, in DACH die Häufigkeit eines Themas über mehrere Wellen (Annahmen, siehe `kontext/bitecentric/wettbewerb.md`). Eigene Entscheidungen stützen sich später auf die eigenen Konto-Daten.

## Harte Regeln
- Quelle ist die **Meta Ad Library API** (`ads_archive`). Länder **DE, AT, GB**; CH entfällt (nicht-politische Anzeigen stehen nur im Archiv, wenn sie in EU oder UK ausgeliefert wurden). Aktive und beendete Anzeigen der letzten 12 Monate, je Wettbewerber und je Suchbegriff.
- **Kein echter API-Abruf**, bevor Alexander Token und Trockenlauf bestätigt hat. Der Echtlauf ist doppelt gesperrt: Schalter `adlib.echtlauf_freigegeben` in `config/meta.json` und Umgebungsvariable `META_ADLIB_ACCESS_TOKEN`.
- **Keine Zugangsschlüssel in Dateien.** Die Snapshot-URL der API enthält laut Doku den Token; das Skript bereinigt sie und speichert nichts, wenn ein Token in den Ausgaben auftaucht.
- **Nur B2B.** Praxen, die Patienten bewerben, werden verworfen (Textmuster; Grenzfälle stehen als „prüfen“ im Log und der Agent entscheidet beim Bericht).
- Keine Texte 1:1 übernehmen. Muster (Aufhänger, Aufruf, Beweisform) ja, Wortlaut nein. Anregungen für eigene Anzeigen gehen vor jeder Verwendung durch Aufrufregel, Ton und `anzeigen_check_meta.py --text`.
- **Seiten-IDs** werden beim ersten Lauf gesucht und **erst nach Bestätigung durch Alexander** in `references/wettbewerber.json` eingetragen.
- Suchbegriffe und Wettbewerber nur in `references/` ändern. Der Lauf ist durch `max_aufrufe` in `config/meta.json` begrenzt; die Obergrenze nicht eigenmächtig anheben.

## Ablauf
**Einmalig (erster Lauf):**
1. Trockenlauf: `python3 -I .claude/skills/meta-wettbewerb/scripts/adlib.py seiten --dry-run` und `… snapshot --dry-run` (kein Netzwerk, zeigt Plan und Obergrenzen; ohne Token eine verständliche Meldung).
2. Nach Freigabe: `adlib.py seiten` schreibt `daten/meta/wettbewerb/seiten-vorschlag.md`. Alexander bestätigt je Wettbewerber die richtige Seite; der Agent trägt die IDs ein (`seiten_ids`, `seiten_ids_bestaetigt` true).

**Wöchentlich:**
1. `python3 -I .claude/skills/meta-wettbewerb/scripts/adlib.py snapshot`: Abfrage nach Seiten-IDs (Blöcke zu 10) und Suchbegriffen, Format-Erkennung Video, Dedupe über die Bibliotheks-ID, Rohdaten `daten/meta/wettbewerb/rohdaten/<Datum>.json`, Log `anzeigen-log.csv` (Länder werden zusammengeführt, manuelle Spalten bleiben).
2. `python3 -I .claude/skills/meta-wettbewerb/scripts/adlib.py report` schreibt `daten/meta/wettbewerb/berichte/<Datum>.md`.
3. **Agent ergänzt** im Log die Spalten Angebot, Aufruf, Aufhänger, Ton für neue Anzeigen und klärt B2B-„prüfen“-Fälle (Anzeigentext und Link ansehen, nicht raten). Danach Abschnitt 5 des Berichts: höchstens drei Anregungen, je mit Aufruf nach Aufrufregel, geprüft mit `anzeigen_check_meta.py --text`. Bericht höchstens eine Seite.
4. Commit von `daten/meta/wettbewerb/`, Kurzfassung (3–5 Sätze) an Alexander. Kernbefunde quartalsweise in `kontext/bitecentric/wettbewerb.md` nachtragen.

## Was das Log enthält
Bibliotheks-ID · Werbetreibender · Land · Start · Ende · Varianten (Zahl der Anzeigen mit gleichem Text desselben Werbetreibenden) · Angebot · Aufruf · Format (video, bild, mehrere Texte/Karussell zu prüfen) · Aufhänger · Ton · EU-Zielgruppenangaben · EU-Reichweite · Link · zuerst gesehen am; zusätzlich Stufe, B2B-Einstufung, Reichweite-Hinweis (für UK Rohwert), Textauszug, Quelle, zuletzt gesehen. API-Details und Unsicherheiten: `references/felder.md`.

## Wochenlauf einplanen
Erst **nach erfolgreichem Trockenlauf und OK von Alexander**. Prompt und Zeitpunkt: `references/wochenlauf-prompt.md`. Bis dahin nicht einplanen.

## Testfälle
`tests/faelle.md` (mit Beispieldaten in `tests/fixtures/`, ohne Netzwerk).
