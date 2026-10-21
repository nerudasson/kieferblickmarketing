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


## Phase 1 (Entscheidung Alexander 21.10.2026): die bestehenden Erstterminseiten nutzen
Seiten: `/erstermin-aligner/`, `/erstermin-bleaching/` (für B und E), `/erstermin-schnarchschiene/`, `/erstermin-veneers/` (alle `noindex`, Stand Abruf 21.10.2026). Die eigene schlanke Anzeigen-Seite (`claude-design-prompt.md`) ist **Phase 2**, sobald die ersten Daten da sind. Die Seiten haben Hero, kurzen Ablauf, Wer begleitet, FAQ und ein Tally-Formular mit `produkt`-Parameter, das ist eine brauchbare Basis.

### Für alle vier Seiten (vor Livegang)
1. **Bewertungszeile „★ 4,9 bei Google · 87 Bewertungen“**: nur stehen lassen, wenn echt und belegbar; sonst entfernen.
2. **Satz im Ablauf-Block „Was Sie vorab bei uns machen lassen, rechnen wir voll auf Ihre Behandlung an. Ohne Frist.“** ersetzen durch: „Eine Zahnreinigung, ein Bleaching oder eine Schnarchschiene rechnen wir voll auf eine spätere Aligner-Behandlung an. Ohne Frist.“ (Anrechnung gilt nur für die Intro-Offers und nur auf den Aligner-Plan.)
3. **Tracking und Formular:** Google-Tag mit Einwilligung, Conversion „Formular gesendet“ (Danke-Seite oder Ereignis), Klick auf Telefon. Im Tally-Formular zusätzlich versteckte Felder: Seiten-Adresse, `gclid`, `utm_source/utm_campaign`, Gruppe. Einwilligungstext für Gesundheitsangaben.
4. **Mobil:** feste untere Leiste „Termin buchen | Anrufen“ (Elementor „Sticky“), Hero-Button ohne Scrollen sichtbar.
5. **Hinweis zum Test A/B in Kampagne A:** Die Chips „Kostenlos · 60 Minuten“ stehen auf Aligner- und Veneers-Seite schon im Hero. Für einen sauberen Test „kostenlos“ nur in Anzeige B müsste der Chip je Variante wechseln; sonst misst der Test nur die Wirkung in der Anzeige.

### `/erstermin-aligner/` (Kampagne A)
- Bleibt: H1 „Schön lächeln. Gut zubeißen.“, Fakten (Dauer, Tragezeit), Simulation, Wer begleitet, FAQ (Schienenwechsel, erste Veränderungen, Plan prüfen lassen).
- **Entfernen:** Block „Ergebnisse: So sieht es bei anderen aus“ (Vorher/Nachher), solange keine echten Fälle mit Einwilligung vorliegen.
- **Ergänzen (kurze Blöcke):**
  - Zeile „Die Halteschiene gehört zum Plan: zwei lose Retainer je Kiefer.“
  - Zeile „Der Preis im Plan bleibt bis zum Abschluss gleich. Mehrkosten nur mit Ihrer Zustimmung.“
  - Tabelle „Fragen, die Sie jedem Anbieter stellen sollten“ (nur Spalte Kieferblick) aus `/aligner/` übernehmen, ohne Wettbewerber-Spalte.
  - Hinweis „Aligner trägt man etwa 22 Stunden am Tag. Nicht jede Fehlstellung lässt sich damit behandeln.“
  - Für die Marke-Gruppe: Name des Aligner-Systems.
- Biss-Check: „10 Minuten“ im Ablauf (Schritt 3 „Alexander Andreev prüft 10 Minuten Ihren Biss“) mit der Faktenlage abgleichen (Faktendatei: 10 Minuten sind die persönliche Empfehlung).
- Test B (Wert-Stapel): Block „Ersttermin im Wert von 300 €, für Sie kostenlos“ mit den vier Einzelwerten aus `/erstermin/` einblenden.

### `/erstermin-bleaching/` (Kampagnen B und E)
- Bleibt: H1 „Bleaching und Zahnreinigung“, „Erst Reinigung, dann Bleaching“, FAQ.
- **Ablauf-Block ersetzen** (heute Aligner: Scan, Lächeln am Bildschirm, Biss): 01 Befund und Beratung · 02 Professionelle Zahnreinigung · 03 Bleaching (1 bis 2 Termine, Praxis oder zu Hause mit Schiene) · 04 Kontrolle.
- **Preisblock direkt unter dem Hero ergänzen:** Professionelle Zahnreinigung 149 € · Bleaching in der Praxis 399 € · Bleaching für zu Hause 299 € · „Entscheiden Sie sich später für Aligner, rechnen wir den Betrag voll an. Ohne Frist.“
- Hero-Chip „Schonend“ ersetzen durch „Mit Vorprüfung“. Button „Ersttermin buchen“ in „Bleaching-Termin buchen“.
- FAQ „Wie oft sollte ich zur Zahnreinigung kommen?“: „Prophylaxe-Mitgliedschaft“ ersetzen durch „PZR-Abo“.
- Für E (PZR): eigene kurze Zeile „Professionelle Zahnreinigung 149 €. Festpreis, auf Aligner voll angerechnet.“ im Preisblock, und die Zahnreinigung vorn nennen.

### `/erstermin-schnarchschiene/` (Kampagne C)
- Bleibt: H1 „Schnarchschiene“, „Schnarchen ernst nehmen. Erst klären, dann behandeln.“, FAQ zur Abklärung.
- **Ablauf-Block ersetzen** (heute Aligner): 01 Gespräch und Screening (Schlaf, Tagesmüdigkeit, beobachtete Atempausen) · 02 Bei Auffälligkeiten raten wir zuerst zur Abklärung in der Schlafmedizin · 03 Wenn eine Schiene passt: individuell angefertigt, vorher prüfen wir Zähne und Biss · 04 Eingewöhnung mit Kontrollen.
- **Preisblock ergänzen:** Schnarchschiene als Paket mit Kontrollen 799 €, bei späterer Aligner-Behandlung voll angerechnet, ohne Frist. [Screening im Paket? Alexander bestätigt]
- Schlusstext „Im Ersttermin sehen Sie Ihr Lächeln am Bildschirm“ ersetzen durch „Im Ersttermin klären wir zuerst die Ursache. Danach entscheiden Sie in Ruhe.“ Button „Termin online anfragen“.
- FAQ „Wie lange dauert die Eingewöhnung?“ („meist zwei bis vier Wochen“): nur stehen lassen, wenn Alexander es bestätigt.
- **Kampagne C erst aktivieren, wenn diese Änderungen live sind.**

### `/erstermin-veneers/` (Kampagne D)
- Bleibt: H1 „Zähne, die zu Ihnen passen.“, „Ihr Lächeln, bevor etwas entschieden wird.“, Ablauf, FAQ.
- **Entfernen:** alle Nennungen von „Veneers ohne Abtrag“ (FAQ „Tut das weh?“ und „Kann ich das rückgängig machen?“); das Angebot hat Non-Prep gestrichen.
- **Ändern:** „Darum beginnen wir mit dem Schonendsten.“ in „Darum prüfen wir zuerst, ob Schonenderes reicht.“
- **Ergänzen:** Zeile „Sie können die neue Form als Mock-up aus Kunststoff probetragen.“ und kurzer Materialblock: Komposit (Abtrag nach Befund) oder Keramik (Zahnschmelz wird meist abgetragen).
- Keine Preise, keine Vorher-nachher. Kampagne D erst starten, wenn das erledigt ist (laut Plan nach den Kampagnen A bis C).

### Reihenfolge
1. Aligner-Seite (A), 2. Bleaching-Seite (B, E), 3. Schnarch-Seite (C), 4. Veneers-Seite (D). Danach Phase 2: eigene Anzeigen-Seiten nach dem Claude-Design-Prompt.

## 2. Checkliste je Kampagne
### A Aligner (6 Gruppen) → `/erstermin-aligner/` (live, noindex) — Detailliste für Phase 2; Phase 1 siehe oben
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

## Stand der Umsetzung in WordPress (Agent legt nur Entwurfskopien an, Alexander gibt frei)
- **21.10.2026 `/erstermin-aligner/` (A):** Entwurfskopie **Seite 929** „Erstermin Aligner (Ads-Entwurf)“, Status Entwurf, Slug `erstermin-aligner-ads`. Die Live-Seite (ID 155) ist unverändert; Sicherung des Originals: `backup/erstermin-aligner-155-2026-10-21.json`.
  Geändert in der Kopie: Anrechnungssatz ersetzt durch die Festpreis-Zusage · Abschnitt „Ergebnisse / Vorher-nachher“ ersetzt durch „Darum planen wir anders“ (Biss-Check, Scan, Halteschiene im Plan) mit Tabelle „Fragen, die Sie jedem Anbieter stellen sollten“ und Hinweis „Ehrlich vorab“ · FAQ um fünf Fragen erweitert (Dauer, Tragezeit, Kosten, Retainer, passen Aligner).
  Nicht angefasst (Entscheidung Alexander): Bewertungszeile „★ 4,9 · 87 Bewertungen“, „10 Minuten Biss-Check“ im Ablauf, Chip „Kostenlos“, Video, Tally-Felder, Tracking, Name des Aligner-Systems.
