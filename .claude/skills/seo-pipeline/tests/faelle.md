# Testfälle seo-pipeline
1. **Normalfall:** Queue mit 3 offenen Zeilen („zähne verschieben sich“, „retainer draht gelöst“, „aligner kosten“). Erwartung: 3 Entwürfe, 3 Prüfungen, Status geprueft, nichts auf publish.
2. **Compliance rot:** Keyword „zähne begradigen ohne risiko“ verleitet zu Garantie. Erwartung: Reviewer meldet rot, Writer korrigiert oder Status blockiert, nie WP-Entwurf mit rot.
3. **Fakten fehlen:** `material/fakten.md` leer, Keyword „aligner erfahrungen“. Erwartung: `[FAKT FEHLT]`-Marker, keine erfundene Patientengeschichte.
4. **Doppelung:** „aligner kosten“ und „aligner kosten preise“. Erwartung: `warteschlange.py check` meldet Überschneidung.
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

## Fall 15: Länge folgt dem SEO-Brief (19.10.2026)
- Ausgangslage: Plan `retainer-zahne` mit ziel_woerter 1200-1600, Brief empfiehlt 1600-2400; Plan `retainer-entfernen-kosten` 1000-1500, Brief 2900-4400.
- Erwartung: `skelett.py plan-check` meldet beide als FEHLER („liegt unter der SEO-Empfehlung“); der Planer legt Abschnitte und Budgets neu aus. Bei fertigem Entwurf nennt `lesbarkeit.py` Abschnitte unter 70 % ihres Budgets.

## Fall 16: SEO-Prüfungen (19.10.2026)
- Plan ohne Keyword-Zuordnung oder mit weniger als 2 Phrasen in H2/FAQ: `plan-check` FEHLER.
- Entwurf, in dem die Fokus-Phrase nicht oder mehr als 3,5 % vorkommt: harter Fehler; Dichte außerhalb 0,5–2,5 %, leeres Drittel, weniger als 4 zugeordnete Nebenkeywords oder weniger als 2 interne Links: nur Hinweis, kein Rücklauf.

## Fall 17: Tiefe gegenüber der Konkurrenz (19.10.2026)
- Plan ohne Lücken-Abschnitt (`LÜCKE:`), mit weniger als 5 FAQ-Fragen oder (Intent Kosten) ohne Belegfrage zum Kostenrahmen: `plan-check` FEHLER.
- Brief enthält „Wettbewerber-Elemente (Median …)“: Plan hat mindestens so viele Tabellen-Abschnitte (max. 3) und FAQ (min. 5, max. 8 gefordert).
- Preis mit Quelle (`[B..]`) als Marktüberblick wird vom Prüfskript nicht beanstandet; Preis ohne Quelle außerhalb der erlaubten Liste ist hart.
- `wp_publish.py`: Inhaltsverzeichnis erst ab 1.200 Wörtern; Feld `kb_geprueft` = Veröffentlichungsdatum des Entwurfs.

## Fall 18: Theme-Verträglichkeit (19.10.2026)
- Entwurf mit Zitaten: im WordPress-HTML stehen `<sup>n</sup>`, keine `[n]`; keine Klasse `kb-toc`, kein H2 „Quellen“, Quellenbox mit `open`.

## Fall 18: Muster-Vorprüfung (19.10.2026)
- Entwurf mit „nachweislich“, „Julia“, „Sie müssen nicht sofort handeln“, „genau steuern“, „100 %“ ohne Zitat: `hwg_check.py` meldet HART, `pipeline.py check/gates/abschluss` PRÜFEN, `wp_publish.py` bricht ab.
- „nicht genau vorhersagen“, „nicht für immer“, „am besten“ (Redewendung), zitierter Vergleich: kein Treffer.
- Vor-Fix-Fassungen aus Commit 6622412 (`git show 6622412:daten/entwuerfe/zahnbleaching.md`) liefern die Befunde des Reviews vom 19.10.

## Fall 19: Endstand (19.10.2026)
- `pipeline.py abschluss <slug>`: bei neuen `[B..]`-Zitaten läuft `finalize`, danach erneut check; Ausgabe „ABSCHLUSS OK“ oder die Fehlerliste. 13 Quellen: `finalize` nennt die nur einmal zitierten.

## Fall 20: Leeres Review-Log (19.10.2026)
- `pipeline.py review` mit leerem Log: Standardwert 0 statt 99, nur die ersten 3 Artikel je Thema, Kosten/Vergleich, Praxis-Block, Kasse/Recht und viele Zitate werden geprüft.

## Fall 21: Themenobergrenze (19.10.2026)
- `waehle_keywords.py --top 10`: höchstens 3 neue Artikel je Thema; „zahnspange draht“ gehört zum Thema retainer (kein überflüssiger Beleg-Lauf).

## Fall 22: Backlog (19.10.2026)
- `backlog.py add nebenartikel <slug> "<Text>"` zweimal mit gleichem Text: zweiter Aufruf meldet „schon vorhanden“.
