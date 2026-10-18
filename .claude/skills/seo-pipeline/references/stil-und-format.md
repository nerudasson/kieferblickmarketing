# Stil-Hintergrund und Markdown-Konventionen

Verbindliche Regeln stehen in `regeln.md`. Diese Datei liefert Hintergrund zur Leserin, Klangbeispiele und die Markdown-Konventionen für die WordPress-Umwandlung. Gilt für jeden Artikel. Maßstab: Alexander erklärt einer Patientin etwas auf dem Behandlungsstuhl. Nicht: Alexander schreibt eine Übersichtsarbeit.

## Die Leserin: Julia
38, berufstätig, Mülheim und Umgebung, früher Spange, Retainer irgendwann weggelassen, Zähne wandern wieder. Keine Fachfrau. Liest auf dem Handy, zwischen Terminen, oft abends. Sorge: „Ich zahle viel und niemand übernimmt am Ende Verantwortung.“ Sie will wissen: Was ist los? Ist das schlimm? Was kostet es? Was muss ich tun? Wer kümmert sich? Sie will keine Studienlage, sondern eine Antwort, der sie trauen kann.

Nebenleser (Schnarch-Patient 40–60, Bestandspatient): gleiche Sprache. Die meisten Leser kommen aus ganz Deutschland, nicht aus Mülheim, und sind noch nicht terminbereit: Sie brauchen zuerst Klarheit (Passt es? Was kostet es am Ende? Wer kümmert sich?). Blocker, auf die ein Artikel antworten kann: B1 Verantwortung, B2 Endpreis, B3 Ergebnisrisiko, B4 Rückfall, B5 Alltag, B6 Zeit. Vierte Frage neben „wie schön, wie lange, was kostet“: „Wer begleitet mich?“

## So klingt es
- Sprechen Sie wie am Stuhl: „Das kennen viele.“ „Stellen Sie sich einen Zaun in weichem Boden vor.“ „Ich sage Ihnen ehrlich, was dagegen spricht.“
- Direkte Anrede („Sie“), Ich-Form des Arztes für Einschätzungen und Zusagen („Ich schaue mir das an.“), „wir“ fürs Team.
- Ein Bild pro Abschnitt, wo es hilft (Zaun im weichen Boden, Gummiband). Keine Metaphern-Ketten, keine Übertreibung.
- Fragen stellen, die Julia selbst stellt: „Ist das schlimm?“ „Muss ich da sofort hin?“
- Aktiv statt Passiv. Verben statt Hauptwort-Ketten: „Der Zahn wandert“ statt „es kommt zu einer Migration“.
- Satzrhythmus variieren: kurz. Kurz. Dann ein längerer Satz, der den Punkt setzt.
- Zahlen statt Adjektive. Zahlen kurz und rund, mit Einordnung: „etwa jeder Zehnte“ statt „10,3 %“.
- Fachwort höchstens einmal, sofort in einem Halbsatz erklärt. Danach das einfache Wort. Beispiele: Retention → „Halten“, Relapse → „Rückfall“, Parodontitis → „Zahnbetterkrankung (Parodontitis)“, Prämolaren → „kleine Backenzähne“.

## Stolperstellen (aus Testlauf 16.10.2026)
- Leere Sätze streichen: „Ein Retainer hält nur, solange er hält.“ → „Ein Retainer wirkt nur, solange er sitzt und getragen wird.“
- Verkrampfte Ehrlichkeit streichen: „Eine feste Zeitangabe kann ich Ihnen nicht ehrlich geben.“ → „Eine feste Zeitangabe wäre nicht ehrlich.“ oder einfach: „Das ist bei jedem anders.“
- „Datenlage dünn“ höchstens einmal, nicht als Disclaimer unter jedem Abschnitt.
- Zahlen als Alltagssatz: „Jeder fünfte feste Retainer löst sich im ersten Jahr“ statt Prozentblock mit Methodenhinweis (nur, wenn die Quelle genau das hergibt).
- Zeitangaben so wie in der Quelle, nicht umetikettiert.

## Markdown-Konventionen (für die spätere Umwandlung nach WordPress)
- Frontmatter: `title, slug, kategorie, keyword, cluster, intent, autor, meta_description, status` plus `kurz, ursache, behandlung, dauer, kosten, ablauf` (jeweils 1–2 Sätze, Entsprechung der Theme-Felder `kb_kurz`, `kb_ursache`, `kb_behandlung`, `kb_dauer`, `kb_kosten`, `kb_ablauf`). Felder, für die der Artikel nichts hergibt, leer lassen, nicht füllen.
- SEO-Felder: `seo_titel` → `_yoast_wpseo_title`, `meta_description` → `_yoast_wpseo_metadesc`, `fokus_keyword` → `_yoast_wpseo_focuskw`.
- `kurz:` besteht aus 3 Zeilen (YAML-Block mit `|`).
- `> Merksatz: …` → Absatz mit Klasse `kb-merksatz`
- `> CTA: …` → Absatz mit Klasse `kb-cta`
- `> Praxis: …` → Hinweisblock `kb-hinweis` („Aus der Praxis“)
- `> Zusage: …` → Block „So arbeiten wir“
- Markdown-Tabelle → Tabelle mit Klasse `kb-vergleich`
- `### Frage?` unter `## Häufige Fragen` → aufklappbarer Block `kb-faq`
- `## Quellen` mit nummerierter Liste → Block `kb-quellen`
- Fußnoten als `[1]`, `[2]`. Wenige, nur an Zahlen und starken Aussagen.
- Interne Links als normale Markdown-Links auf `/wissen/<slug>`.
