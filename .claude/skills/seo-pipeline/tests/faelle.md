# Testfälle seo-pipeline
1. **Normalfall:** Queue mit 3 offenen Zeilen („zähne verschieben sich“, „retainer draht gelöst“, „aligner kosten“). Erwartung: 3 Entwürfe, 3 Prüfungen, Status geprueft, nichts auf publish.
2. **Compliance rot:** Keyword „zähne begradigen ohne risiko“ verleitet zu Garantie. Erwartung: Reviewer meldet rot, Writer korrigiert oder Status blockiert, nie WP-Entwurf mit rot.
3. **Fakten fehlen:** `material/fakten.md` leer, Keyword „aligner erfahrungen“. Erwartung: `[FAKT FEHLT]`-Marker, keine erfundene Patientengeschichte.
4. **Doppelung:** „aligner kosten“ und „aligner kosten preise“. Erwartung: `queue.py check` meldet Überschneidung.
5. **Keine Zugangsdaten:** WP-Variablen fehlen. Erwartung: Entwürfe bleiben lokal, klare Meldung.
6. **Lesbarkeit:** Entwurf mit Studienzitaten im Fließtext und 5 Absätzen am Stück. Erwartung: `lesbarkeit.py` meldet PRÜFEN (Flesch, Fließtext-Wüste); nach Überarbeitung OK, Wert ≥ 60.
7. **Formatmix:** Intent „kosten“ ohne Tabelle. Erwartung: Skript meldet „Bausteine fehlen: tabelle“.
8. **Vereinfachung ohne Verfälschung:** Quelle sagt „Datenlage unsicher“. Erwartung: Text sagt es in einem einfachen Satz, schreibt nicht „Studien zeigen“ oder „sicher“; Reviewer meldet sonst gelb/rot.
9. **Reihenfolge und Persönliches:** Artikel ohne „Aus der Praxis“ und ohne „So arbeiten wir“. Erwartung: Skript meldet fehlende Bausteine; fehlt Alexanders Einschätzung in `fakten.md`, steht `> Praxis: [FAKT FEHLT: …]`, keine erfundene Aussage.
10. **Länge:** Info-Artikel mit 1.600 Wörtern. Erwartung: Hinweis „Nebenfragen auslagern“, kein Fehler.
11. **Planer:** Brief mit 14 Nebenkeywords und 4 Fragen. Erwartung: Plan mit 4–7 Abschnitten, jedem Abschnitt ein Element, 4–6 Belegfragen, `plan-check` OK; Preisfragen nur mit „ab“-Preis; Cluster ohne Beleg unter „Nicht abgedeckt“.
12. **Element-Wahl:** Intent Kosten. Erwartung: mindestens ein Abschnitt als Tabelle; nie mehr als zwei Fließtext-Abschnitte hintereinander.
13. **Belegbedarf:** Zwei Artikel desselben Themas. Erwartung: der Researcher recherchiert nur Belegfragen, die nicht schon in der Beleg-Datei stehen, und ergänzt `abgedeckt`.
14. **Ziel-Länge:** Artikel unter 75 % des Zielbereichs. Erwartung: Hinweis „wirkt zu dünn“, kein Fehler.
