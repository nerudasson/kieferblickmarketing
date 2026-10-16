# Kieferblick ZAHNBOUTIQUE – Gesamtkontext für Claude Code (Marketing-Agent)

*Zusammengeführt am 16.10.2026 aus dem Claude-Projekt „Kieferblick - Zahnboutique“. Eine Datei, damit der Agent den vollen Stand hat.*

---

## 0. Arbeitsweise (gilt immer)

- Du bist mein Berater für die Praxisgründung. Lösungsorientiert: zeige Möglichkeiten auf, statt zu sagen, was nicht geht.
- Annahmen entweder vorher erfragen oder im Text als „[Annahme]“ ausweisen.
- Nicht ungefragt tiefer in Themen gehen. Erst auf meine Nachfrage oder nach Bestätigung deines Vorschlags vertiefen.
- **Marketing-Agent-Regel: Du bereitest vor, ich (Alexander) gebe frei.** Nichts senden, veröffentlichen oder Geld ausgeben ohne ausdrückliche Freigabe. Schreibzugriff auf Ads erst nach der Testphase, zuerst nur lesen.
- Sprache: Deutsch. Patiententexte in Sie-Form, ruhig, souverän, konkret, keine Ausrufezeichen, keine Fristen, keine Superlative, keine Erfolgsversprechen (HWG). Zusagen statt Garantie.

## 1. Auftrag in Claude Code

Hier wird der **Marketing-Agent** umgesetzt (Konzept: Teil B). Er analysiert zuerst (Keywords, Wettbewerber, Ads-Allokation) und erstellt danach Entwürfe (SEO-Artikel, Ads, LinkedIn, Mails). Der volle Projektkontext steht in diesem Dokument.

**Erste Schritte (Vorschlag, aus dem 4-Wochen-Plan):**
1. Ordnerstruktur anlegen: `kontext/`, `daten/`, `material/`, `.claude/skills/`, `experiment-log.md`.
2. Dieses Dokument als `CLAUDE.md` ablegen (oder in `kontext/` aufteilen, falls es zu groß wird).
3. Skills klein anfangen: keyword-research (DataForSEO, Ausgabe als CSV), dann competitor-analysis, dann seo-article-draft mit compliance-check als Subagent.
4. Keyword-Daten: `Kieferblick_Keyword-Auswertung_v1.xlsx` als CSV in `daten/` (ca. 7.800 Keywords, Stand Juni/August 2025, Kontext siehe Teil D).

**Offene Entscheidungen, die du von Alexander brauchst:** monatliches Ads-Budget, Tally-Plan (Webhooks), Freigabe der Intro-Offer-Preise auf der Website, Wochenkontingent Smile-Check.

## 2. Aufbau und Gültigkeit

| Teil | Inhalt | Quelle im Projekt |
|---|---|---|
| A | Projektzusammenfassung (Hauptquelle: Markt, Avatar, Offer, Money Model, Lead Engine, Recht, offene Punkte) | Projekt_Zusammenfassung_Boutique_Praxis_v8 |
| B | Marketing-Agent Konzept (Skills, Schnittstellen, Betrieb, 4-Wochen-Plan) | Marketing-Agent_Konzept_v1 |
| C | Texte und Stimme: Artikel-Module, Smile-Check-Seite, Tonalität, Wortwelt, Farben | Website_Copy_Gesamtstand_v2, Brand_Identity_v2 |
| D | Daten und Recht: Keyword-Basis, Kanäle, Lead-Magnet-Formate, rechtliche Befunde | Akquise-Funnel_Erkenntnisse_v1 |
| E | CRM und Journey: Status, Marker, Automatisierungen, Kennzahlen, Mail-Serie | CRM-Spec_und_Zusammenfassung_v1, Customer-Journey_ab-Nurturing_v1 |

**Konfliktregel:** Bei Widerspruch gilt Teil A (v8, Stand 15.10.2026). Ältere Stände sind in C bis E dort überholt, wo sie von v8 abweichen. Bekannte Abweichungen: Aligner-Preise und drei Pläne (statt zwei), PZR-Abo und Retainer-Klub (statt Prophylaxe-Mitgliedschaft), kostenlose Erstberatung Wert 300 € und digitale Einstiegsleiter.

**Nicht enthalten (liegen im Projekt, bei Bedarf bei Alexander anfordern):** Kieferblick_Sales-Baum_v1 (inhaltlich in Teil A, Abschnitt 6 enthalten), Verkaufssheet_und_GOZ-Kostenvoranschlag_v2, Smile-Check_Landingpage_Copy_v1, Blogpost-Offer_3-Module_v3, Akquise-Flowchart_v5, Manuskript „Die 3x Aligner-Formel“, Website-Copy-HTML.

---

# TEIL A · Projektzusammenfassung (v8)

*Stand: 15.10.2026 (Fassung v8, ergänzt) · Fokus: Patientenseite · Neu gegenüber v7: **Abschnitt 5** (drei Aligner-Pläne statt zwei, PZR-Abo und Retainer-Klub als zwei getrennte Angebote, Erstberatung im Wert von 300 €), **Abschnitt 6** (Money Model v5 aus dem Sales-Baum: Intro-Offers, Pläne Basis/Ideal/Premium, Zahlungsreihenfolge, Festpreis-Zusage, Retainer-Wahl, Stufe 3 nach dem Ja), **Abschnitt 9 und 10** (Preise, Sales-Ablauf als 4-Step-Menü), **Abschnitt 12** (Stand, offene Schritte, Folgedokumente), neuer **Abschnitt 13d** (Entscheidungen vom 13.10.2026). **Ergänzt am 15.10.2026:** digitale Einstiegsleiter für Artikel-Besucher (Checkliste, Smile-Check 19 €, Ersttermin) in Abschnitt 6, 7 und 12 sowie neuer **Abschnitt 13e**. Sonst inhaltlich unverändert gegenüber v7.*
*Preise und Quoten sind Arbeitshypothesen. Quellen: Praxis- und Kettenseiten, Ratgeber, Verbraucherzentrale, Wettbewerbsrecht-Quellen, eigenes Manuskript, Hormozi („4-Step Menu Close“, „$100M Money Models“, „$100M Offers“, Zusammenfassungen Dritter), Jim Edwards (Zusammenfassungen Dritter).*

---

## 1. Projekt in einem Satz

Alexander Andreev übernimmt das Inventar der Praxis Dr. Dorl (Leineweberstr. 72, 45468 Mülheim) und baut unter dem Namen **Kieferblick (Subheader ZAHNBOUTIQUE)** eine **rein private Zahnpraxis im Boutique-Stil** mit Kern **Aligner** (funktionsorientiert), dazu **Bleaching, PZR-Abo, Retainer-Klub, Schiene für die Nacht (Schnarch-/Funktionsschiene)** und **Formkorrektur (Veneers)**. Premium-Positionierung, seriöse Medizin, Aufbau nach **Hormozi** (Avatar, Offer, Money Model).

**Fokus jetzt:** diesen einen Standort zur bestmöglichen Praxis machen, bei Patientengewinnung und bei Delivery/Operations. Die langfristige Vision (B2B, Beratung, Education, Standorte) steht in Abschnitt 14 und ist bewusst nicht Teil des Kerns.

**Entscheidung: keine Abrechnung über die GKV.** Bestandspatienten sind vermutlich überwiegend Kassenpatienten (Praxis wird laut Portal als gesetzlich versichert geführt). Folgen: frühes, klares Anschreiben zum Systemwechsel; ein Teil der Kartei wird abspringen (in der Planung einrechnen); Empfehlung an Partnerpraxen für Leistungen ohne Boutique-Angebot.

Direkte Nachbarn: Dr. Fiedeler (Leineweberstr. 65), Zahnärzte Kaiserstraße (Kaiserstr. 20, PLZ 45468).

---

## 2. Marktbild (deutschlandweit + lokal)

**Kein Anbieter gefunden, der genau deine Kombination als Boutique führt** (Aligner-Kern + Schnarch + Bleaching + Prophylaxe + Veneers, privat, premium).

| Typ | Beispiele | Merkmal |
|---|---|---|
| Aligner-Spezialist | Smile Club One (Köln/FFM/MUC; ca. 3.500–4.000 Fälle, Mülheim-Landingpage) | Preisstufen 1.499 / 1.999 / 2.499 €, Online-Beratung, Klarna |
| Ketten | DrSmile/Impress (Impress kaufte DrSmile), ilovemysmile, 8smile | Impress Ø 3.190–4.190 € (andere Seite 3.500–5.000), DrSmile ab 3.990 €; >110 Standorte; Verbraucherzentrale kritisierte Transparenz |
| MVZ-Kette | AllDent (Köln-Preisliste, Eigenanteil) | Invisalign 2.100 / 2.500 / 2.999 €, PZR 99–130, Bleaching 290, Veneer Keramik ab 780 (Ø ca. 1.500 laut Standortseiten); zinsfrei 24 Monate |
| Premium-Ästhetik | Smile Meets Design (Köln), B-KÖ Smiles + Am Malkasten (Düsseldorf), Hémmat (Berlin) | Generalisten mit Ästhetik-Fokus, Digital Smile Design, Personenmarke |
| Schnarchschienen | RUE104 Essen (Partner Ruhrlandklinik), Beyond Dental Bern (Überweisermodell) | Spezialisierung + Netzwerk zu HNO/Pneumologie |
| Schnarch online | Snorly | Festpreis 495 € inkl. Abdruckset, ohne Praxisbesuch, 60 Nächte Geld-zurück-Garantie (Preisdruck von unten) |
| Prophylaxe-Club (Praxis) | Dr. Strohkendl, Stuttgart | Erwachsene 260 €/Jahr für 3 PZR, Partner 460 €, KFO-Jugendliche 180 € (2 PZR), Firmentarife 189–240 €/Person; dazu Speicheltest, 7 Jahre Garantie auf Vollkeramik, Recall, einmal jährlicher Einzug |
| Prophylaxe-Flatrate (Versicherung) | u. a. Vigo (16,90 €/Monat), Tarife ab ca. 12,94 € | Zusatzversicherung erstattet PZR unbegrenzt; Preisanker im Kopf der Patienten (ca. 150–200 €/Jahr) |
| **Online-Vorabeinschätzung (neu 15.10.)** | USA: DentalChat 29 $ (15 Min), TeleDentists 59 $ / 199 $ (Zweitmeinung), Toothpic 10 $ / 35 $; Deutschland: dentinostic 29 / 49 / 79 € (fotobasiert) | Bezahlte Teledentistry-Einschätzungen sind im Markt üblich, kostenlose Vorberatung ebenfalls; **kein bezahlter, aligner-spezifischer Smile-Check mit Veneers-Vergleich gefunden** (keine Vollerhebung) |
| **Mülheim lokal** | Zahnärzte Kaiserstraße (Aligner + Schnarch + Ästhetik), Dr. Strickhausen, Praxis Alpaslan (Podcast), DEIN DENTAL (Retainer inklusive), DentSpa, KFO Schneider/Konietzny/Bahrs | Viele Generalisten; **kein sichtbarer Spezialist mit Fallzahlen/Belegen** |

**Marktpreise nach Komponente:**

| Komponente | Marktspanne |
|---|---|
| Aligner komplett | 1.500–5.000 (Ketten/Praxen), KFO bis ca. 8.500 |
| Retainer fest (pro Kiefer) | 150–600, typisch 250–500 |
| Retainer herausnehmbar / Ersatz | 150–350 / 150–400 |
| Bleaching In-Office / Home | 300–700 (bis 900) / 200–600 |
| PZR | 80–150 (Einzelpreis); im Prophylaxe-Club ca. 87 € je PZR |
| Veneers pro Zahn | Keramik 700–1.500 (einzelne Praxen bis 2.000–2.500), Non-Prep 600–1.200, Komposit 250–500; Düsseldorfer Premium-Praxis 1.000–1.500 |
| Schnarchschiene (Zahnarzt) | 1.200–2.000 (Ratgeber teils bis 2.200); online 495 € |
| Knirscherschiene (Aufbissschiene) | 300–600, bis ca. 800; Funktionsdiagnostik ca. 300 extra; einfache Schiene meist GKV-Leistung |

**Wichtige Muster:** Aligner allein differenziert nicht. Ketten sind bei Preis/Reichweite stark, schwach bei Endpreis-Klarheit, Zuständigkeit, Nachsorge. Retainer ist bei Ketten oft extra (Impress). Schnarchschiene ist lokal kein Alleinstellungsmerkmal (mind. 5 Anbieter in Mülheim); Kassenleistung nur bei Schlafapnoe nach gescheiterter CPAP-Therapie. Kein Aligner-Anbieter mit Prophylaxe-Mitgliedschaft gefunden (Stand Recherche, keine Vollerhebung). Knirscherschiene: Kassenleistung in der einfachen Form, Suchintention vermutlich preissensibel (Hypothese, über Test klären).

---

## 3. Avatar „Julia“ (Arbeitshypothese)

**Steckbrief:** 38, berufstätig (Verwaltung/Handel/Gesundheit/Wissenschaft), Mülheim/Umgebung, als Teenager Spange, Retainer irgendwann weggelassen, Zähne wieder in Bewegung. Preisfenster, in dem sie vergleicht: ca. 1.500–4.200 €.

**Warum plausibel:** Rezidiv nach Behandlung ist gut belegt (Studien: 40–90 % unbefriedigende Unterkieferfront nach 10 Jahren). 34 % achten beim ersten Treffen zuerst auf Zähne, 19 % sind unzufrieden. Arztwahl: 83 % fragen Freunde/Familie, 53 % erwarten ≥4 Sterne bei Google.

**Was sie sucht:** „Aligner Erfahrungen“, „Aligner Kosten“, „Zähne wieder schief nach Zahnspange“, „Aligner Mülheim“. Eigentliche Frage: *Ist das seriös, klappt es bei mir, und was kostet es am Ende?*

**Primäre Sorge:** *„Ich zahle viel und niemand übernimmt am Ende Verantwortung.“*

**Was sie bewegt:** Auslöser (Foto/Videocall, Jobwechsel, Hochzeit, Geburtstag, Kind bekommt Spange), Selbstsicherheit ohne Aufwand, diesmal soll es halten, wenig Termine.

**Marken/Geschmack (Hypothese):** „ruhiges Premium“ – skandinavisch-reduziert (Apple, Braun, Muuto/Vitra), Self-Care (Rituals, Oral-B iO), aktiv/gesund (On, Urban Sports Club, Oura).

**Design:** ruhig, warm, redaktionell; helle Naturtöne, klare Typografie; kein klinisches Blau-Weiß, kein Start-up-Neon; **Beweise statt Deko** (Arzt namentlich, echte Fälle, offene Preisrahmen).

**Anti-Avatar:** Rabattjäger, Fernbehandlungs-Erwartung ohne Kontrolle.

**Weitere Zielgruppen (Arbeitshypothese):**
- **Schnarch-Patient:** eher 40–60, oft männlich, Partnerin/Partner als Treiber; Leidensdruck statt Ästhetik; eigene Seite und eigene Botschaft, sonst verwässert die Marke. Brücke zur Marke: Funktion.
- **Bestandspatient (bisher Kasse):** kennt die Praxis, wird über Anamnese-Update und Intro-Offers (PZR, Bleaching, Schiene) angesprochen.
- **Artikel-Besucherin bundesweit (neu 15.10.):** kommt über Suchbegriffe, wohnt meist nicht in Mülheim, ist noch nicht bereit für einen Termin. Sie braucht erst Klarheit (Passt es? Was kostet es am Ende? Wer kümmert sich?) und bekommt dafür die digitale Einstiegsleiter (Abschnitt 6).

**Tonalität:** „Sie“, ruhig, souverän, konkret; ehrlich über Nachteile (Attachments, Lispeln, 22 h Tragezeit, Retainer); „diskret“ statt „unsichtbar“; entlastend („Zähne bewegen sich ein Leben lang“); Ich-Form des Behandlers.

---

## 4. Blocker entlang der Journey

| # | Blocker | Kern |
|---|---|---|
| B1 | Vertrauen / Verantwortung | Wer haftet, wer ist erreichbar, gibt es die Praxis in 2 Jahren? |
| B2 | Endpreis | Retention, Refinements, Vorbehandlung, Finanzierung |
| B3 | Ergebnisrisiko | Sieht es aus wie erwartet, wird mein Fall gelöst? |
| B4 | Rückfall | Retainer für immer, wieder schief? |
| B5 | Alltag / Disziplin | 22 h, Lispeln, Druckschmerz, Essen/Reisen |
| B6 | Zeit | Wartezeit, Verlängerung, Motivationsdelle in der Mitte |

Verteilt über 8 Phasen: Auslöser → Recherche → Beratung → Start → Tragephase → Halbzeit → Abschluss → Danach.

---

## 5. Positionierung und Offer

**Intern:** die vollständigste, am besten begleitete Aligner-Behandlung im Markt. **Extern:** *„Die vollständig begleitete Aligner-Behandlung“* (kein Superlativ, keine Namensvergleiche).

**Name:** *Die begleitete Aligner-Behandlung* · **Leitzeile:** *Ein Arzt. Ein Plan. Bis zum Retainer.* · **Dachzeile für die digitale Leiter (neu 15.10.):** *Erst Klarheit. Dann entscheiden.*

**Module (Angebotsstapel):**
1. **Klarheit vor dem Start:** kostenlose **Erstberatung im Wert von 300 €** (3D-Scan, Foto- und Bissanalyse, Kiefergelenk-Check, Ergebnis vorab mit Smile-Simulation und persönlicher Empfehlung, ca. 60 Min; Angebot mit Unterschriftsmöglichkeit am selben Tag), Leistungsumfang auf einer Seite (inkl. Refinement-, Planänderungs-, Abbruchregel), Erwartungs-Briefing, Bedenkzeit als Recht des Patienten, Zweitmeinung willkommen. Nach der Unterschrift: Röntgen, Funktionsdiagnostik und Feinplanung mit Planungsprotokoll und verbindlichem Heil- und Kostenplan. **Für Besucher aus der Ferne davor:** Checkliste und Smile-Check (Abschnitt 6)
2. **Ein Arzt, ein Plan:** du persönlich, fester Ansprechpartner, Direktkanal mit Antwortzeit, Vertretung, Datenübergabe
3. **Weg mit Landkarte:** Zeitleiste, Willkommensset, Wechseltag-/Alltagsguide, Halbzeit-Check, Zwischencheck
4. **Alltag gesichert:** Ersatzregel bei Verlust/Bruch, Prophylaxe während der Behandlung
5. **Ergebnis geklärt:** Abschlussgespräch mit Dokumentation, Bisscheck
6. **Damit es hält:** herausnehmbarer Retainer (**entschieden: 2 Schienen pro Kiefer im Plan enthalten**, fester Retainer als Aufpreis, im Premiumplan inklusive), danach **Retainer-Klub** und **PZR-Abo** als zwei getrennte Angebote
7. **Festpreis-Zusage:** Der Preis im Plan bleibt bis zum Abschluss der Behandlung gleich, inklusive üblicher Nachkorrektur, keine Nachforderungen (Antwort auf Blocker B1/B2). Ausnahmen [Annahme]: Wunschänderungen des Patienten und verlorene Schienen
+ **Option Finish:** Bleaching (Praxis oder Zuhause), „Weiß und gerade“

**Praxiszusagen** (statt Erfolgsgarantie): Antwortzeit, Kostenklarheit (Mehrkosten nur mit Zustimmung; Festpreis-Zusage), Nachkorrektur im Umfang, Notfalltermin, Datenübergabe, Zweitmeinung.

**Verstärker (angepasst):** Knappheit = echte Behandlungsplätze pro Quartal und begrenzte Erstterminplätze pro Woche (beim Smile-Check ein Wochenkontingent, nicht in der Box genannt); Dringlichkeit = keine Fristen (auch Intro-Offers ohne Frist); Boni = benannte Bausteine des Umfangs, keine „Gratis“-Extras; Garantie = Leistungszusagen und Festpreis-Zusage (beim Smile-Check die Erstattungs-Zusage); Name ohne Superlative.

**Angebotsarchitektur (Regel, angepasst 13.10.2026):** Stufen nur dort, wo der Patient in der Situation wirklich wählen muss. Aligner: **drei Pläne** — Basis/Ästhetischer Plan (nur Front), Idealplan (funktionell, alle Zähne) und Premiumplan (wie Ideal mit Premium-Material und -Service). Der Gesprächsablauf bleibt eine Prescription: Alexander empfiehlt den Idealplan, Premium dient als Anker, Basis erscheint nur bei einem Geld-Einwand. Variante nach Befund: Veneers als zweiter Anker (Weiche in Abschnitt 10). PZR-Abo und Retainer-Klub sind **zwei** Angebote (kombinierbar). Bleaching: Praxis oder Zuhause, zwei Intro-Offer-Preise, keine weiteren Stufen. Veneers: ein Angebot als Preisrahmen pro Fall, Material nach Befund. Schiene für die Nacht: **ein** Angebot, die Abklärung entscheidet die Variante. Variabilität entsteht im Gespräch, nicht in Menüs auf der Website.

**Rückfall-Schutz (Vorschlag, nicht bestätigt):** Retainer-Ersatz, jährliche Stellungskontrolle und kleine Nachkorrektur zu festem Preis als **Leistungszusage** (keine Erfolgsgarantie, Rechtscheck). Antwort auf Blocker B4. Träger ist jetzt der **Retainer-Klub** (Stellungskontrolle, neuer Retainer alle 6 Monate).

---

## 6. Money Model + Preise (Version 5, Sales-Baum vom 13.10.2026; Einstiegsleiter ergänzt 15.10.2026)

Struktur nach Hormozi in drei Stufen: **Einstieg** (Cash am Start, Vertrauen), **mehr Cash pro Fall** (4-Step-Menü), **Bindung nach dem Ja**. Vollständiger Baum mit Texten: „Kieferblick Sales-Baum v1“.

### Stufe 1 · Einstieg

**Digitale Einstiegsleiter (neu 15.10.2026), für Artikel-Besucher bundesweit.** Drei Schritte, jeder für sich nützlich, in drei festen Modulen auf jeder Artikel-Seite (Texte: Teil C):

| Schritt | Angebot | Preis | Ablauf |
|---|---|---|---|
| 1 | Checkliste „7 Fragen vor der Unterschrift“ | gratis | Tally → PDF per Mail → Rückruf oder Nurturing |
| 2 | **Smile-Check** | **19 €, nicht anrechenbar** | Tally: 8 Fragen, 5 Handyfotos, optional PDF eines fremden Angebots → persönliches Video von Alexander in 2 Werktagen |
| 3 | Ersttermin | kostenlos, Wert 300 € | Tally → Rückruf ≤10 Min |

Der Smile-Check klärt offen: ob Aligner das Richtige sind (Ampel), ob Veneers eine Alternative sind und warum, grobe Einschätzung zu Dauer und Kosten (Rahmen, nur im Video), Einordnung eines vorhandenen Angebots. Er ist eine erste Einschätzung, keine Diagnose, und ersetzt den Ersttermin nicht. Statt Anrechnung gilt die Erstattungs-Zusage (kurze Nachricht genügt). Es gibt eine feste Smile-Check-Seite mit Video (VSL) und Tally im Hero (Teil C). Kein Preiskampf mit Zweitmeinung: Das Fremdangebot ist ein Baustein im Smile-Check.

**Erstberatung im Wert von 300 €, kostenlos für den Patienten.** Zusammensetzung (Werte nach GOZ-Positionen, Arbeitsstand):

| Leistung | Wert |
|---|---|
| 3D-Scan | 64 € |
| Foto- und Bissanalyse | 70 € |
| Kiefergelenk-Check | 75 € |
| Ergebnis vorab (Untersuchung, Smile-Simulation, persönliche Empfehlung) | 91 € |
| **Gesamt** | **300 €** |

Belegt sind GOZ 0065 (10,35 € bei 2,3-fach, viermal je Sitzung) und die Auswertung analog 6010 (23 €). Die übrigen Beträge sind Schätzungen [Annahme], GOZ-Punktzahlen für 0010, 6000 und 8000 sind noch zu prüfen. **Bestandspatienten:** kurzes Anamnese-Update, ca. 15–20 Min.

**Intro-Offers (voll auf den Aligner-Plan anrechenbar, keine Frist, SEPA-Mandat vor Ort):**

| Angebot | Preis |
|---|---|
| PZR | 149 € |
| Bleaching in der Praxis | 399 € |
| Bleaching für zu Hause | 299 € |
| Schnarchschiene (Paket inkl. Kontrollen, Screening vorab) | 799 € |

Bleaching ist das kleine Ja, wenn Aligner nicht passen. Funktionsschiene (Zentrik) bleibt geparkt (ca. 700–900 €, Hypothese). Der Smile-Check gehört nicht zu den anrechenbaren Intro-Offers.

### Stufe 2 · 4-Step-Menü Aligner

1. **Unselling:** Alexander sagt klar, was der Fall nicht braucht (Ampel). Veneers-Weiche aus Anamnese und Klinik (Abschnitt 10). Der Smile-Check nimmt diese Ampel schon vorweg; im Ersttermin wird sie durch den Befund bestätigt oder korrigiert.
2. **Prescription:** „Idealplan für XX €/Monat“. Persönliche Empfehlung mit einem Satz Begründung aus dem Befund, kein Auswahlmenü. Beispiel bei 48 Monaten ca. 198 €/Monat, bei 36 Monaten ca. 253 € [Annahme: 9,9 % effektiver Jahreszins, Bank offen].
3. **Anker zuerst, dann Ideal:** Premium (oder Veneers) zuerst nennen, dann die Prescription auf Ideal, danach die Zahlungswege. Der Ästhetische Plan kommt nur bei Geld-Einwand, nach den Zahlungswegen.
4. **A/B-Fragen und Zahlung** (Retainer, Zahlungsweg), SEPA-Mandat am Tisch.

**Die drei Pläne:**

| | Basis (Ästhetischer Plan) | Idealplan | Premiumplan |
|---|---|---|---|
| Preis | ca. **3.900 €** | ca. **7.900 €** | **11.900 €** (Faktor 1,5 zu Ideal; ca. +101 €/Monat bei 48 Raten (Ideal ca. 198 €, Premium ca. 299 €)) |
| Umfang | Kleine Korrektur von Eckzahn zu Eckzahn | Korrektur aller Zähne, funktionell | Wie Ideal |
| Attachments | – | Standard-Kunststoff | Stufung und Attachments aus Hochleistungs-Kunststoff |
| Schienenmaterial | – | Einlagig | Mehrlagig, schonende Bewegung |
| Digitale Kiefergelenk-Vermessung | nicht enthalten | **inklusive** | **inklusive** |
| Retainer | 2 lose pro Kiefer inklusive | 2 lose pro Kiefer inklusive, fest 599 € pro Kiefer als Aufpreis | **fester Retainer inklusive** (Wert 1.198 € für beide Kiefer) |
| Extras | 1 Nachkorrektur-Set inklusive | Nachkorrektur im Behandlungsziel inklusive | Premium-Zubehör, Premium-WhatsApp-Hilfe |
| Rolle im Gespräch | Fallback bei Geld-Einwand, nur bei passendem Befund | Empfehlung aus Schritt 2 | Anker und vollwertiger Plan |

Begründung Kiefergelenk-Vermessung: Wenn alle Zähne bewegt werden, verändert sich die Bisslage. Beim Basisplan ist das nur sehr begrenzt der Fall [Annahme]. Der Kiefergelenk-Check der Erstberatung (klinisch) ist davon getrennt.

**Durchschnittliche Fallgröße Idealplan:** 60–70 Schienen (Max-Stufe im FUNCTIONAL-Laborpaket, unlimitierte Step-Anzahl, 5 Jahre Behandlungsfrist).

**Zahlungswege** (feste Reihenfolge, hochpreisig zuerst):
1. Einmalzahlung (Ideal: 7.900 €, ohne Rabatt)
2. Phasen 30/40/30 (Ideal: 2.370 € · 3.160 € · 2.370 €)
3. Rate über die Partnerbank (Beispiel Ideal bei 48 Monaten ca. 198 €/Monat, bei 36 Monaten ca. 253 € (9,9 % effektiv, Annahme); **Laufzeit und Konditionen offen**)

Gesamtkosten immer ausweisen.

**Retainer-Wahl (A/B):** lose (2 pro Kiefer im Plan enthalten) oder fest (599 € pro Kiefer, Premium inklusive).

**Abzweige (jederzeit gültig):**

| Signal | Antwort |
|---|---|
| Ausdrücklicher Zweifel an der Tragedisziplin | Veneers-Ausstieg mit Komposit-Mock-up zum Probetragen. Komposit ca. 2.400–4.000 € · Keramik ca. 8.400–12.800 € (Preisrahmen pro Fall; Non-Prep gestrichen) |
| Bedenkzeit | Kein Downsell. Rückruftermin im Raum, Einwandtyp notieren, Nachfass-Sequenz ca. 4 Wochen. Anrechenbare Intro-Offers bleiben gültig |
| Nein, passt nicht | Bleibt im Bestand, Zweitmeinung willkommen. Bleaching als kleines Ja |

**Cash am Start (Rechenbeispiel Ideal):** Phase 1 bei 30/40/30 = 2.370 €, abzüglich Laborpaket laut Kostenplan-Entwurf (1.891 €) bleiben ca. **480 €** (unter dem Benchmark von 600–800 € pro Fall). Mit Bankauszahlung bei Rate ca. 6.000 € vor Gebühren [Annahme, Bank klären].

### Stufe 3 · Nach dem Ja

| Schritt | Inhalt |
|---|---|
| Falldokumentation mit Bildern | **200 € Rabatt** auf den Plan als Gegenleistung für die Dokumentation (Ideal: 7.700 € statt 7.900 €); gilt für alle Pläne [Annahme] |
| Halbzeit-Check | Natürlicher Moment für den ersten Upsell, z. B. Farbe vor Form |
| Abschlusstermin | 10 Min Alexander, 10 Min Beraterin, Retainer-Übergabe, Smile-Video |

**Upsell nach Erfolgserlebnis:**

| Angebot | Preis | Inhalt |
|---|---|---|
| **PZR-Abo** | **229 € pro Jahr** | 2 PZR pro Jahr statt 298 € einzeln (2 × 149 €), Ersparnis 69 € |
| **Retainer-Klub** | **249 € pro Jahr** (beide Kiefer), **149 €** (ein Kiefer) | Alle 6 Monate ein neuer herausnehmbarer Retainer pro Kiefer (also 4 bzw. 2 pro Jahr), Stellungskontrolle. Materialkosten pro Retainer [Annahme 25–40 €, mit Labor prüfen] |
| **Kombi** PZR-Abo + Retainer-Klub | **429 € pro Jahr** | Statt 478 € einzeln, Ersparnis 49 €. Ein Termin im Halbjahr: PZR, Stellungskontrolle, neuer Retainer |
| Weiß-und-gerade-Bleaching | Praxis 399 € · Zuhause 299 € | Nach Entfernen der Attachments |

Start jeweils im Abschlusstermin (SEPA).

**Referral:** (1) Bewertung erfragen: alles gut → Google-Bewertung per QR, sonst meldet sich Alexander binnen 48 Stunden und liest nach. (2) Empfehlung erfragen, **Form der Prämie offen** (rechtlich prüfen, Abschnitt 11). (3) Neuer Fall: der Kreis schließt sich bei Erstberatung oder Intro-Offers.

**Referenzwert Netzwerk / offener Punkt:** Functional-Kollegen kalkulieren vergleichbare Fälle (inkl. Gelenksvermessung + separater Funktionsschiene) bei 10–12 k €. Idealplan (7.900 €) liegt bewusst darunter, **der Premiumplan (11.900 €) liegt jetzt in der Kollegen-Spanne**. Das bleibt über Positionierung, Material und Service zu begründen. **Offen für Wirtschaftlichkeit (Abschnitt 12, Punkt 3):** Marge bei 60–70 Schienen und längerer Behandlungsdauer gegen das interne Honorar für Refinement-Freigaben und Compliance-Checkpoints (grob geschätzt: 55–80 € pro Refinement-Zyklus bei Arzt- und Beraterin-Zeit) gegenrechnen; zusätzlich Kosten der Premium-Bestandteile (fester Retainer, Material) und der Falldoku-Rabatt.

**Cross-Selling-Logik:** Funktion → Stellung → Farbe → Form. Wer knirscht, braucht erst funktionelle Stabilität (Schiene vor Veneers). Bleaching am Abschluss (nach Entfernen der Attachments), Veneers nur bei Indikation, Farbe vor Form.

**Preisposition:** Aligner über Impress/DrSmile und Ketten (DTC-Obergrenze ca. 5.000 €), Idealplan unterhalb der Netzwerk-Kollegen-Referenz (10–12 k €), Premium innerhalb davon. Veneers im oberen Marktbereich. Schnarchschiene über dem Online-Preis (495 €), unter dem üblichen Zahnarzt-Bereich (1.200–2.000 €). Zahlungsbereitschaft in Mülheim = Hypothese; Test über Abschlussquote nach dem Erstermin.

**Folgen der kostenlosen Erstberatung:**
1. **Kein bezahlter Einstieg:** Schutz vor Rabattjägern und No-Shows über Fragebogen bei Buchung, Bestätigung und Erinnerung, begrenzte Erstterminplätze, **keinen Unterschriftsrabatt**. (Der Falldoku-Rabatt von 200 € ist an die Dokumentation gekoppelt, nicht an die Unterschrift.) **Ergänzung 15.10.:** Der Smile-Check (19 €) ist ein bezahlter Vor-Einstieg für Fern-Interessentinnen und filtert zusätzlich; er ersetzt die kostenlose Erstberatung nicht.
2. **Kosten des Termins** (Arzt 10 Min, Beraterin ca. 60 Min, Scan, Material) sind Akquisekosten und gehen in die Wirtschaftlichkeitsrechnung ein. Mit Abschlussquote 30–40 % ist sie der stärkste CAC-Hebel.
3. **Kern-Preis trägt** Röntgen, Funktionsdiagnostik und Feinplanung (Arbeitsannahme, in der Wirtschaftlichkeit prüfen).
4. **Preisrahmen vs. Feinplanung:** Am Erstermin gilt der Preisrahmen aus Simulation und Kurzbefund. Zeigt die Feinplanung Mehrbedarf, gibt es Mehrkosten nur mit Zustimmung (und im Rahmen der Festpreis-Zusage); Planänderungs- und Abbruchregel stehen im Ein-Seiter.
5. **Bestand:** Der volle 60-Minuten-Termin lohnt nur bei Aligner-Interesse. Für PZR-, Bleaching- und Schienen-Patienten reicht das kurze Anamnese-Update.
6. **Überschneidung Erstberatung / GOZ-Kostenplan Block 1:** Scan, Foto- und Bissanalyse und Kiefergelenk-Check dürfen nicht doppelt berechnet werden. Klären, welche Posten kostenlos bleiben und was nach dem Ja im Heil- und Kostenplan steht (Abschnitt 12, Punkt 2).

**Zu Bleaching (Arbeitsstand):** Home-Bleaching (299 €) spart Stuhlzeit, In-Office (399 €) bringt am Anfang den Wow-Moment für Bewertungen und Fälle (freie Stuhlzeit vorhanden). Schienen zunächst extern fertigen lassen (Labor/Fräszentrum); eigener DLP-Drucker erst ab fester Fallzahl.

**Zu Veneers (Arbeitsstand):** Keine Stufen auf der Preisliste. Türöffner ist ein Mock-up in Komposit zum Probetragen. Knirschen und Bisslage vor Keramik klären. Ehrlich über Haltbarkeit (Studienlage: Keramik ca. 95 % nach 10 Jahren, Komposit ca. 88 % nach 5 Jahren).

---

## 7. Lead Engine (High Level)

**Aktualisiert 08.10.2026, ergänzt 15.10.2026.** Details und Plan: Teil B (Marketing-Agent Konzept).

**B2B (Eingang C, Überweiser/Netzwerk):** (1) **Netzwerk / Überweiser** (Praxen, Physio/Osteopathie/HNO, Labore) über **E-Mail und Brief an die Liste eingewilligter Zahnarztpraxen in NRW** und **LinkedIn** (persönliche Ansprache, Verweis auf Videos, Konsultation anbieten). Ein Agent entwirft, Alexander sendet. Rahmen: keine Vorteilsgewährung, kein Tausch (Abschnitt 8 und 11).

**B2C, Fundament:** **Google + lokale Präsenz** (Profil, Bewertungen, Mülheim-Seite), **Bestandspatienten** und Empfehlungen.

**B2C, skalierbar (Agent-tauglich):**
- **SEO-Wissensartikel auf WordPress in großer Menge** (Longtail- und viel gesuchte Keywords, programmatisch aus einer Artikel-Vorlage). **Neu gegenüber v6:** Dort stand „nicht als Kern: tausende Blogartikel (Spam-Risiko bei Google; lieber wenige hundert tiefe Seiten mit echten Fällen)“. Alexander berichtet aus eigener Erfahrung, dass Wissensartikel für Patienten sehr gut funktionieren (Annahme, noch nicht in den Daten belegt). Leitplanken: Autor Alexander, echte Fakten oder Fälle, Antwort auf die Suchfrage, HWG-Check pro Artikel; Wirkung früh in der Search Console beobachten. **Neu 15.10.2026, Conversion:** Die meisten Besucher sind Patienten aus ganz Deutschland, Alexander ist lokal. Darum trägt jeder Artikel **drei feste Module** (Kopf-Box, Smile-Check-Box nach der zweiten Überschrift, Schluss; auch mobil) mit der digitalen Einstiegsleiter Checkliste → Smile-Check → Ersttermin (Abschnitt 6). Alle Buttons führen zu Tally-Formularen (Checkliste, Smile-Check, Ersttermin) mit der Artikel-Adresse als verstecktem Feld, damit Seite und Keyword dem Lead zugeordnet werden. Texte: Teil C.
- **Google Ads** als erster Paid-Test (Ruhr-Umkreis, fester Budgetdeckel), **Meta Ads** (Instagram und Facebook) als zweiter Test, nur wenn Landingpage und Tracking stehen. Meta schränkt Gesundheitswerbung ein (keine „Sie haben“-Ansprache, keine Vorher-nachher-Bilder, keine Ergebnisversprechen).
- Mail-Serie an Leads und Bestand.

**Verstärker:** Fall-Content. **Vorher-nachher-Bilder** sind rechtlich offen (OLG Frankfurt 06.11.2025 untersagte sie bei nicht indizierten Eingriffen auch in Storys, Übertragbarkeit auf Aligner ungeklärt), deshalb bis zur Klärung ohne Vorher-nachher planen. **Später:** lokale Partner (Salons ohne Gegenleistung), Instagram organisch, YouTube. **Entfällt:** Kaltansprache an Patienten.

**Reihenfolge der Kanäle zum Start:** (1) Fundament (Tracking, Landingpage, Google-Profil), (2) **Bestandskartei** (Anschreiben zum Systemwechsel, Anamnese-Update, Intro-Offers PZR, Bleaching und Schiene), (3) Überweiser, Empfehlungen und B2B-Ansprache, (4) SEO-Artikel, (5) Google-Ads-Test, (6) Meta-Test. **Schnarch-Test:** eigene lokale Landingpage plus Google-Profil, kleines Budget mit festem Deckel, Suchvolumen vorab mit dem Keyword-Tool (DataForSEO) prüfen, Messgrößen Kosten pro Erstberatung und Abschlussquote. Werberecht beachten (Formulierung „Schnarchen“, keine Erfolgsversprechen).

**Roter Faden:** Nische „komplexe funktionsorientierte Aligner-Fälle“ + Marke Alexander Andreev + Beweise (Fälle, Bewertungen).
**Phasen:** Aufbau (Website, Google-Profil, dokumentierte Fälle, Partnerliste) → Start (Gespräche, erste Fälle, Bewertungen) → Ausbau (Content, Ads-Test, lokale Partner).
**Trichter-KPIs:** Anfragen → gebuchte Termine → erschienen → Abschlüsse, mit Kosten je Stufe; No-Show-Quote als eigene Kennzahl (kostenlose Erstberatung). Neu: Anteil Ideal/Premium/Basis, gewählter Zahlweg, Cash am Start. **Neu 15.10.:** Conversion je Artikel und Modul (Checkliste, Smile-Check gekauft, Ersttermin angefragt), Erstattungsquote Smile-Check, Anteil Smile-Check → Ersttermin → Abschluss. Benchmark aus deinem Buch: **600–800 € pro gestartetem Fall**.

**Überweiser:** siehe Abschnitt 8 (Offer „Functional-Netzwerk Ruhr“). **Weitere Angebote:** Abschnitt 9.

---

## 8. Überweiser-Offer: „Functional-Netzwerk Ruhr“

**Avatar:** Zahnärztinnen/Zahnärzte mit komplexen oder funktionell heiklen Aligner-Fällen, die sie nicht selbst tragen wollen (zuerst Allgemeinpraxen; später Aligner-erfahrene Praxen an ihren Grenzen; Physio/Osteopathie/HNO/Labore als Variante). Gegenwind: Allgemeinpraxen behalten Aligner-Fälle zunehmend selbst → gezielt **komplexe** Fälle ansprechen.

**Was sie wollen (Wertgleichung):** Fall gelöst, **Patient bleibt ihrer**, kein Haftungsrisiko, schnelle Antwort, kein Papierkrieg.

| Problem der Praxis | Lösung |
|---|---|
| Angst, den Patienten zu verlieren | **Kollegen-Charta:** Patient bleibt Ihrer; Prophylaxe, Kons, Prothetik bleiben bei der Hauspraxis |
| Haftung bei funktionellen Fällen | Dein **Functional-Protokoll** (funktionelle Planung, zentrische Position, Kap. 9) als dokumentierter Standard |
| Unklar, wann/wohin überweisen | Indikations-Checkliste + Ein-Seiten-Formular |
| Kein Feedback | Berichte nach Planung, Halbzeit, Abschluss |
| Kein Vertrauen in Unbekannten | Fall-Dossiers, Fachabende, persönlicher Besuch |
| Keine Zeit | Alles läuft über dich; Praxis schickt Scans + Befund |

**Angebotsstapel:** (1) Überweisungspaket mit Antwortfrist, (2) zwei Modi: ganzer Fall abgeben oder selbst behandeln mit deiner Functional-Planung, (3) Berichtswesen, (4) Rückübergabe inkl. Retainer-Protokoll, (5) Functional-Abende, (6) Fall-Dossier-Zugang, (7) Empfehlungsliste für Leistungen, die du nicht anbietest.

**Deine drei Ideen – Bewertung:**
- **Functional als Köder:** ja – Methode statt „noch ein Aligner“. Hook: Functional-Checkliste („Wann ein Fall funktionell geplant werden sollte“), Fall-Zweitmeinung auf Anfrage.
- **Partys:** ja, als **Fachabend mit Party-Gefühl** (15–25 Personen, 6–8 pro Jahr, Fallimpuls + Fallbesprechung + Essen, Fortbildungspunkte, persönliches Nachfassen).
- **Eigene Patienten für Endo/Kons/Prothetik weiterschicken:** ja, als **Empfehlungsliste**, **nicht als Tausch** (kein „ich schicke dir X, du mir Y“, keine Mengenzählung) – sonst greifen Berufsrecht und § 299a StGB und das Netzwerk wird angreifbar.

**Verstärker:** Knappheit = begrenzte Fälle pro Monat, feste Gründungspartner; Bonus = Fortbildung, Checkliste, Dossiers; Zusagen statt Garantie = Antwortzeit, Berichtsfrist, Rückübergabe, Charta.
**Name:** *Functional-Netzwerk Ruhr* · **Zeile:** *Komplexe Fälle, kollegial gelöst. Ihr Patient bleibt Ihrer.*
**KPIs:** aktive Zuweiser, Überweisungen pro Zuweiser, Antwortzeit, Rückübergabequote, Fälle mit Bericht.
**Offener Punkt:** Bei überwiesenen Patienten Prophylaxe/Bleaching bei der Hauspraxis lassen (Charta-Konsistenz); bei eigenen Patienten unverändert.
**Kanäle für die Ansprache (neu 08.10.2026):** E-Mail und Brief an eingewilligte NRW-Praxen, LinkedIn (siehe Abschnitt 7).

---

## 9. Weitere Angebote: Bleaching, Formkorrektur, Schiene für die Nacht

Aligner-Kern bleibt Hauptmotor. PZR, Bleaching und Schnarchschiene sind wegen geringem Aufwand und hoher Marge auch als **Intro-Offers** gedacht, vor allem für Bestandspatienten und Menschen, die (noch) keinen Aligner wollen. Alle Intro-Offers sind voll auf den Aligner-Plan anrechenbar.

| | Bleaching | Formkorrektur (Veneers) | Schiene für die Nacht |
|---|---|---|---|
| Kunde | Bestand, Google-Suche, Aligner-Abschluss | Eigene Aligner-Patienten, Bleaching-Patienten, Patienten mit rein kosmetischem Wunsch | Schnarcher + Partner, meist 40+; Knirscher/CMD über Anamnese und Physio/Osteopathie |
| Ticket | Praxis 399 € · Zuhause 299 € | Preisrahmen pro Fall: Komposit ca. 2.400–4.000 €, Keramik ca. 8.400–12.800 € (Non-Prep gestrichen) | Schnarch 799 € (Paket inkl. Kontrollen); Funktionsschiene ca. 700–900 € (geparkt) |
| Kanal | Bestand, Anamnese, Google | Warm (Kernpatienten), Fall-Content, Mock-up, Weiche im Aligner-Gespräch, **Smile-Check (Veneers als Alternative im Video)** | Überweiser (HNO, Schlafmedizin, Pneumologie), Anamnese, eigene Landingpage (Test) |
| Aufwand | Niedrig (In-Office: Stuhlzeit) | Mittel (Labor, Portfolio) | Klinisch einfach; Screening und Aufklärung nötig |
| Synergie | Hoch (Farbe vor Form, Auffrischung über Weiß-und-gerade-Angebot) | Sehr hoch (Stellung → Farbe → Form) | Mittel (Funktion, Kontrolle über Retainer-Klub/PZR-Abo) |

**Schnarchschiene (Regeln):** Ohne GKV-Weg (Selbstzahler). **Nicht umgehen:** kurzes Screening auf Schlafapnoe (Fragebogen); auffällig → Überweisung an Schlafmedizin aus dem Netzwerk, unauffällig → Schiene. Aufklärung: Protrusionsschiene kann Zähne und Biss verändern, Abstimmung mit Aligner und Retainer. Abgrenzung zu Online-Anbietern über ärztliche Begleitung, nicht über den Preis.

**Funktionsschiene (geparkt):** Verkauft wird Funktionsdiagnostik + Zentrikschiene + Kontrolle, nicht die einfache Kassenschiene. Wer nur eine einfache Schutzschiene braucht, bekommt die Empfehlung an eine Kassenpraxis. Eine Funktionsschiene kann teilweise den Retainer ersetzen (klinische Entscheidung im Behandlungsplan, keine Produktvariante).

**Bündelung:** Schnarch- und Funktionsschiene als **ein** Angebot „Schiene für die Nacht“ prüfen (eine Seite, ein Zweig im Erstgespräch). *Bestätigung offen.*

**Reihenfolge-Vorschlag:** PZR, Bleaching und Schnarchschiene als Intro-Offers ab Start für Bestand und Netzwerk; Veneers über Aligner-Abschluss, Anamnese-Weiche und Mock-up, sobald Labor und Portfolio stehen. *Bestätigung offen.* **Ergänzung 15.10.:** Die Veneers-Seite geht erst mit Labor und echten Fällen live; bis dahin zeigt der Smile-Check Veneers nur im Video und verlinkt nicht dorthin.

**Hinweise Veneers:** schonende Varianten zuerst (Bonding, Komposit-Mock-up), Keramik mit Portfolio; in Mülheim bieten mehrere Praxen Veneers/Bleaching an, Premium-Wettbewerb eher Köln/Düsseldorf. Schnarchschiene lokal mind. 5 Anbieter (RUE104 Essen als Vorbild mit Klinik-Partner, Beyond Dental Bern Überweisermodell).

---

## 10. Sales-System (aus dem Buch „Die 3x Aligner-Formel“ + Hormozi 4-Step-Menü)

**Formel:** Gewinn pro Fall = ↑Preis − ↓Material − (↓Termine × ↓Personalkosten/Std.) − ↓Kosten pro Neupatient.

| Stufe | Buch | Übertrag auf die Boutique |
|---|---|---|
| Erstkontakt | Rückrufkette: Anruf ≤10 Min, SMS +5 Min, 2. Anruf nächster Tag; Antwort ≤2 Std.; Online-Buchung | übernehmen |
| Beratung | Ein-Termin-Modell in 8 Schritten, Arzt 10 Min, Aligner-Beraterin führt, Einstieg „Was stört Sie am meisten?“, 3 Einverständnis-Checks | Kostenlose Erstberatung (Wert 300 €) als Ein-Termin-Modell; Beraterin führt alle Schritte außer Schritt 6, du machst Befund + Freigabe (10 Min) persönlich |
| Angebot | Stufenplan: Option 1 (funktionell, Refinement eingepreist) → Option 2 (Front) × 3 Zahlungswege in fester Reihenfolge | **4-Step-Menü** (Abschnitt 6): Unselling → Prescription Ideal → Anker (Premium oder Veneers) → A/B-Fragen und Zahlung; Reihenfolge der Zahlwege Einmal → 30/40/30 → Rate; Basis nur bei Geld-Einwand; Ein-Seiter Leistungsumfang |
| Zögerer | Nachfass in 3 Schritten (E-Mail, Anruf, weitere E-Mails) nach Einwandtyp | übernehmen, ruhiger Ton, ca. 4 Wochen; kein Downsell bei Bedenkzeit |
| Start | Ablauf sofort erklären, Einwilligung vor Bonding, Erinnerung | Onboarding-Paket; Röntgen, Funktionsdiagnostik, Feinplanung erst nach Unterschrift; Falldoku (200 € Rabatt) |
| Abschluss | 2×10 Min, 5 Zufriedenheitsfragen, Bewertungsbitte | Ergebnisabgleich, Retainer-Übergabe, Smile-Video |
| Wiederkehr | Retainer-Abo (alle 6 Monate), im Buch 150 € zweimal pro Jahr bzw. 300 €/Jahr über ca. 5 Jahre | **PZR-Abo (229 €/Jahr) und Retainer-Klub (249 €/Jahr, ein Kiefer 149 €), Kombi 429 €**; Start im Abschlusstermin bei der Beraterin |
| Steuerung | 5 Kennzahlen (Abschlussquote, Kosten/Neupatient, Umsatz/Fall, Gewinn/Fall, Refinement-Rate) | Trichter-Tracking |

**Zahlen aus dem Buch:** Refinement-Rate 70–80 % = Standard (einpreisen!); Abschlussquote 25–40 % solide, >40 % sehr gut (in Kap. 6 stehen 75 % im Ersttermin als Zielwert → für die Planung mit **30–40 %** rechnen); Beraterin senkt Arztzeit pro Beratung auf ca. 10 Min.

**Sales-Ablauf v2 (Patientenseite, Ablauf-Ebene; Skripte und Details bewusst später):**

Anfrage → Erstkontakt (Rückruf, Fragebogen, Buchung) → **Erstberatung, kostenlos** (8 Schritte, ca. 60 Min) → Entscheidung (Unterschrift oder Bedenkzeit; bei Bedenkzeit Nachfass in 3 Schritten) → Nach der Unterschrift (Röntgen, Funktionsdiagnostik, Feinplanung) → Behandlung (Start, Halbzeit-Check) → Abschluss und danach (Ergebnis, Retainer, Abos, Referral).

**Ergänzung 15.10.2026, Anfrage aus der Ferne:** Artikel-Besucher durchlaufen vor dem Erstkontakt die Einstiegsleiter (Checkliste → Smile-Check, Abschnitt 6). Ein Smile-Check wird vom Arzt persönlich per Video beantwortet (Ampel für Aligner, Veneers-Alternative, grober Rahmen für Dauer und Kosten, ggf. Einordnung eines Fremdangebots); danach führt der Weg in den Rückruf und den Erstberatungstermin oder in die Nurturing-Mails. Das Fragenformular des Smile-Checks (u. a. „22 Stunden tragen“) füllt die Veneers-Weiche vorab.

| Schritt in der Erstberatung | Wer |
|---|---|
| 1. Empfang mit Namen | Beraterin |
| 2. Anamnese und Profil | Beraterin |
| 3. Scan, Fotos, Smile Video | Beraterin |
| 4. Warteraum-Pause, max. 5 Min | (Pause) |
| 5. Smile-Simulation | Beraterin |
| 6. Klinische Prüfung, 10 Min | **Alexander** |
| 7. 4-Step-Menü: Unselling, Prescription, Anker, A/B-Fragen, Zahlungsweg, Unterschrift | **Beraterin** (Unselling und Prescription gehen aus Schritt 6 hervor, die Empfehlung kommt von Alexander) |
| 8. Einwilligung, Röntgen planen | Beraterin |

**Grenze kostenlos / danach:** Kostenlos sind Scan, Fotos, Bissanalyse, Kiefergelenk-Check, Smile-Simulation und der 10-Minuten-Check. Nach der Unterschrift folgen Röntgen, Funktionsdiagnostik und Feinplanung. Bedenkzeit bleibt ein Recht des Patienten (kein Nachfassen am selben Tag). Zur Abgrenzung gegenüber dem GOZ-Kostenplan siehe Abschnitt 6, Punkt 6 der Folgen.

**Veneers-Weiche** (Anamnese: „Ist 22 h Tragen ein Problem?“; Klinik: Front mit vielen Füllungen, Abrasionen oder schlechter Farbe?):

| Anamnese 22 h Problem | Klinik mindestens ein Ja | Veneers im Menü |
|---|---|---|
| Ja | egal | Von Anfang an als Anker und Alternative |
| Nein | Ja | Als Anker, Aligner bleibt Empfehlung |
| Nein | alles Nein | Nicht anbieten (Unselling), Premium ist der Anker. Veneers nur auf Patientenwunsch |

**Anpassungen fürs Boutique-Konzept:**
1. Statt Unterschrifts-Rabatt: **echter Startplatz** (Rabatt zieht Rabattjäger an). Ausnahme: 200 € für die Falldokumentation (Gegenleistung des Patienten, keine Unterschriftsprämie).
2. Retainer entschieden: lose 2 pro Kiefer im Plan, fest 599 € pro Kiefer, Premium fest inklusive; danach Retainer-Klub und PZR-Abo.
3. **Vierte Patientenfrage** ergänzen: „Wer begleitet mich?“ (neben wie schön, wie lange, was kostet).
4. Bewertungen: **alle** um eine Bewertung bitten, nicht nur bei fünf positiven Antworten; Unzufriedenes zusätzlich intern nachfassen.
5. „Lass sie nicht entkommen“ bleibt intern; nach außen ruhiger Ton in Sie-Form.
6. Rollen: Die Beraterin (ZFA mit Kommunikationsstärke) führt den gesamten Erstermin inklusive Schritt 7. Du bist in Schritt 6 (klinischer Check, 10 Min) persönlich aktiv; dein Arztanteil bleibt sichtbar (Vorstellung, Freigabe, Empfehlung).
7. Einleitung des Buchs stellt dich als Nicht-Behandler dar → für Überweiser-Positionierung Autorenrolle (Berater) und Praxisrolle (Behandler) trennen.
8. **Erstberatung kostenlos** statt bezahltem Planungstermin (Buch: Ein-Termin-Modell ohne Pause zwischen Diagnostik und Angebot); No-Show-Schutz über Fragebogen, Bestätigung, Erinnerung.
9. **Bedenkzeit als Recht**, nicht als Standardzweig: Abschluss am selben Tag ist das Angebot, nie eine Bedingung.
10. **Anamnese als Entscheidungsbaum:** Die Anamnese ist der Verzweigungspunkt, je nach Antwort wird **ein** passendes Angebot gemacht (siehe Tabelle unten).
11. **Bestandspatienten:** kurzes Anamnese-Update statt 60-Minuten-Termin; Kostenaufklärung schriftlich vor jeder Privatleistung; Anschreiben zum Systemwechsel vorab.

**Entscheidungsbaum in der Anamnese (Entwurf):**

| Antwort | Angebot |
|---|---|
| Zähne schief, früher Spange, Retainer weggelassen | Aligner-Kern (4-Step-Menü) |
| Zähne zu dunkel | Bleaching (Praxis 399 € / Zuhause 299 €) |
| Schnarchen (selbst oder Partner) | Screening, dann Schnarchschiene (799 €) oder Überweisung an Schlafmedizin |
| Knirschen, abgenutzte Kanten | Funktionsschiene (geparkt), ggf. später Formkorrektur |
| Form oder Lücken stören | Formkorrektur (Veneers), Material nach Befund |
| Anderes (Füllungen, Routine) | Empfehlung an Partnerpraxis (Empfehlungsliste ohne Gegenleistung); PZR als Intro-Offer |
| Bei jedem Ergebnis | PZR-Abo und Retainer-Klub als Anschluss |

---

## 11. Vor Livegang klären (Fachanwalt / Zahnärztekammer)

Kurzliste, damit nichts veröffentlicht wird, das später zurückgenommen werden muss:
- **Praxisname:** „Kieferblick“ mit Zusatz „ZAHNBOUTIQUE“ (Zulässigkeit von Name und Zusatz bei der Zahnärztekammer Nordrhein, Markenrecherche Klasse 44, Abgrenzung zu kieferorthopädischen/kieferchirurgischen Fachpraxen)
- Formulierungen ohne Erfolgsversprechen; Vorher-nachher-Nutzung (Patienten vs. Fachkreise), Einwilligungen/Bildrechte. **Neu 08.10.2026:** OLG Frankfurt (06.11.2025, 6 U 40/25) untersagte Vorher-nachher bei medizinisch nicht indizierten Eingriffen auch in Instagram-Storys; Zahnärzte werden im Fachartikel bei ästhetischen Behandlungen genannt, Übertragbarkeit auf Aligner offen
- Preisangaben auf der Website (Orientierung vs. Heil- und Kostenplan), Honorarvereinbarung nach § 2 GOZ für Preisniveau — Mechanismus-Entwurf für den Idealplan liegt vor (Verkaufssheet & GOZ-Kostenvoranschlag), rechtlich noch nicht geprüft; **muss auf drei Pläne angepasst werden**
- Zahlung in Phasen / Vorschuss auf Labor- und Materialkosten; Ratenzahlung mit ausgewiesenen Gesamtkosten
- Zuwendungen/Boni, Zugaben und Rabatte (**neu:** Falldoku-Rabatt 200 €, Referral-Prämie, Anrechnung der Intro-Offers)
- **Neu 13.10.2026:** Werbung mit „Erstberatung im Wert von 300 €“ (Plausibilität des Wertes, GOZ-Basis, Abgrenzung zum Heil- und Kostenplan); **Festpreis-Zusage** (Formulierung, Ausnahmen)
- **Neu 15.10.2026, Smile-Check:** bezahlte Foto-Einschätzung ohne Untersuchung (Fernbehandlung, Berufsrecht; der Akquise-Flowchart v5 hatte Foto-Beurteilung bisher bewusst ausgeschlossen, Kritik von DGKFO und Verbraucherzentrale beachten), Einordnung hochgeladener Fremdangebote, Rückruf- und Telefon-Einwilligung in den Tally-Formularen, Gesundheitsdaten (Fotos, Fragen, PDF) in Tally, „kostenlos“, „Wert 300 €“ und „ohne Verpflichtung“ in den Modulen (§ 7 HWG, Rechtsprechung zu „kostenlos“), Wortlaut der Erstattungs-Zusage („Zusage“ statt „Garantie“), Vergütung einer Video-Beratung (GOÄ-Empfehlung der BZÄK; Beträge nicht belegt)
- Überweiser-Zusammenarbeit ohne Vorteilsgewährung und ohne Tausch (Berufsordnung, § 299a StGB); Empfehlungsliste statt Gegengeschäft; Labore ohne Rabatt-Koppelung
- Übernahme der Patientenkartei / Ansprache von Bestandspatienten
- Datenschutz bei Formularen und Fallpräsentationen
- Kostenlose Erstberatung / kostenlose Erstleistungen (Scan, Simulation) und die Werbung damit
- Preisgespräch und Unterschrift durch die Beraterin (Delegation der wirtschaftlichen Aufklärung; ärztliche Aufklärung bleibt beim Arzt)
- Reihenfolge Unterschrift → Röntgen (rechtfertigende Indikation), Angebot am Erstermin vs. verbindlicher Heil- und Kostenplan nach Feinplanung
- **PZR-Abo und Retainer-Klub:** PZR wird nach GOZ 1040 je Zahn berechnet, Jahresbeitrag muss sich sauber in GOZ-Rechnungen aufschlüsseln lassen; Erstattung durch Zusatzversicherungen läuft über Einzelrechnungen (Einschätzung, klären lassen); Laufzeit und Kündigung transparent; SEPA-Mandat
- **Rückfall-Schutz / Nachkorrektur** als Leistungszusage, nicht als Erfolgsgarantie
- **Bleaching:** Zulässigkeit von Wirkstoffkonzentration und Alter; Delegation der In-Office-Sitzung an Fachpersonal; Vorher-nachher-Werbung
- **Schnarchschiene:** Heilmittelwerberecht bei Werbung zu Schnarchen und Apnoe; Screening-Fragebogen und Überweisungsweg dokumentieren; Aufklärung zu Zahn- und Bissveränderungen
- **Systemwechsel auf rein privat:** schriftliche Kostenaufklärung für Bestandspatienten, Anschreiben, Umgang mit laufenden Kassenbehandlungen, Honorarvereinbarung (§ 2 GOZ) für die Privatleistungen
- **Empfehlung an Partnerpraxen:** nur als Empfehlungsliste ohne Gegenleistung
- **Neu 08.10.2026, Marketing-Agent:** Mails und Briefe an Praxen (Einwilligungen prüfen), Bewertungsanfragen, Empfehlungsprämien, Markenbegriffe wie „Invisalign“ in Anzeigen, KI-generierte Texte (HWG), Gesundheitsdaten in Tests und Formularen, Anzeigen auf Meta und Google im Gesundheitsbereich

---

## 12. Hormozi-Flow: Stand und offene Schritte

**Erledigt:** Avatar · Probleme/Blocker · Bausteine + Priorisierung · Offer · Positionierung · **Money Model + Preise v5** (drei Aligner-Pläne Basis 3.900 € / Ideal 7.900 € / Premium 11.900 €, Erstberatung im Wert von 300 €, Intro-Offers, Festpreis-Zusage, Zahlungsreihenfolge, Retainer-Wahl, PZR-Abo 229 €, Retainer-Klub 249 €/149 €, Kombi 429 €) · **Sales-Baum v1** · Lead-Engine-Überblick (inkl. Bestandskartei-Reihenfolge) · Sales-System aus dem Buch gesichtet · Sales-Ablauf v2 (4-Step-Menü) · **Anamnese als Entscheidungsbaum (Entwurf)** inkl. Veneers-Weiche · Überweiser-Offer (Functional-Netzwerk Ruhr) · Weitere Angebote im Überblick · **4-Felder-Beratungssheet (Entwurf)** und **GOZ-Heil-und-Kostenplan-Mechanik für Idealplan (Entwurf)** (Anpassung an v8 steht aus) · **Name festgelegt: Kieferblick · ZAHNBOUTIQUE** (29.09.2026), Logo-Entwurf liegt vor · Akquise-Funnel (Erkenntnisse, Flowchart v5, Customer Journey ab Nurturing), CRM-Spec, **Marketing-Agent Konzept v1** · **Neu 15.10.2026: digitale Einstiegsleiter für Artikel-Besucher** (Checkliste, Smile-Check 19 €, Ersttermin), Copy der drei Artikel-Module und der Smile-Check-Seite inkl. Video-Skript, Einarbeitung in den Sales-Baum.

**Offen (Reihenfolge-Vorschlag):**
1. **Folgedokumente an v8 anpassen** (neu): Verkaufssheet & GOZ-Kostenvoranschlag, Customer-Journey ab Nurturing, Website-Copy (Gesamtstand und HTML), CRM-Spec, Marketing-Agent Konzept, Akquise-Funnel Erkenntnisse; ungeprüft: Brand Identity v2, Akquise-Flowchart v5, Manuskript. Die Konflikte im Einzelnen stehen im Abgleich vom 13.10.2026 (Pläne, Preise, Non-Prep, Falldoku-Rabatt, Erstberatung gegen GOZ-Kostenplan Block 1, CRM-Felder). **Ergänzt 15.10.:** Customer-Journey (Zweig Checkliste/Smile-Check vor dem Erstkontakt), CRM-Spec (Quellen-Felder Artikel-URL und Smile-Check-Status), Akquise-Flowchart v5 (Foto-Beurteilung jetzt Teil des Angebots) und Marketing-Agent Konzept (Artikel-Vorlage mit drei Modulen) noch einarbeiten.
2. **Erstberatung gegen GOZ-Kostenplan Block 1 abgrenzen** (neu): Welche Posten bleiben kostenlos, was steht nach dem Ja im Kostenplan, kein Doppelansatz. Dazu GOZ-Punktzahlen für 0010, 6000, 8000 prüfen und die geschätzten Beträge der Erstberatung ersetzen.
3. **Ein-Seiter Leistungsumfang** (Refinement-, Planänderungs-, Abbruchregel; Preisrahmen vs. Feinplanung) mit **Festpreis-Zusage** und je Plan (Basis: 1 Set inklusive; Ideal und Premium: im Behandlungsziel inklusive), Compliance-Kopplung über bestehende Checkpoints (Schritt 1/8/16), Abbruchregel als leistungsbezogene Teilabrechnung (Arbeitsannahme, Rechtscheck offen). Ausnahmen der Festpreis-Zusage (Annahme: Wunschänderungen, verlorene Schienen) bestätigen.
4. Wirtschaftlichkeit (Dorl-Konditionen, Kosten pro Fall inkl. Kosten der kostenlosen Erstberatung, Break-even je Angebot, CAC-Deckel für Schnarchschiene, Liquidität; internes Honorar für Refinement-Freigaben und Compliance-Checkpoints je Plan; Marge Ideal bei 60–70 Schienen; **neu:** Kosten Premium (fester Retainer, Material), Falldoku-Rabatt, Retainer-Klub-Materialkosten 25–40 € pro Retainer [Annahme], **Cash am Start nur ca. 480 €**; **neu 15.10.:** Aufwand je Smile-Check-Video gegen 19 € und Wochenkontingent)
5. **Bank:** Auszahlung am Start, Konditionen, Laufzeit (48 Monate bei 9,9 % effektiv ist das Rechenbeispiel)
6. Rechtscheck (Abschnitt 11) — **Rechtsfragenliste an den Fachanwalt** formulieren und früh anstoßen (Woche 1 im Plan); **ergänzt 15.10.** um die Smile-Check-Punkte
7. Delivery & Kapazität (Arzt-/Team-Momente, Vorlagen, Fälle pro Quartal)
8. Test der ersten 10 Fälle (Preis, Botschaft, Abschlussquote je Angebot, Anteil Ideal/Premium/Basis)
9. Bindung & Empfehlung: **Form der Referral-Prämie** offen, Bewertungsanfrage, Preis und Zuschnitt von PZR-Abo/Retainer-Klub/Kombi im Test; Bestandstarif nur PZR als Einstieg (jetzt Intro-Offer 149 €)
10. **Geparkt:** Funktionsschiene als Intro-Offer (Suchvolumen prüfen, Preis gegen Abschlussquote testen), Bündelung „Schiene für die Nacht“
11. Später: Sales-Skript nach dem Baum (Wortlaute, Zahlungsblatt, Nachfass-Texte, KPIs pro Stufe), Kollegen-Charta + Überweisungsformular, Ablauf Functional-Abend, Mini-Offers
12. **Marketing-Agent aufbauen:** 4-Wochen-Plan in Teil B (Zugänge beantragen, DataForSEO, Landingpage mit Lead Magnet, Skills, SEO-Artikel, Ads-Test). **Offen: monatliches Ads-Budget.**
13. **Vision-Optionen (Abschnitt 14):** erst nach den ersten Fällen und stabilen Kennzahlen wieder aufgreifen, kein Aufwand im Aufbau
14. **Neu 15.10.2026, Einstiegsleiter umsetzen:** Checkliste „7 Fragen vor der Unterschrift“ als PDF schreiben; Video (VSL) und Beispiel-Smile-Check (erfundener Fall, beide Wege Aligner und Veneers) aufnehmen; drei Tally-Formulare bauen (Zahlung, Foto- und PDF-Upload, mehrseitiges Formular im Hero, Webhook zu n8n) und Tally-Plan prüfen; Wochenkontingent Smile-Check [Annahme 15] mit Warteliste festlegen; Datenschutz-Text für Fotos und Upload; Qualifikationssatz und Foto von Alexander für die Smile-Check-Seite

*Erledigt gegenüber v7: Retainer-Entscheidung (erster Satz im Kern: ja, 2 lose Schienen pro Kiefer inklusive).*

---

## 13. Entscheidungen dieser Runde (21.09.2026)

- Rein privat, keine GKV-Abrechnung; Bestandskartei als erster Kanal mit kurzem Anamnese-Update.
- Ein kostenloser Erstermin für alle; die Anamnese ist der Entscheidungsbaum.
- Prophylaxe-Mitgliedschaft (eine Stufe) als Rückgrat der Wiederkehr, statt Retainer-Abo und Jahres-Check. *(Überholt durch 13d: PZR-Abo und Retainer-Klub als zwei Angebote.)*
- Bleaching als Intro-Offer: Home-Bleaching mit individueller Schiene plus PZR, In-Office als Option. *(Preise und Zuschnitt überholt durch 13d.)*
- Veneers ohne Stufen, Preisrahmen pro Fall, Preisniveau nach oben angepasst.
- Schnarchschiene bei ca. 700–800 €, ohne GKV-Weg, mit Screening; Funktionsschiene geparkt. *(Preis überholt durch 13d: 799 €.)*
- Regel: Stufen nur, wo der Patient wirklich wählen muss. *(Präzisiert durch 13d.)*
- Vision (B2B, Beratung, Education, Standorte) wird im Projekt festgehalten, der Fokus bleibt der eine Standort.

---

## 13a. Entscheidungen dieser Runde (22.09.2026)

- Aligner-Angebotsarchitektur von vier Stufen (Kompakt/Standard/Umfassend/Fokus-Korrektur) auf **zwei Pläne** reduziert: Idealplan (funktionell) und Ästhetischer Plan (konventionell, Downsell). *(Überholt durch 13d: jetzt drei Pläne.)*
- Preise: Idealplan **7.900 €** (inkl. Gelenksvermessung als Teil der Funktionsdiagnostik), Ästhetischer Plan **3.900 €**. Bewusst unter der Netzwerk-Kollegen-Referenz (10–12 k €), über DTC-Ketten.
- Ersatz-/Stornoregel bewusst **nicht** an FUNCTIONAL-Herstellergebühren (29 €/Ersatz-Aligner, 149 € Storno) angelehnt — passt nicht zur Boutique-Positionierung, bleibt eigenständig zu formulieren.
- Refinement-Kontingent je Plan direkt aus dem FUNCTIONAL-Laborpaket abgeleitet (Korrekturpaket ist bereits im Einkaufspreis der Stufe enthalten); interne Honorarkosten (Arzt-Freigabe, Beraterin-Zeit) separat in der Wirtschaftlichkeitsrechnung zu berücksichtigen.
- Compliance-Kopplung für die Refinement-Zusage über die ohnehin geplanten Kontrollpunkte (Schritt 1/8/16), keine zusätzliche Dauerüberwachung (bewusster Unterschied zu DrSmile/Impress-Modell).

---

## 13b. Entscheidungen dieser Runde (29.09.2026)

- **Name festgelegt: Kieferblick**, Subheader **ZAHNBOUTIQUE** (ersetzt den Arbeitsnamen Alluxea und die Zeile „Zahnmedizin Mülheim“).
- Logo-Entwurf liegt vor (Wortmarke „kieferblick“ klein, Bildzeichen mit Linie sowie Salbei- und Sandfläche, siehe Brand Identity v2, Abschnitt 9).
- Der Ortsbezug Mülheim steht nicht mehr im Logo, sondern in Kicker, Titel, Adresse, Footer und Google-Profil (Annahme, bei Bedarf ändern).
- Weiterhin offen: Markenrecherche, Kammer-Check (Name und Zusatz), Domain und Handles.
- **Money Model v4 bestätigt** (Idealplan ca. 7.900 €, Ästhetischer Plan ca. 3.900 €). Die Startseite-Copy Sektion 9 wurde daran angepasst. Auf der Startseite steht nur der Idealplan-Preis, der Ästhetische Plan wird ohne Preis erwähnt (Annahme, bestätigen). Offen: Preis des Ästhetischen Plans auf der Preisseite zeigen oder nur im Erstermin nennen. *(Website-Anpassung an drei Pläne steht aus, siehe 13d.)*

---

## 13c. Entscheidungen dieser Runde (08.10.2026, Marketing-Agent)

- **Marketing-Agent in Claude Code:** analysiert zuerst, bereitet danach Entwürfe vor. **Der Agent bereitet vor, Alexander gibt frei** (nichts senden, veröffentlichen oder ausgeben ohne Freigabe). Skills nach Aufgabe gegliedert, Kanalwissen in Referenzdateien. Details: Teil B.
- **SEO-Schnittstelle: DataForSEO** (Guthaben, kein Abo). Der Keyword Planner ist nicht der gewählte Weg.
- **B2B-Kanäle:** E-Mail und Brief an eingewilligte NRW-Praxen, LinkedIn mit persönlicher Ansprache, Verweis auf Videos und Konsultationsangebot.
- **B2C skalierbar:** SEO-Wissensartikel in Menge auf WordPress (Annahme aus Alexanders Erfahrung, weicht von der Vorsicht in v6 ab), Google-Ads-Test zuerst, Meta-Test danach, jeweils mit Budgetdeckel.
- **Landingpage in WordPress (Elementor), Formulare mit Tally.** Experiment-Log wird geführt.
- **Betrieb:** zunächst lokal, später optional Strato-VPS. Zeitbudget Alexander anfangs ca. 20 Stunden pro Woche (Annahme). **Ads-Budget offen.**
- **Neuer Rechtshinweis:** Vorher-nachher bis zur Klärung nicht verwenden (OLG Frankfurt, 06.11.2025), betrifft den geplanten Fall-Content.

---

## 13d. Entscheidungen dieser Runde (13.10.2026, Sales-Baum)

Hormozi „4-Step Menu Close“ und „$100M Money Models“ sind in einen durchgängigen Sales-Baum übersetzt (Einstieg, 4-Step-Menü, Bindung nach dem Ja).

- **Erstberatung kostenlos im Wert von 300 €** (3D-Scan 64, Foto- und Bissanalyse 70, Kiefergelenk-Check 75, Ergebnis vorab 91 €; Beträge teils geschätzt). Der Preisbezug (Wert 300 €) darf auch auf der Website erscheinen.
- **Intro-Offers, voll anrechenbar, ohne Frist:** PZR 149 €, Bleaching Praxis 399 €, Bleaching Zuhause 299 €, Schnarchschiene 799 €.
- **Drei Aligner-Pläne** (Regel „Stufen nur, wo gewählt wird“ präzisiert): Basis ca. 3.900 €, Ideal ca. 7.900 €, **Premium 11.900 €**. Premium: Hochleistungs-Attachments, mehrlagiges Material, Premium-Zubehör, Premium-WhatsApp-Hilfe, fester Retainer inklusive.
- **Digitale Kiefergelenk-Vermessung** ist im Ideal- und im Premiumplan enthalten, nicht im Basisplan.
- **Gesprächsablauf:** Unselling → Prescription Ideal → Anker zuerst (Premium oder Veneers) → A/B-Fragen und Zahlung; Basis nur bei Geld-Einwand.
- **Veneers:** Non-Prep gestrichen; Komposit ca. 2.400–4.000 €, Keramik ca. 8.400–12.800 € (Preisrahmen pro Fall); Weiche über Anamnese (22 h Tragen) und Klinik.
- **Festpreis-Zusage** statt weiterer Garantien (Ausnahmen als Annahme: Wunschänderungen, verlorene Schienen). Marge zunächst nachrangig.
- **Zahlungsreihenfolge:** Einmal → Phasen 30/40/30 → Rate über die Bank.
- **Retainer:** lose (2 pro Kiefer) im Plan enthalten, fest 599 € pro Kiefer als Aufpreis.
- **Falldokumentation:** 200 € Rabatt (Ideal 7.700 €).
- **PZR-Abo und Retainer-Klub sind zwei getrennte Angebote:** PZR-Abo 229 € pro Jahr (2 PZR, Ersparnis 69 €); Retainer-Klub 249 € pro Jahr für beide Kiefer (alle 6 Monate neuer herausnehmbarer Retainer pro Kiefer), 149 € für einen Kiefer; **Kombi 429 €**.
- **Referral:** Bewertung erfragen, Empfehlung erfragen (Prämie offen), neuer Fall.
- **Offen:** GOZ-Beträge der Erstberatung prüfen, Abgrenzung zum Kostenplan Block 1, Bank, Ausnahmen der Festpreis-Zusage, Referral-Prämie, Materialkosten Retainer, Anpassung der Folgedokumente (Abschnitt 12, Punkt 1).

---

## 13e. Entscheidungen dieser Runde (15.10.2026, Programmatic SEO und digitale Einstiegsleiter)

Ausgangslage: Alexander will massenhaft Artikel und Landingpages aus einer Artikel-Vorlage für viele Keywords bauen. Die Mehrzahl der Leser sind Patienten aus ganz Deutschland, er ist lokal. Gesucht war ein skalierbares Angebot, das Wert gibt (Hormozi-Stil, Copy nach Jim Edwards, Design wie das vorhandene Artikel-Layout). Frühere Entwürfe (komplexes Modulsystem, Selbsttest, Anrechnung des Smile-Checks) sind verworfen.

- **Drei feste Module auf jeder Artikel-Seite, auch mobil:** Kopf-Box (im Header), Smile-Check-Box (inline, nach der zweiten Überschrift), Schluss (am Ende). Dachzeile: **„Erst Klarheit. Dann entscheiden.“**
- **Digitale Einstiegsleiter:** (1) Checkliste „7 Fragen vor der Unterschrift“, gratis; (2) **Smile-Check, 19 €**; (3) Ersttermin, kostenlos, Wert 300 € mit vier benannten Bestandteilen. Schritte 1 und 3 sind Tally-Formulare (Lead einsammeln, dann Rückruf oder Mail).
- **Smile-Check asynchron:** 5 Handyfotos, 8 Fragen, optional PDF eines Angebots einer anderen Praxis (Baustein statt eigenem Zweitmeinungs-Produkt, kein Preiskampf), persönliches Video von Alexander in 2 Werktagen.
- **Smile-Check offen formuliert:** klärt, ob Aligner das Richtige sind (ehrliche Ampel), ob Veneers eine Alternative sind und warum (oder warum nicht), und gibt eine grobe Einschätzung zu Dauer und Kosten (Rahmen, nur im Video, keine Plan-Preise auf der Website).
- **Smile-Check wird nicht angerechnet.** Risikoumkehr durch Erstattungs-Zusage (kurze Nachricht genügt; keine Antwort in 2 Werktagen ebenfalls). Er ist eine erste Einschätzung, keine Diagnose, und ersetzt den Ersttermin nicht.
- **Eine feste Smile-Check-Seite (/smile-check)** für alle Artikel: Video (VSL) im Hero, Tally-Formular im Hero, drei Hauptnutzen, danach Ablauf, Inhalt des Videos, Beispiel-Smile-Check (erfundener Fall), Alexander, Zusage, FAQ, Schluss.
- **Copy-Prinzip:** Nutzen vor Merkmal, jede Aufzählung „[Merkmal], damit [Nutzen]“ (nach Zusammenfassungen zu Jim Edwards; das Buch selbst ist nicht geprüft). Sie-Form, Marke spricht „Wir“, keine Ausrufezeichen, keine Fristen.
- **Offen:** Checkliste als PDF schreiben; Video und Beispiel-Smile-Check aufnehmen; Tally-Funktionen (Zahlung, Upload, Webhook) im gebuchten Plan prüfen; Wochenkontingent und Warteliste; Datenschutz für Fotos und Upload; Rechtscheck (Abschnitt 11); Einzelwerte der Erstberatung (70/75/91 €) bleiben Schätzungen.
- Texte der Module und der Seite: Teil C. Einordnung im Money Model: Abschnitt 6.

---

## 14. Vision und spätere Optionen (bewusst nicht Fokus)

**Fokus bleibt:** diesen Standort zum besten machen, den es gibt: Patientengewinnung, Delivery und Operations optimieren. Die Optionen unten sind Richtungen, keine Aufgaben für den Aufbau.

**Optionen (nicht priorisiert, Reihenfolge ist keine Rangfolge):**
1. **Buch veröffentlichen** („Die 3x Aligner-Formel“) und damit B2B öffnen, also Praxen als Kunden statt nur Patienten.
2. **Beratung für andere Praxen** (auch als eigenständiges Geschäft, das Beratung allein verkauft).
3. **Education-Business:** Kurse, Trainings, Vorlagen und Checklisten aus dem Buch (Kapitel-Checklisten sind schon vorhanden).
4. **Skalierung über weitere Standorte** mit angestellten Ärzten unter der Dachmarke, oder als **übertragbares Konzept**. Diese Frage steht auch in der Brand Identity (Abschnitt 4, offene Frage) und entscheidet, wie stark die Marke von Alexander gelöst sein muss.

**Warum der Standort zuerst kommt:** Für B2B sind eigene Zahlen, Fälle und Bewertungen aus der Praxis das Beweismaterial. Beratung und Education sind glaubwürdig, wenn sie auf einer laufenden Praxis mit belegten Kennzahlen aufbauen.

**Was schon jetzt zahlt, ohne den Fokus zu verlieren:**
- Kennzahlen sauber tracken (Trichter, Abschlussquote, Kosten pro Neupatient, Umsatz und Gewinn pro Fall, Refinement-Rate).
- Prozesse dokumentieren (Erstermin-Ablauf, Vorlagen, Checklisten), sodass sie übertragbar sind.
- Fälle und Bewertungen sauber sammeln (mit Einwilligungen).
- Functional-Abende und das Netzwerk sind die Keimzelle für spätere Education-Formate.

**Spannungsfelder (zum Merken, noch nicht entscheiden):**
- **Überweiser-Netzwerk vs. Beratung:** Wer Praxen berät, bringt ihnen bei, Aligner-Fälle selbst zu behandeln. Das steht im Gegensatz zum Überweiser-Modell in Abschnitt 8 (Gegenwind: Allgemeinpraxen behalten Aligner-Fälle zunehmend selbst). Beratung eher für Praxen außerhalb des Ruhr-Einzugsgebiets denken.
- **Rolle:** Die Buch-Einleitung stellt dich als Nicht-Behandler dar. Für B2B und für die Praxis sind Autorenrolle (Berater) und Praxisrolle (Behandler) getrennt zu halten (siehe Abschnitt 10, Punkt 7). Ggf. spätere Anpassung des Buchs.
- **Marke und Name:** Name (Kieferblick · ZAHNBOUTIQUE) und Praxisform müssen Skalierung tragen (Markenrecherche, Kammer, Inhaberangabe, BAG/MVZ). Der Subheader ZAHNBOUTIQUE ist der Teil, der bei mehreren Standorten am ehesten zu prüfen ist.
- **Recht:** Berufsrecht und Werbung für Beratung, Haftung bei Beratungsleistungen, Umgang mit Zahlen aus der eigenen Praxis.

**Zeitpunkt zum Wiederaufgreifen (Vorschlag, Bestätigung offen):** nach den ersten 10 Fällen und stabilen Kennzahlen.

---

# TEIL B · Marketing-Agent Konzept (v1, Stand 08.10.2026)

*Arbeitshypothesen, keine Rechtsberatung. Preise und Zugänge der Schnittstellen stammen teils aus Anbieterblogs und sind vor der Nutzung gegenzuprüfen.*

## Ziel und Rahmen

Ein Marketing-Agent in Claude Code, der zuerst analysiert (Keywords, Wettbewerber, Ads-Allokation) und später Entwürfe erstellt (SEO-Artikel, Ads, LinkedIn, Mails). **Der Agent bereitet vor, Alexander gibt frei.** Er veröffentlicht, versendet und gibt kein Geld aus, ohne ausdrückliche Freigabe.

- **Ressourcen:** Alexander hat anfangs ca. 20 Stunden pro Woche für Aufbau und Optimierung des Agent (Annahme). Das monatliche Ads-Budget ist offen.
- **Kontext für Claude Code:** dieses Dokument als `CLAUDE.md` plus Ordner `kontext/`, `daten/`, `material/` und `experiment-log.md`.

## Kanalstrategie

**B2B (Eingang C, Functional-Netzwerk Ruhr)**
- E-Mail und Brief an die Liste eingewilligter Zahnarztpraxen in NRW (Einwilligung laut Alexander vorhanden).
- LinkedIn: persönliche Ansprache, Verweis auf Videos, Konsultation anbieten. Der Agent entwirft Posts, Kommentare, Kontaktanfragen und Mails, Alexander sendet.
- Rahmen: keine Vorteilsgewährung, kein Tausch (§ 299a StGB, siehe Teil A, Abschnitt 8 und 11).

**B2C, Fundament (nicht skalierbar, hohe Wirkung):** Bestandskartei, Google-Profil mit Bewertungen, Empfehlungen, Überweiser.

**B2C, skalierbar (Agent-tauglich):**
1. **SEO-Wissensartikel auf WordPress in großer Menge** (Longtail und viel gesuchte Keywords). Grundlage ist Alexanders Erfahrung (Annahme). Weicht von der bisherigen Vorsicht ab (wenige hundert tiefe Seiten statt tausender Artikel). Daher pro Artikel: Autor Alexander, echte Fakten oder Fälle, HWG-Check. **Jeder Artikel trägt die drei festen Module aus Teil C.**
2. **Google Ads** (Search) als erster Paid-Test, Ruhr-Umkreis statt nur Mülheim, fester Budgetdeckel. Das Volumen ist der Engpass, nicht der Preis (siehe Teil D).
3. **Meta Ads** (Instagram und Facebook, ein Anzeigenkonto) als zweiter Paid-Test. Meta schränkt Gesundheitswerbung ein: keine „Sie haben …“-Ansprache, keine Vorher-nachher-Bilder, keine Ergebnisversprechen, Landingpage wird mitgeprüft (Quelle ist ein Tracking-Anbieter, gegen Metas Richtlinien prüfen).
4. **Mail-Serie an Leads und Bestand** über n8n und Brevo.

**Später / geparkt:** Instagram organisch (erst mit Fällen), YouTube, lokale Partner, Jameda, Funktionsschiene.

## Skills (nach Aufgabe gegliedert)

Kanalwissen (Google, Meta, LinkedIn, HWG) liegt als Referenzdatei im jeweiligen Skill, nicht in eigenen Kanal-Skills.

| Bereich | Skills |
|---|---|
| Analyse | keyword-research, competitor-analysis, ads-allocation |
| Ads | ad-writing (Referenzen Google, Meta, HWG), ads-optimizing (Daten lesen, berichten, Vorschlag), ab-test-planning mit Experiment-Log |
| Content | seo-article-draft, linkedin-post, comment-draft, connection-request-draft, email-outreach-draft |
| Qualität | compliance-check als Subagent mit eigenem Kontext, prüft jeden Text gegen HWG und Markenton |
| Reporting | weekly-report aus den CRM-Kennzahlen |

**Aufbauregeln (Anthropic-Doku):** Beschreibung nennt Zweck und Auslöser; SKILL.md unter 500 Zeilen, Details in Zusatzdateien, nur eine Ebene tief verlinkt; feste Abläufe als Skript, Strategie und Texte als Anweisung; vor dem Bau mindestens drei Testfälle; klein anfangen (Recherche als CSV, dann Auswertung, dann Entwurf).

**Experiment-Log:** Jeder Test mit Hypothese, Variante, Budget, Ergebnis (Kennzahlen ① bis ⑥, siehe Teil E), Entscheidung und Rechtscheck, damit neue Varianten auf Ergebnissen aufbauen.

## Schnittstellen

| Zweck | Wahl / Stand |
|---|---|
| Keyword- und SERP-Daten | **DataForSEO (gewählt):** Guthaben ab 50 $, kein Abo, Abfragen für Standort Mülheim/Ruhr. Preise pro Abfrage auf der Produktseite prüfen; Local-Pack/Maps-Daten unklar. Google Keyword Planner nicht als Weg gewählt |
| Eigene Seite | Search Console, Google Analytics (nach meiner Kenntnis kostenlos) |
| Google Ads | Google Ads API mit Developer Token (Freigabe dauerte laut Blog 2+ Wochen). Offizieller MCP nur lesend, Schreiben über Drittanbieter oder eigenes Skript |
| Meta Ads | Meta Marketing API, offizieller Ads-MCP in Open Beta (Stand April 2026, Blogangabe). Schreibzugriff löst echte Ausgaben aus, zuerst nur lesen |
| Google-Profil | Business Profile API, Zugang per Antrag (Geschäftsgrund, Cloud-Projekt, Website) |
| WordPress | eingebaute Schnittstelle (nach meiner Kenntnis), Artikel als Entwurf anlegen |
| LinkedIn | Posten auf persönlichem Profil ohne Prüfung möglich (App an Unternehmensseite koppeln). Eigene Posts und Kommentare lesen nicht möglich, keine Zeitplanung, Token läuft nach 60 Tagen ab. Themenradar daher über Webquellen |
| CRM, Mail, Ablauf, Formulare | Baserow, Brevo, n8n, Tally (siehe Teil E) |
| Semrush | für den Start zu teuer (API-Tarif ca. 549 $/Monat plus Einheiten) |

## Betrieb

- Zunächst lokal entwickeln. Danach optional Linux-VPS bei Strato (z. B. VPS M, 2 Kerne, 4 GB, ca. 10 €/Monat, Root-Zugriff, keine Backups im Tarif). Normales Webhosting vermutlich nicht geeignet (nicht geprüft).
- Claude Code läuft ohne Oberfläche per `claude -p`, im Skript-Modus mit API-Schlüssel statt Abo-Login (zusätzliche Nutzungskosten). Berechtigungen per Freigabeliste, nicht Erlaubtes wird abgelehnt.
- Alternative ohne eigenen Server: geplante Aufgaben in Claude (Verfügbarkeit im Plan prüfen).
- Landingpages in WordPress (Elementor), schlank und ohne Navigation für Anzeigen, Formulare mit Tally (Webhook-Fähigkeit im Plan offen).

## Weitere Bausteine

Messung (Conversion-Tracking, Cookie-Banner mit Einwilligung, Pflichtfrage zur Quelle, Kennzahlen aus dem CRM) · Freigabe-Ablauf (Entwurf, Rechtscheck, Freigabe, Veröffentlichung) · Landingpage mit Lead Magnet und Rückrufkette · Schutzgeländer (Budgetdeckel pro Kanal, Schreibzugriff auf Ads erst nach Testphase) · Stilmaterial von Alexander (LinkedIn-Posts, Texte, Videos, Fälle mit Einwilligung).

## 4-Wochen-Plan (Annahmen: 20 Std./Woche, Budget offen, Mengen sind Richtwerte)

- **Woche 1, Fundament und Wartezeiten:** Rechtsfragenliste an den Fachanwalt; Zugänge beantragen (Google Ads, Meta Ads, Business Profile), DataForSEO-Konto; Messung (Cookie-Banner, Quellenfrage, Search Console, Analytics); Agent lokal aufsetzen.
- **Woche 2, Daten und Landingpage:** DataForSEO anbinden, Skills keyword-research und competitor-analysis; Landingpage mit Lead Magnet (Endpreis-Ratgeber), Tally-Formular, Rückrufkette; Bestandskartei-Anschreiben vorbereiten (Versand nach Rechtscheck).
- **Woche 3, Content und B2B:** seo-article-draft und compliance-check, Entwürfe mit Freigabe; LinkedIn-Entwürfe, E-Mail und Brief an die NRW-Praxen; Google-Profil einrichten, Bewertungsablauf festlegen.
- **Woche 4, Ads-Test:** ads-allocation und ad-writing; Google Ads zuerst, dann Meta, jeweils mit Deckel und nur wenn Landingpage und Tracking stehen; erste Auswertung im Experiment-Log, Wochenbericht, Entscheidung über Budget und nächste Tests.
- **Danach:** Strato-VPS für den Dauerbetrieb, Instagram organisch und Fachabend sobald Fälle vorliegen.

## Rechtliche Leitplanken (Auszug, Details in Teil A Abschnitt 11 und Teil D)

- **Vorher-nachher:** Das OLG Frankfurt (06.11.2025, 6 U 40/25) hat sie bei medizinisch nicht indizierten Eingriffen auch in Instagram-Storys untersagt. Der Fachartikel nennt Zahnärzte bei ästhetischen Behandlungen, die Übertragbarkeit auf Aligner ist offen. Bis zur Klärung nicht verwenden. Das betrifft den geplanten Fall-Content.
- Kostenloser Erstermin (§ 7 HWG), Bewertungsanfragen, Empfehlungsprämien, Markenbegriffe wie „Invisalign“, KI-generierte Texte (HWG): Fachanwalt klären.
- Mails an Praxen nur an Einwilligungen.

## Offene Punkte

- [ ] Monatliches Ads-Budget festlegen
- [ ] Rechtsfragenliste an Fachanwalt formulieren und senden
- [ ] Zugänge beantragen (Google Ads, Meta Ads, Business Profile), DataForSEO-Konto anlegen
- [ ] Preise pro Abfrage bei DataForSEO und Local-Pack-Daten prüfen
- [ ] Tally-Plan: Webhooks möglich?
- [ ] Skills bauen und je mindestens drei Testfälle schreiben
- [ ] Ob SEO-Artikel in Menge tragen: nach den ersten Artikeln in Search Console beobachten (Experiment-Log)

## Quellen (aus dem Konzept)

Anthropic Skill Best Practices (platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) · Claude Code programmatisch ausführen (code.claude.com/docs/en/headless) · Coupler.io „Claude Code for Marketing“ · Marketing-Skills-Sammlung (github.com/mysticaltech/marketingskills) · Ryan Doser „Claude Code Marketing Agents“ · Meta Ads MCP Guide · Google Ads MCP mit Claude Code · Meta: sensible Kategorien (wetracked.io) · IWW: Vorher-nachher-Urteil · DataForSEO Preise und MCP (contextbolt.com) · Semrush API Preise · Google Business Profile APIs (developers.google.com/my-business) · LinkedIn API Zugang · STRATO vServer.
Hinweis: Die Praxisbeispiele zu Marketing-Skills stammen aus Blogs und Open-Source-Sammlungen, nur die Aufbauregeln aus der Anthropic-Doku. Mehrere Schnittstellen-Angaben stammen von Anbietern mit eigenem Interesse.

---

# TEIL C · Texte und Stimme

*Quellen: Website_Copy_Gesamtstand_v2 (Stand 15.10.2026) und Brand_Identity_v2 (29.09.2026). Platzhalter in [eckigen Klammern]. Klinische Aussagen prüft Alexander. Rechtscheck (Fachanwalt) steht für alle Seiten aus.*

## C1. Entscheidungen, die in allen Texten stecken (Website-Copy v2, Abschnitt A)

- **Rein private Praxis.** Keine Aussagen zu Kasse, Erstattung oder Zusatzversicherung. Falls nötig, ein Satz: „Wir sind eine reine Privatpraxis.“
- **Umgang mit Geld (Mittelweg, entschieden 14.10.):**
  - **Intro-Offer-Preise stehen auf der Website:** Professionelle Zahnreinigung 149 €, Bleaching in der Praxis 399 €, Bleaching für zu Hause 299 €, Schnarchschiene 799 €. Jeweils mit dem Satz, dass der Betrag bei späterer Behandlung voll angerechnet wird, ohne Frist.
  - **Der Smile-Check (19 €) steht ebenfalls auf der Website, wird aber nicht angerechnet.** Erlaubte Zahlen in den Artikel-Modulen: 19 €, 2 Werktage, 5 Fotos, 8 Fragen, 7 Fragen (Checkliste), ca. 60 Minuten, Wert 300 € mit den vier Einzelwerten.
  - **Plan-Preise (Basis, Ideal, Premium), „ab“-Beträge und konkrete Raten stehen nicht auf der Website.** Sie kommen im Erstgespräch. Auch die grobe Kosteneinschätzung im Smile-Check steht nur im Video, nicht auf der Seite.
  - **Ablauf und Rate werden genannt:** Festpreis schriftlich im Erstgespräch, Ratenzahlung möglich, Guthaben schon abgezogen.
  - **Endpreis-Ratgeber als PDF (Lead Magnet)** [noch zu erstellen]. Daneben die Checkliste „7 Fragen vor der Unterschrift“ als Lead Magnet für die Artikel.
  - Kein Navigationspunkt „Preise“.
- **Festpreis-Zusage.** Der Preis im Plan bleibt bis zum Ende der Behandlung gleich, inklusive üblicher Nachkorrektur. Ausnahmen: nachträglich geänderte Wünsche, verlorene Schienen [Ausnahmen bestätigen]. Immer „Zusage“, nie „Garantie“.
- **Guthaben statt Rabatt.** Wörter: „Guthaben“, „anrechnen“. Nicht: „Rabatt“, „Aktion“, „Gutschein“. Die Falldokumentation (200 € Guthaben) steht **nicht** auf der Website, sie wird nur im Gespräch angeboten. **Ausnahme: Der Smile-Check wird nicht angerechnet** (bei ihm ersetzt die Erstattungs-Zusage die Anrechnung).
- **Anrede und Stimme.** Sie-Form. Die Praxis spricht „Wir“. Alexander Andreev in dritter Person, ausgenommen ein freigegebenes Zitat (im Smile-Check-Video spricht er selbst).
- **Ton.** Ruhig, direkt, ehrlich über Nachteile. Keine Ausrufezeichen, keine Dringlichkeit, keine Superlative, kein „garantiert“, kein „Luxus“. „diskret“ statt „unsichtbar“.
- **Kein Wirkversprechen.** Zusagen statt Garantie. Besonders bei Schnarchen, Knirschen, Ästhetik (Heilmittelwerbegesetz). Der Smile-Check ist „eine erste Einschätzung, keine Diagnose“.
- **Keine Namen von Wettbewerbern.**
- **Funktionsschiene und Schnarchschiene sind zwei verschiedene Produkte.**
- **Reihenfolge der Behandlung:** Funktion, Stellung, Farbe, Form.
- **Beweise nur mit echten Belegen.** Fälle, Vorher/Nachher, Zitate und Sterne nur mit Einwilligung und nach Rechtscheck (Vorher/Nachher: OLG Frankfurt 06.11.2025, Übertragbarkeit offen). Der Beispiel-Smile-Check ist ein erfundener Fall und wird als solcher gekennzeichnet.
- **Drei Pläne, nur zwei sichtbar im Gespräch.** Premium zuerst, Ideal als Empfehlung, Basis nur als Downsell bei Geld-Einwand. Plan-Namen stehen nicht auf der Website.
- **Entscheidung vor Ort ist normal.** Ein Satz am Ende von „Ihr erster Schritt“: Sie können im Erstgespräch starten oder den Plan mitnehmen. Beides ist in Ordnung.
- **Artikel-Vorlage mit drei festen Modulen** (Kopf-Box, Smile-Check-Box, Schluss) auf allen programmatischen SEO-Seiten, auch mobil. Copy-Prinzip (Jim Edwards, nach Zusammenfassungen, Buch nicht geprüft): Nutzen vor Merkmal, jede Aufzählung als **[Merkmal], damit [Nutzen]**, ein klarer nächster Schritt je Fläche. Roter Faden: **„Erst Klarheit. Dann entscheiden.“**

**Geteilte Bausteine (Auszug):**
- **Baustein Guthaben:** „Was Sie vorab bei uns machen lassen, rechnen wir voll auf Ihre Behandlung an. Ohne Frist.“ (gilt nicht für den Smile-Check)
- **Baustein Festpreis-Zusage:** „Der Preis in Ihrem Plan bleibt bis zum Ende der Behandlung gleich, inklusive üblicher Nachkorrektur.“
- **Baustein Entscheidung vor Ort:** „Sie können gleich im Erstgespräch starten, wenn Sie möchten. Oder Sie nehmen Ihren Plan mit nach Hause. Beides ist in Ordnung.“
- **Baustein Smile-Check-Zusage:** „Hat Ihnen der Smile-Check nichts gebracht, genügt eine kurze Nachricht, und Sie erhalten die 19 € zurück. Kommt Ihre Antwort nicht in 2 Werktagen, ebenfalls.“ [Wortlaut Rechtscheck]
- **Baustein Smile-Check-Hinweis:** „Eine erste Einschätzung, keine Diagnose. Den Befund erheben wir im Ersttermin.“
- **Mitgliedschaft (Kurzwortlaut):** „Mit dem PZR-Abo haben Sie zwei Zahnreinigungen im Jahr, bei denen wir auch Biss und Schiene prüfen. Mit dem Retainer-Klub bekommen Sie alle sechs Monate einen neuen herausnehmbaren Retainer.“

**Drei Tally-Formulare für alle Artikel:** **Checkliste** (Vorname, E-Mail, optional Telefon mit eigener Einwilligung), **Smile-Check** (acht Fragen, fünf Fotos, optional Angebot als PDF, Zahlung), **Ersttermin anfragen** (Rückruf). In jedem ein verstecktes Feld mit der Seiten-Adresse des Artikels. Die Smile-Check-Frage 1 deckt die Veneers-Weiche ab (22 Stunden tragen).

**Sitemap (Auszug):** /smile-check (neu), /wissen/… (Artikel-Vorlage, neu), /mitgliedschaft (PZR-Abo, Retainer-Klub, Kombi), /zusagen, /erstermin, /aligner, /bleaching-zahnreinigung, /veneers (live erst mit Labor und Fällen), /schnarchschiene, /funktionsschiene (Produkt geparkt), /unsere-idee. **Links:** Alle SEO-Artikel führen zu Smile-Check, Checkliste und Ersttermin. Ein Link auf eine noch nicht live Seite wird ausgeblendet. Die Veneers-Seite ist nicht aus dem Smile-Check verlinkt, solange sie nicht live ist.

## C2. SEO-Artikel-Vorlage: drei feste Module (Website-Copy v2, Abschnitt 11)

Auf jeder programmatischen Artikel-Seite, gleich für alle Keywords, auch mobil. Die Fakten-Zeilen der Kopf-Box (Ursache, Behandlung, Dauer) bleiben je Seite; die Zeile **Kosten** ist fest: *Rahmen vorab im Smile-Check, Festpreis im Ersttermin.* Gibt es weniger als drei Überschriften, entfällt Modul 2.

| Modul | Wo | Zweck |
| --- | --- | --- |
| 1 · Kopf-Box | im Header (Desktop rechts in „Auf einen Blick“, mobil direkt unter dem Lead) | Treppe zeigen, ein Button |
| 2 · Smile-Check-Box | inline, nach der zweiten Überschrift | Hauptangebot |
| 3 · Schluss | am Ende, vor den Quellen | drei Wege, Ersttermin mit Bestandteilen, P.S. |

### Modul 1 · Kopf-Box

> **Erst Klarheit. Dann entscheiden.**
> Drei Schritte, jeder für sich nützlich. Sie bestimmen, wie weit Sie gehen.
>
> **1 · Checkliste: 7 Fragen vor der Unterschrift** · gratis
> So zahlen Sie am Ende nur, was vereinbart war, und stehen danach nicht allein da.
>
> **2 · Smile-Check** · 19 €
> Sie wissen in 2 Werktagen, welcher Weg zu Ihnen passt und womit Sie bei Dauer und Kosten rechnen müssen.
>
> **3 · Ersttermin** · kostenlos, Wert 300 €
> Sie gehen mit Ihrem Ergebnis auf dem Bildschirm und Ihrem Festpreis schriftlich nach Hause.
>
> [ **Checkliste laden** ]
> *Gratis · als PDF per E-Mail*

### Modul 2 · Smile-Check-Box (inline)

> SMILE-CHECK · 19 €
>
> **Aligner, Veneers oder nichts davon? In 2 Werktagen wissen Sie, welcher Weg zu Ihnen passt.**
>
> Dieser Artikel erklärt, wie es im Allgemeinen ist. Ihre Zähne sind aber Ihre. Darum sieht sich Alexander Andreev Ihren Fall persönlich an und sagt Ihnen offen, was zu Ihnen passt, ohne Termin und ohne Anreise.
>
> Sie senden fünf Handyfotos (mit Anleitung) und beantworten acht Fragen, etwa fünf Minuten. Bis übermorgen bekommen Sie ein persönliches Video:
>
> – **Ob Aligner das Richtige für Sie sind,** ehrlich als Ampel (sinnvoll, mit Einschränkung oder eher nicht), damit Sie keine Zeit und kein Geld in den falschen Weg stecken.
> – **Ob Veneers eine Alternative sind, und warum (oder warum nicht),** damit Sie vergleichen können, was zu Ihrem Wunsch und Ihrem Alltag passt.
> – **Eine grobe Einschätzung zu Dauer und Kosten Ihres Weges,** damit Sie nicht erst im Beratungsgespräch erfahren, womit Sie rechnen müssen.
> – **Eine Einordnung Ihres Angebots, wenn Sie schon eins haben** (PDF hochladen), damit Sie sehen, was darin steht und was fehlt.
>
> [ Beispiel ansehen: So sieht ein Smile-Check aus ] *(Beispielfall, keine echte Patientin)*
>
> **19 €. Hat Ihnen der Smile-Check nichts gebracht, genügt eine kurze Nachricht, und Sie erhalten die 19 € zurück.** Kommt Ihre Antwort nicht in 2 Werktagen, ebenfalls.
>
> [ **Smile-Check starten · 19 €** ]
> *Eine erste Einschätzung, keine Diagnose. Den Befund erheben wir im Ersttermin.*

**Alternativ-Überschriften zum Testen (Text darunter bleibt gleich):**
- *Wissen, ob es bei Ihnen klappt, bevor Sie einen Termin machen.*
- *Nicht jeder Fall braucht Aligner. Ob Ihrer einen braucht, sagen wir Ihnen ehrlich.*
- *Aligner, Veneers oder etwas ganz anderes? Sie bekommen eine ehrliche Antwort, mit Begründung.*

### Modul 3 · Schluss

> **Wie weit Sie gehen, entscheiden Sie.**
>
> **Checkliste** · gratis
> Die 7 Fragen, die Sie jeder Praxis stellen sollten, damit Sie am Ende nur zahlen, was vereinbart war. [ Checkliste laden ]
>
> **Smile-Check** · 19 €
> Ihre persönliche Antwort in 2 Werktagen, damit Sie wissen, welcher Weg zu Ihnen passt: Aligner, Veneers oder keiner von beiden. [ Smile-Check starten ]
>
> **Ersttermin** · für Sie kostenlos, Wert 300 €
> Etwa 60 Minuten vor Ort. Das ist drin:
> – **3D-Scan** · 64 €
> Angenehm und in Minuten, ohne Abdruckmasse. Ihr Plan baut auf genauen Daten statt auf Schätzungen.
> – **Foto- und Bissanalyse** · 70 €
> Wir behandeln die Ursache, nicht nur die Optik, damit Ihr Ergebnis länger hält.
> – **Kiefergelenk-Check** · 75 €
> Sie wissen vorher, ob etwas die Behandlung stören könnte, und erleben später keine Überraschung.
> – **Ihr Ergebnis vorab** · 91 €
> Untersuchung, Smile-Simulation und 10 Minuten mit Alexander Andreev. Sie sehen, wie Ihr Lächeln werden kann, und erfahren ehrlich, welcher Weg zu Ihnen passt.
> **Zusammen 300 €. Für Sie kostenlos.** Dazu bekommen Sie Ihren Festpreis schriftlich.
> [ Ersttermin anfragen ]
>
> *Sie können gleich im Ersttermin starten, wenn Sie möchten. Oder Sie nehmen Ihren Plan mit nach Hause. Beides ist in Ordnung.*
>
> **P.S.** *Zwei Fragen schützen Sie bei jeder Praxis: Was kostet es am Ende, schriftlich? Und wer ist nach der Behandlung noch für mich da? Alle sieben Fragen stehen in der Checkliste, gratis. Haben Sie schon ein Angebot, schicken Sie es mit dem Smile-Check, wir zeigen, was darin steht und was fehlt.*

## C3. Smile-Check-Seite /smile-check (Website-Copy v2, Abschnitt 12)

Eine feste Seite für alle Artikel; Ziel der Buttons „Smile-Check starten“ und „Beispiel ansehen“. Hero: Video (VSL) und Tally-Formular, dazu die drei Hauptnutzen. Mobil: Überschrift, Video, 3 Nutzen, Formular, dann der Rest.

**12.1 Hero.** Kicker: SMILE-CHECK · 19 €. H1: *Aligner, Veneers oder nichts davon? In 2 Werktagen wissen Sie, welcher Weg zu Ihnen passt.* Sub: *Fünf Handyfotos, acht Fragen. Alexander Andreev sieht sich Ihren Fall persönlich an und antwortet Ihnen im Video. Ohne Termin, ohne Anreise.* Video (VSL, ca. 90 Sek.), Titel: *Alexander Andreev erklärt in 90 Sekunden, was Sie bekommen.*

Drei Hauptnutzen:
1. **Ob Aligner das Richtige für Sie sind.** Ehrlich als Ampel, damit Sie keine Zeit und kein Geld in den falschen Weg stecken.
2. **Ob Veneers eine Alternative sind, und warum.** Damit Sie vergleichen können, was zu Ihrem Wunsch und Ihrem Alltag passt.
3. **Womit Sie bei Dauer und Kosten rechnen müssen.** Eine grobe Einschätzung vorab, damit es im Gespräch keine Überraschung gibt.

Formular-Box (Tally, erste Seite im Hero): *Smile-Check starten · 19 €* · Vorname · E-Mail · „Was stört Sie an Ihrem Lächeln?“ (freies Feld, 1 Zeile) · [ **Weiter zu den Fotos** ] · *Zahlung erst am Ende. Hat Ihnen der Smile-Check nichts gebracht, erhalten Sie die 19 € zurück.* Vertrauenszeile: Persönlich von Alexander Andreev · Antwort in 2 Werktagen · Rückerstattung auf Nachricht.

**12.2 So läuft es ab.** Überschrift: *Fünf Minuten für Sie. Die Antwort kommt von uns.* (1) Sie beantworten acht Fragen und laden fünf Handyfotos hoch (Anleitung zeigt jeden Winkel). (2) Alexander Andreev sieht sich Ihren Fall an, persönlich, nicht automatisch. (3) Sie bekommen Ihr Video, bis übermorgen per E-Mail.

**12.3 Das bekommen Sie im Video.** Überschrift: *Vier Antworten, die Sie sonst erst nach einem Termin bekämen.* Aligner: ja, mit Einschränkung oder eher nicht (mit Begründung). Veneers als Alternative, und warum (oder warum nicht). Dauer und Kosten als grober Rahmen mit Zahlungsbeispiel (Festpreis schriftlich im Ersttermin). Einordnung eines vorhandenen Angebots (PDF). Hinweis: *Eine erste Einschätzung, keine Diagnose. Den Befund erheben wir im Ersttermin.*

**12.4 Beispiel.** Überschrift: *So sieht ein Smile-Check aus.* Text: *Ein Beispielfall, keine echte Patientin: ihre Fotos, ihre Fragen, die Antwort im Video. Schauen Sie sich an, was bei Ihnen ankommt, bevor Sie etwas bezahlen.* [Video: Beispiel-Smile-Check, erfundener Fall]

**12.5 Wer Sie begleitet.** Überschrift: *Die Antwort kommt von Alexander Andreev.* Text: *Alexander Andreev ist Zahnarzt und führt die Kieferblick Zahnboutique in Mülheim an der Ruhr. Er sieht sich jeden Smile-Check selbst an. Wenn Aligner nicht passen, sagt er das. Wenn Sie keine Behandlung brauchen, auch.* [Foto, 1 Satz zur Qualifikation]

**12.6 Die Zusage.** Überschrift: *Wenn es Ihnen nichts bringt, zahlen Sie nichts.* Text: *Hat Ihnen der Smile-Check nichts gebracht, genügt eine kurze Nachricht, und Sie erhalten die 19 € zurück. Kommt Ihre Antwort nicht in 2 Werktagen, ebenfalls. Fragen dazu stellen wir Ihnen nicht.*

**12.7 FAQ.** Ersetzt der Smile-Check einen Termin? Nein, er sagt, ob sich ein Termin lohnt; den Befund erheben wir vor Ort. · Werden die 19 € angerechnet? Nein, dafür die Zusage oben. · Muss ich danach etwas buchen? Nein. · Was passiert mit meinen Fotos? [Datenschutz-Text prüfen: Zweck, wer sieht sie, Löschfrist, Einwilligung] · Reichen Handyfotos? Ja, mit Anleitung; fehlt etwas, melden wir uns. · Ich habe schon ein Angebot einer anderen Praxis: als PDF hochladen, wir ordnen es ein. · Ich wohne nicht in Mülheim: der Smile-Check läuft komplett online.

**12.8 Schluss.** Überschrift: *Erst Klarheit. Dann entscheiden.* Text: *Wenn Sie lieber zuerst etwas lesen: Die Checkliste mit den 7 Fragen vor der Unterschrift ist gratis. Wenn Sie lieber gleich vor Ort starten: Der Ersttermin ist für Sie kostenlos, Wert 300 €.* Buttons: Smile-Check starten · 19 € / Checkliste laden / Ersttermin anfragen.

**12.9 Video-Skript (Vorschlag, ca. 90 Sek., Alexander in der Ich-Form).** (1) Hook: „Sie überlegen, ob Aligner das Richtige für Sie sind. Oder ob es etwas anderes sein sollte. Und Sie wollen wissen, was auf Sie zukommt.“ (2) Problem: „Die meisten erfahren das erst nach einem Termin, und dann liegt oft schon ein Angebot auf dem Tisch.“ (3) Lösung: „Im Smile-Check senden Sie mir fünf Fotos und beantworten acht Fragen. Ich sehe mir Ihren Fall persönlich an.“ (4) Inhalt: „Sie bekommen von mir ein Video: ob Aligner bei Ihnen Sinn machen, ob Veneers eine Alternative sind und warum, und womit Sie bei Dauer und Kosten rechnen müssen. Haben Sie schon ein Angebot, schauen wir uns das auch an.“ (5) Risikoumkehr: „Es kostet 19 Euro. Bringt es Ihnen nichts, schreiben Sie mir kurz und Sie bekommen das Geld zurück.“ (6) CTA: „Starten Sie gleich neben diesem Video. Ich freue mich auf Ihre Fotos.“

## C4. Marke, Sprache, Design (Brand Identity v2)

**Markenpersönlichkeit:** ruhig, präzise, persönlich. Archetyp: der kompetente Begleiter (nicht Verführer, nicht Techniker). Die Marke ist nicht: laut, rabattig, klinisch, luxuriös im Wortsinn.

**Name und Architektur:** **Kieferblick** · ZAHNBOUTIQUE (Versalien, gesperrt), darunter „Behandlung durch Alexander Andreev“. Im Logo klein („kieferblick“), im Fließtext „Kieferblick“. Ortsangabe Mülheim steht in Adresse, Footer, Google-Profil, SEO-Texten. Offene Prüfungen: Markenrecherche Klasse 44, Zahnärztekammer Nordrhein (Name und Zusatz), Domain und Handles.

**Kernbotschaft:** Intern: Ich plane und begleite Ihre Zahnstellung persönlich, vom ersten Scan bis zum Retainer, mit klaren Preisen und klaren Zusagen. Extern: *Ein Arzt. Ein Plan. Bis zum Retainer.* Haltungssatz: *Zähne bewegen sich ein Leben lang. Ich begleite sie.* Nicht verwenden: „Damit es diesmal hält“ (klingt nach Versprechen). Drei Belege: Persönlich (Befund, Plan und Freigabe macht Alexander selbst), Klar (Endpreis, Leistungsumfang, Ausschlüsse vorab auf einer Seite), Durchgehend (Betreuung bis zum Retainer und darüber hinaus).

**Fünf Sprachprinzipien:** (1) Klar statt blumig: eine Aussage pro Satz, Zahlen statt Adjektive. (2) Ehrlich statt glatt: Nachteile und Grenzen selbst nennen (Attachments, Lispeln am Anfang, Retainer). (3) Ruhig statt laut: keine Ausrufezeichen, keine Dringlichkeit, kein Druck. (4) Persönlich statt Firma: Ich-Form des Arztes, Sie-Form für Patienten, feste Ansprechperson. (5) Hochwertig durch Zurückhaltung: Das Wort „Luxus“ kommt nicht vor.

| Wir sagen | Wir sagen nicht |
|---|---|
| Plan, Weg, begleiten | Traumlächeln, Hollywood, Wow-Effekt |
| diskret | unsichtbar |
| Endpreis, Umfang, enthalten / nicht enthalten | ab-Preis, Aktion, Rabatt |
| Zusage | Garantie, Rundum-sorglos |
| realistisch | perfekt, garantiert |
| Ihre Zahnstellung | Ihr neues Ich |
| Ich zeige Ihnen … | Wir bieten Ihnen … |

Ton: eher förmlich mit Wärme, sachlich mit einem Satz Empathie, zurückhaltend mit klarer Haltung. **Test für jeden Text:** Würde ein souveräner Arzt das so zu einer neuen Patientin sagen? „Boutique“ meint klein, persönlich, überschaubar, nicht luxuriös.

**Musterformulierungen:** Ehrlich über Nachteile: *„In den ersten Tagen spüren Sie Druck und sprechen vielleicht etwas anders. Das legt sich meist nach einer Woche.“* · Bei Zögern: *„Nehmen Sie sich Zeit. Sie dürfen den Plan auch bei einem Kollegen prüfen lassen.“* · Erste Nachricht nach Anfrage: *„Guten Tag Frau …, hier ist Kieferblick. Ich melde mich heute noch kurz bei Ihnen.“* · Antwort auf Bewertung: *„Vielen Dank für Ihre Rückmeldung. Dass Sie sich während der Behandlung gut begleitet gefühlt haben, war mein Ziel. Alles Gute weiterhin, Alexander Andreev.“*

**Farben:** Tannengrün `#1F4A3F` (Anker, Text, Hauptbuttons), Safran `#E3A93F` (Akzent, nur Punkte/Icons), Salbei `#B9CFC2` (Flächen), Sand `#DCC8B4` (Zweitton), Creme `#F4EFE4` (Hintergrund). Gewichtung: Creme 60 %, Salbei und Sand 25 %, Tannengrün 12 %, Safran 3 %. Kein Klinikblau, Türkis, Neon. Safran nie für Fließtext. **Schriften:** Fraunces (Überschriften, Wortmarke), DM Sans (Fließtext), lokal hosten (DSGVO).

**Bildsprache:** Echte Menschen statt Stock (Alexander bei der Arbeit), Tageslicht und warme Töne, Details statt Lächel-Posen, natürliche Zähne, Vorher-nachher standardisiert und nur nach Rechtsklärung. Grafik: weicher Bogen als Bildmaske, Zeitleiste mit Punkten (Planung → Start → Halbzeit → Retainer, Safran-Punkt = „Hier stehen Sie“), feine Linien-Icons.

**Textbausteine für Sektionen (Brand Identity 12.4, Kurzfassung):** Grundmuster jeder Sektion: Wunsch und Nutzen zuerst, dann die Sicherheit, dann der nächste Schritt. Ängste nur benennen, wo sie ehrlich aufgelöst werden. Hero: Kicker (Ort und Thema), H1 mit zwei kurzen Sätzen, ein Satz Erklärung, drei Chips, ein Button. Alltagsszene (zwei bis drei kurze Sätze im Präsens aus Sicht der Leserin, danach „Das passt für Sie, wenn:“ mit drei Bullets). Zusagen (drei fette Kurzsätze, je ein Beleg: Mensch, Preis, Ergebnis). Ablauf (Zeitleiste in vier Schritten). Person (Ich-Form, ein Satz Werdegang, ein Satz Haltung). Preis (Rahmen, Begründung, Ausschlüsse selbst nennen, Zahlungsweg mit Gesamtkosten). Ehrlich über Nachteile (ein Satz was ungewohnt ist, ein Satz wie lange, ein Satz Alternative). Bei Zögern (Druck herausnehmen, Zweitmeinung erlauben). FAQ (Frage in Alltagssprache, Antwort in zwei Sätzen). **Satzbau:** kurze Hauptsätze, eine Aussage pro Satz, Zahlen statt Adjektive, keine Ausrufezeichen, kein Satz beginnt mit einem Versprechen, das nach Ergebnis klingt. **Prompt-Muster für neue Sektionen:** „Schreibe die Sektion [Name] nach diesem Briefing. Ton: ruhig, klar, persönlich. Sie-Form, kurze Sätze, keine Superlative, keine Erfolgsversprechen. Unbekannte Fakten als [Platzhalter] lassen. Gib zwei Varianten und nenne, welchen Blocker der Zielperson die Sektion auflöst.“

**Rechtliche Leitplanken für alle Texte:** Keine Erfolgs- oder Ergebnisversprechen (Zusagen ja, Garantie nein). Vorher-nachher, Zitate, Sterne, Fallkarten nur mit Einwilligung und echten Belegen. Preise als Rahmen und Orientierung, verbindlich erst im Heil- und Kostenplan. „Kostenlos“ beim Erstermin und Aussagen zu Schnarchen und Knirschen werberechtlich prüfen. Gesundheitsangaben in Formularen brauchen ausdrückliche Einwilligung.

**Bekannte Konflikte mit dem Live-Text der Website (nicht geändert, Alexander entscheidet):** /aligner „Zwei Wege“ nennt noch zwei Pläne (es gibt drei); „Prophylaxe-Mitgliedschaft“ im Live-Text statt PZR-Abo und Retainer-Klub; Startseite zeigt Vorher/Nachher und Zitat (OLG Frankfurt, Rechtscheck); Kennzahlen „400 Behandlungen, 1.000 Pläne, Google 4,9 / 87“ sind auf Belegbarkeit zu prüfen; /erstermin steht auf noindex; Akquise-Flowchart v5 schloss Foto-Beurteilung aus, der Smile-Check macht sie zum Angebot (Rechtscheck).

---

# TEIL D · Daten, Kanäle und rechtliche Befunde

*Quelle: Akquise-Funnel_Erkenntnisse_v1 (Stand 07.10.2026), Arbeitshypothesen, keine Rechtsberatung. Datenstand: Keyword-Exporte Juni und August 2025, Recherchen Oktober 2026. Preise der Pläne stehen in Teil A (dort gilt v8; die Zwei-Pläne-Angabe der Quelle ist überholt).*

## D1. Theoretische Basis: Hormozi „$100M Leads“

Hormozi zählt nicht Leads, sondern Engaged Leads: Menschen, die Interesse gezeigt haben, kaufen können und wollen. Grundlage sind Zusammenfassungen Dritter, das Buch selbst nicht im Original gelesen.

| Core Four | Idee | Im Projekt (Hypothese) |
|---|---|---|
| Warm Outreach | Menschen ansprechen, die dich kennen | Bestandskartei, Empfehlungen |
| Content | 1-zu-viele, wärmt kalte Kontakte | Fall-Content, Wissensseiten |
| Cold Outreach | gezielte Ansprache Fremder | im Projekt gestrichen; Überweiser eher als Lead Getter |
| Paid Ads | Traffic und Volumen steuerbar | Test mit festem Budgetdeckel |

- **Lead Magnet:** kostenloser Einstieg, der ein kleines Problem löst und das nächste zeigt, das das Kernangebot löst. **Lead Getter:** andere bringen Leads (Patienten, Team, Überweiser).
- **More, Better, New:** erst Volumen steigern, dann Qualität, dann neue Kanäle. **Fokus-Regel:** einen Kanal meistern, bevor der nächste kommt.
- **Grenze:** Das Modell stammt aus der US-Online-Welt. In Deutschland setzen Berufsrecht und HWG Grenzen.

## D2. Julia im Funnel

Julia wird vermutlich durch Menschen und Momente auf das Thema gebracht und prüft dann digital (Hypothese). Zwei Fragen: Wo entsteht der Gedanke, und wo prüft sie, ob sie vertraut?

| Auslöser | Wo ist Julia in dem Moment? | Mögliche Berührungspunkte |
|---|---|---|
| Foto oder Videocall | Handy, Laptop, Social Media | Instagram/Reels, Google-Suche direkt danach |
| Anlass voraus (Hochzeit, Geburtstag, Jobwechsel) | Planung mit Freundinnen, Kolleginnen, Familie | Gespräche, Empfehlung, Messenger-Gruppen |
| Kind bekommt Spange | KFO-Praxis, Elternumfeld | Gespräche, Kita/Schule |
| Beobachtung im Alltag | Spiegel, eigene Zahnreinigung | eigene Zahnarztpraxis, Hinweis bei der Prophylaxe |
| Kollegin trägt Aligner | Arbeitsplatz, Freundeskreis | Mundpropaganda, Instagram, Bewertungen |

Phasen: Auslöser (sie sucht noch nicht), Recherche (Google, Maps, Bewertungen, YouTube, Websites), Entscheidung (Empfehlung, Website, Erstkontakt, Erstermin). These: Viele Auslöser sind sozial, digitale Kanäle bestätigen eher, als dass sie auslösen. Offen: Welcher Auslöser kommt bei echten Patientinnen am häufigsten vor? Fünf kurze Gespräche mit echten Julias würden mehr zeigen als jede Hypothese.

## D3. Recherche: Wie Patientinnen suchen und prüfen

- Empfehlung und Google gehören zusammen: Laut einem Fachartikel von 2017 wählen rund 40 % der Neupatienten per Empfehlung, weitere 40 % über Google oder Bewertungsportale. Datenlage dünn, keine deutsche Studie speziell zu Aligner-Selbstzahlerinnen.
- Bewertungen: Eine US-Marketingquelle nennt 72 % der Patienten, die Online-Bewertungen prüfen (2023). Google-Bewertungen erscheinen direkt in lokaler Suche und Maps.
- Aligner und Social Media: In einer indischen Umfrage mit 300 Aligner-Patienten war Instagram (68,6 %) vor YouTube (56,2 %) am einflussreichsten. In einer italienischen Auswertung waren 54,8 % von 1.503 Instagram-Posts während der Therapie negativ, meist wegen Schmerzen.
- Deutschland, 30 bis 49 Jahre: 2022 nutzten 47 % Facebook wöchentlich; laut Medienstudie 2024 liegt Instagram insgesamt vor Facebook.
- Was Julia beim Suchen findet: Verzeichnisse (arzt-auskunft.de: 136 Treffer für Zahnmedizin in Mülheim, nur 1 unter Ästhetischer Zahnheilkunde), neutrale Ratgeber (TK: 3.000 bis 8.000 €), Anbieterseiten mit breiten Preisspannen (1.500 bis 9.000 €).
- Hypothese: Keine gefundene Seite beantwortet die Frage, die bei Kieferblick an erster Stelle steht: Wer übernimmt am Ende Verantwortung? Nicht geprüft: echte Google- und Maps-Ergebnisse mit Bewertungen in Mülheim.

## D4. Keyword-Datenbasis

Für Julias Kerncluster (Kosten, Erfahrung, Anbieter) gibt es bundesweit rund 11.700 Suchen pro Monat. Im Ruhr-Kern grob etwa 200, in Mülheim allein etwa 24 (Hochrechnung nur nach Bevölkerungsanteil: Mülheim 0,2 %, Ruhr-Kern aus Mülheim, Essen, Duisburg, Oberhausen 1,7 %; Annahme). Echte Regionalzahlen liefert DataForSEO bzw. der Keyword Planner.

| Phase | Beispiele (Suchen pro Monat bundesweit, Schwierigkeit 0–100) |
|---|---|
| Auslöser | zähne richten lassen 590 (6) · zähne verschieben sich 590 (3) · zähne begradigen 480 (4) · schiefe zähne 3.600 (25) |
| Rückfall/Retainer | retainer 27.100 (51) · wie lange retainer tragen 390 (3) · retainer draht gelöst 390 (3) |
| Kosten | invisalign kosten 6.600 (27) · durchsichtige zahnspange kosten 390 (5) · invisalign preise 320 (6) |
| Erfahrung | invisaligns erfahrungen 920 (4) · aligner test 390 (9) · invisalign schlechte erfahrungen 390 (5) |
| Anbieter | aligner zahnarzt 320 (8) · invisalign zahnarzt 210 (15) · invisalign in meiner nähe 140 (13) |
| Marke/Kategorie | invisalign 40.500 (46) · aligner 9.900 (49) |

- **Marke:** „Invisalign“ hat vier Mal so viele Suchen wie „Aligner“. Markenbegriffe in Texten und Anzeigen sind ein Rechtspunkt, wenn Kieferblick nicht mit Invisalign arbeitet.
- **Auslöser-Keywords:** leicht rankbar (Schwierigkeit 2 bis 6), aber klein. „Zähne verschieben sich“ passt fast wörtlich zu Julias Geschichte.
- **Kosten:** größtes Recherche-Thema. In den Aligner-Ergebnissen rankt eine kritische Verbraucherseite („Kostenfalle Zahn“, geschätzt 1.600 Besuche pro Monat).
- **Lokal:** In den Daten nur ein Mülheim-Begriff („veneers mülheim an der ruhr“, 10). „Invisalign essen“ meint „mit Invisalign essen“, nicht die Stadt.
- **Wettbewerber:** DrSmile rankt stark über Marke und Gesundheitsthemen (Platz 2 für „kreuzbiss“). Ketten gewinnen mit Stadtseiten (Konzept Weiss: rund 400 Stadt-Keyword-Zeilen). Kleine Praxen erreichen mit Fachinfo-Serien Platz 12 bis 43 für „aligner“, mit wenig Traffic.
- **Bleaching und Veneers:** deutlich mehr Nachfrage als lokale Aligner-Begriffe (bleaching 49.500, zähne bleaching 8.100, bleaching kosten 5.400; veneers 49.500). Lokal bei Veneers klein: Dortmund 70, Essen 50, Mülheim 10. Bei Bleaching starker Wettbewerb durch Ketten.
- **Ads-Szenario (Annahmen: CPC 1 bis 2 €, Anfragequote 3 bis 8 %, Erscheinen 70 %, Abschluss 30 bis 40 %):** 45 bis 320 € Werbekosten pro gewonnenem Fall, gegen den Benchmark von 600 bis 800 €. Für 5 Fälle pro Monat wären 223 bis 794 Klicks nötig, mehr als die geschätzten Suchen im Kerncluster. **Das Volumen ist der Engpass, nicht der Preis.** Der frühere Ads-Forecast (ganz Deutschland, CPC 0,31 €, Conversion-Rate 4,58 %) war nicht verwertbar.
- **Datei:** Auswertung mit rund 7.800 Keywords als Excel (Kieferblick_Keyword-Auswertung_v1.xlsx: Funnel-Zuordnung, Kernbegriffe, Lokal-Szenario, Wettbewerber). **Datenlücken:** Schnarchen/Schnarchschiene, Knirschen/Funktionsschiene, PZR/Prophylaxe, „Zahnarzt Mülheim“ fehlen; regionale Suchvolumen für Mülheim/Ruhr fehlen.

## D5. Kanäle: Kosten-Nutzen und Automatisierbarkeit

Alle Bewertungen sind Einschätzung, keine Messwerte. Geld: € unter ca. 100 €/Monat, €€ 100 bis 1.000 €, €€€ darüber (Annahme).

| Kanal | Phase | Passt zu Julia | Geld | Zeit | Nutzen | Wirkung nach | Automatisierbar |
|---|---|---|---|---|---|---|---|
| Google-Profil + Bewertungen | Recherche, Entscheidung | hoch | € | mittel | sehr hoch | 2–6 Monate | hoch |
| Website + lokale Landingpage | Recherche, Entscheidung | hoch | €€ einmalig | mittel | hoch | 3–9 Monate | hoch |
| Empfehlung von Patienten | Auslöser, Entscheidung | hoch | € | gering | hoch | 3–12 Monate | niedrig bis mittel |
| Bestandskartei | Auslöser | mittel | € | mittel | mittel bis hoch | sofort | hoch |
| Google Ads (lokal) | Recherche | hoch | €€ bis €€€ | gering | hoch, aber Volumen begrenzt | sofort | mittel |
| Instagram organisch | Auslöser | hoch | € | hoch | mittel | 6+ Monate | mittel |
| Instagram/Meta-Ads | Auslöser | mittel | €€ | mittel | mittel | nach Content-Basis | mittel |
| Überweiser/Netzwerk | Auslöser | niedrig bis mittel | € | hoch | hoch für Fallqualität, wenig Volumen | 3–12 Monate | niedrig bis mittel |
| Jameda und Co. | Recherche | mittel | € bis €€ | gering | mittel | 3–6 Monate | mittel |
| Lokale Partner (Friseur, Fitness, Kita) | Auslöser | mittel | € | mittel | unklar | Testfall | niedrig |
| YouTube | Recherche | mittel | €€ bis €€€ | hoch | unklar | 12+ Monate | niedrig |

Fundament: Google-Profil, Bewertungen, Website mit lokaler Landingpage. Schnell testbar: Bestandskartei und Google Ads mit Budgetdeckel. Verstärker sobald Fälle vorliegen: Instagram organisch, Empfehlung, Überweiser. Später/Experiment: YouTube, Meta-Ads, lokale Partner. **Automatisierung:** größter Hebel im Anfragen-Management (Rückrufkette: Anruf in 10 Minuten, SMS nach 5 Minuten, Erinnerungen gegen No-Shows). Ein KI-Agent bereitet vor, ein Mensch gibt frei. Zu prüfen: DSGVO bei Gesundheitsangaben und Auftragsverarbeitung, HWG bei KI-Texten, rechtliche Prüfung der Ansprache der Bestandskartei.

## D6. Funnel-Architektur (Entscheidung 07.10.2026)

Alles in einem Funnel, bewusst einfach. Bleaching, Schnarchschiene und Funktionsschiene bekommen keine eigenen Stränge, sondern laufen als Angebote hinter derselben Tür („Kieferblick-Check“).

```
EINGÄNGE                       TREPPE                          DANACH
A  sie sucht (Google)     ->  Stufe 1  Information (gratis)  \
B  Bestand/Empfehlung/        Ratgeber, Selbsttest, Mails      \
   Content                ->  Stufe 2  Kontakt/Auskunft        ->  Abschluss -> Bindung
C  Überweiser             ->  Stufe 3  Erstermin (Kern)            -> Empfehlung -> Stufe 1
```

Eingang A steigt bei der Information ein, B beim Kontakt, C direkt beim Erstermin. Nach dem Abschluss speisen Bewertungen und Weiterempfehlung wieder Stufe 1. **Stand seit 15.10.:** Die digitale Einstiegsleiter (Checkliste → Smile-Check → Ersttermin, Teil A Abschnitt 6) ist die konkrete Umsetzung von Stufe 1 bis 3 für Artikel-Besucher.

## D7. Lead-Magnet-Formate (Ampel = Einschätzung der Rechtslage, keine Rechtsberatung)

| Format | Idee für Kieferblick | Löst vor allem | Recht | Automatisierbar |
|---|---|---|---|---|
| PDF-Ratgeber / Checkliste | „Was Aligner wirklich kosten“ mit 7 Fragen an jede Praxis | Endpreis, Vertrauen | grün | hoch |
| Quiz / Selbsttest | 30-Sekunden-Eignungscheck oder Rückfall-Check | Auslöser, Segmentierung | grün bis gelb (Gesundheitsangaben: Einwilligung, Ergebnis ohne Diagnose) | hoch |
| Endpreis-Rechner | Preisrahmen und Ratenbeispiel | Endpreis | gelb | hoch |
| Mini-E-Mail-Serie | 5 Mails zu Ablauf, Nachteilen, Retainer, Verantwortung | Bedenkzeit, Ergebnisrisiko | grün | sehr hoch |
| Infoabend / Webinar | „Zähne wandern wieder: Was hilft?“ (allgemeine Aufklärung) | Auslöser, Vertrauen | grün bis gelb | mittel |
| Aufklärungsvideos | 3 Minuten mit Alexander, z. B. „Was passiert beim Bisscheck?“ | Verantwortung, Person | grün | niedrig |
| Fall-Dossiers | dokumentierte Fälle mit Einwilligung | Ergebnisrisiko | gelb (Vorher-nachher) | mittel |
| Online-Informationsgespräch | 15 Minuten Video oder Rückruf, nur Information, keine Diagnose | Verantwortung | gelb | mittel |
| Plan-Zweitmeinung | Angebot einer anderen Praxis prüfen | Endpreis, Vertrauen | gelb (individuelle Leistung) | niedrig |
| KI-Smile-Simulation online | Foto hochladen, Vorschau erhalten | Auslöser | rot bis gelb | hoch |
| Messenger-Info-Chat | Chat ähnlich Impress (WhatsApp) | schnelle Antwort | gelb (Datenschutz) | hoch |

Beispiel aus dem Markt: Impress bietet ein 30-Sekunden-Quiz zur Eignung, einen unverbindlichen Infotermin mit Untersuchung, 3D-Scan und Röntgen sowie WhatsApp-Chat und Telefon. Smile-Simulations-Tools (Musely, SmileFy) arbeiten per Foto-Upload bzw. im Behandlungsraum; Voreinstellungen wie „Hollywood-Lächeln“ passen nicht zum ruhigen Ton.

## D8. Intro Offers im Funnel (Einschätzung, Preise siehe Teil A)

Bleaching passt als Bewertungs- und Fall-Motor und für den Bestand (Schwäche: harter Wettbewerb durch Ketten, Rabattjäger-Gefahr). Die Schnarchschiene braucht einen eigenen Strang über das Netzwerk (HNO, Schlafmedizin, Partner; Stärke: hohes Ticket, klinisch einfach; Schwäche: mind. 5 lokale Anbieter, Online-Preis 495 €, keine Keyword-Daten). Die Funktionsschiene bleibt geparkt (Suchintention vermutlich preissensibel, keine Daten). Schnarchschiene: Screening auf Schlafapnoe bleibt Pflicht (Fragebogen, Überweisung an Schlafmedizin), Werbung nach HWG prüfen. Die alte Bleaching-FAQ trägt noch den Namen Alluxea und Aussagen wie „Zufriedenheitsgarantie“, „perfekte Schienen“, 499 €: vor Nutzung an Marke, Ton und Leitplanken anpassen.

## D9. Rechtliche Befunde und Konsequenzen

Der kostenlose Erstermin mit Scan, Simulation und 10-Minuten-Check ist ein echtes Rechtsrisiko und muss vom Fachanwalt geklärt werden. Angaben stammen aus Fachmedien und Zusammenfassungen, nicht aus den Urteilen selbst. Keine Rechtsberatung.

| Fund | Inhalt | Bedeutung für Kieferblick |
|---|---|---|
| LG Braunschweig, 25.03.2021 (22 O 582/20) | Werbung für kostenlose Implantat-Sprechstunde untersagt; individuelle fachliche Beratung nur gegen Entgelt (§ 7 HWG, Zuwendung) | Erstermin mit individuellem Befund ist vermutlich betroffen |
| LG Stade (8 O 37/15) und LG Stuttgart (11 O 75/15), 2015 | Kostenloser „Vitalitätsplan“ mit Abformung und kostenlose Zahnreinigung als unzulässige Werbegaben | kostenlose Scans und Leistungen als Lockmittel sind heikel |
| Fachartikel zu § 7 HWG | Zulässig bleiben Auskünfte und Ratschläge ohne individuelle Leistung | Information kostenlos, individuelle Leistung eher entgeltlich |
| Berufsgericht Münster, 19.06.2023 (18 K 3561/21.T) | Aligner-Werbung mit emotionalen Slogans und Herstellerfokus als berufswidrig gewertet | Texte sachlich halten; Kammer Nordrhein hat eigene Berufsordnung, klären |
| DGKFO, Verbraucherzentrale, Bundestags-Stellungnahme | Eigentherapie mit selbst genommenen Abdrücken abgelehnt; Foto-Kontrollen angezweifelt; Videosprechstunde nur als Beratung | Foto-Vorab-Einschätzung (Smile-Check) ist heikel, Rechtscheck nötig |

Weitere Prüfpunkte: Empfehlungsprämien und Zuwendungen, Werbung zu Schnarchen und Knirschen, Gesundheitsdaten in Tests, Markenbegriffe wie „Invisalign“, Vorher-nachher, Slogan „Schön lächeln. Gut zubeißen.“. **Mögliche Treppe laut Quelle:** (1) Information kostenlos, (2) Kontakt und Auskunft (Rückruf in 10 Minuten, Online-Informationsgespräch ohne Diagnose), (3) individuelle Leistung (Scan, Simulation, klinischer Check) vermutlich entgeltlich und anrechenbar. Die Projektentscheidung „Erstberatung kostenlos“ (Teil A) steht unter dem Vorbehalt der Fachanwalt-Klärung.

## D10. Offene Datenlücken und nächste Schritte

- Regionale Suchvolumen für Mülheim und den Ruhr-Raum (DataForSEO mit Standort).
- Echte Google- und Maps-Ergebnisse in Mülheim inklusive Bewertungen der Nachbarn.
- Fünf kurze Gespräche mit Patientinnen, die zu Julia passen.
- Im Erstkontakt die Quelle erfassen: „Wie sind Sie auf uns gekommen?“
- Rechtsfragenliste für den Fachanwalt.

---

# TEIL E · CRM, Automationen und Customer Journey

*Quellen: CRM-Spec_und_Zusammenfassung_v1 (07.10.2026) und Customer-Journey_ab-Nurturing_v1 (07.10.2026). Arbeitshypothesen, keine Rechtsberatung. **An v8 noch anzupassen** (Teil A, Abschnitt 12, Punkt 1): Plan-Feld braucht „Premium“ (drei Pläne); „Prophylaxe-Mitgliedschaft“ ist jetzt PZR-Abo und Retainer-Klub (229 / 249 / 429 € pro Jahr statt „390–450 €“); neue Quellenfelder **Artikel-URL** und **Smile-Check-Status** (bezahlt, Fotos eingegangen, Video gesendet, Erstattet); Status für die digitale Einstiegsleiter (Checkliste geladen, Smile-Check gekauft). Der Zweig Checkliste/Smile-Check vor dem Erstkontakt fehlt in der Journey noch.*

## E1. Entscheidungen und Stack

| Thema | Entscheidung |
|---|---|
| Website, Formulare | WordPress mit Elementor, Tally mit minimalem Formular |
| CRM | Baserow Cloud (laut Alexander rechtlich geklärt). Nicht Airtable (EU-Speicherung nur im Plan Enterprise Scale). Keine Eigenentwicklung zum Start |
| Kontaktweg | Rückruf statt Direktbuchung, Online-Beratung darf buchbar sein |
| Zielgruppe | nur Erwachsene |
| Erstgespräch | Entscheidung und Angebot fallen im Termin |
| Zahlung | Einmalzahlung, Phasen oder Monatsraten. Vorerst manuell in Stripe auslösen, Zahlungsstatus von Hand im Fall pflegen, Anbindung später |
| Umfang | vier Ansichten plus Formular, keine Rollenlogik |
| Recht | Prüfung vorgesehen für Ratenzahlung, Empfehlungsanreize, Bewertungsanfragen, Werbung (HWG), Einwilligungen |

| Aufgabe | Wahl | Kosten |
|---|---|---|
| Mails und SMS senden | Brevo, Free-Plan als Absender für Vorlagen | 0 €, bis 300 Mails pro Tag, SMS-Preis nicht geprüft |
| Ablauflogik (Mail-Serie, Nachfassen, Erinnerungen) | n8n Cloud Starter, fragt täglich Baserow ab, Server in Frankfurt | 20 € im Monat bei Jahreszahlung, 2.500 Abläufe |
| Website-Chat | Crisp Free, optional später | 0 €, 2 Plätze |
| WhatsApp | WhatsApp-Business-App, manuell | 0 € |
| Rückruf | Telefon | – |

Die Logik liegt im CRM: Die Felder Nächste Aktion und Fällig am sagen, was ansteht, n8n löst die Mail über Brevo aus. Make wäre günstiger (ca. 12 $/Monat), nennt aber nur „EU oder Nordamerika“; n8n nennt Frankfurt ausdrücklich. Preise Stand Oktober 2026 laut Anbieterseiten, vor dem Start gegenprüfen.

**Cody Schneider (Einordnung aus Podcasts, nicht aus einzelnen Posts):** Ads-Agent mit festem Budgetdeckel (recherchiert Pain Points, testet Creatives, stoppt Verlierer; das Suchvolumen ist der Engpass); KI-Recherche nach Pain Points in Foren als Quelle für Anzeigen und Content; ein Aufklärungsvideo wird zu mehreren Kanälen verwertet; Pflichtfeld „Wie haben Sie von uns erfahren?“ zeigt oft ein anderes Bild als Analytics; Kaltansprache im Projekt gestrichen, bei Überweisern persönliche, teilautomatisierte Ansprache; Leitplanken für HWG und DSGVO gehören in jeden Agent.

## E2. Aufbau des CRM

Drei Ebenen: Stufe (grob), Status (fein, pro Stufe), Marker (frei kombinierbare Filter). Keine festen Phasen mit Gates, sondern eine Kette mit Kennzahlen je Quelle. Ein Kontakt = eine erwachsene Person, kann mehrere Fälle haben (Aligner, später Bleaching, Funktion/Schlaf). Die Quelle wird beim Erstkontakt erfasst und bleibt bis zur Empfehlungsfrage. Jede Statusänderung wird mit Zeitstempel protokolliert (Verweildauern, Engpässe). Der Status-Katalog liegt als eigene Tabelle vor. Annahme: Im CRM stehen nur Termine, Status, Zahlungen und Einwilligungen; Befunde, Fotos und Diagnosen bleiben im Praxisverwaltungssystem (bei Smile-Check-Fotos Datenschutz klären).

| Tabelle | Zweck | Wichtige Felder |
|---|---|---|
| Kontakte | Person, Erreichbarkeit, Einwilligungen | Name, E-Mail, Telefon, Wunschkanal (Rückruf, WhatsApp, Online-Gespräch), Einwilligung Mail/SMS/Telefon mit Datum |
| Fälle | Ein Anliegen eines Kontakts durch die Journey | Kontakt, Fall-Typ, Quelle, Magnet, aktueller Status, Nächste Aktion, Fällig am, Verlustgrund, Plan, Behandlungswert |
| Statusverlauf | Protokoll jeder Änderung | Fall, von Status, nach Status, Zeitpunkt, wer/was hat es ausgelöst |
| Status-Katalog | Liste aller Status, pflegbar | Name, Stufe, Reihenfolge, nächste Aktion, Frist, aktiv ja/nein |
| Termine | Orientierungsgespräch, Erstgespräch, Abschluss | Fall, Art, Datum, Video gesehen, erschienen, Ergebnis |
| Zahlungen | Zahlungsweg und Mitgliedschaft | Fall, Weg (Einmal, Phasen, Rate, Mitgliedschaft), Betrag, Status (offen, bezahlt, fehlgeschlagen), vorerst von Hand |
| Quellen und Magnete | Stammdaten für Auswertung | Eingang (A, B, C), Kanal, Magnet, Kosten je Zeitraum |
| Kommunikation (optional) | Was wurde wann gesendet | Fall, Kanal, Vorlage, Zeitpunkt, Ergebnis |

## E3. Status-Katalog

Fristen und Mail-Abstände sind Annahmen, im Betrieb zu testen.

| Stufe | Status | Auslöser | Nächste Aktion | Frist |
| --- | --- | --- | --- | --- |
| Eingang | Lead neu | Magnet geladen oder Formular abgesendet | Mail 1 mit Magnet und nächstem Schritt | sofort |
| Eingang | Mail-Serie läuft | Mail 1 gesendet | Mails 2 bis 5 nach Plan | Tag 2, 4, 7, 10 bis 12 |
| Kontakt | Kontaktwunsch | Anfrage nach Rückruf, WhatsApp oder Online-Gespräch | Rückruf oder Gespräch anbieten | 10 Min |
| Kontakt | Nicht erreicht | Rückruf ohne Erfolg | Versuch 2 und 3, dann Nachricht mit Rückrufwunsch-Link | 24 h (Annahme) |
| Kontakt | Orientierungsgespräch | Online-Gespräch vereinbart (10 Min) | Passungs-Check, Termin anbieten | Wunschtermin |
| Termin | Termin gebucht | Buchung | Mail-Serie stoppen, Bestätigung, Video-Link | sofort |
| Termin | Video offen | Video 24 h vorher nicht gesehen | SMS mit Link | 24 h vorher |
| Termin | Video gesehen | Video angesehen | keine, nur Kennzahl ⑤ | – |
| Termin | Erschienen | Erstgespräch hat stattgefunden | Ausgang erfassen | Termintag |
| Termin | No-Show | nicht erschienen | Nachricht mit Neubuchungslink | 1 h danach (Annahme) |
| Ausgang | Unterschrift Idealplan | Zusage im Erstgespräch | Röntgen, Funktionsdiagnostik, Feinplanung, Ein-Seiter, Onboarding | im Termin |
| Ausgang | Zahlungsweg gewählt | Geld-Einwand beim Idealplan | Wege in fester Reihenfolge, dann Ästhetischer Plan (nur bei passendem Befund), dann Unterschrift | im Termin |
| Ausgang | Veneers-Ausstieg | ausdrücklicher Zweifel an der Tragedisziplin | Komposit-Mock-up, Aufklärung, Aligner-Sheet bleibt offen | im Termin |
| Ausgang | Bedenkzeit | Angst, Zeit oder Unsicherheit | Einwandtyp notieren, Rückruftermin vereinbaren, Nachfass-Sequenz | Tag 1, 3, 7, 14, 28 |
| Ausgang | Nein, passt nicht | Absage | Bestand, Empfehlungsliste, bei Aligner-Nein Bleaching | im Termin |
| Behandlung | Onboarding | Unterschrift | Start-Onboarding | nach Unterschrift |
| Behandlung | In Behandlung | Behandlungsstart | Halbzeit-Check einplanen | zur Halbzeit |
| Behandlung | Abschlusstermin | Behandlung beendet | Zufriedenheit, Retention, Retainer-Übergabe | Termin |
| Nachsorge | Bewertung | nach dem Abschlusstermin | 5 Fragen, dann Google-QR für alle; Unzufriedene melden sich binnen 48 h | im Termin |
| Nachsorge | Mitgliedschaft angeboten | nach der Bewertung | SEPA im Termin, bei Ablehnung Retainer-Selbstcheck nach 3 und 6 Monaten | im Termin |
| Nachsorge | Empfehlungsfrage | aktiv im Termin | Rückfluss als Quelle im Eingang B | im Termin |
| Reaktivierung | Kalt geworden | Mail-Serie ohne Buchung oder Bedenkzeit ohne Ergebnis | neuer Fall oder Infoabend-Einladung | 6 bis 8 Wochen |
| Ausstieg | Verloren | Absage oder keine Reaktion | Verlustgrund als Pflichtfeld | sofort |
| Ausstieg | Abgemeldet | Abmeldung | alle Sequenzen sofort beenden | sofort |

Bleaching, Schnarchschiene und Funktions-/Schlaftermin laufen durch dieselbe Kette (Marker Fall-Typ, keine eigenen Status).

## E4. Marker

| Marker | Werte (Startliste) |
|---|---|
| Eingang | A sie sucht, B sucht noch nicht, C Überweisernetzwerk |
| Kanal | Google-Profil, Website/SEO, Ads, Bestand, Empfehlung, Content, lokale Partner, HNO/Schlafmedizin, Physio/Osteopathie |
| Magnet | Selbsttest, PDF Aligner oder Veneers, PDF 7 Gründe, Retainer-Selbstcheck, Endpreis-Ratgeber, Infoabend, Schlaf-/Knirsch-Check; **neu:** Checkliste „7 Fragen“, Smile-Check |
| Fall-Typ | Aligner, Veneer/Ästhetik, Bleaching-Paket, Schnarchschiene, Funktion/Schlaf |
| Plan | Idealplan, Ästhetischer Plan (**ergänzen: Premiumplan**) |
| Einwandtyp | Preis, Angst, Zeit, Unsicherheit, Tragedisziplin |
| Zahlungsweg | Einmal, Phasen, Rate, Mitgliedschaft |
| Einwilligung | Mail, SMS, Telefon, jeweils mit Datum |
| Überweiser | Praxis oder Person, nur bei Eingang C |
| Verlustgrund | Preis, anderer Anbieter, Termin passte nicht, keine Rückmeldung, Aligner passt nicht |

## E5. Ansichten

Jeder Fall hat die Felder Nächste Aktion und Fällig am, die der Status-Katalog bei jedem Statuswechsel automatisch setzt.

| Ansicht | Typ | Filter | Sortierung | Sichtbare Felder |
|---|---|---|---|---|
| Heute | Tabelle auf Fälle | Fällig am bis heute, Stufe nicht Ausstieg | Fällig am aufsteigend, überfällig rot | Kontakt, Telefon, Wunschkanal, Status, Nächste Aktion, Fällig am, Quelle, Fall-Typ, Notiz |
| Pipeline | Kanban nach Status | Stufe nicht Ausstieg | Fällig am | Karte: Kontakt, Quelle, Fall-Typ, Fällig am |
| Fall | aufgeklappte Zeile | – | – | Blöcke: Kontakt und Quelle · Termin und Video · Erstgespräch-Ergebnis (Ampel, Plan, Ausgang, Einwandtyp, Zahlungsweg, Behandlungswert) · Zahlung |
| Auswertung | gruppierte Tabelle oder Dashboard | – | Quelle, dann Status | Anzahl je Quelle und Status, Verlustgrund, Behandlungswert, Kosten je Quelle |

Dazu ein Formular zum Anlegen neuer Kontakte (Name, Telefon, E-Mail, Wunschkanal, Quelle, Fall-Typ, Einwilligungen), das den Status Kontaktwunsch vorbelegt. Vor dem Bau prüfen: Kanban gruppiert nach einem Auswahlfeld (Status = Auswahlfeld in Fälle, Namen identisch mit dem Katalog); Auswertung als Dashboard oder gruppierte Tabelle hängt vom Baserow-Plan ab. Baserow hat seit 2.0 einen KI-Assistenten (Kuma), MCP-Unterstützung und ein frei wählbares KI-Modell.

## E6. Automatisierungen (n8n fragt Baserow ab, Versand über Brevo)

| Auslöser | Aktion |
|---|---|
| Tally-Formular oder Magnet-Download | Fall anlegen, Quelle und Einwilligung speichern, Mail 1 senden |
| Fall ohne Kontakt nach 10 Min | Hinweis ans Team (Mail oder Chat) |
| Status Termin gebucht | Mail-Serie stoppen, Bestätigung und Video-Link senden |
| 24 h vor Termin, Video nicht gesehen | SMS mit Link |
| Status No-Show | Nachricht mit Neubuchungslink |
| Status Bedenkzeit | Nachfass-Sequenz nach Einwandtyp (Tag 1, 3, 7, 14, 28) |
| Status Unterschrift oder Zahlungsweg gewählt | Zahlung manuell in Stripe auslösen, Zahlungsstatus von Hand pflegen |
| Später, nach Stripe-Anbindung: Zahlung fehlgeschlagen | Status Rate offen, Erinnerung, danach persönlicher Anruf |
| Status Abschlusstermin | Bewertungsablauf mit Tablet-Fragen und Google-QR |
| Mitgliedschaft abgelehnt | Retainer-Selbstcheck nach 3 und 6 Monaten |
| Status Verloren oder Abgemeldet | alle Sequenzen beenden, Verlustgrund prüfen |
| 6 bis 8 Wochen nach Kalt geworden | Reaktivierung mit neuem Fall oder Infoabend-Einladung |

## E7. Kennzahlen (je Quelle, aus Fällen und Statusverlauf)

| Nr. | Kennzahl | Berechnung im CRM |
|---|---|---|
| ① | Reichweite, Besucher | extern (Analytics, Ads), je Kanal in Quellen eingetragen |
| ② | Magnet-Downloads | Fälle mit Status Lead neu, Anteil von ① |
| ③ | Anfragen in 10 Min erreicht | Fälle mit Kontaktwunsch, davon Zeit bis zum ersten Kontakt unter 10 Min |
| ④ | Termine gebucht | Fälle mit Status Termin gebucht, Anteil von ③ |
| ⑤ | Video gesehen, erschienen | Fälle mit Video gesehen und Erschienen, Anteil von ④ |
| ⑥ | Abschluss und Kosten je Patient | Fälle mit Unterschrift, Behandlungswert, Kosten je Quelle geteilt durch Abschlüsse |

Zusätzlich: Verlustgründe je Status und Verweildauer je Status. **Neu aus v8:** Conversion je Artikel und Modul, Erstattungsquote Smile-Check, Anteil Smile-Check → Ersttermin → Abschluss, Anteil Ideal/Premium/Basis.

**Offene Punkte CRM:** Tally-Plan (Webhooks an n8n?), Brevo-AV-Vertrag und EU-Hosting, Baserow-Plan (Kanban/Dashboard), Anzahlung bei Ratenzahlung, Rechtsprüfung (Ratenzahlung, Empfehlungsanreize, Bewertungsanfragen, HWG, Einwilligungen), Patienten-App/Dental Monitoring später (im CRM nur ein Marker), Fristen und Mail-Abstände testen, Stripe-Anbindung als zweite Ausbaustufe.

## E8. Customer Journey ab Nurturing

**Kette:** Lead-Magnet → Mail-Serie → Kontakt → Termin gebucht → Video → Erstgespräch → Ausgang (5 Wege) → Behandlung → Abschlusstermin → Bewertung → Mitgliedschaft → Empfehlungsfrage.

**Entscheidungen:** Video kommt nach der Buchung. Mitgliedschaft (jetzt PZR-Abo/Retainer-Klub) wird nach der Bewertung angeboten. Idealplan ist klinisch immer möglich, der Ästhetische Plan nur eingeschränkt (Ampel von Alexander in Schritt 6).

**Mail-Serie Aligner (5 Mails, je ein Blocker, ein CTA, Zeitpunkte sind Annahmen):**

| Mail | Zeitpunkt | Blocker | Inhalt |
| --- | --- | --- | --- |
| 1 | Tag 0 | – | Magnet liefern, nächster Schritt (Rückruf oder Orientierungsgespräch) |
| 2 | Tag 2 | B1 Verantwortung | Ein Arzt, ein Plan, Praxiszusagen |
| 3 | Tag 4 | B2 Endpreis | Was ein Fall am Ende kostet, Refinement ist eingepreist, Zahlungswege |
| 4 | Tag 7 | B5 Alltag | 22 h, Attachments, Lispeln; ehrlich, auch für wen es nichts ist |
| 5 | Tag 10–12 | B3/B4 | Fall-Dossier, Retainer/Rückfall, Termin buchen |

Buchung beendet die Serie. Keine Reaktion nach Mail 5 → Reaktivierung nach 6–8 Wochen. Wer über „Aligner oder Veneers?“ kam, bekommt Mail 2 mit Ästhetik-Fokus.

**Video nach Buchung (5–8 Min, Alexander, nur Information):** (1) Wer übernimmt Verantwortung? (2) Ablauf des Termins: Beraterin führt, Alexander prüft 10 Min. (3) Was Aligner leisten und was nicht, inklusive „Refinement ist Standard“. (4) Preisrahmen und Zahlungswege (Plan-Preise nur gemäß aktueller Entscheidung, siehe Teil C). (5) Bedenkzeit ist Recht des Patienten, Zweitmeinung willkommen. Nicht gesehen 24 h vorher → SMS mit Link. Nur Information, keine individuelle Einschätzung, keine Garantiezusagen.

**Erstgespräch (60 Min, Beraterin führt):** Schritt 2 Anamnese = Weiche (Auslöser, Was stört am meisten?, früher Spange/Retainer?, Tragedisziplin, PKV/Beihilfe). Schritt 5 Smile-Simulation mit Check „Sind Sie zufrieden mit diesem Ergebnis?“. Schritt 6 Alexander 10 Min mit Ampel. Schritt 7 Beraterin: 3 Einverständnis-Checks → Sheet → Plan → Zahlungswege → Unterschrift. Röntgen, Funktionsdiagnostik und Feinplanung erst nach der Unterschrift (Abweichung vom Buch, Rechtspunkt).

**Entscheidungsbaum nach Schritt 7:**

| Signal | Antwort |
| --- | --- |
| Ja, will starten | Unterschrift → Röntgen, Funktionsdiagnostik, Feinplanung, Ein-Seiter Leistungsumfang, Onboarding |
| Geld-Einwand | Zahlungswege in fester Reihenfolge (Einmal → Phasen → Rate), dann Basis, nur bei passendem Befund. Danach Unterschrift |
| Ausdrücklicher Zweifel an der Tragedisziplin | Veneers-Ausstieg: Komposit-Mock-up zum Probetragen, Aufklärung Irreversibilität. Aligner-Sheet bleibt offen. Keine Rate und kein Downsell, das löst kein Disziplinproblem |
| Bedenkzeit (Angst, Zeit, Unsicherheit) | Kein Downsell. Rückruftermin im Raum, Einwandtyp notieren, Nachfass-Sequenz |
| Nein / passt nicht | Bleibt im Bestand, Zweitmeinung willkommen, Empfehlungsliste. Aligner passt nicht: Bleaching als kleines Ja |

**Nachfass-Sequenz bei Bedenkzeit (ca. 4 Wochen, Annahme):** Im Termin: Einwandtyp notieren, Rückruftermin und Kanal vom Patienten wählen lassen, Mail-Einwilligung einholen. Tag 1: Mail mit Simulation, Plan und Ein-Seiter (kein neuer Pitch, am selben Tag kein Nachfassen). Tag 3: Anruf zum vereinbarten Termin, nur Bedenken ausräumen. Tag 7: Mail passend zum Einwand (Preis: Zahlungsweg bzw. Basis; Angst: Fall-Dossier; Zeit: Terminplan; Unsicherheit: Zweitmeinung oder Infoabend). Tag 14: Kontakt im Wunschkanal, Hinweis auf echte Behandlungsplätze im Quartal (keine Frist, kein Rabatt). Tag 28: letzte Mail, danach Reaktivierung nach 6–8 Wochen. Nein oder Abmeldung beendet die Sequenz sofort.

**Nach der Unterschrift:** Start-Onboarding, Halbzeit-Check, Prophylaxe läuft mit. Abschlusstermin: 10 Min Alexander (zufrieden?), 10 Min Beraterin (Retention, Smile-Video, Retainer-Übergabe). Bewertung: 5 Fragen auf dem Tablet, danach Google-QR für **alle**; Unzufriedene: Alexander meldet sich binnen 48 h; keine Gegenleistung für Bewertungen. Mitgliedschaft nach der Bewertung (jetzt PZR-Abo 229 €, Retainer-Klub 249 €/149 €, Kombi 429 €, SEPA im Termin); lehnt der Patient ab: Retainer-Selbstcheck nach 3 und 6 Monaten. Empfehlungsfrage aktiv im Termin, zurück in Eingang B.

**Rechtspunkte der Journey:** Mail-Einwilligung und Telefonkontakt (Rückruftermin im Termin vereinbaren), Bewertungsanfrage ohne Gegenleistung und ohne selektives Einholen (Google-Richtlinien nach eigener Kenntnis, gegenchecken), Abrechnung PZR nach GOZ 1040 je Zahn, Laufzeit und Kündigung transparent.

---

*Ende des Dokuments. Für alles, was hier nicht steht (Sales-Baum-Volltext, GOZ-Kostenvoranschlag, Akquise-Flowchart, Manuskript), Alexander um die jeweilige Datei bitten.*
