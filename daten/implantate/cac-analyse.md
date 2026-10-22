# Implantat-Lead-Generation Deutschland: Klickpreise und Customer Acquisition Cost (CAC)

Stand: 22.10.2026 · Daten: DataForSEO (Google Ads Keyword Planner, Deutschland, Sprache Deutsch), Abfragen vom 22.10.2026, Kosten der Abfragen 0,27 $. Alle Funnel-Werte und Fallumsätze sind **Annahmen** und in `annahmen.json` änderbar. Rechnen: `python3 daten/implantate/cac_modell.py [--budget N]`.

## Antwort zuerst

- **Klickpreis:** Implantat-Keywords kosten in Deutschland laut Keyword Planner im Schnitt **2,50 bis 3,00 € pro Klick** (volumengewichtet, 756 Keyword-Gruppen). Die Google-Prognose für eine Kampagne mit 208 Keywords (Phrase Match) landet effektiv bei **1,41 € (Gebot 2,50 €) bis 1,79 € (Gebot 4,00 €)**. Die Prognose ist meist zu optimistisch, daher rechnet das Basis-Szenario mit 2,50 €.
- **CAC je Auftrag (Basis-Szenario): ca. 420 €**, Spanne 125 € (optimistisch) bis 2.300 € (pessimistisch). Je Lead ca. 36 €, je erschienenem Beratungstermin ca. 150 €.
- **Verhältnis zum Fallumsatz:** Bei 4.000 € Ø Fallumsatz (Annahme) liegt der CAC im Basisfall bei **10 %**, beim Einzelimplantat mit Krone (ca. 2.700 €) bei 15 %. Das passt zum Benchmark aus dem Buch (600–800 € je gestartetem Fall) und zum Wert, den die einzige deutsche Quelle nennt (250–500 € je Implantat-Neupatient in Großstädten, Quelle unsicher).
- **Als Lead-Gen-Geschäft:** Pro Lead verkauft (60–100 €) bleiben im Basisfall 24–64 € Marge je Lead. Pro erschienenem Termin verkauft (150–250 €) bleibt im Basisfall fast nichts (4–104 €), weil die Erscheinensquote und die Terminquote beim Vermittler liegen, aber die Praxis sie beeinflusst. **Lead-Abrechnung ist rechnerisch das robustere Modell, Termin-Abrechnung nur mit sehr gutem Funnel.**
- **Skalierbarkeit:** Nachfrage ist groß (ca. 125.000 Suchen/Monat bundesweit nur mit „Implantat“ im Begriff, ohne Versicherungs- und Herstellerbegriffe). Die Google-Prognose sieht für das Keyword-Set rund **4.900 bis 5.800 Klicks pro Monat für 7.000 bis 10.400 €** erreichbar. Daraus folgen im Basisfall ca. 200 bis 400 Leads und 17 bis 40 Aufträge pro Monat bundesweit. Der Engpass ist nicht das Suchvolumen, sondern die regionale Verteilung: pro Stadt ist die Nachfrage dünn, und Implantat-Leads lassen sich nur an Praxen im Umkreis verkaufen.

## 1. Klickpreise aus DataForSEO

Datei: `keywords-de-2026-10-22.csv` (756 Keyword-Gruppen; Google fasst Wortreihenfolge-Varianten zusammen, die stehen in der Spalte „varianten“). Ausgeschlossen: Zahnzusatzversicherung (CPC 10,51 €, Versicherer-Wettbewerb), Herstellermarken (Straumann, Camlog), Auslandsbehandlung, Hörimplantate, Jobs.

| Absicht | Suchen/Monat | Gruppen | CPC gewichtet | Gebot oben (hoch) gewichtet |
|---|---|---|---|---|
| allgemein (zahnimplantat, implantate …) | 66.280 | 304 | 2,93 € | 2,94 € |
| kosten/preis | 34.530 | 243 | 2,52 € | 2,50 € |
| anbieter (implantologe, implantate zahnarzt …) | 10.360 | 69 | 2,99 € | 3,31 € |
| versorgung (all on 4, sofortimplantat, oberkiefer …) | 8.570 | 90 | 2,80 € | 2,55 € |
| info (schmerzen, haltbarkeit, risiken …) | 5.770 | 50 | 1,73 € | 1,45 € |
| **gesamt** | **125.510** | **756** | **ca. 2,80 €** | |

Wichtigste Begriffe (Suchen/Monat, CPC, Gebotsspanne oben niedrig–hoch):

| Keyword | Volumen | CPC | Gebot oben |
|---|---|---|---|
| zahnimplantat / zahnimplantate | 27.100 | 3,03 € | 0,81–3,08 € |
| implantate | 14.800 | 3,10 € | 0,88–3,00 € |
| kosten für zahnimplantate (+ Varianten) | 9.900 | 2,36 € | 0,73–2,28 € |
| implantat kosten | 5.400 | 2,26 € | 0,76–2,31 € |
| implantat zahn kosten | 2.900 | 2,50 € | 0,84–2,41 € |
| kosten implantat backenzahn | 1.900 | 2,88 € | 0,87–3,18 € |
| implantologie | 1.600 | 3,78 € | 1,17–5,86 € |
| implantat oberkiefer | 1.300 | 2,25 € | 0,60–1,86 € |
| implantate zahnarzt | 590 | 5,35 € | bis 7,95 € |
| all on 4 implantate | 590 | 4,77 € | bis 4,65 € |
| zahnarzt implantologie | 390 | 6,44 € | bis 6,51 € |

Lesart: Anbieter-Begriffe („implantate zahnarzt“, „implantologe“) sind mit 4,50 bis 6,50 € die teuersten, aber kaufnächsten. Kosten-Begriffe sind mit ca. 2,50 € günstiger und haben das meiste Volumen. Saisonalität bei „zahnimplantat“: 33.100 Suchen im Jan–März, 22.200 im Juli/August.

Google-Prognose (`google-prognose-2026-10-22.json`, Phrase Match, nächster Monat, 208 Keywords):

| Gebot | Klicks/Monat | Kosten/Monat | effektiver CPC |
|---|---|---|---|
| 2,50 € | 4.934 | 6.973 € | 1,41 € |
| 4,00 € | 5.802 | 10.411 € | 1,79 € |

Lücke: Die Prognose liefert keine Impressionen, also keine CTR. Sie gilt für ein Konto mit durchschnittlichem Qualitätsfaktor und ist erfahrungsgemäß eher optimistisch.

## 2. Funnel-Annahmen

| Stufe | pessimistisch | basis | optimistisch | Begründung |
|---|---|---|---|---|
| CPC | 3,50 € | 2,50 € | 1,80 € | Keyword-CPC 2,5–3,0 €, Prognose 1,4–1,8 € |
| Klick → Lead (Formular/Anruf) | 4 % | 7 % | 10 % | US-Benchmark Zahnmedizin 10,7 % (LocaliQ), Deutschland unbekannt |
| Lead → vereinbarter Termin | 25 % | 35 % | 45 % | Annahme: Erreichbarkeit, Budget, Umkreis |
| Termin erschienen | 60 % | 70 % | 80 % | Annahme, typische No-show-Quoten |
| erschienen → Auftrag | 25 % | 35 % | 40 % | Planungsannahme im Projekt 30–40 % |

## 3. Ergebnis

| Szenario | CPC | Klicks je Lead | € je Lead | € je Termin | € je erschienenem Termin | Klicks je Auftrag | CAC je Auftrag |
|---|---|---|---|---|---|---|---|
| pessimistisch | 3,50 € | 25 | 88 € | 350 € | 583 € | 667 | **2.333 €** |
| basis | 2,50 € | 14 | 36 € | 102 € | 146 € | 167 | **416 €** |
| optimistisch | 1,80 € | 10 | 18 € | 40 € | 50 € | 69 | **125 €** |

CAC in Prozent vom Fallumsatz (Fallumsätze sind Annahmen, siehe Abschnitt 5):

| Szenario | Einzelimplantat mit Krone (2.700 €) | Ø Implantatpatient (4.000 €) | große Versorgung (8.000 €) |
|---|---|---|---|
| pessimistisch | 86 % | 58 % | 29 % |
| basis | 15 % | 10 % | 5 % |
| optimistisch | 5 % | 3 % | 2 % |

Mengengerüst bei 7.000 € Klickbudget pro Monat (bundesweit):

| Szenario | Klicks | Leads | Termine | erschienen | Aufträge |
|---|---|---|---|---|---|
| pessimistisch | 2.000 | 80 | 20 | 12 | 3 |
| basis | 2.800 | 196 | 69 | 48 | 17 |
| optimistisch | 3.889 | 389 | 175 | 140 | 56 |

## 4. Lead-Gen als Geschäft

Marge je Einheit, wenn die Praxis pro qualifiziertem Lead (60–100 €) oder pro erschienenem Termin (150–250 €) zahlt (Preise: Annahme, abgeleitet aus US-Lead-Preisen für Implantate von über 100 $ und dem Buch-Benchmark 600–800 € je Fall):

| Szenario | Kosten je Lead | Marge je Lead | Kosten je erschienenem Termin | Marge je Termin |
|---|---|---|---|---|
| pessimistisch | 88 € | −28 bis 12 € | 583 € | −433 bis −333 € |
| basis | 36 € | 24 bis 64 € | 146 € | 4 bis 104 € |
| optimistisch | 18 € | 42 bis 82 € | 50 € | 100 bis 200 € |

Was das bedeutet:
- **Hebel Nr. 1 ist die Lead-Rate der Landingpage** (4 % gegen 10 % verdoppelt bis verdreifacht die Marge). Hebel Nr. 2 ist die Terminquote, die hängt an der Rückrufzeit (Kennzahl ③ im Projekt: in ≤10 Minuten erreicht).
- **Rechnung der Praxis:** Im Basisfall zahlt sie bei 80 € je Lead und 35 % Terminquote, 70 % Erscheinen, 35 % Abschluss rund **930 € je Auftrag**. Bei 4.000 € Fallumsatz ist das vertretbar, beim Einzelimplantat (2.700 €) knapp. Der Verkaufsargument-Rahmen liegt also eher bei 50–80 € je Lead oder einer Mischung aus Grundgebühr plus Lead-Preis.
- **Regionale Grenze:** Ein Lead ist nur im Umkreis einer zahlenden Praxis verwertbar. Bundesweite Klicks ohne Praxis im Umkreis sind verlorenes Budget. Das Geschäft skaliert deshalb über die Zahl der Städte mit Partnerpraxis, nicht über das Suchvolumen. Annahme nach Einwohneranteil: eine Großstadt wie Essen (0,7 % der Bevölkerung) hat ca. 900 Implantat-Suchen/Monat, davon ca. 250 Kosten-Suchen; das reicht nach Basis-Annahmen für etwa 5–8 Leads pro Monat je Stadt bei Geo-Targeting (Rechenbeispiel, keine Messung).
- **Wettbewerb in der Suche:** Die geprüften Ergebnisseiten („zahnimplantat kosten“, „zahnimplantat“, „implantate zahnarzt“) zeigten am 22.10.2026 **keine Anzeigen** im Desktop-Abruf von DataForSEO und ein Local Pack aus Praxen. Organisch dominieren Praxisseiten mit Kostenrechnern (dr-roemer.de, dorow-clinic.de, zahnarzt-dr-rick.de) sowie Barmer. Das stützt den moderaten CPC: der Markt ist von Praxen besetzt, nicht von Lead-Portalen. Lücke: Anzeigen-Abrufe schwanken, eine Wochenbeobachtung wie bei `ads-wettbewerb` wäre nötig.

## 5. Quellen und Lücken

- Fallumsatz: Einzelimplantat mit Aufbau und Krone 1.800–3.500 € (Richtwert 2026, [deutschland-rechner.de](https://www.deutschland-rechner.de/zahnimplantat-kosten-rechner)), 1.500–3.500 € ([longren.com](https://search.longren.com/de/posts/2e92fbb8)), 1.200–2.200 € nur Implantat ([Allianz](https://www.allianz.de/gesundheit/zahnzusatzversicherung/zahnbruecke/)). Knochenaufbau 300–2.000 € extra, bei 30–50 % der Patienten. Der Mittelwert 2.700 € und der Ø Fallumsatz 4.000 € (Mehrfachimplantate, Knochenaufbau) sind Annahmen.
- Benchmarks Lead-Kosten: USA Zahnmedizin CPC 8,00 $, Conversion 10,67 %, 72,97 $ je Lead ([LocaliQ via webtonic](https://www.webtonic.io/blog/google-ads-benchmarks)); Implantat-Leads über 100 $ ([Delmain](https://delmain.co/?p=258821)); Deutschland 250–500 € je Implantat-Neupatient in Großstädten, CPC-Angabe 8–35 € dort nicht nachvollziehbar und durch DataForSEO widerlegt ([rework](https://resources.rework.com/de/libraries/dental-clinic-growth/google-ads-for-dentists)).
- **Lücken:** keine deutschen Messwerte für Klick-zu-Lead und Lead-zu-Termin; keine CTR aus der Prognose; Österreich und Schweiz nicht abgefragt (je Land eine Abfrage, ca. 0,20 $); Meta-Ads-Kosten nicht enthalten; HWG-Rahmen für Lead-Landingpages Dritter nicht geprüft (Vermittlung von Patienten gegen Entgelt berührt § 299a StGB und die Berufsordnung, Rechtsfrage vor Start klären).

## 6. Nächster Schritt (Vorschlag, nicht gestartet)

Ein Test mit 1.000 bis 1.500 € Klickbudget in einer Stadt mit einer Partnerpraxis (oder Kieferblick selbst, falls Implantate ins Angebot passen) würde die beiden unbekannten Quoten (Klick → Lead, Lead → Termin) messen. Danach lässt sich das Modell mit echten Zahlen rechnen.
