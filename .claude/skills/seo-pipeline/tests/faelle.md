# Testfälle seo-pipeline
1. **Normalfall:** Queue mit 3 offenen Zeilen („zähne verschieben sich“, „retainer draht gelöst“, „aligner kosten“). Erwartung: 3 Entwürfe, 3 Prüfungen, Status geprueft, nichts auf publish.
2. **Garantie-Keyword:** Keyword „zähne begradigen ohne risiko“ verleitet zu einer Garantie. Erwartung: Der Writer formuliert ohne Zusage (Zusagen statt Garantie), der Entwurf kommt mit Hinweis an Alexander in WordPress.
3. **Fakten fehlen:** `material/fakten.md` leer, Keyword „aligner erfahrungen“. Erwartung: `[FAKT FEHLT]`-Marker, keine erfundene Patientengeschichte.
4. **Doppelung:** „aligner kosten“ und „aligner kosten preise“. Erwartung: `queue.py check` meldet Überschneidung.
5. **Keine Zugangsdaten:** WP-Variablen fehlen. Erwartung: Entwürfe bleiben lokal, klare Meldung.
