# Ad Library API: Stand der Dokumentation (recherchiert 04.11.2026)

Quellen: developers.facebook.com/docs/graph-api/reference/ads_archive/ und …/archived-ad/, transparency.meta.com/researchtools/ad-library-tools/, Metas Paket Radlibrary (facebookresearch.github.io/Radlibrary). Die offizielle API-Seite facebook.com/ads/library/api war nicht abrufbar.

## Aufruf
`GET https://graph.facebook.com/<Version>/ads_archive` mit `access_token`. Aktuelle Referenzversion v27.0; im Skript v26.0 (belegt). Nur lesen.
- Pflicht: `ad_reached_countries` (ISO-Codes oder ALL). Weitere: `ad_type` (ALL …), `ad_active_status` (ACTIVE | ALL | INACTIVE, Standard ACTIVE; wir nehmen ALL), `search_terms` (höchstens 100 Zeichen; Leerzeichen = UND; nicht übersetzt), `search_type` (KEYWORD_UNORDERED | KEYWORD_EXACT_PHRASE), `search_page_ids` (bis zu 10), `ad_delivery_date_min/max`, `publisher_platforms`, `languages`, `media_type` (ALL | IMAGE | MEME | VIDEO | NONE), `limit`, Cursor `after`.
- Felder für alle Anzeigen: `id`, `page_id`, `page_name`, `ad_creation_time`, `ad_delivery_start_time`, `ad_delivery_stop_time`, `ad_creative_bodies`, `ad_creative_link_titles`, `ad_creative_link_captions`, `ad_creative_link_descriptions`, `ad_snapshot_url`, `languages`, `publisher_platforms`, `total_reach_by_location` (EU, BR, UK). UK und EU: `target_ages`, `target_gender`, `target_locations`, `age_country_gender_reach_breakdown`. Nur EU: `eu_total_reach`, `beneficiary_payers`. `spend`, `impressions`, `bylines` u. a. nur für politische Anzeigen, nicht für unsere Zwecke.
- Es gibt **kein Formatfeld**. Das Skript erkennt Video über einen zweiten Durchlauf mit `media_type=VIDEO`; mehrere Texte/Titel deuten auf Karussell oder Varianten und gelten als „prüfen“.

## Länder
- DE, AT: Anzeigen mit EU-Auslieferung (ad_type ALL), mit EU-Reichweite und Zielgruppenangaben (DSA).
- GB: Feldreferenz nennt „UK & EU“; Hinweistext bei `ad_reached_countries` nennt nur die EU (Widerspruch in der Doku). Reichweite für UK nur über `total_reach_by_location` (Struktur nicht verifiziert, das Skript speichert den Rohwert), kein `eu_total_reach`. Klärt sich im ersten Echtlauf.
- CH: keine Aussage in der Doku, Annahme nicht abgedeckt. Schweizer Anbieter nur sichtbar, wenn sie nach DE oder AT ausliefern.
- Archiv: nicht-politische Anzeigen ein Jahr nach der letzten Auslieferung.

## Zugang und Grenzen
- Identitäts- und Standortbestätigung per Ausweis (laut Radlibrary 1–2 Tage), Entwicklerkonto und Meta-App; die Abfrage schlägt für ein Land fehl, für das man nicht bestätigt ist. Ob App Review nötig ist, ist nur aus Drittquellen („nein“) belegt.
- Token: Explorer-Token kurzlebig; langlebiger User-Token ca. 60 Tage (`fb_exchange_token`, serverseitig). Fehler 190 = Token ungültig, 613/4/17/32 = Rate-Limit (keine Zahl dokumentiert; Plattformlimit „200 × Nutzer je Stunde“). Das Skript pausiert zwischen Aufrufen (`pause_sekunden`) und bricht bei Limit-Fehlern mit gespeichertem Teilergebnis ab (Exit-Code 3).
- Ein `limit`-Maximum ist nicht dokumentiert (Radlibrary: bis 1000 Zeilen); Standard im Skript 50.
- Massendownload der Kreativdateien ist laut Doku nicht erlaubt; das Skript speichert nur Texte und Metadaten.
- Die Kombination `search_page_ids` plus `search_terms` ist nicht ausdrücklich erlaubt und wird nicht verwendet.
- Die Meta Content Library deckt keine Anzeigen ab (nur Forschende) und ist nicht relevant.
