# Testfälle ad-writing
Muster in diesem Ordner sind **Testmuster**, keine echten Kampagnen. Befehle vom Projektstamm.

1. **Sauberes Muster besteht:** `python3 -I .claude/skills/ad-writing/scripts/anzeigen_check.py .claude/skills/ad-writing/tests/muster-gut.json`
   Erwartung: „OK (0 hart, 0 weich)“, Exit-Code 0.
2. **Fehler werden gefunden:** gleiche Prüfung mit `muster-fehler.json`.
   Erwartung: Exit-Code 1 und HART-Treffer für: Tagesbudget über Deckel, Klickpreis über Obergrenze, Broad-Keyword, Landingpage nicht https/kieferblick.de, Überschrift über 30 Zeichen, Beschreibung über 90, doppelte Texte, „beste“, „Kieferorthopäde“, Ausrufezeichen, „Rabatt“, „jetzt sofort“, „Invisalign“, „Garantie“, Telefonnummer, „perfekt“, „für immer“, „unsichtbar“, Überschrift 1 ohne Themabegriff. WEICH: „kostenlos“, Preis „149 €“, „sofort“, zu wenige Überschriften/Beschreibungen.
3. **Export nur nach bestandener Prüfung:** Kopie von `muster-gut.json` in den Arbeitsordner, `anzeigen_export.py <kopie>`. Erwartung: `.csv` mit Kampagnenzeile `Paused`, Negativen als „Campaign Negative Phrase“, je Keyword eine Zeile Exact/Phrase, eine RSA-Zeile mit 12 Überschriften, 4 Beschreibungen, `Headline 1 position` = 1; dazu `-einstellungen.md`. Mit `muster-fehler.json` bricht der Export ab („Export abgebrochen: 19 HART-Treffer“), es entsteht keine Datei.
4. **Offene Entscheidung bleibt sichtbar:** Im sauberen Muster ein Feld `"entscheidung": "Preis offen"` an der Anzeige ergänzen. Erwartung: WEICH-Zeile „Offene Entscheidung“, auch in der Einstellungsdatei.
5. **Import (einmalig von Hand):** Erste CSV im Google Ads Editor importieren. Erwartung: Spalten werden erkannt, Kampagne pausiert. Abweichungen in `references/google.md` unter „Export-Format“ eintragen.
