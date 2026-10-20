# Umsetzungsplan Artikel (Stand 20.10.2026)

Quelle: `daten/themenplan.csv` (erzeugt von `.claude/skills/keyword-research/scripts/themenplan.py` aus Excel 2025 und `daten/keywords-export.csv` 2026-10). Alles Annahmen, wo markiert; Zusammenlegen geschieht über Wortstämme, nicht über SERP-Daten, die Zahl der Themen ist eine Obergrenze.

## Ausgangslage
15.165 Keywords → 8.653 relevant (ohne Kinder, Städte außerhalb des Ruhrgebiets, Tiere, englische Begriffe, Marken, geparkte Produkte, ohne Themenzuordnung) → 2.010 offene Artikelthemen (ohne die 41 Artikel, die schon Queue-Zeile oder Brief haben).

## Reihenfolge (Wellen)
| Welle | Inhalt | Themen | Batches | Zeitpunkt |
|---|---|---|---|---|
| 0 | Hauptartikel (Kopfbegriffe, Schwierigkeit > 40, Volumen ≥ 200) | 11 | 4 | zuerst, damit alle Folgeartikel auf sie verlinken können |
| 1 | beste 100 von Stufe A (Volumen ≥ 200, Schwierigkeit ≤ 40) nach Score | 100 | 14 | sofort danach |
| 2 | Rest von Stufe A | 33 | 6 | nach Messung der Welle 1 |
| 3 | Stufe B (Volumen 100–199, Schwierigkeit ≤ 40) | 147 | 18 | nur nach Search-Console-Auswertung |
| 9 | Volumen < 100 | 1.719 | – | nicht umsetzen; die Begriffe fließen als Nebenkeywords in Artikel ein |

Score = Kopf-Volumen / (1 + Schwierigkeit/10) × Produktgewicht × Intentgewicht. Produktgewichte (Annahme): Aligner 1,0 · Retainer 0,9 · Schnarchen 0,9 · Aligner-Bissfehler 0,8 · Bleaching/PZR 0,8 · Veneers 0,4 (Veneers-Seite geht erst mit Labor und echten Fällen live, siehe `angebot-und-preise.md`). Intentgewichte (Annahme): Kosten und Erfahrung 1,3 · Auslöser und Rückfall 1,2 · sonst 1,0.
Innerhalb einer Welle gilt die Produktreihenfolge Retainer → Bleaching → Aligner → Bissfehler → Schnarchen → PZR → Veneers (zuerst Produkte mit vorhandenem Faktenblatt, Schnarchen und Bissfehler brauchen ein neues). Ein Batch besteht aus höchstens 10 Themen eines Produkts.

## Kosten
- Direkte Kosten: nur DataForSEO. Ein Brief je Artikel (Keyword) kostet etwa 0,025 USD (0,018–0,034), der Cluster-Plan nutzt die Briefe aller Artikel des Batches. Welle 0–2: 144 Briefe ≈ 3,60 USD; mit Welle 3: 291 ≈ 7,30 USD; alle 2.010 Themen ≈ 50 USD.
- KI-Verbrauch (Max-Abo): grob 64.000 Tokens je Artikel im schlanken Ablauf, im Veneers-Batch real etwa 110.000 mit Review und Überarbeitung. Wie viel das gegen die Nutzungsgrenzen des Abos zählt, ist nicht bekannt (Lücke): nachts erst 2 Batches, Verbrauch messen, dann anpassen.

## Hebel für geringe Kosten
1. Briefe erst unmittelbar vor dem Batch holen (nicht auf Vorrat): kein Geld für verworfene Themen, Daten bleiben frisch.
2. Zusammengelegte Varianten brauchen keinen eigenen Brief: Die Nebenkeywords des Hauptbriefs decken sie ab (Spalte „nebenkeywords“ im Themenplan).
3. Faktenblatt je Produkt einmal (Bleaching, Retainer, Veneers liegen vor; neu nötig: Schnarchen, Zahnspange/Aligner, Bissfehler = 3 Blätter, Alexander liest sie).
4. Infobox konstant je Produkt (`material/infoboxen.md`): kein Generieren, keine Nacharbeit.
5. Sprachregeln stehen jetzt im Schreibpaket und in der Prüfung: keine zweite Überarbeitungsrunde nötig.
6. Review nur gezielt: die ersten 3 je Produkt, danach jeder vierte und alles mit Skript-Warnung.
7. Wiederaufnahme: `pipeline.py prepare` überspringt vorhandene Briefe; ein Abbruch (z. B. 502) kostet kein Geld doppelt.

## Ablauf je Batch (nachts)
Themen aus `themenplan.csv` (Spalte `batch`) in die Queue (`waehle_keywords.py` bzw. Zeilen übernehmen) → `prepare` (Briefe) → Cluster-Tabelle → Faktenblatt falls Produkt neu → 10 Schreiber parallel → `gates` → Review gezielt → WordPress-Entwurf (nie veröffentlichen) → Commit und Push. Abbruch bei zwei harten Fehlern in Folge.

## Tore (Entscheidung Alexander)
- Vor Welle 1: Faktenblatt und Infobox-Felder offen für Schnarchen und PZR; Retry für DataForSEO (502).
- Nach Welle 1 (Veröffentlichung gestaffelt): Search Console auswerten (Indexierung, Impressionen, Klicks). Erst dann Welle 2 und 3.
- Alexanders Lesekapazität (Annahme 10 Minuten je Entwurf, 20 Stunden pro Woche) begrenzt auf etwa 120 Entwürfe pro Woche.
