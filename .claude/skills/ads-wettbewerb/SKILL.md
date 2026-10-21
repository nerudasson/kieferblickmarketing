---
name: ads-wettbewerb
description: Beobachtet wöchentlich die Google-Anzeigen der Wettbewerber in Mülheim, Essen und Düsseldorf (DataForSEO SERP) und wertet Langläufer, Sichtbarkeit und neue Anzeigen aus. Nutzen für die Wettbewerber-Beobachtung, vor dem Schreiben neuer Anzeigen und im wöchentlichen Ads-Bericht.
---
# ads-wettbewerb

Ziel: Hypothesen für Anzeigenwinkel und CTAs aus dem Markt gewinnen. **Beobachtet wird, was geschaltet wird, nicht was performt.** Als Indiz für Wirtschaftlichkeit gilt die Laufzeit einer Anzeige (Annahme). Eigene Entscheidungen beruhen später auf den eigenen Konto-Daten.

## Ablauf
1. Momentaufnahme: `python3 .claude/skills/ads-wettbewerb/scripts/beobachtung.py snapshot [--dry-run]` (81 Abfragen, ca. 0,16 USD, Obergrenze `max_abfragen` in `references/beobachtung.json`). Ergebnis: `daten/ads/beobachtung/<Datum>.json`.
2. Auswertung: `python3 .claude/skills/ads-wettbewerb/scripts/beobachtung.py report` schreibt `daten/ads/beobachtung/auswertung.md` (Sichtbarkeit je Werbetreibender, Langläufer ab 3 Wochen, neue und verschwundene Anzeigen).
3. Kurzbericht: drei bis fünf Auffälligkeiten (neue Werbetreibende, neue Winkel, Langläufer-Texte) und was davon als Testhypothese in `experiment-log.md` gehört.

## Regeln
- Keine Texte 1:1 übernehmen. Muster (Winkel, CTA, Beweisform) ja, Wortlaut nein. Alles geht vor Freigabe durch den compliance-reviewer (HWG).
- Suchbegriffe und Standorte nur in `references/beobachtung.json` ändern.
- Fehlgeschlagene Abfragen stehen mit `fehler` in der Datei und fließen nicht in die Auswertung. Stehen viele Fehler drin, später wiederholen.
- Der Lauf kostet Guthaben; die Obergrenze nicht eigenmächtig anheben.

## Testfälle
`tests/faelle.md`
