# Testfälle reel-agent

1. **Gewinner-Auswertung:** `reels.py winners` mit `raw/2026-10-27_top.csv`. Erwartet: drmarkcostes ohne Treffer (max 2,8x); QUEEN01 und TIF01 als „wahrscheinlich beworben“; KOIS01/03/05 beworben; doctor.avi DdMtzfrxjkE ≈ 750x. Zahlen mit deutschem Tausenderpunkt.
2. **Check, gutes Beispiel:** `reels.py check daten/reels/output/2026-10-27_weekly.md` gibt „Keine Treffer“ (Exit 0).
3. **Check, schlechtes Beispiel:** Hook mit „guaranteed“, „lazy“, „ClinCheck“ ohne ⚠️, 18 Wörtern, Trigger „rage“, Ausrufezeichen und Skript mit Stichwort FREEBIE plus Preis. Erwartet: je ein FEHLER pro Verstoß, Preis als HINWEIS, Exit 1 (am 27.10.2026 geprüft).
4. **Lernschleife leer:** `reels.py own` bei leerer `own_performance.csv` meldet die Lücke und rechnet nicht.
5. **Wochenlauf ohne frischen Scout:** Der Agent arbeitet mit vorhandenen Rohdaten, nennt die Lücke (Hook-Frames, Reel-Codes) in Abschnitt 1 und stellt die Frage nach dem Scout in Abschnitt 6.
6. **Persönliche Geschichte:** Ein Hook mit „I used to …“ trägt immer [ ] und ⚠️; der Agent erfindet keine Biografie.
