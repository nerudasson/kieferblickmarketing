# Dateiformat `daten/meta/kampagnen/<kampagne>.json`

```
{
  "kampagne": "Kalt Fall-Clip Leseprobe",
  "stufe_kontakt": "kalt",                  // kalt | kalt_fall | warm | heiss_nicht_erschienen | heiss
  "ziel": "Anmeldung Leseprobe/Werkzeug",
  "optimierungsereignis": "Lead",           // häufigstes Ereignis
  "tagesbudget_eur": 9,                     // Deckel: config/meta.json ads.kampagnen_eur[kalt|warm|heiss]
  "laender": ["DE", "AT", "CH"],
  "zielgruppe": {
    "alter_min": 32, "alter_max": 65,
    "berufe_oder_interessen": ["Zahnarzt"], // Detailtargeting-IDs trägt Alexander in Meta nach
    "custom_audiences": ["intro_besucht"]   // Schlüssel aus config/meta.json ads.zielgruppen_ids (warm/heiß Pflicht)
  },
  "ausschluesse": ["kunden"],               // Pflicht
  "begruendung": "...", "erwartete_wirkung": "...",   // Pflicht (Änderungsprotokoll)
  "entscheidung": "optional: offener Punkt für Alexander",
  "anzeigengruppen": [{
    "name": "Fall in Bildern",
    "anzeigen": [{
      "nr": 1,
      "creative_typ": "fall-in-bildern",    // fall-in-bildern | gruendergeschichte | entscheidung-am-fall | teilnehmerstimme | qualifikation
      "fall_dossier": "FD-001",             // Kennung, keine Inhalte
      "bild_quelle": "fall-dossier",        // fall-dossier | eigene-aufnahme | dokument; nie KI oder Stock
      "format": "video",                    // video (video_id) | bild (bild_datei)
      "video_id": "", "bild_datei": "",
      "einwilligung_vorhanden": true,       // Pflicht bei teilnehmerstimme
      "beleg": "",                          // Pflicht bei qualifikation (Zertifikat, Punkte)
      "primaerer_text": "...", "titel": "...", "beschreibung": "...",
      "cta_button": "DOWNLOAD",
      "hauptaufruf": "leseprobe", "nebenaufruf": null,
      "link": "https://bitecentric.de/leseprobe?utm_source=meta&utm_medium=paid&utm_campaign=leseprobe&utm_content=anzeige-001",
      "utm": {"utm_source": "meta", "utm_medium": "paid", "utm_campaign": "leseprobe", "utm_content": "anzeige-001"}
    }]
  }]
}
```
- Pflicht und erlaubte Werte: `references/aufruf-regeln.json`; Prüfung `scripts/anzeigen_check_meta.py`.
- `utm_content` = `anzeige-<nr>` mit der Nummer der Anzeige; die Nummer ist je Kampagnendatei eindeutig, damit HubSpot-Zahlen und Ausgaben zusammenpassen.
- Textlängen sind Richtwerte (Primärtext 300, Titel 40, Beschreibung 30 Zeichen); sie stammen aus der Praxis, nicht aus der recherchierten Meta-Doku.
- Muster: `tests/muster-gut.json` (Testmuster, keine echte Kampagne).
