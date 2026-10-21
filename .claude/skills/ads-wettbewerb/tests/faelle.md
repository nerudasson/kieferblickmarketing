# Testfälle ads-wettbewerb
1. **Kostenvorschau:** `beobachtung.py snapshot --dry-run` nennt Zahl der Abfragen und Kosten, ohne Netzwerkzugriff und ohne Datei. Erwartung: "81 Abfragen, ca. 0.16 USD".
2. **Vergleich zweier Wochen:** Zwei Dateien in `daten/ads/beobachtung/` (Fixtures mit einer gleichen und einer neuen Anzeige), `report`. Erwartung: neue Anzeige unter "Neu seit", verschwundene unter "nicht mehr gesehen", Langläufer-Abschnitt sagt "noch keine".
3. **Fehler:** Abfrage schlägt dreimal fehl. Erwartung: Eintrag mit `fehler`, kein Abbruch, Auswertung zählt ihn nicht mit.
4. **Obergrenze:** `max_abfragen` auf 10 setzen. Erwartung: Abbruch mit Meldung vor jeder Abfrage.
