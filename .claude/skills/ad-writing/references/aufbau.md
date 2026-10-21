# Dateiformat `daten/ads/kampagnen/<kampagne>.json`
```
{
  "kampagne": "A Aligner Zone 1",
  "budget_key": "aligner",            // Schlüssel in config/budget.json → google_kampagnen_eur und in obergrenzen.json
  "tagesbudget_eur": 19,
  "gebotsstrategie": "Klicks maximieren",
  "max_cpc_eur": 6,
  "zone": "Zone 1",
  "standorte": ["Mülheim an der Ruhr", "Essen", "..."],
  "negativ": ["kasse", "kinder", "..."],
  "gruppen": [{
    "name": "Behandler",
    "thema_begriffe": ["aligner", "zahnarzt"],   // Überschrift 1 enthält mindestens einen
    "winkel": "Ein Arzt begleitet bis zum Retainer",
    "cta": "Erstberatung buchen",
    "landingpage": "https://kieferblick.de/...",
    "marke_im_text_ok": false,
    "keywords": [{"text": "aligner zahnarzt", "match": "exact"}, {"text": "aligner zahnarzt", "match": "phrase"}],
    "anzeigen": [{
      "variante": "A",
      "kontrast": "Winkel Begleitung",
      "ueberschriften": ["... (höchstens 30 Zeichen)"],
      "beschreibungen": ["... (höchstens 90 Zeichen)"],
      "pfad1": "aligner", "pfad2": "mülheim",
      "entscheidung": "Preis in der Anzeige offen (nicht enthalten)"
    }]
  }]
}
```
Obergrenzen je `budget_key` (Gebote) stehen in `references/obergrenzen.json` (aus `kontext/google-ads-strategie.md`). Monatsbudget je Kampagne steht in `config/budget.json`.
