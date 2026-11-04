# Auswertung: Meta-Zahlen und HubSpot (Stand 04.11.2026)

## Datenquellen
| Was | Woher | Zugang |
|---|---|---|
| Ausgaben, Anzeigenleistung je Anzeige | Meta Ads (MCP-Werkzeuge `ads_get_ad_entities`, Insights) | erst nach `ads.lesezugriff_freigegeben` |
| Leads, MQL, SQL, Käufer nach Quelle | HubSpot (MCP, nur lesen und zählen) | bereits verbunden (Portal 149702228) |

## HubSpot-Zählungen (nur Zahlen, keine Kontaktzeilen)
Filter immer `utm_source = meta`, gruppiert nach `utm_campaign` und `utm_content`. Stufe erreicht, wenn das Datum gesetzt ist:
- Lead: `hs_v2_date_entered_lead` im Zeitraum bzw. bis heute
- MQL: `hs_v2_date_entered_marketingqualifiedlead`
- SQL: `hs_v2_date_entered_salesqualifiedlead`
- Customer: `hs_v2_date_entered_customer` (oder Deals in „Gewonnen“ der Pipeline „Vorgespräch“)

Werkzeuge: `query_crm_data` (SQL-ähnlich, keine Joins) oder `search_crm_objects` mit Zählung; vor der ersten Abfrage `tool_guidance` aufrufen und die Syntax prüfen (nicht selbst erprobt). Ergebnis als Zählwerte in die Eingabedatei für `scripts/kennzahlen.py` (Format im Kopf des Skripts). **Keine Namen, E-Mail-Adressen oder Kontakt-IDs notieren.**

Ergänzend nützlich: Verteilung `bc_funnel_status`, `bc_aligner_erfahrung` und `bc_schwerpunkt` je Anzeige (Passen die Leute zu Krämer oder Berger?), Deals nach `bc_angebot` und `bc_grund_bei_nein`.

## Auswertung und Entscheidungen
1. `python3 -I .claude/skills/meta-ads/scripts/kennzahlen.py <eingabe.json> --ausgabe daten/meta/wochen/<JJJJ-Www>.md`
2. Aussagekraft beachten: unter etwa 30 Leads (Annahme) nur Tendenz, ohne Käufer nur MQL/SQL-Quote.
3. Höchstens drei Vorschläge pro Woche, jeder mit Begründung und erwarteter Wirkung. Alexander entscheidet; jede Änderung im Werbekonto kommt ins Protokoll `daten/meta/protokoll.md`.
4. Tests mit Hypothese ins `experiment-log.md`.

## Hinweise zur Zuordnung
- HubSpot Free zeigt Anzeigen-Attribution nur als „letzte Anzeigeninteraktion“. Die Leitgröße rechnet daher über die UTM-Felder am Kontakt, nicht über HubSpots Attributionsberichte.
- Kontakte ohne `utm_source` (z. B. Buchleser) fehlen in der Meta-Zahl; die Pflichtfrage „Wie sind Sie auf uns aufmerksam geworden?“ (`bc_genannte_quelle`) hilft bei der Gegenprobe.
- Ohne Workflows, die aus `bc_funnel_status` die Lebenszyklusphase setzen, bleiben MQL/SQL/Customer leer (nicht geprüft).
