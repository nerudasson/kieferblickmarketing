# Stil und Format der Wissensartikel

Gilt für jeden Artikel. Maßstab: Alexander erklärt einer Patientin etwas auf dem Behandlungsstuhl. Nicht: Alexander schreibt eine Übersichtsarbeit.

## Die Leserin: Julia
38, berufstätig, Mülheim und Umgebung, früher Spange, Retainer irgendwann weggelassen, Zähne wandern wieder. Keine Fachfrau. Liest auf dem Handy, zwischen Terminen, oft abends. Sorge: „Ich zahle viel und niemand übernimmt am Ende Verantwortung.“ Sie will wissen: Was ist los? Ist das schlimm? Was kostet es? Was muss ich tun? Wer kümmert sich? Sie will keine Studienlage, sondern eine Antwort, der sie trauen kann.

Nebenleser (Schnarch-Patient 40–60, Bestandspatient): gleiche Sprache. Die meisten Leser kommen aus ganz Deutschland, nicht aus Mülheim, und sind noch nicht terminbereit: Sie brauchen zuerst Klarheit (Passt es? Was kostet es am Ende? Wer kümmert sich?). Blocker, auf die ein Artikel antworten kann: B1 Verantwortung, B2 Endpreis, B3 Ergebnisrisiko, B4 Rückfall, B5 Alltag, B6 Zeit. Vierte Frage neben „wie schön, wie lange, was kostet“: „Wer begleitet mich?“

## Ziel Lesbarkeit
- **Flesch-Index (Amstad) mindestens 60, Ziel 65.** Prüfung mit `scripts/lesbarkeit.py`. Der Wert gilt für den ganzen Text, nicht nur für den Anfang.
- Ø 10–14 Wörter pro Satz, kein Satz über 25 Wörter.
- Wenige lange Wörter: Das ist der größte Hebel. Das Skript zählt Silben, nicht Fachlichkeit.

## So klingt es
- Sprechen Sie wie am Stuhl: „Das kennen viele.“ „Stellen Sie sich einen Zaun in weichem Boden vor.“ „Ich sage Ihnen ehrlich, was dagegen spricht.“
- Direkte Anrede („Sie“), Ich-Form des Arztes für Einschätzungen und Zusagen („Ich schaue mir das an.“), „wir“ fürs Team.
- Ein Bild pro Abschnitt, wo es hilft (Zaun im weichen Boden, Gummiband). Keine Metaphern-Ketten, keine Übertreibung.
- Fragen stellen, die Julia selbst stellt: „Ist das schlimm?“ „Muss ich da sofort hin?“
- Aktiv statt Passiv. Verben statt Hauptwort-Ketten: „Der Zahn wandert“ statt „es kommt zu einer Migration“.
- Satzrhythmus variieren: kurz. Kurz. Dann ein längerer Satz, der den Punkt setzt.
- Zahlen statt Adjektive. Zahlen kurz und rund, mit Einordnung: „etwa jeder Zehnte“ statt „10,3 %“.
- Fachwort höchstens einmal, sofort in einem Halbsatz erklärt. Danach das einfache Wort. Beispiele: Retention → „Halten“, Relapse → „Rückfall“, Parodontitis → „Zahnbetterkrankung (Parodontitis)“, Prämolaren → „kleine Backenzähne“.

## Was raus muss (wirkt wissenschaftlich)
- Studiennamen, Jahreszahlen, Stichprobengrößen, „Metaanalyse“, „Verzerrungsrisiko“, „randomisiert“, „Cochrane“ im Fließtext. Das gehört in die Quellenbox am Ende. Im Text höchstens: „Studien zeigen …“ [1] oder „Fachleute sind sich hier nicht einig.“ [2].
- Verschachtelte Sätze mit „sofern“, „hinsichtlich“, „diesbezüglich“, „darüber hinaus“, „gegebenenfalls“, „im Rahmen von“.
- Einschränkungsketten („kann unter Umständen in manchen Fällen“). Ein „kann“ pro Aussage reicht.
- Mehr als ein Beleg pro Satz. Ehrlichkeit über die Datenlage in einem kurzen Satz, nicht in einem Absatz: „Die Datenlage ist dünn. Ich sage Ihnen, was ich daraus mache.“
- Aufzählungen der Art „laut A, laut B, laut C“. Stattdessen: das Ergebnis, dann Quelle in Klammer [n].

Die Faktenregel bleibt: Jede Zahl und Behauptung steht in `material/fakten.md` oder hat eine Quelle in der Quellenbox. Einfach schreiben heißt nicht ungenau schreiben. Wenn eine Aussage sich nicht einfach sagen lässt, ohne falsch zu werden, bleibt sie draußen oder bekommt `[FAKT FEHLT: …]`.

## Aufbau des Artikels: erst Julias Frage, dann der Hintergrund
Julia fragt „Ist das schlimm, und was mache ich jetzt?“ Die Studienlage kommt danach. Reihenfolge:

| # | Baustein | Umfang | Pflicht |
|---|---|---|---|
| 1 | **Kurzfassung** (Frontmatter `kurz`) | 3 Sätze, je ein Satz = eine Aussage. Im Theme als Box oben. | immer |
| 2 | **Einstieg** | 2–3 Sätze: direkte Antwort (die KI-Übersicht von Google zeigt sie ebenfalls), Julias Situation benennen | immer |
| 3 | **Was Sie jetzt tun können / Wann ein Termin sinnvoll ist** | Liste, 3–5 Punkte, ohne Druck, ohne Diagnose. Steht vorn, nicht am Ende. | immer |
| 4 | **Abschnitte (H2)**, meist als Fragen aus dem SEO-Brief | je 1–2 kurze Absätze, dann Liste, Tabelle oder Merksatz | 3–5 |
| 5 | **Aus der Praxis** (`> Praxis: …`) | 3–5 Sätze in Alexanders Ich-Form, nur aus `material/fakten.md` (Abschnitt „Persönliche Einschätzung“). Fehlt sie dort: `> Praxis: [FAKT FEHLT: …]`, nichts erfinden. | immer |
| 6 | **Nachteile ehrlich** | Liste | immer |
| 7 | **Tabelle** bei Vergleich, Kosten, Varianten | 2–4 Spalten, höchstens 6 Zeilen | Pflicht bei Intent Kosten/Vergleich |
| 8 | **FAQ** | 3–5 Fragen, Antwort höchstens 3 Sätze | immer |
| 9 | **Schlussblock „So arbeiten wir“** (`> Zusage: …`) | 2–3 Sätze: „Ein Arzt. Ein Plan. Bis zum Retainer.“ Was heißt das für dieses Thema konkret? Nur belegte Zusagen (Antwortzeit, Festpreis-Zusage, Nachkorrektur, Notfalltermin, Zweitmeinung; siehe `kontext/angebot-und-preise.md`). Link auf `/zusagen/` | immer |
| 10 | **CTA** (`> CTA: …`) | ein Satz, eine Handlung, passend zur Einstiegsleiter: Checkliste „7 Fragen vor der Unterschrift“, Online-Smile-Check (19 €, persönliche Einschätzung von Alexander, `/smile-check/`) oder kostenlose Erstberatung vor Ort (Wert 300 €, `/erstermin-aligner/`). Kein Druck, keine Frist | immer |
| 11 | **Weiterlesen** | 2–4 interne Links aus `daten/linkplan.csv` | immer |
| 12 | **Quellen** | nummerierte Liste | immer |

**Module der Vorlage:** Kopf-Box, Smile-Check-Box (nach der zweiten Überschrift) und Schlussmodul fügt die WordPress-Vorlage automatisch ein. Der Writer schreibt sie nicht und erfindet keine eigenen Lead Magnets. Der CTA im Text bleibt ein einzelner, zum Thema passender Satz, damit nichts doppelt wirkt.

Feste Schlussüberschrift vor Zusage und CTA: „Was heißt das für Sie?“ (nicht „Fazit“).

Boxen sparsam: höchstens **2** Merksätze oder Hinweise pro Artikel (`> Merksatz:`). Mehr nimmt ihnen die Wirkung.

Wechsel-Regel: Nie mehr als 3 Absätze Fließtext hintereinander. Danach muss ein anderes Element kommen. Ein Absatz hat höchstens 3 Sätze.

Fließtext ist richtig für: Erklärung eines Zusammenhangs, Bild, persönliche Einschätzung. Liste für: Gründe, Schritte, Fragen, Vor- und Nachteile. Tabelle für: Vergleich mehrerer Dinge in mehreren Merkmalen. Merksatz für: die eine Sache, die hängen bleiben soll.

## Länge
Keine Mindestlänge, keine feste Obergrenze. Die Länge folgt der **einen Hauptfrage**. Richtwerte (ohne Quellen): Info bis ca. 1.000 Wörter, Kosten/Vergleich bis ca. 1.400. Das Skript meldet darüber einen Hinweis, keinen Fehler. Wird ein Artikel länger, weil Nebenfragen mitlaufen, diese als eigenen Artikel im Cluster ausgliedern und im Text darauf verlinken. Nicht kürzen, indem man Belege oder Nachteile streicht.

## Markdown-Konventionen (für die spätere Umwandlung nach WordPress)
- Frontmatter: `title, slug, keyword, cluster, intent, autor, meta_description, status` plus `kurz, ursache, behandlung, dauer, kosten, ablauf` (jeweils 1–2 Sätze, Entsprechung der Theme-Felder `kb_kurz`, `kb_ursache`, `kb_behandlung`, `kb_dauer`, `kb_kosten`, `kb_ablauf`). Felder, für die der Artikel nichts hergibt, leer lassen, nicht füllen.
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

## Selbstcheck vor der Abgabe
1. `python3 .claude/skills/seo-pipeline/scripts/lesbarkeit.py daten/entwuerfe/<slug>.md` ausführen, bis der Lauf „OK“ meldet (max. 3 Überarbeitungen).
2. Test „Stuhl“: Laut lesen. Würde Alexander das so zu einer Patientin sagen? Stolpert er, ist der Satz zu lang oder zu technisch.
3. Test „Handy“: Scrollt man durch, sieht man in jedem Bildschirm etwas anderes als Fließtext?
