# Google-Ads-Agent: Konzept (Stand 08.10.2026, Entwurf zur Freigabe)

Quelle: `CLAUDE.md`, `kontext/` und `config/budget.json`. Die Übergabedatei `daten/uebergabe-2026-10-08.md` lag nicht im Repo; sie ist hier nicht eingeflossen. Alles mit „Annahme“ ist offen.

## Grundsatz
Der Agent **liest frei, schreibt nur nach Freigabe.** Freigabe heißt: Alexander gibt ein konkretes Änderungspaket frei, nicht den Agent allgemein. Die Sicherungen liegen im Skript, nicht im Prompt.

## Ablauf Schreiben (Vorschlag → Freigabe → Ausführung)
1. Agent legt `daten/ads/vorschlaege/<datum>-<nr>.md` an: Ziel, Hypothese, genaue Änderung (Kampagne, Anzeigengruppe, Texte, Gebote, Budget), Budgetwirkung, Compliance-Ampel, Eintrag für `experiment-log.md`.
2. `compliance-reviewer` prüft alle Anzeigentexte (HWG, Berufsordnung, Markenton). Rot blockiert das Paket.
3. Alexander setzt im Kopf des Pakets `status: freigegeben` mit Datum.
4. Skript `ads_apply.py` führt aus, nur wenn:
   - der Status freigegeben ist und der Hash des Pakets mit dem Hash zur Freigabe übereinstimmt (nachträgliche Änderung macht die Freigabe ungültig),
   - die Summe der Tagesbudgets den Deckel aus `config/budget.json` einhält (Google: 900 €/Monat, Annahme),
   - die Operation auf der Erlaubtliste steht.
5. Neue Kampagnen, Anzeigengruppen und Anzeigen entstehen **pausiert**. Aktivieren ist eine eigene Freigabe.
6. Jede Ausführung wird mit Vorher-/Nachher-Zustand in `daten/ads/audit.jsonl` protokolliert, Ergebnis später in den Experiment-Log.

**Erlaubt nach Freigabe:** Kampagne/Anzeigengruppe/Anzeige anlegen, Texte ändern, Keywords und Negativ-Keywords hinzufügen, Budget innerhalb Deckel, pausieren/aktivieren.
**Nie, auch nicht mit Freigabe über den Agent:** löschen, Deckel ändern, Zahlungsdaten, Kontozugriffe, Conversion-Definitionen umbauen (nur manuell).

## Start-Struktur (Annahme, Alexander bestätigt)
- Eine Search-Kampagne, Ruhr-Umkreis statt nur Mülheim, Landingpage ohne Navigation.
- Anzeigengruppen nach Suchphase (aus `keyword-daten.md`): Kosten · Erfahrung · Auslöser/Rückfall („zähne verschieben sich“) · Anbieter („aligner zahnarzt“).
- Phrase/Exact, von Anfang an Negativliste (z. B. kostenlos, selber, Ausbildung, Jobs).
- Konversion: Tally-Formular und Rückrufwunsch, Quelle im CRM (Kennzahlen ②–④).
- Volumen ist der Engpass: Ruhr-Kern grob 200 Suchen/Monat im Kerncluster (Hochrechnung nach Einwohnern, Annahme). Echte Zahlen kommen aus der Standortabfrage über DataForSEO und bestimmen Radius und Budget.

## Skills (laut Plan, Reihenfolge)
1. `ads-allocation`: Budget je Kanal und Anzeigengruppe aus Regionalzahlen, CPC und Szenario (Lücke: echte CPC für Region).
2. `ad-writing` mit `google.md` (Formate, Zeichenlimits) und `hwg.md`: Entwürfe, jeweils durch compliance-reviewer.
3. `ads-optimizing`: wöchentlich lesen (Suchbegriffe, Kosten, Konversionen), Bericht, **Vorschlagspakete**. Zeitgesteuert über Routines.
4. `ab-test-planning`: eine Variable pro Test, Mindestlaufzeit und Entscheidungsregel vorab im Experiment-Log.

## Zugänge (früh beantragen)
Google-Ads-Konto, Manager-Konto, Developer Token (Freigabe laut Blog 2+ Wochen), OAuth-Client. Alles als Umgebungs-Secrets der Cloud-Umgebung (`GOOGLE_ADS_*`), nie im Repo. Schreibweg: eigenes Skript mit Google-Ads-API-Client, da der offizielle MCP nur liest.
Bis zum Token: Konto manuell, Agent arbeitet mit Exporten und DataForSEO.

## Offen (Alexander)
1. Markenbegriffe („Invisalign“) in Anzeigen und Keywords: Rechtsstatus in `recht.md` nicht dokumentiert, daher gelb. Als Keyword (nicht im Anzeigentext) sinnvoll?
2. Erstermin-Wording in Anzeigen (kostenlos oder entgeltlich, anrechenbar).
3. Budget 900 € Google bestätigen; Aufteilung im Monat gleichmäßig oder Test-Start mit weniger.
4. Freigabeweg: Datei im Repo bearbeiten, oder Chat-Freigabe, die der Agent ins Paket schreibt (weniger sicher, kein Hash-Nachweis).
