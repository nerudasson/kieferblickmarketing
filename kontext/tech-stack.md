# Tech-Stack (Quelle: CRM-Spec und Zusammenfassung v1, 07.10.2026; Preise vor Kauf gegenprüfen)

| Aufgabe | Wahl |
|---|---|
| Website | WordPress mit Elementor |
| Formulare | Tally, minimales Formular (Webhook-Fähigkeit im Plan zu prüfen) |
| CRM | Baserow Cloud (laut Alexander rechtlich geklärt). Nicht Airtable (EU-Speicherung nur im Plan Enterprise Scale) |
| Automation | n8n Cloud Starter (Frankfurt, ca. 20 €/Monat bei Jahreszahlung), fragt Baserow täglich ab |
| Mail/SMS | Brevo Free (AVV und EU-Hosting zu bestätigen) |
| Website-Chat | Crisp Free, optional |
| WhatsApp | WhatsApp-Business-App, manuell |
| Zahlung | Stripe, vorerst manuell, Anbindung später |

- CRM enthält nur Termine, Status, Zahlungen, Einwilligungen. Befunde, Fotos, Diagnosen bleiben im Praxisverwaltungssystem.
- Tabellen: Kontakte, Fälle, Statusverlauf, Status-Katalog, Termine, Zahlungen, Quellen und Magnete, Kommunikation. Marker: Eingang, Kanal, Magnet, Fall-Typ, Plan, Einwandtyp, Zahlungsweg, Verlustgrund.
- Quelle wird im Erstkontakt erfasst („Wie sind Sie auf uns gekommen?“). Daraus entstehen die Kennzahlen je Quelle.

## Schnittstellen für den Marketing-Agent (Stand 08.10.2026, Quellen teils Anbieterblogs, vor Nutzung gegenprüfen)
| Zweck | Wahl / Stand |
|---|---|
| Keyword- und SERP-Daten | **DataForSEO (gewählt):** Guthaben ab 50 $, kein Abo, Standort-Abfragen. Preise pro Abfrage auf der Produktseite prüfen. Local-Pack/Maps-Daten unklar |
| Semrush | zu teuer für den Start (API-Tarif ca. 549 $/Monat plus Einheiten) |
| Google Keyword Planner | nicht als Weg gewählt |
| Eigene Seite | Search Console und Google Analytics (kostenlos nach meiner Kenntnis) |
| Google Ads | Google Ads API, Developer Token nötig (Freigabe dauert laut Blog 2+ Wochen). Offizieller MCP nur lesend, Schreiben über Drittanbieter oder eigenes Skript |
| Meta Ads | Meta Marketing API, offizieller Ads-MCP in Open Beta (April 2026, Blogangabe). Schreibzugriff löst echte Ausgaben aus: erst nur lesen |
| Google-Profil | Business Profile API, Zugang per Antrag (Geschäftsgrund, Cloud-Projekt, Website) |
| WordPress | eingebaute Schnittstelle (nach meiner Kenntnis), Artikel als Entwurf anlegen |
| LinkedIn | Posten auf persönlichem Profil ohne Prüfung möglich, App muss an Unternehmensseite gekoppelt sein. Eigene Posts/Kommentare lesen nicht möglich, keine Zeitplanung, Token läuft nach 60 Tagen ab |
| CRM, Mail, Ablauf | Baserow, Brevo, n8n (siehe oben) |

## Betrieb des Agent
- Zunächst lokal entwickeln. Danach optional Linux-VPS bei Strato (z. B. VPS M, 2 Kerne/4 GB, ca. 10 €/Monat, Root-Zugriff, keine Backups im Tarif). Normales Webhosting vermutlich nicht geeignet (nicht geprüft).
- Claude Code läuft ohne Oberfläche per `claude -p`, im Skript-Modus (`--bare`) mit API-Schlüssel statt Abo-Login (zusätzliche Nutzungskosten). Berechtigungen per `--allowedTools`, nicht Erlaubtes wird bei unbeaufsichtigtem Lauf abgelehnt.
- Alternative ohne eigenen Server: geplante Aufgaben in Claude (Verfügbarkeit im Plan prüfen).
- Zugangsschlüssel nie in Dateien im Projektordner ablegen, sondern in Umgebungsvariablen.

## Idee für den Marketing-Agent (Cody-Schneider-Ansatz, aus Podcasts, nicht tief geprüft)
Ads-Agent mit festem Budgetdeckel, Pain-Point-Recherche in Foren, ein Video für mehrere Kanäle verwerten. HWG- und DSGVO-Leitplanken gehören in jeden Agent. Grundsatz: Der Agent bereitet vor, ein Mensch gibt frei.
