# Anweisung: neue Belege in bestehende Artikel einbauen

Einarbeitung, kein Neuschreiben. Der Prompt nennt die neuen Aussagen (Faktenblatt und B-IDs) und die Artikelgruppe, die du bearbeiten darfst (nur diese Dateien unter `daten/entwuerfe/`).

1. Lies die neuen Aussagen im Faktenblatt (Spalten Aussage, Einschränkung, **Formulierung**; Quelle zur ID in der Quellentabelle). Die Einschränkung gilt verbindlich: Zahlen, Population und Studiengüte nicht überdehnen.
2. Suche in den erlaubten Artikeln (`grep`) die Stellen, an denen die Aussage eine Lücke füllt, eine unbelegte Formulierung stützt oder eine ältere Aussage korrigiert. Baue nur ein, wo sie zum Thema des Artikels passt. Kein Pflichteinbau: passt sie nirgends, lass es.
3. Einbau mit gezielten Edit-Änderungen: ein bis zwei Sätze, die Formulierung aus der Faktenblatt-Spalte als Vorlage, Zitat als Marker `[B75]` (B-ID in eckigen Klammern) direkt hinter dem Satz. `pipeline.py abschluss <slug>` setzt die Nummer und trägt die Quelle in die Quellenliste ein (an einem Beispiel geprüft).
4. Höchstens 60 Wörter Zuwachs je Artikel. Unverändert lassen: Frontmatter, Kurz gesagt (3 Zeilen), Infobox-Felder, Preise, Merksatz, Zusage/CTA. Keine Euro-Beträge, die nur eine Quelle tragen (Einzelquelle steht in der Einschränkung). Widerspricht die neue Aussage einem Satz im Artikel, korrigiere den Satz.
5. Regeln: Mengenwörter höchstens 6, keine Studiensprache (Leitlinie, randomisiert, Studienlage, Kohorte), Rechtschreibung/Großschreibung korrekt, keine Superlative, keine Heilversprechen, keine Marken, interne Links `/<kategorie>/<slug>/`.
6. Nach jedem geänderten Artikel `python3 .claude/skills/seo-pipeline/scripts/pipeline.py abschluss <slug>`; bei PRÜFEN höchstens eine weitere Runde.
7. Schreibe die Liste der geänderten Artikel (ein Slug je Zeile, mit B-ID) nach `daten/einarbeitung/belege-<gruppe>.txt` (Gruppenname steht im Prompt). Bericht höchstens 30 Wörter: Anzahl geänderter Artikel, Anzahl eingebauter Belege.
