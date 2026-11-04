# HubSpot-Felder für die Auswertung (geprüft am 04.11.2026 im Portal 149702228)

Zugang über den HubSpot-MCP-Server (OAuth), **nur lesen und zählen**. Keine Kontaktzeilen in Repository oder Logs, nur Zählwerte. Das Portal meldet `onboarded=false`; das ist für das Lesen unerheblich.

## Kontakt
| Feld | Werte |
|---|---|
| `bc_funnel_status` | kontakt · werkzeug_buch · fall_einschaetzung · fallabend · intro_angemeldet · intro_besucht · kursanfrage · vorgespraech_gefuehrt · kunde · alumni |
| `bc_kursinteresse` | basiskurs · curriculum · einzelbegleitung · unklar |
| `bc_aligner_erfahrung` | keine · 1_5_faelle · mehr_als_5 · regelmaessig_seitenzahn_biss |
| `bc_schwerpunkt` | allgemein · prothetik · implantologie · kfo · sonstiges |
| `bc_gebuchte_angebote` | basiskurs · curriculum · einzelbegleitung · erstfall |
| `bc_genannte_quelle` | Freitext |
| `utm_source` · `utm_medium` · `utm_campaign` · `utm_content` | Text |
| `lifecyclestage` | subscriber · lead · marketingqualifiedlead · salesqualifiedlead · opportunity · customer · evangelist · other |
| `hs_v2_date_entered_lead` / `_marketingqualifiedlead` / `_salesqualifiedlead` / `_customer` | Datum des Eintritts in die Phase |
| `hs_analytics_source` | u. a. PAID_SOCIAL (von HubSpot gesetzt) |

## Deal-Pipeline „Vorgespräch“
Kursanfrage (10 %) → Vorgespräch gebucht (20 %) → Vorgespräch geführt (40 %) → Angebot gesendet (60 %) → Gewonnen / Verloren.
Deal-Felder: `bc_angebot` (basiskurs · curriculum · einzelbegleitung · erstfall) · `bc_gruppe` (Text) · `bc_zahlungsweise` (einmal · raten) · `bc_grund_bei_nein` (zeit · preis · kein_passender_fall · noch_zu_frueh · anderes).

## Abbildung auf die Qualitätsstufen der Anzeigen
| Stufe | HubSpot |
|---|---|
| Lead (Werkzeug/Leseprobe) | `hs_v2_date_entered_lead` gesetzt |
| MQL (Intro besucht) | `hs_v2_date_entered_marketingqualifiedlead` gesetzt |
| SQL (Vorgespräch geführt) | `hs_v2_date_entered_salesqualifiedlead` gesetzt |
| Customer | `hs_v2_date_entered_customer` gesetzt, oder Deal „Gewonnen“ |

Annahme: Die Lebenszyklusphasen werden durch Workflows aus `bc_funnel_status` gesetzt (Intro besucht → MQL, Vorgespräch geführt → SQL, Deal gewonnen → Customer). Ob diese Workflows existieren, ist nicht geprüft; ohne sie bleiben die Zählwerte leer (siehe To-do).
