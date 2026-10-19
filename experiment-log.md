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

## 2026-10-19 · Batch mit 10 Artikeln (neue Keywords) und Prozess-Optimierung
- Hypothese: Der Ablauf Plan → Belege je Thema → Schreiben → Review → Fix schafft 10 Entwürfe pro Batch ohne Qualitätsverlust; Review und Koordination sind die Wartezeit.
- Test: veneers, bleaching, retainer, aligner, zahnbleaching, zähne aufhellen, schiefe zähne, zähne verschieben sich, zahnspange draht, zähne richten lassen (WP-Entwürfe 610–619; elf alte Entwürfe im Papierkorb).
- Ergebnis: Alle Hürden grün nach einer Fix-Runde, Review 1× rot (veneers: „100 von 100“ aus einer Studie mit 48 Veneers), 9× gelb (1–5 wichtige Befunde). Kosten: DataForSEO 0,25 USD für 10 Briefe (0,018–0,034 USD je Brief), KI-Verbrauch grob 1,9 Mio. Tokens (Schreiben und Fix ca. 50 %, Plan 22 %, Review 14 %, Belege 14 %); Agentenzeit ca. 15 Min., Review seriell ca. 9 Min. Probleme: Review-Log geleert (Standardwert 99 erzwang Vollprüfung), Stufen-Barrieren, zwei Themen für einen Artikel (überflüssiger Beleg-Lauf), Befunde von Hand weitergereicht, Regelkonflikte (Zahlenprüfung, Quellenlimit, Wortbudget), Korrekturen ungeprüft, 7 von 10 Artikeln ohne Praxis-Block.
- Entscheidung (Alexander 19.10.2026: alle Verbesserungen umsetzen): `hwg_check.py` (Muster vorab), Spalte „Formulierung“ in der Beleg-Tabelle, `pipeline.py abschluss`, Review je Artikel parallel mit Befunddatei, kurze Agentenberichte plus `backlog.py`, Themenobergrenze 3, Workflow `artikel-batch`, Review-Log-Standard 0, harte Längengrenze 60 %. Messung im nächsten Batch: Zahl wichtiger Befunde je Artikel (Ziel unter 2), Dauer und Tokens.

## 2026-10-19 · Entscheidung: Batch = ein Themencluster
- Hypothese: Ein Batch aus einem Themengebiet (z. B. Retainer) spart Rechenaufwand und Rückfragen: ein Researcher-Lauf, Kostenrahmen und Praxisfragen einmal, Cluster-Plan trennt Blickwinkel und Nebenkeywords, interne Links gehen im Cluster auf.
- Umsetzung: `waehle_keywords.py` wählt standardmäßig ein Thema, Cluster-Plan-Stufe, Beleg-Review einmal je Thema, Linkplan `geplant` → `live`, `weiterlesen`, Workflow `artikel-batch` mit Thema.
- Offene Messung (erster Themen-Batch, Vorschlag Retainer): Tokens und Dauer je Artikel gegenüber dem Mischbatch (ca. 190.000 Tokens je Artikel), Zahl wichtiger Befunde je Artikel (Ziel unter 2), Zahl der Researcher-Läufe, Zahl der zusammengelegten Keywords; später Ranking-Vergleich Cluster gegenüber Einzelartikeln (Annahme: Cluster ranken besser, nicht belegt).

## 2026-10-19 · Test Themen-Batch „aligner“ (Workflow artikel-batch) gegen Mischbatch
- Hypothese: Ein Themencluster spart Rechenaufwand, senkt wichtige Review-Befunde je Artikel (Ziel unter 2) und vermeidet Dubletten.
- Test: 10 Keywords des Themas aligner, Workflow artikel-batch (Cluster-Plan, Einzelpläne, Belege + Beleg-Review einmal, Schreiben, Review, Fix). Entwürfe nur lokal, keine WordPress-Entwürfe.
- Ergebnis (Workflow): 34 Agenten, 1,91 Mio. Tokens, 21,2 Min. Laufzeit, 0 Fehler. Cluster-Plan legte 2 von 10 Keywords zusammen → 8 Artikel; ca. 239.000 Tokens je Artikel (Mischbatch grob 190.000; nicht streng vergleichbar, weil dort nur die Summe der Berichte geschätzt wurde und hier Cluster-Plan, Beleg-Review und Beleg-Korrektur dazukommen). Wichtige Review-Befunde je Artikel: 1,0 (2/1/2/0/0/2/0/1) gegenüber 3,1 im Mischbatch; Beleg-Review fand 3 wichtige und 5 kleine Befunde vor dem Schreiben. HWG-Muster-Prüfung bei allen 8 grün, Lesbarkeit 61–71, Wörter 990–1.575 (Mischbatch 1.200–1.900).
- Auffälligkeiten: (1) Alle 8 Artikel wurden reviewt, weil die Rückfallregel griff (Rot bei veneers in den letzten 10 Prüfungen, Ø 3,0), die Stichprobe sparte also nichts. (2) Briefe dünn (Volumen None, 0–3 Nebenkeywords), Artikel kürzer; Vergleich eingeschränkt. (3) „drähte nach zahnspange“ und „schiene nach zahnspange“ sind Retainer-Themen und überschneiden sich mit den bestehenden Artikeln retainer und zahnspange-draht: Themenzuordnung in themen.json (Regel „zahnspange“ greift vor Retainer-Mustern). (4) Fix-Runde nur bei 5 von 8 Artikeln nötig.
- Entscheidung/offen: Themenzuordnung korrigieren, Rückfallregel nach einem Rot nur für das betroffene Thema anwenden, Praxisfragen des Clusters an Alexander (Backlog), Länge pro Brief prüfen.

## 2026-10-19 · Lauf 2 „schlanke Kette“ (aligner), fehlerhaft, Messung ungültig
- Änderungen gegenüber Lauf 1: Cluster-Planer schreibt alle Einzelpläne, Schreibpaket, Review mit Patches durch Skript, Beleg-Korrektur nur bei wichtigen Befunden, Rückfallregel je Thema.
- Ergebnis: 20 statt 34 Agenten, 1,14 Mio. statt 1,91 Mio. Tokens, 18,3 statt 21,2 Min.; aber nur 4 von 7 aktiven Artikeln lagen am Ende als Entwurf vor (3 Writer scheiterten, der Workflow meldete „fertig“). Ursache: Der Beleg-Review galt nach der Beleg-Korrektur als „veraltet“ (Datei-Zeitstempel), `prepare` legte deshalb kein Skelett an; ein Writer baute es von Hand, die anderen scheiterten still. Dazu zwei Schwächen: der Workflow prüfte nicht, ob ein Entwurf entstand, und zwei Artikel kamen mit Lesbarkeit 59 (Grenze 58) durch.
- Entscheidung: `pipeline.py belegreview-ok <thema>` nach der Korrektur, Writer meldet {abschluss: ok|pruefen|kein_entwurf}, Workflow überspringt Review ohne Entwurf und listet fehlende Artikel. Lauf 3 mit denselben 10 Keywords vom gleichen Ausgangsstand.
