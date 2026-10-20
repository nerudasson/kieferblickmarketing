# Anweisung: Zusatz-Keywords in ältere Artikel einarbeiten

Einarbeitung, kein Neuschreiben. Zielartikel `<slug>` steht im Prompt.

1. Lies `daten/einarbeitung/<slug>.md` (Nebenkeywords und Fragen zusammengelegter Themen), `daten/entwuerfe/<slug>.md`, falls vorhanden `daten/pakete/<slug>.md` und das Faktenblatt des Themas (`daten/belege/<thema>-web.md`: aligner, biss, bleaching, retainer, schnarchen oder veneers).
2. Arbeite die Nebenkeywords und Fragen mit gezielten Edit-Änderungen ein: Phrasen gebeugt oder umschrieben in vorhandene Absätze, H2 oder FAQ-Fragen; höchstens 2 neue FAQ-Einträge, nur wenn mit vorhandenen Quellen [n] oder `material/fakten.md` belegbar, sonst weglassen.
3. Keine neuen Tatsachen ohne Beleg. Wortzuwachs höchstens 150.
4. Unverändert lassen: Frontmatter (title, seo_titel, meta_description, Infobox-Felder), Kurz gesagt (3 Zeilen), Quellenliste und Zitatnummern, Preise, Merksatz, Zusage/CTA.
5. NICHT einarbeiten: Phrasen zu Kindern/Jugendlichen, Marken, Städten, Superlative (bester, effektivster), Retainer-Preise, Selbstanleitungen.
6. Regeln: Mengenwörter höchstens 6, keine Studiensprache (Leitlinie, randomisiert, Studienlage), Rechtschreibung und Großschreibung korrekt auch in H2/FAQ, keine Heilversprechen, Schlafapnoe nur ärztlich abgeklärt, Veneers ohne Kieferblick-Preise, interne Links nur `/<kategorie>/<slug>/` (Überbiss: `/aligner/uberbiss/`, Unterbiss: `/aligner/unterbiss/`).
7. Danach `python3 .claude/skills/seo-pipeline/scripts/pipeline.py abschluss <slug>`; bei PRÜFEN höchstens eine weitere Runde.
8. Bericht höchstens 25 Wörter: Anzahl eingearbeiteter Phrasen + ABSCHLUSS-Status.
