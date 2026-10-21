# Google Ads: Strategie (Arbeitsstand 21.10.2026, von groß nach klein; Annahmen markiert)
Datenbasis: `daten/ads/` (Regionalzahlen, CAC-Modell, Zonen-Klickschätzung, Wettbewerber-Anzeigen). Alle Konversionsraten sind Annahmen bis zum ersten Test.

## Ebene 1: Rolle von Ads
- Ads greift vorhandene Nachfrage ab. Reichweite und Vertrauen kommen aus SEO, Google-Profil, Empfehlungen.
- Erste vier Wochen = Lernen (Klickpreise, Konversionsraten, Kosten je Fall), nicht Skalieren.
- Erfolgsmaß: Kosten je gestartetem Fall gegen Benchmark 600–800 € (Annahme Mitte Aligner ca. 380 €).

## Ebene 2: Portfolio (Entscheidung Alexander 21.10.2026: "passt so"; 900 € Google/Monat, Annahme)
| Kampagne | Budget | Ziel | Zone |
|---|---|---|---|
| A Aligner | ca. 600 € | Erstberatung vor Ort | Zone 1 (bis ca. 20 km) |
| B Bleaching | ca. 200 € | Intro-Offer buchen (399/299 €) | Zone 1 |
| C Schnarchschiene | ca. 100 € | Screening, dann Termin (799 €) | Zone 1 (Annahme) |
Später: Aligner Zone 2 (20–45 km) mit Smile-Check, Marken-Kampagne, Meta. Geparkt: Retainer.
**Mitgeplant (Alexander 21.10.2026):** D Veneers und E PZR als kleine Testkampagnen, Start nach A bis C (Woche 3 bis 4), jeweils 100 € aus der Reserve (Entscheidung Alexander 21.10.2026, `config/budget.json` angepasst, Reserve jetzt 0). Klickschätzung Zone 1 (Gebot Veneers 5 €, PZR 4 €): Veneers 244 Klicks / 580 € / CPC 2,38 €, PZR 227 Klicks / 488 € / CPC 2,15 € (`daten/ads/zone1-veneers-pzr-2026-10-21.json`). CAC (Annahmen): Veneers opt./Mitte/pess. ca. 174 / 452 / 1.630 € (Fallwert 2.400–12.800 €), PZR ca. 37 / 64 / 240 € (Umsatz 149 €, Wert liegt im PZR-Abo und in der Anrechnung). Korrektur: die früheren Werte (Veneers ca. 740 €, PZR ca. 150 €) beruhten auf höheren Keyword-Planner-CPC.
Voraussetzungen: D erst mit Veneers-Seite, Labor und echten Fällen. E braucht eine eigene PZR-Seite (Intro-Offer 149 €).
Zone 2 erst nach Start von Zone 1 und Fertigstellung des Smile-Checks; PLZ-Feld im Smile-Check-Formular zeigt die echte Anreisebereitschaft.

## Ebene 3: Keywords (Entscheidungen Alexander 21.10.2026)
Befund Städtenamen: Stadt-Keywords lohnen kaum. "Kieferorthopäde + Stadt" ist groß (NRW: Dortmund 2.900, Düsseldorf 2.400, Bochum 1.600, Gelsenkirchen 1.000, Mülheim 720, Ratingen 590, Bottrop 480), Bleaching + Stadt mittel (Düsseldorf 260/390, Essen 110/140, Dortmund 140/210), Aligner + Stadt winzig (meist 10–30), Schnarchschiene + Stadt null. Lücke: Essen, Duisburg, Oberhausen fehlen bei "Kieferorthopäde" (vermutlich Schnittstellenlücke, prüfen).
- **Eine Kampagne je Thema** (Entscheidung c), Standort "Präsenz", Stadt über Standorterweiterung und Anfahrtswinkel im Text.
- **Schicht 1:** Themenbegriffe ohne Stadt. **Schicht 2:** Stadt-Keywords nur wo Volumen existiert.
- **A Aligner, Gruppen nach Suchabsicht:** Behandler (aligner zahnarzt, aligner behandlung) · Erwachsene/unsichtbar (unsichtbare zahnspange, zähne begradigen, zahnspange erwachsene) · Kosten (aligner kosten, zahnspange erwachsene kosten) · **Marke Invisalign als eigene Gruppe** (Entscheidung a) mit eigenem Budgetdeckel · **Kieferorthopäde + Stadt nur testweise mit Vorsicht** (Entscheidung b): Anzeigentext "Zahnarzt, Aligner für Erwachsene" (Alexander ist Zahnarzt, nicht Fachzahnarzt für KFO), strenge Negativbegriffe (Kinder, Jugendliche, Kasse), Berufsbezeichnung vor Livegang kurz rechtlich prüfen lassen.
- **B Bleaching:** bleaching, zahnbleaching, zahnaufhellung (je auch "zahnarzt", "kosten") plus Essen, Duisburg. Negativ: Streifen, Set, Drogerie, dm, kaufen, Hausmittel.
- **C Schnarchen:** schnarchschiene, protrusionsschiene, unterkieferprotrusionsschiene, schlafapnoe schiene. Negativ: Test, kaufen, Amazon, online.
- Offen: Anzeigenwinkel und Landingpage je Gruppe (nächster Schritt), Ebenen 4 und 5.

- **D Veneers (Test):** veneers kosten, veneers zahnarzt, keramikveneers, komposit veneers. Winkel: Mock-up vorab, ehrlich wann Aligner schonender sind, Kostenrahmen. Negativ: Veneers To-Go, Clip-on, aufkleben, Ausland, Türkei, selber. Seite: Veneers-Seite.
- **E PZR (Test):** professionelle zahnreinigung, zahnreinigung kosten, zahnreinigung zahnarzt. Winkel: Festpreis 149 €, anrechenbar, Termin. Negativ: Hund, Katze, Tier, Pferd, Gerät, Set, Ausbildung, Kurs, zuhause. Seite: eigene PZR-Seite.

## Ebene 5: Aufbau, Texte, Gebote, Betrieb (Stand 21.10.2026; Fundament wird als gegeben angenommen)
Quellen: Praxisregeln für Google Ads (Annahme) und die Daten in `daten/ads/`. Zahlen zu Konversionen sind Annahmen.

### Struktur
- 14 Anzeigengruppen, je Gruppe ein Thema und 4–10 Keywords (ca. 60–80 im Start): A 5 (Behandler, Erwachsene/unsichtbar, Kosten, Marke Invisalign, KFO-Test) · B 3 · C 2 · D 2 · E 2.
- Anzeigen: Responsive Suchanzeigen (15 Überschriften à 30 Zeichen, 4 Beschreibungen à 90). A je Gruppe 2 Anzeigen, B 1–2, C bis E 1. Thema fest in Position 1, sonst nur rechtlich kritische Zeilen fest.
- Erweiterungen: Sitelinks (Ablauf, Preise, über Alexander), Anruf, Standort, Zusagen als Zusatzinfo.

### Keyword-Optionen
- Start nur **Exact und Phrase**. Kein Broad, solange keine Konversionsdaten da sind (Abdriften zu Kasse, Kindern, Heimprodukten).
- Abschalten: Suchpartner, Display, automatisch erzeugte Anzeigentexte, Seitenerweiterung (AI Max), automatisch angewendete Empfehlungen. Grund: keine ungeprüften Gesundheitstexte.
- Broad erst als Kampagnen-Experiment ab ca. 30 Konversionen je Monat und Kampagne.

### Gebote und Position
- Start: Klicks maximieren mit Obergrenze je Klick (A ca. 6 €, B 4 €, C 4 €, D 5 €, E 4 €). Umstellung auf Konversionen maximieren, später Ziel-CPA, ab ca. 15–30 Anfragen in 30 Tagen je Kampagne.
- Position ist kein Ziel, Kosten je Fall sind das Ziel. Oben anzeigen (Anteil ca. 60–70 %) bei A Behandler, A Erwachsene, Marke. Position 2–3 reicht (Anteil ca. 40–50 %) bei Kosten-Suchen, Bleaching, PZR, den Tests. Annahme, wird anhand Impressionsanteil und CAC überprüft.
- Marke Invisalign mit eigenem Budgetdeckel.

### Texte und Tests
- Winkel je Gruppe laut Ebene 3. Anzeigentexte schreibt der Agent, der compliance-reviewer prüft, Alexander gibt frei.
- Testbarkeit: In A nur ca. 5.000 Impressionen im Monat, je Anzeige ca. 500. Ein CTR-Vergleich von 5 % gegen 7 % braucht ca. 2.000 Impressionen je Variante. Daher wenige große Kontraste (Preis in Überschrift ja/nein, Erstberatung gegen Kostenplan als Winkel), eine Änderung je Gruppe, Tendenz nach 4–6 Wochen, alles im `experiment-log.md`.
- Wettbewerber: `ads-wettbewerb` (wöchentlich) liefert Langläufer und neue Winkel als Hypothesen. Keine 1:1-Übernahme.

### Rolle des Agent (Entscheidung Alexander 21.10.2026: Agent schreibt und optimiert die Anzeigen)
- **Schreiben:** Anzeigengruppen, Keywords, Negativ-Listen, Überschriften und Beschreibungen als Datei (Import in den Google Ads Editor) unter `daten/ads/kampagnen/`. Vorher compliance-reviewer. Geplanter Skill `ad-writing` (Referenzen google.md, hwg.md, Winkel je Gruppe).
- **Optimieren:** Geplanter Skill `ads-optimizing` liest wöchentlich die Konto-Daten und schreibt Vorschläge nach `daten/ads/vorschlaege/<Datum>.md`: Negativbegriffe, neue Keywords, Gebote (Schritte höchstens ±20 %, höchstens alle 14 Tage), Textwechsel, Budgetumschichtung. Jeder Vorschlag mit Daten, Begründung, Risiko. Alexander gibt frei, der Import erfolgt von ihm.
- **Grenzen (Entscheidung Alexander 21.10.2026):** Alexander stellt später die Google Ads API bereit. Dann legt der Agent Kampagnen direkt im Konto an, **pausiert** (= Entwurf), und Alexander gibt sie dort frei, indem er sie aktiviert. Der Agent setzt nie „aktiv“. Laufende Kampagnen ändert er nicht selbst: Gebote, Budgets und Pausierungen kommen als Vorschlag, neue Texte und Keywords stellt er pausiert neben die laufenden. **Ausnahme (Alexander 21.10.2026): Negativbegriffe darf er später direkt eintragen**, nur hinzufügen, mit Konfliktprüfung, Wochenlimit und Protokoll (Regeln in `api-push.md`). Bis die API da ist, gilt der Weg über CSV und Google Ads Editor (`ad-writing/scripts/anzeigen_export.py`, Kampagne pausiert). Budgetdeckel aus `config/budget.json`, Gebotsgrenzen aus `ad-writing/references/obergrenzen.json`. Details: `.claude/skills/ad-writing/references/api-push.md`.

### Takt
| Takt | Aufgabe |
|---|---|
| täglich (automatisch) | Ausgaben gegen Deckel, Alarm bei Abweichung |
| wöchentlich | Suchbegriffe (Negatives, neue Keywords), Bericht, Wettbewerber-Beobachtung (Montag, automatisch) |
| 14-tägig | Gebote |
| monatlich | CAC je Kampagne, Budget, neue Testidee |
| quartalsweise | Struktur, Seiten, Zone 2 |
Hebel nach Wirkung: 1. Suchbegriffe und Negatives, 2. Seite und Anfragequote, 3. Gebote, 4. Texte. Faustschwellen (Annahme): Negativ sofort bei offensichtlich Unpassendem (Kasse, Kinder, DIY, Tier); sonst Prüfung ab ca. 15 Klicks ohne Anfrage.

### Ergänzung Ebene 3 (Alexander 21.10.2026): Winkel und neue Testgruppe
- Rangfolge der Winkel: Kern „Schön lächeln. Gut zubeißen.“, dann Abgrenzung (bejahend, ohne Namen), dann Absicherung; Details in `kontext/anzeigenwinkel.md`.
- Smile-Check nicht in den lokalen Gruppen (Zone 1). „Rückruf in 10 Minuten“ gestrichen. Test „Ersttermin kostenlos, Wert 300 €“ in Behandler B.
- **Neue Gruppe 6 „Erfahrungen und Zweifel“ (Test)** in Kampagne A: aligner erfahrungen, aligner schlechte erfahrungen, smileunion erfahrungen, ilovemysmile erfahrungen, drsmile erfahrungen, drsmile alternative. Volumen sehr klein (Planner, NRW: smileunion erfahrungen 110, aligner erfahrungen 70, übrige ca. 10; Zone 1 vermutlich 20–30 Suchen im Monat). Konkurrenz-Markenwörter nur als Keyword, nie im Anzeigentext. Die Wettbewerber-Namen stehen deshalb nicht mehr in der Negativliste.

## Stand Kampagnen und Seiten (21.10.2026, Abend)
**Kampagnen als Entwurf geschrieben, geprüft (Skript 0 hart, Compliance-Review eingearbeitet), nichts live:** A Aligner (6 Gruppen, 12 Anzeigen) · B Bleaching (4 Gruppen) · C Schnarchschiene (2) · D Veneers-Test (2) · E PZR-Test (2). Budget je Kampagne und Tagesbudget: `config/budget.json` (A 600, B 200, C 100, D 100, E 100 €/Monat).
**Winkel-Rangfolge:** Kern „Schön lächeln. Gut zubeißen.“ vor Abgrenzung (bejahend, ohne Namen) vor Absicherung; Smile-Check nicht in Zone 1; kein „Rückruf in 10 Minuten“; „Ersttermin kostenlos, Wert 300 €“ nur als Test in Behandler B; kein Aligner-Preis. Details `kontext/anzeigenwinkel.md`.
**Seiten, Phase 1 (Entscheidung Alexander 21.10.2026):** bestehende Erstterminseiten `/erstermin-aligner/`, `/erstermin-bleaching/` (B und E), `/erstermin-schnarchschiene/`, `/erstermin-veneers/`. Änderungsliste und Stand in `daten/ads/landingpages/seiten-checkliste.md`. Aligner: Entwurfskopie als WordPress-Seite 929 angelegt, wartet auf Freigabe; Bleaching, Schnarchschiene und Veneers folgen nach derselben Methode (zuerst Entwurfskopie). Phase 2: eigene schlanke Seiten nach `claude-design-prompt.md`; Designgrundlage `design/wissen/` liegt auf dem Branch `claude/eloquent-heisenberg-6b419h`.
**Voraussetzungen vor Livegang:** Seiten-Änderungen live, Tracking und Einwilligung, Google-Ads-Konto und API (Alexander, später), Entscheidungen zu Preis und „kostenlos“ in Anzeigen, Bewertungszeile echt oder entfernt.
**Betrieb:** wöchentlich Montag 08:45 Uhr Wettbewerber-Beobachtung (Routine `trig_017NmDE91zArdC8Enpx1ofT6`, schreibt in `daten/ads/beobachtung/` auf den Branch `claude/vigilant-knuth-s1ckgc`).
