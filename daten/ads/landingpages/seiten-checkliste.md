# Landingpages für Google Ads: Standards und Checkliste je Kampagne (Stand 21.10.2026)
Grundlage: Recherche (unten), Projektdokumente (`kontext/anzeigenwinkel.md`, `kontext/funnel-und-kanaele.md`), Abruf der Live-Seiten am 21.10.2026 (Inhalt der Seiten kann sich geändert haben). Kampagnen: `daten/ads/kampagnen/`, Reviews: `daten/reviews/ads-*.md`. Alles Arbeitshypothesen, keine Rechtsberatung.

## 1. Standards für alle Anzeigen-Seiten
**Aufbau (von oben nach unten, mobil gleich)**
1. Kopf: Logo, Telefon, ein Button. Keine Hauptnavigation (die Seiten sind `noindex`, das ist für Anzeigen-Seiten in Ordnung).
2. Hero: H1 = Kern der Anzeige (Message Match), ein Satz Nutzen, Fakten-Leiste (Dauer, Termine, Ort), **ein** Haupt-Button, Video (VSL) von Alexander. Auf dem Handy ist der Button ohne Scrollen sichtbar.
3. Vertrauen: Alexander (Foto, Qualifikation, ein Satz), echte Google-Bewertung (nur mit echten Zahlen), Zusagen.
4. Der Weg in 3 Schritten, ehrlich zu Nachteilen (Tragezeit, Empfindlichkeit, Abtrag).
5. Einwände als FAQ entlang der Blocker B1 bis B6.
6. Angebot und Preise (nur Freigegebenes), dann Formular/Button wiederholt (nach jedem Beweisblock ein CTA).
7. Fuß: Impressum, Datenschutz, Einwilligung ändern. Mobil: feste untere Leiste „Ersttermin buchen | Anrufen“.

**Copy:** Nutzen vor Merkmal ([Merkmal], damit [Nutzen]); Sie-Form; Praxis „Wir“; Alexander dritte Person; „Zusage“, nie „Garantie“; kein „unsichtbar“, keine Ausrufezeichen, keine Superlative, keine Ergebnisversprechen („Ohne Kieferknacken“ nicht). Keine Aussagen, die die Anzeigen nicht gemacht haben, und umgekehrt: **jede Aussage der Anzeige steht auf der Seite.**

**Technik:** Ladezeit unter 3 Sekunden (Ziel 1 bis 2) auf dem Handy, Bilder in WebP, Schriften lokal gehostet (DSGVO), kein Pop-up über dem Hero. Einwilligungsbanner mit Consent Mode, Google-Tag, Conversions: Formular gesendet (je Produkt), Klick auf Telefon, optional Video gestartet. **Formular:** kurz (Vorname, Telefon oder E-Mail, Wunschzeit optional), Einwilligung für Gesundheitsangaben, versteckte Felder: Quelle `google-ads`, Gruppe/Kampagne, `gclid`, Seiten-Adresse, `produkt`. Danke-Seite mit nächstem Schritt (damit Conversion messbar). Offene Frage: Anruf als zweiter CTA (Vorschlag ja, mit Anruf-Tracking).

**Recht (Inhalt prüft Alexander):** Impressum und Datenschutz vollständig, Hinweis zur Verarbeitung von Gesundheitsangaben beim Formular, keine Vorher-nachher-Platzhalter, keine Bewertungszahlen ohne Beleg, Vergleiche nur bejahend und ohne pauschale Aussagen über Wettbewerber, Berufsbezeichnung „Zahnarzt“.

**Benchmark für die Erwartung:** Unbounce (Auswertung bis Juli 2024): Zahnmedizin median 4,3 % Seiten-Conversion, Gesundheit gesamt 5,1 %, bezahlte Google-Suche in der Gesundheit 4,7 %. Das deckt sich mit der Planungsannahme von 3 bis 8 % (Mitte 4 %). Herstellerangaben, nur als Richtwert.

**Länge:** Bei erklärungsbedürftigen Leistungen mit hohem Preis funktionieren längere Seiten oft besser (CXL), wenn der Button nach jedem Beweisblock wiederkehrt. Wir testen kurz gegen lang, wir raten nicht. Formularlänge und feste Mobil-Leiste sind aus der Recherche nicht belegt: eigener Test.

**Messung:** Je Seite Aufrufe, Formulare, Anrufe, Termine (Baserow), Abschlüsse; nicht nur Formulare zählen, sondern gebuchte Ersttermine und Abschlüsse zurückspielen.

## 2. Checkliste je Kampagne
### A Aligner (6 Gruppen) → `/erstermin-aligner/` (live, noindex)
Kernbotschaft der Seite: **„Schön lächeln. Gut zubeißen.“ plus „Kiefer und Biss mitgeplant“.**
- [ ] Platzhalter raus oder echt: „4,9 bei Google · 87 Bewertungen“, Vorher-nachher-Bilder („Fall 1“).
- [ ] Video (VSL, Alexander, ca. 90 Sekunden) einbauen.
- [ ] Ablauf klären und konsistent führen: **Biss-Check (10 Minuten?)**. In der Faktendatei sind die 10 Minuten die persönliche Empfehlung mit Alexander; die Seite nennt sie als Biss-Check. Eine Aussage festlegen, Anzeigen nennen keine Minuten.
- [ ] Scan in der Praxis, ohne Abdruckmasse; Halteschiene gehört zum Plan (2 lose pro Kiefer); Tragezeit etwa 22 Stunden; Dauer meist 6 bis 12 Monate.
- [ ] Festpreis-Zusage: „Preis im Plan bleibt bis zum Abschluss gleich, Mehrkosten nur mit Ihrer Zustimmung“ (Ausnahmen klären).
- [ ] Tabelle „Fragen, die Sie jedem Anbieter stellen sollten“ aus `/aligner/` als Block (Gruppen Kosten B und Erfahrungen), ohne pauschale Aussagen über „Aligner per Post“.
- [ ] Marke-Gruppe: nennen, welches Aligner-System die Praxis nutzt (steht in keiner Faktendatei).
- [ ] Test B (Behandler): Wert-Stapel „Ersttermin kostenlos, Wert 300 €“ (64 + 70 + 75 + 91 €) auf der Seite sichtbar, Festpreis schriftlich.
- [ ] Kopfzeile „Zahnarzt“, nicht „Kieferorthopäde“. Standort-Hinweis zwischen Essen und Duisburg.
- [ ] Formular: Tally mit versteckten Feldern, Danke-Seite, Anruf-Button mit Tracking.
- [ ] Variante je Gruppe (Test): Überschrift und erste Zeile folgen der Gruppe (Behandler, Erwachsene, Kosten, Marke, Erfahrungen), Rest gleich.

### B Bleaching (4 Gruppen) → `/bleaching-zahnreinigung/` (live)
Kernbotschaft: **Erst Reinigung, dann Bleaching. Preise offen. Voll auf Aligner angerechnet.**
- [ ] Preisblock „Ihr Einstieg“ (PZR 149 €, Bleaching Praxis 399 €, zu Hause 299 €, voll angerechnet auf Aligner, ohne Frist) **nach oben** (bei den Kosten-Suchen heute weit unten).
- [ ] Hero mit Ersttermin-Hinweis ersetzen durch „Bleaching-Termin buchen“ (Intro-Offer, kein Aligner-Ablauf).
- [ ] Bleaching macht ein Zahnarzt: Alexander nennen, Aussage „selbst oder angeleitet“ klären.
- [ ] Ehrlich: Empfindlichkeit, Haltbarkeit, Füllungen/Kronen hellen nicht auf; „Manchmal hilft schon die Zahnreinigung“.
- [ ] Platzhalter (Bewertungen, Fälle) raus. Schlanke Variante ohne Navigation prüfen.
- [ ] Stadt-Gruppe: Lage „zwischen Essen und Duisburg“, Anfahrt.

### C Schnarchschiene (2 Gruppen) → `/erstermin-schnarchschiene/` (live) — **Kampagne erst aktivieren, wenn dies erledigt ist**
Kernbotschaft: **Erst klären, dann behandeln.**
- [ ] Preis 799 €, „Paket mit Kontrollen“, „auf den Aligner-Plan anrechenbar, ohne Frist“ ergänzen.
- [ ] Ablauf-Block ersetzen (heute vom Aligner: „Ihr Lächeln am Bildschirm“).
- [ ] Screening auf Schlafapnoe vorab und Verweis bei Auffälligkeiten (Wortlaut mit Praxisablauf abgleichen), Eingewöhnung begleitet (keine Dauerzahl, solange nicht bestätigt).
- [ ] Begriffe „Protrusionsschiene“/„Unterkieferprotrusionsschiene“ erklären (Gruppe 2).
- [ ] Gesundheitswerbung: keine Wirksamkeits- oder Erfolgsaussage. Einwilligung für Gesundheitsangaben im Formular.

### D Veneers (Test, 2 Gruppen) → `/veneers/` (live) — **Anzeigen erst nach Seitenanpassung aktivieren**
Kernbotschaft: **Erst das Schonendere prüfen. Mock-up zum Probetragen.**
- [ ] „Wir beginnen immer mit dem Schonendsten“ auf „Wir prüfen zuerst, ob Schonenderes reicht“.
- [ ] Non-Prep-Abschnitt entfernen (Angebot: gestrichen), Abtrag-Aussage tragen (Komposit nach Befund, Keramik meist Zahnschmelzabtrag).
- [ ] Vorher-nachher-Platzhalter raus (nur echte Fälle mit Einwilligung).
- [ ] Preisfrage ehrlich einordnen (Rahmen nach Untersuchung), Preisrahmen nur mit Freigabe.
- [ ] Veneers-Seite ist laut Plan erst mit Labor und echten Fällen live: Startzeitpunkt klären.

### E PZR (Test, 2 Gruppen) → eigene schlanke Seite (empfohlen), bis dahin `/bleaching-zahnreinigung/`
Kernbotschaft: **Professionelle Zahnreinigung 149 €, auf Aligner voll angerechnet.**
- [ ] Eigene Seite „Professionelle Zahnreinigung in Mülheim“: Was wir tun (Beläge, Zahnstein, oberflächliche Verfärbungen, polieren), 149 €, Anrechnung, Zahnarztpraxis in Mülheim, Termin-Button.
- [ ] PZR-Abo nur als Folgeangebot für Aligner-Patienten erwähnen; Preis steht auf `/mitgliedschaft/`.
- [ ] Erwartung: Viele Suchende wollen die Kassenleistung oder Preise um 100 €. Die Seite sagt früh „reine Privatpraxis“.

## 3. Design-Fahrplan (Claude Design)
Das Design-System in deinem Konto ist angelegt, aber noch leer (kein Kieferblick-Inhalt). Vorschlag: (1) Kieferblick-Design-System anlegen aus `kontext/marke-und-ton.md` (Tannengrün #1F4A3F, Safran #E3A93F nur Akzent, Salbei #B9CFC2, Sand #DCC8B4, Creme #F4EFE4; Fraunces/DM Sans; kein Klinikblau, kein Neon; echte Menschen, Tageslicht), (2) Vorlage „Anzeigen-Seite“ als Entwurf mit den Blöcken aus Abschnitt 1, Handy und Desktop, (3) je Kampagne eine Variante, (4) Alexander baut sie in Elementor nach.

## Quellen
- Unbounce, Health & Wellness / Dental Benchmarks (über webtonic.io zusammengefasst): https://www.webtonic.io/blog/health-wellness-landing-page-statistics
- CXL, Long Form oder Short Form: https://cxl.com/blog/long-form-or-short-form/
- Redefine Web, Dental-PPC-Seiten: https://redefineweb.com/blog/best-dental-ppc-landing-pages-dentists-book-patients/
- Medizinio, Arztpraxis-Werbung (HWG, Einwilligung): https://medizinio.de/blog/praxismarketing-was-ist-erlaubt
- Google Ads Hilfe, Zielseitenerfahrung: https://support.google.com/google-ads/answer/7050591
- Landerlab, Google-Ads-Landingpage (Message Match, Ladezeit, Hersteller-Blog): https://landerlab.io/blog/google-ads-landing-page
Hinweis: Mehrere Quellen sind Hersteller- oder Agenturblogs; Zahlen sind Richtwerte und nicht unabhängig geprüft.
