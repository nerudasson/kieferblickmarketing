# Meta: Stand der Dokumentation (recherchiert 04.11.2026)

Quellen: offizielle Meta-Dokumentation, per Abruf geprüft; Lücken sind markiert. Vor dem Bau von Neuem erneut prüfen, die Dokumentation ändert sich schnell.

## Ads-MCP-Server
- URL `https://mcp.facebook.com/ads`. Open Beta seit 29.04.2026, seit 16.07.2026 kann jede App verbinden; kein GA-Datum. Quellen: developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-overview, Blog 16.07.2026.
- **Anbindung mit eigener Meta-App (gewählt):** App unter developers.facebook.com/apps anlegen, Use Case „Create & manage ads with ads MCP server“ hinzufügen, Redirect-URL in „Facebook Login for Business“ passend zum Client eintragen. Claude Code: `claude mcp add --transport http --client-id <META_APP_ID> meta-ads https://mcp.facebook.com/ads`. Scopes: `ads_mcp_management` plus `ads_read` oder `ads_management` (optional `business_management`, `pages_show_list`, `instagram_basic`). Advanced Access/App Review nur für Fremdkonten (Agenturen). System-User-Tokens nur mit Employee-Rolle. Quelle: …/ads-mcp-server-get-started.
- Werkzeuge anlegen: `ads_create_campaign`, `ads_create_ad_set`, `ads_create_ad`, `ads_create_creative`, `ads_update_entity`, `ads_activate_entity`; „Write tools create entities in a paused state“. Lesen u. a. `ads_get_ad_entities` (mit Metriken), `ads_get_creatives`, `ads_get_ad_preview`, `ads_library_search`, Insights. Kein Bild-Upload-Werkzeug dokumentiert. Quelle: …/ads-mcp-server-tools-ad-creation-and-management, …-tools-comprehensive-reporting.
- **Ads MCP Rules** (begrenzte Verfügbarkeit): je Werbekonto lassen sich Erstellen, Budgeterhöhungen, Targeting-/Creative-Änderungen, Statusänderungen oder alle Aktionen verbieten (Business Suite oder API). Quelle: …/ads-mcp-server-rules-best-practices.
- Meta Platform Terms gelten auch für den Agenten, der im Namen des Nutzers handelt; für Agenten mit nicht vertrauenswürdigem Input keine Schreibrechte vergeben (developers.facebook.com/documentation/mcp).
- **Nicht belegt:** MCP-spezifische Rate-Limits, Parameter-Schemas, Scopes je Werkzeug, Live-Modus/Business-Verifizierung der App. Der Weg über den Custom Connector in claude.ai ohne eigene App stammt aus einer Drittquelle.

## Marketing API
- Aktuell v26.0 (29.07.2026); v20.0 entfernt 24.09.2026. Eigenes Werbekonto: Zugriffsstufe „Limited Access“ (früher Standard) genügt, kein App Review; Upgrade auf Full Access nach 500 Aufrufen in 15 Tagen bei Fehlerquote unter 15 %. Quelle: …/marketing-api/overview/authorization/, Blog 29.07.2026.
- Limits (Marketing API, für den MCP vermutlich ähnlich, Annahme): Punktesystem, Lesen 1, Schreiben 3; 4 Budgetänderungen je Anzeigengruppe und Stunde.
- Anlegen: `status` bei Erstellung nur ACTIVE oder PAUSED; `special_ad_categories` ist Pflichtfeld, für Fortbildung `[]`/NONE (Annahme, die Doku nennt weder Gesundheit noch Fortbildung). Bilder über `/act_<id>/adimages` (image_hash). Quelle: …/reference/ad-campaign-group/, …/special-ad-category/.
- Langlebiger User-Token ca. 60 Tage (`fb_exchange_token`); System-User-Token nicht ablaufend oder 60 Tage.
- `meta_push.py` ist **nur gegen einen lokalen Testserver getestet**, nicht gegen ein echtes Konto. Parameter wie `is_adset_budget_sharing_enabled` und das Targeting sind nach bestem Wissen gesetzt; bei einer Fehlermeldung im ersten Lauf Payload anpassen.

## Anzeigenrichtlinien (Auszug)
- „Personal attributes“: keine Zuschreibung von Gesundheitszuständen oder persönlichen Eigenschaften („Sie haben …“). Seite nur als Suchauszug lesbar (Abruf 404).
- Health & Wellness (Stand 22.07.2026): keine Heilversprechen; Zahnprodukte wie Bleaching von der Altersgrenze 18+ ausgenommen. Regeln speziell für Anzeigen an Fachpublikum: keine gefunden.
- Das Landing-Page-Review und die Konto-Prüfung bleiben bei Meta; Ablehnungen im Protokoll vermerken.
