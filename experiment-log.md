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

## 2026-10-19 · Testlauf 2 (neue Mechanik) mit denselben 5 Keywords
- Hypothese: Länge aus SEO-Brief und Plan-Budget, Keyword-Zuordnung, Lücken-Abschnitt, Kostenrahmen Dritter und Praxisfragen heben die Entwürfe auf Wettbewerbsniveau.
- Test: veneers, bleaching, retainer-zahne, schiefe-zahne, retainer-entfernen-kosten (WP-Entwürfe 585–589; Test 1 mit 570–574 im Papierkorb).
- Ergebnis: Wörter 1.036 / 1.300 / 1.585 / 1.706 / 2.864 (Test 1: 1.028 / 981 / 1.210 / 923 / 960). Alle Hürden grün, SEO-Hinweise bis auf eine Dichte-Meldung leer, Review 5× gelb (0 rot). Kostenrahmen über GOZ (Retainer, Veneers) und Verbraucherzentrale (Bleaching) belegt. Gefundene Prozessfehler: Belegstufe merkte geänderte Pläne nicht (Stempel eingeführt), „LÜCKE:“ landete in Überschriften, Smile-Check als CTA bei Bleaching.
- Entscheidung: Mechanik behalten. Offen: Praxisfragen an Alexander, Marktspanne Retainer in Euro, Bilder im Beitrag.

## 2026-10-19 · Testlauf 2, Nachbesserung mit Praxisangaben und Marktspannen
- Hypothese: Alexanders Praxisangaben, Euro-Spannen Dritter (mind. zwei Quellen) und gestrichene Zitate schließen die Lücken gegenüber der Konkurrenz (Vergleich 19.10.2026).
- Test: dieselben fünf Entwürfe (WP 585–589) mit Praxis-Block, Dauer/Ablauf, Marktüberblick, Quellenlimit 12.
- Ergebnis: Wörter 1.175 / 1.341 / 1.716 / 1.934 / 3.111, alle Checks grün, Review 2× grün und 3× gelb, Befunde eingearbeitet. Prozessfehler behoben: `finalize` nahm nur die erste Quelle einer Aussage (jetzt alle) und das Limit von 8 Quellen ließ Writer Belege streichen (jetzt 12).
- Geklärt (Alexander 19.10.2026): 2-Jahres-Zusage gilt nur für Kieferblicks eigene feste Retainer, Begriff „Retainer-Klub“ wie im Angebot, Praxis-Zahl „etwa jeder zehnte Patient“ als eigene Erfahrung ok. Offen: Komposit-Veneer-Spanne (nur eine Quelle), Bilder im Beitrag.

## 2026-10-19 · Neuaufsatz der drei älteren Artikel mit der neuen Mechanik
- Test: aligner-kosten, wie-lange-retainer-tragen, zahne-begradigen (neue Briefs, Pläne mit Keyword-Zuordnung und Lücken-Abschnitt, Belege inkl. Aligner-Kostenrahmen Dritter, Praxisangaben aus fakten.md).
- Ergebnis: Wörter 1.187 / 1.470 / 1.647 (alt: 857 / 850 / 1.009), alle Checks grün, Review 3× gelb, Befunde eingearbeitet. WordPress-Entwürfe 602–604; die alten Entwürfe 462, 546, 547, 569 liegen im Papierkorb.
- Offen: zahne-begradigen hat keine eigene Praxis-Zeile in fakten.md (nutzt schiefe-zahne), Alt-Text und Bilder im Beitrag.
