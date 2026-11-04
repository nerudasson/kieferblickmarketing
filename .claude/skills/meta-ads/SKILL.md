---
name: meta-ads
description: Plant, schreibt und wertet Meta-Anzeigen (Facebook, Instagram) für BiteCentric aus, der Fortbildung für Zahnärzte. Entwürfe als prüfbare Datei, Prüfung gegen Aufrufregel, Ton und UTM-Konvention, Anlegen nur pausiert, Wochenauswertung mit HubSpot. Nutzen für neue BiteCentric-Kampagnen, Anzeigentexte, Creative-Ideen und die Meta-Wochenauswertung. Nicht für Kieferblick (Patientenwerbung) und nicht für die Beobachtung von Wettbewerbern (dafür meta-wettbewerb).
---
# meta-ads (BiteCentric)

Ziel: Anzeigen so vorbereiten, dass Alexander sie nur noch im Werbekonto ansieht und **selbst freischaltet**. Der Agent bereitet vor, Alexander gibt frei.

**Freigabestufe: 2, Assistent (aktiv).** Stufe 1 Analyst: lesen, auswerten, vorschlagen. **Stufe 2: zusätzlich pausiert anlegen inkl. Texte und Bildvarianten.** Stufe 3 Autopilot: nicht freigegeben, nicht vorbereiten. Stand und Schalter: `config/meta.json`.

## Harte Regeln
- **Nichts aktivieren, kein Budget ändern, nichts veröffentlichen.** Kampagnen, Anzeigengruppen und Anzeigen entstehen ausschließlich **pausiert**. Bestehende Objekte werden nicht verändert.
- Keine Zugangsschlüssel in Dateien, nur Umgebungsvariablen (Namen in `config/meta.json`).
- Keine Patientendaten in Repository, Logs oder HubSpot-Auswertungen; nur Zählwerte, keine Kontaktzeilen.
- **Kein echter API-Abruf**, solange die Schalter `ads.lesezugriff_freigegeben` und `ads.schreibzugriff` in `config/meta.json` auf false stehen (Alexander setzt sie nach Token und Trockenlauf).
- Kunden werden in jeder Kampagne ausgeschlossen. Nie direkt zu einem bezahlten Kurs; höchstens ein Haupt- und ein Nebenaufruf je Anzeige (Aufrufregel: `kontext/bitecentric/angebot-und-aufrufe.md`).

## Ablauf
1. **Briefing lesen** (nur was nötig ist): `kontext/bitecentric/` (Angebot und Aufrufe, Ton und Zielgruppen, UTM, HubSpot-Felder, Wettbewerb), `daten/meta/wochen/` (letzte Auswertung), `daten/meta/wettbewerb/berichte/` (Anregungen aus dem Monitor), `daten/meta/protokoll.md`, `experiment-log.md`.
2. **Entwurf schreiben** nach `daten/meta/kampagnen/<kampagne>.json` (Format: `references/kampagnen-aufbau.md`). Je Anzeige ein Creative-Typ aus `references/creatives.md`, eine Fall-Dossier-Kennung, ein Hauptaufruf, optional ein Nebenaufruf, Link mit UTM. Fakten nur aus `kontext/bitecentric/`, keine Zahlen erfinden, Lücken benennen.
3. **Skript-Prüfung:** `python3 -I .claude/skills/meta-ads/scripts/anzeigen_check_meta.py daten/meta/kampagnen/<kampagne>.json`. HART beheben, WEICH begründen oder ersetzen.
4. **compliance-reviewer im Meta-Modus** auf die Datei (Ergebnis `daten/reviews/meta-<kampagne>.md`), Befunde einarbeiten, Skript erneut.
5. **Pausiert anlegen** (erst nach Freigabe der Schalter):
   - Trockenlauf (Standard): `python3 -I .claude/skills/meta-ads/scripts/meta_push.py daten/meta/kampagnen/<kampagne>.json`
   - Anlegen: dasselbe mit `--anwenden`. Das Skript trägt jedes Objekt in `daten/meta/protokoll.md` ein.
   - Alternative Weg über den Ads-MCP: siehe unten. Gleiche Vorprüfung, gleiche Regeln.
6. **Übergabe an Alexander:** Kurzbericht (Kampagne, Stufe, Aufrufe, Creative-Typen, offene Entscheidungen, WEICH-Treffer, manuell Nachzutragendes). Hypothese in `experiment-log.md` eintragen (Datum, Kanal Meta, Hypothese, Varianten, Budget). Alexander prüft im Werbekonto und schaltet frei; das ist die Freigabe.

## Optimierungslogik
- Optimiert wird auf das **häufigste Ereignis** (Anmeldung Leseprobe/Werkzeug, Ereignis „Lead“). Qualität kommt als Rückmeldung aus HubSpot über die Lebenszyklusphasen: **Lead** (Werkzeug/Leseprobe) · **MQL** (Intro besucht) · **SQL** (Vorgespräch geführt) · **Customer**.
- **Leitgröße: Gewinnungskosten je Käufer nach Quelle.**
- **Wenige, größere Entscheidungen pro Woche** (höchstens drei), keine täglichen Änderungen (Lernphase). Anzeigengruppen in der Lernphase nicht anfassen; als Faustregel gilt rund 50 Optimierungsereignisse in 7 Tagen (Annahme, Meta-Praxis, vor Gebrauch in der Doku prüfen).
- Wochenrhythmus: Ausgaben je Anzeige lesen (Ads-MCP, nur nach Freigabe) → HubSpot zählen (`references/auswertung.md`) → `scripts/kennzahlen.py` → `daten/meta/wochen/<JJJJ-Www>.md` → bis zu drei Vorschläge → Alexander entscheidet.

## Kampagnen
| Kontaktstufe | Kampagne | Aufruf |
|---|---|---|
| kalt | Fall-Clip | Leseprobe / Werkzeug / Fall-Analyse |
| kalt_fall (konkreter Fall) | Fall-Clip | Fall-Einschätzung |
| warm | Retargeting | Intro |
| heiss_nicht_erschienen | Intro angemeldet, nicht erschienen | Aufzeichnung, Fall-Einschätzung |
| heiss (Intro besucht, Kurs gesucht) | nicht als Meta-Kampagne vorgesehen; die Prüfung erlaubt es | Kursanfrage → Vorgespräch |

Details und Dateiformat: `references/kampagnen-aufbau.md`.

## Ads-MCP (`mcp.facebook.com/ads`, Open Beta), Name in der Konfiguration `meta-ads`
- **Erlaubt (lesen):** `ads_get_ad_accounts`, `ads_get_ad_entities`, `ads_get_creatives`, `ads_get_ad_images`, `ads_get_ad_videos`, `ads_get_ad_preview`, `ads_library_search`, Insights-Werkzeuge, `ads_account_get_activity_logs`.
- **Erlaubt (anlegen, erst Stufe 2 und nach Freigabe):** `ads_create_campaign`, `ads_create_ad_set`, `ads_create_creative`, `ads_create_ad`. Laut Meta-Doku entstehen die Objekte pausiert; **danach immer zurücklesen und Status PAUSED bestätigen**, dann ins Protokoll.
- **Gesperrt:** `ads_activate_entity`, `ads_update_entity` (auch in `.claude/settings.json` verweigert), Zielgruppen ändern, Anzeigen bewerben. Kein Bild-Upload im MCP; Bilder lädt Alexander hoch oder `meta_push.py` über die Marketing API.
- Zusätzlich kann Alexander bei Meta („Ads MCP Rules“ je Werbekonto) Statusänderungen und Budgeterhöhungen für den Agenten sperren (To-do).

## Dateien
`config/meta.json` · `daten/meta/kampagnen/` · `daten/meta/protokoll.md` · `daten/meta/wochen/` · `daten/reviews/meta-*.md` · `references/`: `meta.md` (API/MCP-Stand mit Quellen), `kampagnen-aufbau.md`, `creatives.md`, `auswertung.md`, `aufruf-regeln.json` · Tests: `tests/faelle.md`.

## Offene Punkte (nicht erfunden)
Meta-Budget je Kampagnenstufe, Webadresse (Annahme bitecentric.de), Fall-Dossiers, Facebook-Seite, Pixel und Zielgruppen-IDs. Alle stehen in der To-do-Liste `kontext/bitecentric/todo-meta.md`.
