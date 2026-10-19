# Experiment-Log

Jeder Test wird hier protokolliert, damit neue Varianten auf bisherigen Ergebnissen aufbauen. Zeilen von oben (neu) nach unten (alt).

| Datum | Kanal | Hypothese | Variante A / B | Budget | Laufzeit | Ergebnis (Kennzahlen ①–⑥) | Entscheidung | Rechtscheck |
|---|---|---|---|---|---|---|---|---|
| 16.10.2026 | SEO-Artikel (Prozess) | Plan → Belege je Frage → Schreiben mit harten/weichen Hürden und Stichproben-Review liefert bessere Artikel in kürzerer Zeit als ein Agent mit Recherche im Writer | Lauf 1: alles im Writer; Lauf 2: Plan + Belege + Skelett; Lauf 3: Batch mit 3 Keywords parallel | 0 € (Token) | 3 Tage | Einzelartikel 8 → ca. 3 Min je Artikel im Batch (3 Artikel 7 Min); Writer 360 → 66–117 s; Wörter 534 → ca. 1.000; Reviewer: gelb, 1–3 wichtige Befunde je Artikel, kein Rot | Prozess übernommen (siehe SKILL.md); Ziel-Länge ca. 20 % senken, Praxis-Block pflegen | entfällt |
| | | | | | | | | |

## 2026-10-19 · Testlauf Pipeline mit 5 Keywords
- Hypothese: Der Ablauf Auswahl → Brief → Plan → Belege → Schreiben → Review → Fix → WordPress läuft für 5 neue Themen ohne Rückfragen durch.
- Test: veneers, bleaching, retainer-zahne, schiefe-zahne, retainer-entfernen-kosten (WP-Entwürfe 570–574).
- Ergebnis: alle Hürden grün, Review 5× gelb (0 rot), Lesbarkeit 63–65. Länge 724–924 Wörter, durchgehend unter Ziel (Belege geben mehr nicht her). Fehler gefunden und behoben: `belege_check.py finalize` leerte bei zweitem Lauf die Quellenbox (jetzt idempotent).
- Entscheidung: Ziel-Länge im Plan senken; Praxis-Einträge in `material/fakten.md` für Veneers, Bleaching, Retainer-Entfernung fehlen.
