# Konkurrenz-Monitor Meta: Daten

- `anzeigen-log.csv`: eine Zeile je Anzeige (Bibliotheks-ID, Dubletten ausgeschlossen). Startzeilen `bestand-2026-11-04-NN` stammen aus der Bestandsaufnahme im Browser (ohne Bibliotheks-ID, ohne Link); sie werden vom Skript nie verändert. Die Spalten Angebot, Aufruf, Aufhänger und Ton füllt der Agent beim Wochenbericht, das Skript überschreibt sie nie.
- `rohdaten/<Datum>.json`: normalisierte Antwort je Lauf (ohne Zugriffstoken; die Snapshot-URL wird bereinigt).
- `berichte/<Datum>.md`: Wochenbericht, höchstens eine Seite.
- `seiten-vorschlag.md`: Treffer für die Suche nach Seiten-IDs. Nichts davon ist eingetragen, bis Alexander bestätigt.

Nur B2B. Praxen an Patienten werden verworfen (in den Rohdaten mit Grund aufgeführt). Keine Patientendaten. Quelle: Meta Ad Library API, siehe `.claude/skills/meta-wettbewerb/SKILL.md`.
