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
**Mitgeplant (Alexander 21.10.2026):** D Veneers und E PZR als kleine Testkampagnen, Start nach A bis C (Woche 3 bis 4), jeweils ca. 100 € aus der Reserve (Annahme, Entscheidung offen). Klickschätzung Zone 1 (Gebot Veneers 5 €, PZR 4 €): Veneers 244 Klicks / 580 € / CPC 2,38 €, PZR 227 Klicks / 488 € / CPC 2,15 € (`daten/ads/zone1-veneers-pzr-2026-10-21.json`). CAC (Annahmen): Veneers opt./Mitte/pess. ca. 174 / 452 / 1.630 € (Fallwert 2.400–12.800 €), PZR ca. 37 / 64 / 240 € (Umsatz 149 €, Wert liegt im PZR-Abo und in der Anrechnung). Korrektur: die früheren Werte (Veneers ca. 740 €, PZR ca. 150 €) beruhten auf höheren Keyword-Planner-CPC.
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
