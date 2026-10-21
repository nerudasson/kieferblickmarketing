---
name: ad-writing
description: Schreibt Google-Ads-Kampagnen für Kieferblick als prüfbare Datei (Anzeigengruppen, Keywords, Negativliste, responsive Suchanzeigen) und exportiert sie für den Google Ads Editor. Nutzen, wenn neue Kampagnen oder Anzeigengruppen entworfen oder Texte aus Optimierungsvorschlägen geändert werden sollen. Ohne Freigabe geht nichts live.
---
# ad-writing

Ziel: Kampagnen so schreiben, dass sie nach Prüfung durch Skript und compliance-reviewer **nur noch von Alexander freigegeben und importiert** werden müssen. Der Agent hat keinen Schreibzugriff auf das Konto (`config/budget.json`, `schreibzugriff_ads: false`).

## Ablauf
1. **Briefing lesen** (nicht alles, nur was die Kampagne braucht): `kontext/google-ads-strategie.md` (Gruppen, Winkel, Landingpage, Gebotsgrenzen), `kontext/angebot-und-preise.md` (Preise und Zusagen), `kontext/marke-und-ton.md`, `daten/ads/beobachtung/auswertung.md` (Markt), `experiment-log.md` (frühere Tests), bei Überarbeitung `daten/ads/vorschlaege/`. Referenzen: `references/google.md`, `references/hwg-anzeigen.md`, `references/aufbau.md`.
2. **Entwurf schreiben** nach `daten/ads/kampagnen/<kampagne>.json` (Format in `references/aufbau.md`). Je Anzeigengruppe ein Thema, 4–10 Keywords (Exact/Phrase, nie Broad), je Kampagne eine Negativliste, je Anzeige 10–15 Überschriften und 4 Beschreibungen. Bei Kampagne A zwei Anzeigen je Gruppe mit **einem** großen Kontrast (Winkel oder CTA oder Preis ja/nein), sonst eine. Fakten nur aus den Kontextdateien, keine Zahlen erfinden. Offene Entscheidungen (z. B. Preis in der Anzeige) als Feld `entscheidung` an der Anzeige vermerken und die Standardvariante ohne den offenen Punkt schreiben.
3. **Skript-Prüfung:** `python3 .claude/skills/ad-writing/scripts/anzeigen_check.py daten/ads/kampagnen/<kampagne>.json`. HART muss behoben werden (Zeichenlimits, verbotene Wörter, Broad, Budget und Gebotsgrenze, Berufsbezeichnung). WEICH prüfen und begründen oder ersetzen.
4. **compliance-reviewer** auf die Datei (Anzeigen-Modus: Prüfpunkte der Agentendefinition, Ergebnis `daten/reviews/ads-<kampagne>.md`). Befunde einarbeiten, Skript erneut laufen lassen.
5. **Export:** `python3 .claude/skills/ad-writing/scripts/anzeigen_export.py daten/ads/kampagnen/<kampagne>.json` schreibt `<kampagne>.csv` (Import in den Google Ads Editor, Kampagne **pausiert**) und `<kampagne>-einstellungen.md` (alles, was im Konto von Hand gesetzt wird).
6. **Übergabe an Alexander:** Kurzbericht (Gruppen, Anzeigenzahl, Winkel, offene Entscheidungen, WEICH-Treffer). Test als Hypothese in `experiment-log.md` eintragen (Datum, Gruppe, Variante A/B, Winkel). Alexander importiert und aktiviert.

## Regeln
- Wortwelt aus `kontext/marke-und-ton.md`: Plan, Weg, begleiten, diskret, Endpreis, Zusage. Nicht: unsichtbar (nur als Suchbegriff), perfekt, Garantie, Rabatt, Aktion, Superlative. Keine Dringlichkeit; Knappheit nur als echte Terminplätze.
- Der Arzt ist **Zahnarzt**, nicht Fachzahnarzt für Kieferorthopädie: das Wort „Kieferorthopäde“ steht nie im Anzeigentext, auch nicht in der Gruppe mit dem Keyword „kieferorthopäde + Stadt“.
- Kein Markenname (z. B. Invisalign) im Anzeigentext, nur als Keyword.
- Bewertungsangaben, Fälle, Vorher-nachher: nur wenn echt und freigegeben. Sonst nicht in die Anzeige.
- Nichts veröffentlichen, kein Geld ausgeben. Kampagnen bleiben im Export pausiert.

## Testfälle
`tests/faelle.md`
